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
import Navbar from './Navbar';
import Card from './Card';
import Button from './Button';

const ExperienceAuthenticityAgent = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [githubUrl, setGithubUrl] = useState('');
  const [leetcodeUrl, setLeetcodeUrl] = useState('');
  const [additionalLinks, setAdditionalLinks] = useState([]);
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  // Handle file upload
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.type === 'application/pdf' || file.type === 'application/msword' || 
          file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
        setResumeFile(file);
        setError(null);
      } else {
        setError('Please upload a PDF or Word document');
        setResumeFile(null);
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
    if (!resumeFile) {
      setError('Please upload a resume');
      return;
    }

    setAnalyzing(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('resume', resumeFile);
      
      if (githubUrl) formData.append('github_url', githubUrl);
      if (leetcodeUrl) formData.append('leetcode_url', leetcodeUrl);
      
      // Add additional links
      additionalLinks.forEach((link, index) => {
        if (link.url && link.label) {
          formData.append(`additional_links[${index}][url]`, link.url);
          formData.append(`additional_links[${index}][label]`, link.label);
        }
      });

      const response = await fetch('http://localhost:8000/api/authenticity/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Analysis failed. Please try again.');
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
                    accept=".pdf,.doc,.docx"
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
                      {resumeFile ? resumeFile.name : 'Click to upload PDF or Word document'}
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
                  GitHub Profile URL <span className="text-slate-400 text-xs">(Optional)</span>
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

              {/* Action Buttons */}
              <div className="flex gap-3">
                <Button
                  onClick={handleAnalyze}
                  disabled={analyzing || !resumeFile}
                  className="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-semibold py-3 rounded-lg transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
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
                
                <Button
                  onClick={loadSampleData}
                  className="px-6 bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium py-3 rounded-lg transition-all"
                >
                  View Sample
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
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="text-lg font-semibold mb-1">Authenticity Score</h3>
                      <p className="text-purple-100 text-sm">Overall verification result</p>
                    </div>
                    <div className="w-20 h-20 relative">
                      <svg className="transform -rotate-90 w-20 h-20">
                        <circle
                          cx="40"
                          cy="40"
                          r="32"
                          stroke="rgba(255,255,255,0.2)"
                          strokeWidth="8"
                          fill="none"
                        />
                        <circle
                          cx="40"
                          cy="40"
                          r="32"
                          stroke="white"
                          strokeWidth="8"
                          fill="none"
                          strokeDasharray={`${(results.authenticity_score / 100) * 201} 201`}
                          strokeLinecap="round"
                        />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-2xl font-bold">{results.authenticity_score}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium">Confidence Level:</span>
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getConfidenceColor(results.confidence_level)}`}>
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
                    {results.skill_alignments.map((skill, index) => (
                      <div key={index} className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-semibold text-slate-900">{skill.skill}</span>
                          <span className={`w-2 h-2 rounded-full ${getSkillConfidenceColor(skill.confidence)}`}></span>
                        </div>
                        <div className="w-full bg-slate-200 rounded-full h-1.5">
                          <div 
                            className={`h-1.5 rounded-full ${getSkillConfidenceColor(skill.confidence)}`}
                            style={{ 
                              width: skill.confidence.toLowerCase() === 'high' ? '100%' : 
                                     skill.confidence.toLowerCase() === 'medium' ? '66%' : '33%' 
                            }}
                          ></div>
                        </div>
                        <span className="text-xs text-slate-600 mt-1 block">{skill.confidence} Confidence</span>
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
