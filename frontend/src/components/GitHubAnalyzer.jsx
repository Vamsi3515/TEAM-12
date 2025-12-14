import React, { useState } from 'react';
import { Github, Search, Star, GitFork, AlertCircle, Code2, ExternalLink, Activity, FileText, GitBranch, CheckCircle, TrendingUp, Zap, AlertTriangle, Lightbulb, Award, Eye, Server } from 'lucide-react';
import Navbar from './Navbar';
import Card from './Card';
import Button from './Button';

const GitHubAnalyzer = () => {
  const [repoUrl, setRepoUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState(null);

  const API_BASE_URL = 'http://localhost:8000/api';

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setAnalysis(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/analyze-github`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ repoUrl })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to analyze repository');
      }

      const data = await response.json();
      
      // Transform the data to match our frontend structure
      const transformedData = {
        repository: {
          url: repoUrl,
          name: extractRepoName(repoUrl),
          fullName: extractFullRepoName(repoUrl),
          description: data.repo_summary || 'No description available',
        },
        techStack: data.tech_stack || [],
        metrics: data.metrics || [],
        strengths: data.strengths || [],
        weaknesses: data.weaknesses || [],
        suggestions: data.suggestions || [],
        overallScore: calculateOverallScore(data.metrics),
        evidence: data.evidence_snippets || []
      };
      
      setAnalysis(transformedData);
    } catch (err) {
      setError(err.message);
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const extractRepoName = (url) => {
    const parts = url.replace(/\.git$/, '').split('/');
    return parts[parts.length - 1] || 'repository';
  };

  const extractFullRepoName = (url) => {
    const parts = url.replace(/\.git$/, '').split('/');
    if (parts.length >= 2) {
      return `${parts[parts.length - 2]}/${parts[parts.length - 1]}`;
    }
    return url;
  };

  const calculateOverallScore = (metrics) => {
    if (!metrics || metrics.length === 0) return 0;
    const sum = metrics.reduce((acc, m) => acc + (m.score || 0), 0);
    return Math.round(sum / metrics.length);
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-50 border-green-200';
    if (score >= 60) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    return 'text-red-600 bg-red-50 border-red-200';
  };

  const getProgressColor = (score) => {
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getOverallScoreColor = (score) => {
    if (score >= 80) return 'from-green-500 to-emerald-600';
    if (score >= 60) return 'from-yellow-500 to-orange-500';
    return 'from-red-500 to-rose-600';
  };

  const getOverallScoreRing = (score) => {
    if (score >= 80) return 'stroke-green-500';
    if (score >= 60) return 'stroke-yellow-500';
    return 'stroke-red-500';
  };

  const getScoreBadgeColor = (score) => {
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/30">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12 animate-slide-up">
          <div className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-100 to-cyan-100 text-blue-700 px-4 py-2 rounded-full text-sm font-medium mb-4">
            <Github className="w-4 h-4" />
            <span>AI-Powered Repository Analyzer</span>
          </div>
          <h1 className="text-4xl font-bold text-slate-900 mb-4">
            Analyze GitHub
            <span className="block bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
              Repository Quality
            </span>
          </h1>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Get detailed AI-powered insights with RAG-enhanced analysis
          </p>
        </div>

        {/* Search Form */}
        <Card className="max-w-3xl mx-auto mb-12 animate-fade-in">
          <form onSubmit={handleAnalyze}>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Repository URL
                </label>
                <div className="flex flex-col sm:flex-row gap-3">
                  <div className="flex-1">
                    <input
                      type="text"
                      placeholder="https://github.com/username/repository"
                      value={repoUrl}
                      onChange={(e) => setRepoUrl(e.target.value)}
                      className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                      required
                    />
                  </div>
                  <Button 
                    variant="primary" 
                    size="lg" 
                    icon={Search}
                    type="submit"
                    disabled={loading}
                    className="sm:w-auto w-full"
                  >
                    {loading ? 'Analyzing...' : 'Analyze'}
                  </Button>
                </div>
              </div>
              <p className="text-sm text-slate-500">
                Example: https://github.com/microsoft/vscode or microsoft/vscode
              </p>
            </div>
          </form>
        </Card>

        {/* Error State */}
        {error && (
          <Card className="max-w-3xl mx-auto mb-12 bg-red-50 border-red-200 animate-fade-in">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-semibold text-red-900 mb-1">Analysis Error</h3>
                <p className="text-red-700">{error}</p>
                <p className="text-sm text-red-600 mt-2">
                  Please check the repository URL and try again. Make sure the repository is public or you have access.
                </p>
              </div>
            </div>
          </Card>
        )}

        {/* Loading State */}
        {loading && (
          <div className="flex flex-col items-center justify-center py-16 animate-fade-in">
            <div className="relative">
              <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-4"></div>
              <Server className="w-6 h-6 text-blue-600 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
            </div>
            <p className="text-slate-600 font-medium">Analyzing repository...</p>
            <p className="text-sm text-slate-500 mt-2">Fetching data from GitHub API and running AI analysis</p>
          </div>
        )}

        {/* Results */}
        {analysis && !loading && (
          <div className="space-y-8 animate-fade-in">
            {/* Repository Header Card */}
            <Card className="bg-gradient-to-br from-blue-500 via-blue-600 to-cyan-600 border-none text-white overflow-hidden relative">
              <div className="absolute inset-0 bg-black opacity-5"></div>
              <div className="absolute top-0 right-0 w-64 h-64 bg-white opacity-5 rounded-full -mr-32 -mt-32"></div>
              <div className="absolute bottom-0 left-0 w-48 h-48 bg-white opacity-5 rounded-full -ml-24 -mb-24"></div>
              
              <div className="relative z-10">
                <div className="flex items-start justify-between mb-6">
                  <div className="flex items-center gap-4">
                    <div className="w-16 h-16 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center ring-2 ring-white/30">
                      <Github className="w-8 h-8" />
                    </div>
                    <div>
                      <h2 className="text-3xl font-bold mb-1">{analysis.repository.name}</h2>
                      <p className="text-blue-100 text-lg">{analysis.repository.fullName}</p>
                    </div>
                  </div>
                  <a
                    href={analysis.repository.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 bg-white/20 hover:bg-white/30 backdrop-blur px-4 py-2 rounded-lg transition-all duration-200"
                  >
                    <span className="text-sm font-medium">View on GitHub</span>
                    <ExternalLink className="w-4 h-4" />
                  </a>
                </div>
                
                <p className="text-blue-50 text-base mb-6 leading-relaxed">
                  {analysis.repository.description}
                </p>

                {/* Tech Stack Tags */}
                {analysis.techStack && analysis.techStack.length > 0 && (
                  <div>
                    <p className="text-blue-100 text-sm font-medium mb-3">Technology Stack</p>
                    <div className="flex flex-wrap gap-2">
                      {analysis.techStack.map((tech, idx) => (
                        <span key={idx} className="px-3 py-1.5 bg-white/20 backdrop-blur rounded-lg text-sm font-medium hover:bg-white/30 transition-all">
                          {tech}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </Card>

            {/* Overall Score - Large Circular Visualization */}
            <div className="flex justify-center">
              <Card className="inline-block text-center relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-cyan-50 opacity-50"></div>
                <div className="relative z-10">
                  <div className="relative inline-flex items-center justify-center mb-4">
                    {/* Outer decorative ring */}
                    <div className="absolute inset-0 bg-gradient-to-br from-blue-200 to-cyan-200 rounded-full opacity-20 animate-pulse"></div>
                    
                    {/* SVG Circle Progress */}
                    <svg className="w-56 h-56 transform -rotate-90">
                      {/* Background circle */}
                      <circle
                        cx="112"
                        cy="112"
                        r="100"
                        stroke="currentColor"
                        strokeWidth="16"
                        fill="none"
                        className="text-slate-200"
                      />
                      {/* Progress circle with gradient */}
                      <defs>
                        <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                          <stop offset="0%" stopColor={analysis.overallScore >= 80 ? '#10b981' : analysis.overallScore >= 60 ? '#f59e0b' : '#ef4444'} />
                          <stop offset="100%" stopColor={analysis.overallScore >= 80 ? '#059669' : analysis.overallScore >= 60 ? '#d97706' : '#dc2626'} />
                        </linearGradient>
                      </defs>
                      <circle
                        cx="112"
                        cy="112"
                        r="100"
                        stroke="url(#scoreGradient)"
                        strokeWidth="16"
                        fill="none"
                        strokeDasharray={`${(analysis.overallScore / 100) * 628} 628`}
                        strokeLinecap="round"
                        className="transition-all duration-1000 ease-out"
                        style={{ filter: 'drop-shadow(0 0 8px rgba(59, 130, 246, 0.5))' }}
                      />
                    </svg>
                    
                    {/* Score Display */}
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <div className={`text-6xl font-bold bg-gradient-to-br ${getOverallScoreColor(analysis.overallScore)} bg-clip-text text-transparent mb-2`}>
                        {analysis.overallScore}
                      </div>
                      <div className="text-slate-600 font-semibold text-lg">Overall Score</div>
                    </div>
                  </div>
                  
                  {/* Score Label */}
                  <div className="mt-6">
                    <div className={`inline-flex items-center gap-2 px-6 py-3 rounded-full text-base font-semibold ${getScoreColor(analysis.overallScore)} border-2`}>
                      {analysis.overallScore >= 80 ? <Award className="w-5 h-5" /> : 
                       analysis.overallScore >= 60 ? <Eye className="w-5 h-5" /> : 
                       <AlertTriangle className="w-5 h-5" />}
                      <span>
                        {analysis.overallScore >= 80 ? 'Excellent Quality' : 
                         analysis.overallScore >= 60 ? 'Good Quality' : 
                         'Needs Improvement'}
                      </span>
                    </div>
                  </div>
                </div>
              </Card>
            </div>

            {/* Detailed Metrics - Advanced Grid */}
            <div>
              <h3 className="text-2xl font-bold text-slate-900 mb-6 text-center">Detailed Analysis Metrics</h3>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {analysis.metrics.map((metric, index) => (
                  <Card key={index} hover className="group relative overflow-hidden">
                    {/* Background decoration */}
                    <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-blue-100 to-cyan-100 rounded-full -mr-16 -mt-16 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                    
                    <div className="relative z-10">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex-1">
                          <h4 className="text-lg font-semibold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors">
                            {metric.name}
                          </h4>
                          <p className="text-sm text-slate-600 leading-relaxed">
                            {metric.explanation}
                          </p>
                        </div>
                        <div className="ml-4">
                          <div className={`w-16 h-16 rounded-xl flex items-center justify-center text-2xl font-bold border-2 ${getScoreColor(metric.score)}`}>
                            {metric.score}
                          </div>
                        </div>
                      </div>
                      
                      {/* Advanced Progress Bar with Animation */}
                      <div className="space-y-2">
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-slate-600 font-medium">Performance</span>
                          <span className="text-slate-900 font-semibold">{metric.score}/100</span>
                        </div>
                        <div className="relative h-3 bg-slate-200 rounded-full overflow-hidden">
                          {/* Shimmer effect */}
                          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-30 animate-pulse"></div>
                          <div
                            className={`h-full ${getProgressColor(metric.score)} rounded-full transition-all duration-1000 ease-out relative`}
                            style={{ width: `${metric.score}%` }}
                          >
                            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-30"></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </div>

            {/* Strengths, Weaknesses & Suggestions Grid */}
            <div className="grid lg:grid-cols-2 gap-6">
              {/* Strengths */}
              <Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-green-200">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center">
                    <CheckCircle className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900">Strengths</h3>
                  <span className="ml-auto text-sm font-semibold text-green-700 bg-green-200 px-3 py-1 rounded-full">
                    {analysis.strengths.length}
                  </span>
                </div>
                <ul className="space-y-3">
                  {analysis.strengths.map((strength, idx) => (
                    <li key={idx} className="flex items-start gap-3 text-slate-700 bg-white p-3 rounded-lg">
                      <Zap className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                      <span className="leading-relaxed">{strength}</span>
                    </li>
                  ))}
                </ul>
              </Card>

              {/* Weaknesses */}
              <Card className="bg-gradient-to-br from-orange-50 to-red-50 border-orange-200">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-orange-500 rounded-lg flex items-center justify-center">
                    <AlertTriangle className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900">Areas for Improvement</h3>
                  <span className="ml-auto text-sm font-semibold text-orange-700 bg-orange-200 px-3 py-1 rounded-full">
                    {analysis.weaknesses.length}
                  </span>
                </div>
                <ul className="space-y-3">
                  {analysis.weaknesses.map((weakness, idx) => (
                    <li key={idx} className="flex items-start gap-3 text-slate-700 bg-white p-3 rounded-lg">
                      <AlertCircle className="w-5 h-5 text-orange-600 flex-shrink-0 mt-0.5" />
                      <span className="leading-relaxed">{weakness}</span>
                    </li>
                  ))}
                </ul>
              </Card>
            </div>

            {/* Actionable Suggestions */}
            <Card className="bg-gradient-to-br from-blue-50 to-cyan-50 border-blue-200">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center">
                  <Lightbulb className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-slate-900">Actionable Suggestions</h3>
                  <p className="text-slate-600">Recommendations to improve repository quality</p>
                </div>
              </div>
              <div className="grid md:grid-cols-2 gap-4">
                {analysis.suggestions.map((suggestion, idx) => (
                  <div key={idx} className="flex items-start gap-3 bg-white p-4 rounded-lg border border-blue-100 hover:border-blue-300 transition-all">
                    <span className="w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-500 text-white rounded-lg flex items-center justify-center text-sm font-bold flex-shrink-0">
                      {idx + 1}
                    </span>
                    <span className="text-slate-700 leading-relaxed">{suggestion}</span>
                  </div>
                ))}
              </div>
            </Card>

            {/* RAG Evidence Section */}
            {analysis.evidence && analysis.evidence.length > 0 && (
              <Card className="bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                    <FileText className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold text-slate-900">Knowledge Base Evidence</h3>
                    <p className="text-slate-600">RAG-enhanced analysis references</p>
                  </div>
                </div>
                <div className="space-y-4">
                  {analysis.evidence.map((evidence, idx) => (
                    <div key={idx} className="bg-white p-4 rounded-lg border border-purple-100">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs font-mono font-semibold">
                          {evidence.id}
                        </span>
                        <span className="text-xs text-slate-500">Knowledge Reference {idx + 1}</span>
                      </div>
                      <p className="text-sm text-slate-700 leading-relaxed">{evidence.snippet}</p>
                    </div>
                  ))}
                </div>
              </Card>
            )}

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button
                variant="outline"
                size="lg"
                onClick={() => {
                  setAnalysis(null);
                  setRepoUrl('');
                  setError(null);
                }}
                icon={Search}
              >
                Analyze Another Repository
              </Button>
              {/* <Button
                variant="primary"
                size="lg"
                icon={TrendingUp}
                className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700"
              >
                Export Report
              </Button> */}
            </div>
          </div>
        )}

        {/* Placeholder State */}
        {!analysis && !loading && !error && (
          <Card className="animate-fade-in">
            <div className="text-center py-12">
              <div className="relative inline-block mb-6">
                <div className="absolute inset-0 bg-blue-200 rounded-full blur-xl opacity-50 animate-pulse"></div>
                <Github className="w-20 h-20 text-slate-300 relative" />
              </div>
              <h3 className="text-2xl font-semibold text-slate-900 mb-3">Ready to Analyze</h3>
              <p className="text-slate-600 mb-8 max-w-md mx-auto">
                Enter a GitHub repository URL above to get comprehensive AI-powered insights
              </p>
              
              {/* Feature Highlights */}
              <div className="grid md:grid-cols-3 gap-6 mt-8 max-w-3xl mx-auto">
                {[
                  { icon: Activity, title: 'Code Quality Analysis', desc: 'In-depth evaluation of code structure' },
                  { icon: FileText, title: 'Documentation Review', desc: 'README and comment quality assessment' },
                  { icon: GitBranch, title: 'Best Practices', desc: 'Compare against industry standards' },
                ].map((feature, idx) => {
                  const Icon = feature.icon;
                  return (
                    <div key={idx} className="text-center">
                      <div className="w-12 h-12 bg-gradient-to-br from-blue-100 to-cyan-100 rounded-xl mx-auto mb-3 flex items-center justify-center">
                        <Icon className="w-6 h-6 text-blue-600" />
                      </div>
                      <h4 className="font-semibold text-slate-900 mb-1 text-sm">{feature.title}</h4>
                      <p className="text-xs text-slate-600">{feature.desc}</p>
                    </div>
                  );
                })}
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};

export default GitHubAnalyzer;
