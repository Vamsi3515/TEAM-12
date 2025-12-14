"""Quick test for Learning Flow Generator"""
import asyncio
import json
from app.core.Agents.learning_agent import generate_learning_flow

async def test_learning_flow():
    """Test the learning flow generator"""
    print("Testing Learning Flow Generator...")
    print("-" * 50)
    
    # Test with Python topic
    result = await generate_learning_flow(
        topic="Python Programming",
        experience_level="beginner",
        weekly_hours="5-10"
    )
    
    print("\n✅ Learning flow generated successfully!")
    print(f"\nTopic: Python Programming")
    print(f"Timeline: {result['timeline']}")
    print(f"\nNumber of phases: {len(result['phases'])}")
    
    # Check each phase
    for i, phase in enumerate(result['phases'], 1):
        print(f"\nPhase {i}: {phase['name']}")
        print(f"  Duration: {phase['duration']}")
        print(f"  Description: {phase['description']}")
        print(f"  Key Topics: {', '.join(phase['keyTopics'][:3])}...")
    
    print(f"\n📺 YouTube Channels: {len(result['youtubeChannels'])}")
    for channel in result['youtubeChannels'][:2]:
        print(f"  - {channel['name']}: {channel['url']}")
    
    print(f"\n🎯 Projects: {len(result['projects'])}")
    for project in result['projects']:
        print(f"  - {project['name']} ({project['difficulty']}, {project['estimatedHours']}h)")
    
    print(f"\n📚 Resources:")
    print(f"  Books: {len(result['resources']['books'])}")
    print(f"  Websites: {len(result['resources']['websites'])}")
    print(f"  Communities: {len(result['resources']['communities'])}")
    
    print(f"\n🔍 RAG Evidence: {len(result['evidence_ids'])} documents used")
    for snippet in result['evidence_snippets'][:2]:
        print(f"  - {snippet['id']}: {snippet['snippet'][:80]}...")
    
    print(f"\n📊 Mermaid Diagram: {len(result['mermaidDiagram'])} chars")
    
    # Validate all required fields
    required_fields = ['phases', 'mermaidDiagram', 'youtubeChannels', 'projects', 
                      'timeline', 'prerequisites', 'resources', 'evidence_ids', 'evidence_snippets']
    missing = [f for f in required_fields if f not in result]
    
    if missing:
        print(f"\n❌ Missing fields: {missing}")
    else:
        print("\n✅ All required fields present!")
    
    # Check phase structure
    if result['phases']:
        phase = result['phases'][0]
        phase_fields = ['name', 'duration', 'description', 'keyTopics']
        phase_missing = [f for f in phase_fields if f not in phase]
        if phase_missing:
            print(f"❌ Phase missing fields: {phase_missing}")
        else:
            print("✅ Phase structure correct!")
    
    print("\n" + "=" * 50)
    print("Test completed successfully!")
    
    return result

if __name__ == "__main__":
    result = asyncio.run(test_learning_flow())
