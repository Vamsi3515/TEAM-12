import React, { useState } from 'react';
import { 
  Shield, 
  Upload, 
  Github, 
  Code, 
  Link as LinkIcon, 
  Plus, 
  X, 
  CheckCircle, 
  AlertTriangle,
  TrendingUp,
  FileText,
  Loader,
  Award,
  Target,
  Lightbulb
} from 'lucide-react';
import * as pdfjsLib from 'pdfjs-dist';
import Navbar from './Navbar';
import Card from './Card';
import Button from './Button';

// Set PDF worker from unpkg CDN matching the installed version
pdfjsLib.GlobalWorkerOptions.workerSrc = `https://unpkg.com/pdfjs-dist@${pdfjsLib.version}/build/pdf.worker.min.mjs`;

const ExperienceAuthenticityAgent = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [githubUrl, setGithubUrl] = useState('');
  const [leetcodeUrl, setLeetcodeUrl] = useState('');
  const [additionalLinks, setAdditionalLinks] = useState([]);
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  // Parse resume file (PDF or TXT)
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
        let extractedText = fullText.trim();
        
        // Validate extracted text
        if (!extractedText || extractedText.length < 10) {
          setError('Could not extract text from PDF. The file may be scanned or empty.');
          return null;
        }
        
        // Clean the text by removing problematic control characters but keeping common ones
        extractedText = extractedText.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, ' ');
        
        // Check if we have actual text content after cleaning
        const alphanumericCount = (extractedText.match(/[a-zA-Z0-9]/g) || []).length;
        if (alphanumericCount < 20) {
          setError('PDF does not contain enough readable text. Please use a text-based PDF.');
          return null;
        }
        
        setResumeText(extractedText);
        return extractedText;
      } else if (file.type === 'text/plain') {
        const text = await file.text();
        if (!text || text.trim().length < 10) {
          setError('Text file is empty or too short.');
          return null;
        }
        setResumeText(text);
        return text;
      } else {
        setError('Unsupported file type. Please use PDF or TXT.');
        return null;
      }
    } catch (err) {
      setError('Failed to parse resume file: ' + err.message);
      console.error('Error parsing file:', err);
      return null;
    }
  };

  // Handle file upload
  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (file) {
      setResumeFile(file);
      setError(null);
      
      if (file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' || 
          file.name.endsWith('.docx')) {
        setError('DOCX parsing requires Word document library. Please use PDF or TXT instead.');
        setResumeFile(null);
        setResumeText('');
      } else if (file.type === 'application/pdf' || file.type === 'text/plain') {
        await parseResumeFile(file);
      } else {
        setError('Unsupported file type. Please upload PDF or TXT.');
        setResumeFile(null);
        setResumeText('');
      }
    }
  };

  // Add additional link
  const addLink = () => {
    setAdditionalLinks([...additionalLinks, { id: Date.now(), url: '', label: '' }]);
  };

  // Remove additional link
  const removeLink = (id) => {
    setAdditionalLinks(additionalLinks.filter(link => link.id !== id));
  };

  // Update additional link
  const updateLink = (id, field, value) => {
    setAdditionalLinks(additionalLinks.map(link => 
      link.id === id ? { ...link, [field]: value } : link
    ));
  };

  // Handle form submission
  const handleAnalyze = async () => {
    if (!resumeFile || !resumeText) {
      setError('Please upload a resume');
      return;
    }

    // Validate resume text before sending
    if (resumeText.trim().length < 50) {
      setError('Resume text is too short. Please upload a valid resume.');
      return;
    }

    setAnalyzing(true);
    setError(null);

    try {
      // Build evidences array from URLs
      const evidences = [];
      
      if (githubUrl) {
        evidences.push({
          type: 'github_profile',
          url: githubUrl,
          title: githubUrl.split('/').pop() || 'GitHub Profile',
          metadata: {}
        });
      }
      
      if (leetcodeUrl) {
        evidences.push({
          type: 'leetcode_profile',
          url: leetcodeUrl,
          title: leetcodeUrl.split('/').pop() || 'LeetCode Profile',
          metadata: {}
        });
      }
      
      // Add additional links as evidences
      additionalLinks.forEach((link) => {
        if (link.url && link.label) {
          evidences.push({
            type: 'link',
            url: link.url,
            title: link.label,
            description: link.label,
            metadata: {}
          });
        }
      });

      // Truncate very long text (limit to ~10k chars to prevent API issues)
      const sanitizedResumeText = resumeText.slice(0, 10000);
      
      // Construct request payload matching AuthenticityExtendedInput schema
      const requestBody = {
        resume: {
          raw_text: sanitizedResumeText,
          skills: [],
          experience: [],
          projects: [],
          education: [],
          certifications: []
        },
        evidences: evidences,
        additional_context: `Resume file: ${resumeFile.name}`
      };
      
      console.log('Sending analysis request with resume text length:', sanitizedResumeText.length);

      const response = await fetch('http://localhost:8000/api/analyze-authenticity', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Analysis failed. Please try again.');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message || 'An error occurred during analysis');
    } finally {
      setAnalyzing(false);
    }
  };

  // Load sample data
  const loadSampleData = () => {
    setResults({
      confidence_level: "High",
      authenticity_score: 87,
      strong_evidence: [
        "GitHub profile shows 3+ years of consistent Python contributions",
        "LeetCode profile demonstrates strong algorithmic skills (250+ problems solved)",
        "Resume projects align with GitHub repositories",
        "Technical blog posts match claimed expertise areas",
        "Certifications verified through LinkedIn"
      ],
      risk_indicators: [
        "Gap in activity between 2022-2023 not explained in resume",
        "Some projects lack documentation or README files",
        "Limited contribution to open source projects",
        "No presence on professional platforms like Stack Overflow"
      ],
      overall_assessment: "The candidate demonstrates strong technical authenticity with verifiable evidence across multiple platforms. GitHub activity shows consistent coding patterns matching resume claims. However, some gaps in documentation and community engagement suggest areas for improvement. Overall, the profile presents a credible and authentic representation of skills.",
      improvement_suggestions: [
        "Add detailed README files to GitHub projects to showcase documentation skills",
        "Fill in the 2022-2023 activity gap explanation in resume",
        "Increase participation in open source projects",
        "Create technical blog posts or tutorials to demonstrate expertise",
        "Engage more actively in developer communities (Stack Overflow, dev.to)",
        "Add certifications and continuous learning activities to profile"
      ],
      skill_alignments: [
        { skill: "Python", confidence: "High" },
        { skill: "React", confidence: "High" },
        { skill: "Node.js", confidence: "Medium" },
        { skill: "Machine Learning", confidence: "Medium" },
        { skill: "Docker", confidence: "High" },
        { skill: "AWS", confidence: "Low" },
        { skill: "Data Structures", confidence: "High" },
        { skill: "System Design", confidence: "Medium" }
      ]
    });
  };

  // Get confidence level color
  const getConfidenceColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'high': return 'text-green-600 bg-green-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  // Get skill confidence color
  const getSkillConfidenceColor = (confidence) => {
    switch (confidence?.toLowerCase()) {
      case 'high': return 'bg-green-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50/30 to-blue-50/30">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-8 animate-slide-up">
          <div className="inline-flex items-center gap-2 bg-gradient-to-r from-purple-100 to-blue-100 text-purple-700 px-4 py-2 rounded-full text-sm font-medium mb-4 shadow-sm">
            <Shield className="w-4 h-4" />
            <span>AI-Powered Authenticity Verification</span>
          </div>
          
          <h1 className="text-4xl font-bold text-slate-900 mb-3">
            Experience Authenticity & 
            <span className="block bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent">
              Skill Consistency Agent
            </span>
          </h1>
          
          <p className="text-lg text-slate-600 max-w-3xl mx-auto">
            Verify resume claims with AI analysis of GitHub, LeetCode, and online presence
          </p>
        </div>

        {/* Two Column Layout */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* LEFT COLUMN - INPUT */}
          <div className="space-y-6">
            <Card className="animate-slide-up" style={{ animationDelay: '0.1s' }}>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg flex items-center justify-center">
                  <Upload className="w-5 h-5 text-white" />
                </div>
                <h2 className="text-xl font-bold text-slate-900">Upload Information</h2>
              </div>

              {/* Resume Upload */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Resume / CV <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <input
                    type="file"
                    accept=".pdf,.txt"
                    onChange={handleFileChange}
                    className="hidden"
                    id="resume-upload"
                  />
                  <label
                    htmlFor="resume-upload"
                    className="flex items-center justify-center gap-2 w-full px-4 py-8 border-2 border-dashed border-slate-300 rounded-xl hover:border-purple-500 hover:bg-purple-50/50 transition-all cursor-pointer group"
                  >
                    <FileText className="w-6 h-6 text-slate-400 group-hover:text-purple-500 transition-colors" />
                    <span className="text-slate-600 group-hover:text-purple-600 transition-colors">
                      {resumeFile ? resumeFile.name : 'Click to upload PDF or TXT document'}
                    </span>
                  </label>
                  {resumeFile && (
                    <div className="mt-2 flex items-center gap-2 text-sm text-green-600">
                      <CheckCircle className="w-4 h-4" />
                      <span>File uploaded successfully</span>
                    </div>
                  )}
                </div>
              </div>

              {/* GitHub URL */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-700 mb-2 flex items-center gap-2">
                  <Github className="w-4 h-4" />
                  GitHub Profile URL
                </label>
                <input
                  type="url"
                  value={githubUrl}
                  onChange={(e) => setGithubUrl(e.target.value)}
                  placeholder="https://github.com/username"
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                />
              </div>

              {/* LeetCode URL */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-700 mb-2 flex items-center gap-2">
                  <Code className="w-4 h-4" />
                  LeetCode Profile URL <span className="text-slate-400 text-xs">(Optional)</span>
                </label>
                <input
                  type="url"
                  value={leetcodeUrl}
                  onChange={(e) => setLeetcodeUrl(e.target.value)}
                  placeholder="https://leetcode.com/username"
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                />
              </div>

              {/* Additional Links */}
              <div className="mb-6">
                <div className="flex items-center justify-between mb-3">
                  <label className="block text-sm font-medium text-slate-700 flex items-center gap-2">
                    <LinkIcon className="w-4 h-4" />
                    Additional Links <span className="text-slate-400 text-xs">(Optional)</span>
                  </label>
                  <button
                    onClick={addLink}
                    className="flex items-center gap-1 text-sm text-purple-600 hover:text-purple-700 font-medium transition-colors"
                  >
                    <Plus className="w-4 h-4" />
                    Add Link
                  </button>
                </div>
                
                {additionalLinks.map((link) => (
                  <div key={link.id} className="flex gap-2 mb-3">
                    <input
                      type="text"
                      value={link.label}
                      onChange={(e) => updateLink(link.id, 'label', e.target.value)}
                      placeholder="Label (e.g., Portfolio, LinkedIn)"
                      className="flex-1 px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-sm"
                    />
                    <input
                      type="url"
                      value={link.url}
                      onChange={(e) => updateLink(link.id, 'url', e.target.value)}
                      placeholder="https://..."
                      className="flex-1 px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-sm"
                    />
                    <button
                      onClick={() => removeLink(link.id)}
                      className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </div>
                ))}
              </div>

              {/* Error Message */}
              {error && (
                <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
                  <AlertTriangle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                  <p className="text-sm text-red-800">{error}</p>
                </div>
              )}

              {/* Action Button */}
              <div>
                <Button
                  onClick={handleAnalyze}
                  disabled={analyzing || !resumeFile}
                  className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-semibold py-3 rounded-lg transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {analyzing ? (
                    <>
                      <Loader className="w-5 h-5 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Shield className="w-5 h-5" />
                      Analyze Authenticity
                    </>
                  )}
                </Button>
              </div>
            </Card>
          </div>

          {/* RIGHT COLUMN - RESULTS */}
          <div className="space-y-6">
            {results ? (
              <>
                {/* Overall Score Card */}
                <Card className="animate-slide-up bg-gradient-to-br from-purple-600 to-blue-600 text-white" style={{ animationDelay: '0.2s' }}>
                  <div className="text-center py-8">
                    <h3 className="text-2xl font-bold mb-2">Authenticity Score</h3>
                    <p className="text-purple-100 text-sm mb-6">Overall verification result</p>
                    
                    <div className="flex items-center justify-center mb-6">
                      <div className="w-48 h-48 relative">
                        <svg className="transform -rotate-90 w-48 h-48">
                          <circle
                            cx="96"
                            cy="96"
                            r="88"
                            stroke="rgba(255,255,255,0.2)"
                            strokeWidth="12"
                            fill="none"
                          />
                          <circle
                            cx="96"
                            cy="96"
                            r="88"
                            stroke="white"
                            strokeWidth="12"
                            fill="none"
                            strokeDasharray={`${(results.authenticity_score / 100) * 553} 553`}
                            strokeLinecap="round"
                            className="transition-all duration-1000"
                          />
                        </svg>
                        <div className="absolute inset-0 flex flex-col items-center justify-center">
                          <span className="text-6xl font-extrabold">{results.authenticity_score}</span>
                          <span className="text-xl font-semibold text-purple-100">/ 100</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-center gap-2 pt-4 border-t border-white/20">
                    <span className="text-sm font-medium">Confidence Level:</span>
                    <span className={`px-4 py-1.5 rounded-full text-sm font-bold ${getConfidenceColor(results.confidence_level)}`}>
                      {results.confidence_level}
                    </span>
                  </div>
                  
                  {/* Low Confidence Warning */}
                  {results.confidence_level?.toLowerCase() === 'low' && (
                    <div className="mt-4 p-4 bg-red-500 rounded-lg">
                      <p className="text-white font-bold text-center text-sm">
                        Can't be Analyzed, no supportive evidence is provided.
                      </p>
                    </div>
                  )}
                </Card>

                {/* Overall Assessment */}
                <Card className="animate-slide-up" style={{ animationDelay: '0.3s' }}>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-lg flex items-center justify-center">
                      <Target className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-900">Overall Assessment</h3>
                  </div>
                  <p className="text-slate-700 leading-relaxed">{results.overall_assessment}</p>
                </Card>

                {/* Strong Evidence */}
                <Card className="animate-slide-up" style={{ animationDelay: '0.4s' }}>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg flex items-center justify-center">
                      <CheckCircle className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-900">Strong Evidence</h3>
                  </div>
                  <div className="space-y-3">
                    {results.strong_evidence.map((evidence, index) => (
                      <div key={index} className="flex items-start gap-3 p-3 bg-green-50 rounded-lg border border-green-100">
                        <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                        <p className="text-sm text-slate-700">{evidence}</p>
                      </div>
                    ))}
                  </div>
                </Card>

                {/* Risk Indicators */}
                <Card className="animate-slide-up" style={{ animationDelay: '0.5s' }}>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-lg flex items-center justify-center">
                      <AlertTriangle className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-900">Risk Indicators</h3>
                  </div>
                  <div className="space-y-3">
                    {results.risk_indicators.map((risk, index) => (
                      <div key={index} className="flex items-start gap-3 p-3 bg-yellow-50 rounded-lg border border-yellow-100">
                        <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                        <p className="text-sm text-slate-700">{risk}</p>
                      </div>
                    ))}
                  </div>
                </Card>

                {/* Skill Alignments */}
                <Card className="animate-slide-up" style={{ animationDelay: '0.6s' }}>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                      <Award className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-900">Skill Alignments</h3>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    {results.skill_alignments && results.skill_alignments.map((skill, index) => (
                      <div key={index} className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-semibold text-slate-900">{skill.skill}</span>
                          <span className={`w-2 h-2 rounded-full ${getSkillConfidenceColor(skill.confidence)}`}></span>
                        </div>
                        <div className="w-full bg-slate-200 rounded-full h-1.5 mb-2">
                          <div 
                            className={`h-1.5 rounded-full ${getSkillConfidenceColor(skill.confidence)}`}
                            style={{ 
                              width: skill.confidence.toLowerCase() === 'high' ? '100%' : 
                                     skill.confidence.toLowerCase() === 'medium' ? '66%' : '33%' 
                            }}
                          ></div>
                        </div>
                        <span className="text-xs text-slate-600 block mb-1">{skill.confidence} Confidence</span>
                        {skill.evidence_source && skill.evidence_source.length > 0 && (
                          <div className="text-xs text-slate-500 mt-1">
                            Sources: {skill.evidence_source.join(', ')}
                          </div>
                        )}
                        {skill.supporting_evidence && skill.supporting_evidence.length > 0 && (
                          <div className="text-xs text-slate-600 mt-2">
                            {skill.supporting_evidence.slice(0, 2).map((evidence, idx) => (
                              <div key={idx} className="flex items-start gap-1 mt-1">
                                <CheckCircle className="w-3 h-3 text-green-500 flex-shrink-0 mt-0.5" />
                                <span>{evidence}</span>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </Card>

                {/* Improvement Suggestions */}
                <Card className="animate-slide-up" style={{ animationDelay: '0.7s' }}>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center">
                      <Lightbulb className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-900">Improvement Suggestions</h3>
                  </div>
                  <div className="space-y-3">
                    {results.improvement_suggestions.map((suggestion, index) => (
                      <div key={index} className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg border border-blue-100">
                        <TrendingUp className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                        <p className="text-sm text-slate-700">{suggestion}</p>
                      </div>
                    ))}
                  </div>
                </Card>
              </>
            ) : (
              <Card className="animate-slide-up text-center py-12" style={{ animationDelay: '0.2s' }}>
                <div className="w-20 h-20 bg-gradient-to-r from-purple-100 to-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Shield className="w-10 h-10 text-purple-600" />
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-2">Ready to Verify</h3>
                <p className="text-slate-600 mb-4">
                  Upload your resume and add profile links to start the authenticity analysis
                </p>
                <div className="flex flex-wrap justify-center gap-3 text-sm text-slate-500">
                  <div className="flex items-center gap-2">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span>AI-Powered Analysis</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span>Multi-Platform Verification</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span>Detailed Insights</span>
                  </div>
                </div>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExperienceAuthenticityAgent;
