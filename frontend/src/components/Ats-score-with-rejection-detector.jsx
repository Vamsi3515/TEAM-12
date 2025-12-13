import React, { useState } from 'react';
import { FileText, Upload, CheckCircle, AlertCircle, TrendingUp, Target, Mail } from 'lucide-react';
import * as pdfjsLib from 'pdfjs-dist';
import Navbar from './Navbar';
import Card from './Card';
import Button from './Button';

// Set PDF worker from unpkg CDN matching the installed version
pdfjsLib.GlobalWorkerOptions.workerSrc = `https://unpkg.com/pdfjs-dist@${pdfjsLib.version}/build/pdf.worker.min.mjs`;

const RejectionDetector = () => {
  const [file, setFile] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [email, setEmail] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const parseResumeFile = async (file) => {
    try {
      if (file.type === 'application/pdf') {
        const arrayBuffer = await file.arrayBuffer();
        const pdf = await pdfjsLib.getDocument(arrayBuffer).promise;
        let fullText = '';
        for (let i = 0; i < pdf.numPages; i++) {
          const page = await pdf.getPage(i + 1);
          const textContent = await page.getTextContent();
          const pageText = textContent.items.map((item) => item.str).join(' ');
          fullText += pageText + ' ';
        }
        setResumeText(fullText.trim());
        return fullText.trim();
      } else {
        const text = await file.text();
        setResumeText(text);
        return text;
      }
    } catch (err) {
      setError('Failed to parse resume file: ' + err.message);
      return null;
    }
  };

  const handleFileChange = async (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
      if (selectedFile.type.includes('word') || selectedFile.name.endsWith('.docx')) {
        setError('DOCX parsing requires Word document library. Please use PDF or TXT instead.');
      } else if (selectedFile.type === 'application/pdf' || selectedFile.type === 'text/plain') {
        await parseResumeFile(selectedFile);
      } else {
        setError('Unsupported file type. Please use PDF, TXT, or paste text manually.');
      }
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setAnalyzing(true);
    setError(null);

    if (!resumeText.trim()) {
      setError('Please provide resume text');
      setAnalyzing(false);
      return;
    }

    try {
      const payload = {
        resume_text: resumeText,
        job_description: jobDescription || undefined,
        email: email || undefined,
      };

      const response = await fetch('http://localhost:8000/api/analyze-ats', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError('Analysis failed: ' + err.message);
      console.error(err);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50/30 to-pink-50/30">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12 animate-slide-up">
          <div className="inline-flex items-center gap-2 bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 px-4 py-2 rounded-full text-sm font-medium mb-4">
            <FileText className="w-4 h-4" />
            <span>ATS Score & Rejection Detector</span>
          </div>
          <h1 className="text-4xl font-bold text-slate-900 mb-4">
            Optimize Your Resume for
            <span className="block bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              Applicant Tracking Systems
            </span>
          </h1>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Get your ATS score and identify potential rejection reasons before applying
          </p>
        </div>

        {/* Upload Form */}
        <div className="max-w-4xl mx-auto mb-12">
          <Card className="animate-fade-in">
            <form onSubmit={handleAnalyze}>
              <div className="space-y-6">
                {/* Resume Text Area */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Resume Text
                  </label>
                  <textarea
                    value={resumeText}
                    onChange={(e) => setResumeText(e.target.value)}
                    placeholder="Paste your resume text here or upload a text file..."
                    rows={8}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all resize-none"
                    required
                  />
                  <div className="mt-3 border-2 border-dashed border-slate-300 rounded-lg p-6 text-center hover:border-purple-400 transition-colors">
                    <input
                      type="file"
                      onChange={handleFileChange}
                      accept=".txt,.pdf,.doc,.docx"
                      className="hidden"
                      id="resume-upload"
                    />
                    <label htmlFor="resume-upload" className="cursor-pointer">
                      <Upload className="w-8 h-8 text-slate-400 mx-auto mb-2" />
                      <p className="text-sm text-slate-600">
                        {file ? `File: ${file.name}` : 'Or upload resume (TXT/PDF/DOCX)'}
                      </p>
                    </label>
                  </div>
                </div>

                {/* Email Input */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Email (Optional - to receive results)
                  </label>
                  <div className="flex items-center">
                    <Mail className="w-5 h-5 text-slate-400 absolute ml-3 pointer-events-none" />
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="your.email@example.com"
                      className="w-full pl-10 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                    />
                  </div>
                </div>

                {/* Job Description */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Job Description
                  </label>
                  <textarea
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    placeholder="Paste the job description here for better matching..."
                    rows={6}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all resize-none"
                  />
                </div>

                {/* Error Message */}
                {error && (
                  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                    {error}
                  </div>
                )}

                <Button 
                  variant="primary" 
                  size="lg" 
                  icon={Target}
                  type="submit"
                  disabled={analyzing}
                  className="w-full"
                >
                  {analyzing ? 'Analyzing...' : 'Analyze Resume'}
                </Button>
              </div>
            </form>
          </Card>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          {[
            { icon: CheckCircle, title: 'ATS Score', desc: 'Get instant compatibility score analysis', color: 'from-green-500 to-emerald-500' },
            { icon: Mail, title: 'Email Rejection Alerts', desc: 'Receive detailed rejection reasons via email - unique to our platform!', color: 'from-blue-500 to-cyan-500' },
            { icon: TrendingUp, title: 'Improvement Tips', desc: 'Actionable suggestions to optimize your resume', color: 'from-purple-500 to-pink-500' },
          ].map((feature, idx) => {
            const Icon = feature.icon;
            return (
              <Card key={idx} className="text-center animate-slide-up" style={{ animationDelay: `${idx * 0.1}s` }}>
                <div className={`w-12 h-12 bg-gradient-to-br ${feature.color} rounded-xl mx-auto mb-4 flex items-center justify-center`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="font-semibold text-slate-900 mb-2">{feature.title}</h3>
                <p className="text-sm text-slate-600">{feature.desc}</p>
              </Card>
            );
          })}
        </div>

        {/* Results */}
        {results ? (
          <div className="space-y-6 animate-fade-in">
            {/* Score Card */}
            <Card>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-slate-900">Your ATS Score</h2>
                <div className="text-5xl font-bold text-transparent bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text">
                  {results.ats_score}%
                </div>
              </div>
              {results.sent_to_email && (
                <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-2 rounded-lg text-sm">
                  ✓ Results sent to {email}
                </div>
              )}
            </Card>

            {/* Summary */}
            {results.summary && (
              <Card>
                <h3 className="text-lg font-semibold text-slate-900 mb-3">Summary</h3>
                <p className="text-slate-700">{results.summary}</p>
              </Card>
            )}

            {/* Rejection Reasons */}
            {results.rejection_reasons && results.rejection_reasons.length > 0 && (
              <Card>
                <h3 className="text-lg font-semibold text-red-600 mb-3 flex items-center gap-2">
                  <AlertCircle className="w-5 h-5" />
                  Potential Rejection Reasons
                </h3>
                <ul className="space-y-2">
                  {results.rejection_reasons.map((reason, idx) => (
                    <li key={idx} className="flex items-start gap-3 text-slate-700">
                      <span className="text-red-500 font-bold mt-1">•</span>
                      <span>{reason}</span>
                    </li>
                  ))}
                </ul>
              </Card>
            )}

            {/* Strengths */}
            {results.strengths && results.strengths.length > 0 && (
              <Card>
                <h3 className="text-lg font-semibold text-green-600 mb-3 flex items-center gap-2">
                  <CheckCircle className="w-5 h-5" />
                  Your Strengths
                </h3>
                <ul className="space-y-2">
                  {results.strengths.map((strength, idx) => (
                    <li key={idx} className="flex items-start gap-3 text-slate-700">
                      <span className="text-green-500 font-bold mt-1">✓</span>
                      <span>{strength}</span>
                    </li>
                  ))}
                </ul>
              </Card>
            )}

            {/* Issues */}
            {results.issues && results.issues.length > 0 && (
              <Card>
                <h3 className="text-lg font-semibold text-orange-600 mb-3">Issues Found</h3>
                <ul className="space-y-2">
                  {results.issues.map((issue, idx) => (
                    <li key={idx} className="flex items-start gap-3 text-slate-700">
                      <span className="text-orange-500 font-bold mt-1">⚠</span>
                      <span>{issue}</span>
                    </li>
                  ))}
                </ul>
              </Card>
            )}

            {/* Suggestions */}
            {results.actionable_suggestions && results.actionable_suggestions.length > 0 && (
              <Card>
                <h3 className="text-lg font-semibold text-purple-600 mb-3 flex items-center gap-2">
                  <Target className="w-5 h-5" />
                  Actionable Suggestions
                </h3>
                <ul className="space-y-2">
                  {results.actionable_suggestions.map((suggestion, idx) => (
                    <li key={idx} className="flex items-start gap-3 text-slate-700">
                      <span className="text-purple-500 font-bold mt-1">→</span>
                      <span>{suggestion}</span>
                    </li>
                  ))}
                </ul>
              </Card>
            )}

            {/* Reset Button */}
            <Button
              variant="secondary"
              size="lg"
              onClick={() => {
                setResults(null);
                setResumeText('');
                setJobDescription('');
                setEmail('');
              }}
              className="w-full"
            >
              Analyze Another Resume
            </Button>
          </div>
        ) : (
          <Card className="animate-fade-in">
            <div className="text-center py-12">
              <FileText className="w-16 h-16 text-slate-300 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-slate-900 mb-2">Ready to Analyze</h3>
              <p className="text-slate-600">Enter your resume text and job description above to get started</p>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};

export default RejectionDetector;
