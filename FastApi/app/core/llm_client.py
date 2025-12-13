import os, httpx, json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Provider selection
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "huggingface").lower()  # openai, groq, huggingface, gemini
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def call_chat(prompt, model=None, max_tokens=800, temperature=0.7):
    """
    Call LLM based on configured provider.
    Falls back gracefully if no API key or API call fails.
    """
    provider = LLM_PROVIDER
    
    if provider == "openai":
        return await _call_openai(prompt, model or "gpt-3.5-turbo", max_tokens, temperature)
    elif provider == "groq":
        return await _call_groq(prompt, model or "llama-3.1-8b-instant", max_tokens, temperature)
    elif provider == "gemini":
        return await _call_gemini(prompt, model or "gemini-2.5-flash", max_tokens, temperature)
    else:  # huggingface (default)
        return await _call_huggingface(prompt, model or "Qwen/Qwen2.5-7B-Instruct", max_tokens, temperature)

async def _call_openai(prompt, model, max_tokens, temperature):
    """Call OpenAI API."""
    if not OPENAI_API_KEY:
        return _mock_response()
    
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return _mock_response()

async def _call_groq(prompt, model, max_tokens, temperature):
    """Call Groq LLM API (optimized for reasoning + JSON)."""
    if not GROQ_API_KEY:
        return _mock_response()
    
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert AI that always follows instructions exactly, "
                        "returns strict JSON when requested, and never includes extra words."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )

        # Groq SDK returns a ChatCompletionMessage with `.content` attribute
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Groq API error: {e}")
        return _mock_response()

async def _call_gemini(prompt, model, max_tokens, temperature):
    """Call Google Gemini API."""
    if not GEMINI_API_KEY:
        print("[LLM Client] GEMINI_API_KEY not set, returning mock response")
        return _mock_response()
    
    try:
        
        genai.configure(api_key=GEMINI_API_KEY)
        
        gemini_model = genai.GenerativeModel(model)
        response = gemini_model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
                response_mime_type="application/json",  # enforce JSON-only output
            ),
        )
        
        # Log finish reason to detect truncation
        if hasattr(response, 'candidates') and response.candidates:
            finish_reason = response.candidates[0].finish_reason
            print(f"[LLM Client] Gemini finish_reason: {finish_reason}")
            if finish_reason != 1:  # 1 = STOP (natural completion)
                print(f"[LLM Client] WARNING: Response may be truncated. finish_reason={finish_reason}")
                # Try to handle incomplete JSON
                if hasattr(response, 'text') and response.text:
                    print(f"[LLM Client] Partial response received: {len(response.text)} chars")
        
        if not response.text or len(response.text.strip()) == 0:
            print(f"[LLM Client] ERROR: Empty response from Gemini")
            return _mock_response()
        
        print(f"[LLM Client] Gemini response length: {len(response.text)}")
        return response.text
    except Exception as e:
        print(f"Gemini API error: {e}")
        import traceback
        traceback.print_exc()
        return _mock_response()

async def _call_huggingface(prompt, model, max_tokens, temperature):
    """Call HuggingFace Inference API."""
    if not HF_API_KEY:
        return _mock_response()
    
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": temperature
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                return data[0].get("generated_text", _mock_response())
            return _mock_response()
    except Exception as e:
        print(f"HF API error: {e}")
        return _mock_response()

def _mock_response() -> str:
    """Fallback mock response."""
    return json.dumps({
        "recommended_learning_path": ["Learn the missing technologies", "Build a project"],
        "final_summary": "Focus on hands-on practice"
    })