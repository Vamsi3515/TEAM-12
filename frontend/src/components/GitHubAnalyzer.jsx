import React, { useState } from 'react';
import { Github, Search, Star, GitFork, AlertCircle, Code2, ExternalLink, Activity, FileText, GitBranch, CheckCircle } from 'lucide-react';
import Navbar from './Navbar';
import Card from './Card';
import Button from './Button';

const GitHubAnalyzer = () => {
  const [repoUrl, setRepoUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);

  // Mock data for demonstration - replace with actual API call
  const mockAnalysis = {
    repository: {
      name: 'vscode',
      fullName: 'microsoft/vscode',
      description: 'Visual Studio Code - Open source code editor developed by Microsoft',
      url: 'https://github.com/microsoft/vscode',
      stats: {
        stars: 163245,
        forks: 28456,
        issues: 5234,
        language: 'TypeScript'
      }
    },
    detailedScores: [
      {
        category: 'Code Quality',
        score: 92,
        description: 'Excellent code structure and maintainability'
      },
      {
        category: 'Documentation',
        score: 88,
        description: 'Comprehensive documentation and API references'
      },
      {
        category: 'Complexity',
        score: 75,
        description: 'Moderate complexity level'
      },
      {
        category: 'Activity',
        score: 95,
        description: 'Very active development and contributions'
      },
      {
        category: 'Community Health',
        score: 90,
        description: 'Strong community engagement'
      },
      {
        category: 'Security',
        score: 87,
        description: 'Good security practices implemented'
      }
    ],
    overallScore: 88
  };

  const handleAnalyze = (e) => {
    e.preventDefault();
    setLoading(true);
    
    // Simulate API call - replace with actual GitHub API integration
    setTimeout(() => {
      setAnalysis(mockAnalysis);
      setLoading(false);
    }, 2000);
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/30">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12 animate-slide-up">
          <div className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-100 to-cyan-100 text-blue-700 px-4 py-2 rounded-full text-sm font-medium mb-4">
            <Github className="w-4 h-4" />
            <span>GitHub Repository Analyzer</span>
          </div>
          <h1 className="text-4xl font-bold text-slate-900 mb-4">
            Analyze GitHub
            <span className="block bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
              Repository Quality
            </span>
          </h1>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Get detailed AI-powered insights into repository quality and performance
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
                      type="url"
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
                Example: https://github.com/microsoft/vscode
              </p>
            </div>
          </form>
        </Card>

        {/* Loading State */}
        {loading && (
          <div className="flex flex-col items-center justify-center py-16 animate-fade-in">
            <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-4"></div>
            <p className="text-slate-600 font-medium">Analyzing repository...</p>
            <p className="text-sm text-slate-500 mt-2">This may take a few seconds</p>
          </div>
        )}

        {/* Results */}
        {analysis && !loading && (
          <div className="space-y-8 animate-fade-in">
            {/* Repository Information Card */}
            <Card className="bg-gradient-to-br from-blue-500 to-cyan-600 border-none text-white overflow-hidden relative">
              <div className="absolute inset-0 bg-black opacity-5"></div>
              <div className="relative z-10">
                <div className="flex items-start justify-between mb-6">
                  <div className="flex items-center gap-3">
                    <div className="w-16 h-16 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center">
                      <Github className="w-8 h-8" />
                    </div>
                    <div>
                      <h2 className="text-3xl font-bold mb-1">{analysis.repository.name}</h2>
                      <p className="text-blue-100 text-lg">{analysis.repository.fullName}</p>
                    </div>
                  </div>
                </div>
                
                <p className="text-blue-50 text-lg mb-6 leading-relaxed">
                  {analysis.repository.description}
                </p>

                {/* Statistics Grid */}
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                  <div className="bg-white/10 backdrop-blur rounded-xl p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <Star className="w-5 h-5 text-yellow-300" />
                      <span className="text-sm font-medium text-blue-100">Stars</span>
                    </div>
                    <div className="text-2xl font-bold">{analysis.repository.stats.stars.toLocaleString()}</div>
                  </div>
                  <div className="bg-white/10 backdrop-blur rounded-xl p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <GitFork className="w-5 h-5 text-blue-300" />
                      <span className="text-sm font-medium text-blue-100">Forks</span>
                    </div>
                    <div className="text-2xl font-bold">{analysis.repository.stats.forks.toLocaleString()}</div>
                  </div>
                  <div className="bg-white/10 backdrop-blur rounded-xl p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <AlertCircle className="w-5 h-5 text-orange-300" />
                      <span className="text-sm font-medium text-blue-100">Issues</span>
                    </div>
                    <div className="text-2xl font-bold">{analysis.repository.stats.issues.toLocaleString()}</div>
                  </div>
                  <div className="bg-white/10 backdrop-blur rounded-xl p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <Code2 className="w-5 h-5 text-green-300" />
                      <span className="text-sm font-medium text-blue-100">Language</span>
                    </div>
                    <div className="text-2xl font-bold">{analysis.repository.stats.language}</div>
                  </div>
                </div>

                {/* GitHub Link */}
                <a
                  href={analysis.repository.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-all duration-200 shadow-lg"
                >
                  <span>View on GitHub</span>
                  <ExternalLink className="w-4 h-4" />
                </a>
              </div>
            </Card>

            {/* Overall Score - Centered Circular Badge */}
            <div className="flex justify-center">
              <Card className="inline-block text-center">
                <div className="relative inline-flex items-center justify-center">
                  {/* SVG Circle Progress */}
                  <svg className="w-48 h-48 transform -rotate-90">
                    <circle
                      cx="96"
                      cy="96"
                      r="88"
                      stroke="currentColor"
                      strokeWidth="12"
                      fill="none"
                      className="text-slate-200"
                    />
                    <circle
                      cx="96"
                      cy="96"
                      r="88"
                      stroke="currentColor"
                      strokeWidth="12"
                      fill="none"
                      strokeDasharray={`${(analysis.overallScore / 100) * 553} 553`}
                      className={getOverallScoreRing(analysis.overallScore)}
                      strokeLinecap="round"
                    />
                  </svg>
                  
                  {/* Score Display */}
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <div className={`text-5xl font-bold bg-gradient-to-br ${getOverallScoreColor(analysis.overallScore)} bg-clip-text text-transparent mb-2`}>
                      {analysis.overallScore}
                    </div>
                    <div className="text-slate-600 font-medium text-lg">Overall Score</div>
                    <div className="text-sm text-slate-500 mt-1">Repository Quality</div>
                  </div>
                </div>
                
                {/* Score Label */}
                <div className="mt-6">
                  <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-semibold ${getScoreColor(analysis.overallScore)} border`}>
                    <CheckCircle className="w-4 h-4" />
                    <span>
                      {analysis.overallScore >= 80 ? 'Excellent Quality' : 
                       analysis.overallScore >= 60 ? 'Good Quality' : 
                       'Needs Improvement'}
                    </span>
                  </div>
                </div>
              </Card>
            </div>

            {/* Detailed Scores Section */}
            <div>
              <h3 className="text-2xl font-bold text-slate-900 mb-6 text-center">Detailed Analysis</h3>
              <div className="grid md:grid-cols-2 gap-6">
                {analysis.detailedScores.map((item, index) => (
                  <Card key={index} hover className="group">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <h4 className="text-lg font-semibold text-slate-900 mb-1 group-hover:text-blue-600 transition-colors">
                          {item.category}
                        </h4>
                        <p className="text-sm text-slate-600">{item.description}</p>
                      </div>
                      <div className={`ml-4 px-4 py-2 rounded-lg text-2xl font-bold border ${getScoreColor(item.score)}`}>
                        {item.score}
                      </div>
                    </div>
                    
                    {/* Progress Bar */}
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-slate-600 font-medium">Score</span>
                        <span className="text-slate-900 font-semibold">{item.score}/100</span>
                      </div>
                      <div className="w-full h-3 bg-slate-200 rounded-full overflow-hidden">
                        <div
                          className={`h-full ${getProgressColor(item.score)} rounded-full transition-all duration-1000 ease-out`}
                          style={{ width: `${item.score}%` }}
                        ></div>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </div>

            {/* Action Button */}
            <div className="text-center">
              <Button
                variant="outline"
                size="lg"
                onClick={() => {
                  setAnalysis(null);
                  setRepoUrl('');
                }}
              >
                Analyze Another Repository
              </Button>
            </div>
          </div>
        )}

        {/* Placeholder State */}
        {!analysis && !loading && (
          <Card className="animate-fade-in">
            <div className="text-center py-12">
              <Github className="w-16 h-16 text-slate-300 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-slate-900 mb-2">Ready to Analyze</h3>
              <p className="text-slate-600 mb-6">Enter a GitHub repository URL above to get started</p>
              
              {/* Feature Highlights */}
              <div className="grid md:grid-cols-3 gap-6 mt-8 max-w-3xl mx-auto">
                {[
                  { icon: Activity, title: 'Activity Metrics', desc: 'Commit frequency & contributions' },
                  { icon: FileText, title: 'Documentation', desc: 'README & code comments quality' },
                  { icon: GitBranch, title: 'Code Quality', desc: 'Structure & maintainability' },
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
