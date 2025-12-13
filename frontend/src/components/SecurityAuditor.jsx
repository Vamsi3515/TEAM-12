import React, { useState } from 'react';
import { Shield, Code, AlertTriangle, CheckCircle, XCircle, Lock, FileCode, Zap, ExternalLink, Info, TrendingUp, Award, Bug, ArrowRight } from 'lucide-react';
import Navbar from './Navbar';
import Card from './Card';
import Button from './Button';

const SecurityAuditor = () => {
  const [code, setCode] = useState('');
  const [repoUrl, setRepoUrl] = useState('');
  const [inputType, setInputType] = useState('code'); // 'code' or 'repo'
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const API_BASE_URL = 'http://localhost:8000/api';

  // Sample vulnerable code examples
  const sampleCodes = {
    sql_injection: `def get_user(user_id):
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return cursor.fetchone()`,
    hardcoded_secret: `API_KEY = "sk-1234567890abcdefghijklmnopqrstuvwxyz123456"
GROQ_KEY = "gsk_xyz123"

def authenticate():
    return API_KEY`,
    secure_code: `from sqlalchemy import text
import bcrypt

def get_user_secure(user_id: int, db_session):
    # Using parameterized query
    query = text("SELECT * FROM users WHERE id = :user_id")
    result = db_session.execute(query, {"user_id": user_id})
    return result.fetchone()

def hash_password_secure(password: str) -> str:
    # Using bcrypt for password hashing
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()`
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setAnalyzing(true);
    setError(null);
    setResults(null);

    if (inputType === 'code' && !code.trim()) {
      setError('Please provide code to analyze');
      setAnalyzing(false);
      return;
    }

    if (inputType === 'repo' && !repoUrl.trim()) {
      setError('Please provide a GitHub repository URL');
      setAnalyzing(false);
      return;
    }

    try {
      const payload = inputType === 'code' 
        ? { code: code, inputType: 'code' }
        : { repoUrl: repoUrl, inputType: 'repo' };

      const response = await fetch(`${API_BASE_URL}/security/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Analysis failed');
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

  const loadSample = (type) => {
    setCode(sampleCodes[type]);
    setInputType('code');
    setResults(null);
    setError(null);
  };

  const getRiskColor = (risk) => {
    if (!risk) return 'text-slate-600 bg-slate-50 border-slate-200';
    const riskLower = risk.toLowerCase ? risk.toLowerCase() : String(risk).toLowerCase();
    switch (riskLower) {
      case 'critical': return 'text-red-600 bg-red-50 border-red-200';
      case 'high': return 'text-orange-600 bg-orange-50 border-orange-200';
      case 'medium': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'low': return 'text-green-600 bg-green-50 border-green-200';
      default: return 'text-slate-600 bg-slate-50 border-slate-200';
    }
  };

  const getRiskLevel = (score) => {
    if (score >= 80) return 'low';
    if (score >= 60) return 'medium';
    if (score >= 40) return 'high';
    return 'critical';
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical': return <XCircle className="w-5 h-5 text-red-500" />;
      case 'high': return <AlertTriangle className="w-5 h-5 text-orange-500" />;
      case 'medium': return <Info className="w-5 h-5 text-yellow-500" />;
      case 'low': return <CheckCircle className="w-5 h-5 text-blue-500" />;
      default: return <Info className="w-5 h-5 text-slate-500" />;
    }
  };

  const getScoreGradient = (score) => {
    if (score >= 80) return 'from-green-500 to-emerald-600';
    if (score >= 60) return 'from-yellow-500 to-orange-500';
    if (score >= 40) return 'from-orange-500 to-red-500';
    return 'from-red-600 to-rose-700';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-indigo-50/30 to-purple-50/30">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-8 animate-slide-up">
          <div className="inline-flex items-center gap-2 bg-gradient-to-r from-indigo-100 to-purple-100 text-indigo-700 px-4 py-2 rounded-full text-sm font-medium mb-4 shadow-sm">
            <Shield className="w-4 h-4" />
            <span>OWASP Security Analysis</span>
          </div>
          <h1 className="text-4xl font-bold text-slate-900 mb-3">
            Security
            <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent"> Auditor</span>
          </h1>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Detect vulnerabilities using Hybrid Analysis: Static Patterns + AI with RAG
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Column - Input */}
          <div className="space-y-6">
            <Card className="animate-slide-up" style={{ animationDelay: '0.1s' }}>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                  <Code className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-slate-900">Code Analysis</h2>
                  <p className="text-sm text-slate-600">Submit code for security audit</p>
                </div>
              </div>

              <form onSubmit={handleAnalyze} className="space-y-4">
                {/* Input Type Toggle */}
                <div className="flex gap-2 p-1 bg-slate-100 rounded-lg">
                  <button
                    type="button"
                    onClick={() => setInputType('code')}
                    className={`flex-1 px-4 py-2 rounded-md text-sm font-medium transition-all ${
                      inputType === 'code'
                        ? 'bg-white text-indigo-600 shadow-sm'
                        : 'text-slate-600 hover:text-slate-900'
                    }`}
                  >
                    <Code className="w-4 h-4 inline mr-2" />
                    Code Snippet
                  </button>
                  <button
                    type="button"
                    onClick={() => setInputType('repo')}
                    className={`flex-1 px-4 py-2 rounded-md text-sm font-medium transition-all ${
                      inputType === 'repo'
                        ? 'bg-white text-indigo-600 shadow-sm'
                        : 'text-slate-600 hover:text-slate-900'
                    }`}
                  >
                    <ExternalLink className="w-4 h-4 inline mr-2" />
                    GitHub URL
                  </button>
                </div>

                {/* Conditional Input */}
                {inputType === 'code' ? (
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">
                      Source Code
                    </label>
                    <textarea
                      value={code}
                      onChange={(e) => setCode(e.target.value)}
                      placeholder="Paste your code here..."
                      rows={12}
                      className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent font-mono text-sm"
                    />
                  </div>
                ) : (
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">
                      GitHub Repository URL
                    </label>
                    <input
                      type="text"
                      value={repoUrl}
                      onChange={(e) => setRepoUrl(e.target.value)}
                      placeholder="https://github.com/username/repository"
                      className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    />
                  </div>
                )}

                {/* Sample Buttons - Only show for code input */}
                {inputType === 'code' && (
                  <div className="flex flex-wrap gap-2">
                    <button
                      type="button"
                      onClick={() => loadSample('sql_injection')}
                      className="px-3 py-1.5 text-xs bg-red-50 text-red-700 rounded-lg hover:bg-red-100 transition-colors"
                    >
                      SQL Injection
                    </button>
                  <button
                    type="button"
                    onClick={() => loadSample('hardcoded_secret')}
                    className="px-3 py-1.5 text-xs bg-orange-50 text-orange-700 rounded-lg hover:bg-orange-100 transition-colors"
                  >
                    Hardcoded Secret
                  </button>
                  <button
                    type="button"
                    onClick={() => loadSample('secure_code')}
                    className="px-3 py-1.5 text-xs bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors"
                  >
                    Secure Code
                  </button>
                  </div>
                )}

                {/* Error Display */}
                {error && (
                  <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
                    <AlertTriangle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                    <p className="text-sm text-red-700">{error}</p>
                  </div>
                )}

                {/* Submit Button */}
                <Button
                  type="submit"
                  disabled={analyzing}
                  className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700"
                >
                  {analyzing ? (
                    <>
                      <Zap className="w-5 h-5 animate-pulse" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Shield className="w-5 h-5" />
                      Analyze Security
                    </>
                  )}
                </Button>
              </form>
            </Card>
          </div>

          {/* Right Column - Results */}
          <div className="space-y-6">
            {results ? (
              <>
                {/* Security Score Card */}
                <Card className="animate-slide-up" style={{ animationDelay: '0.2s' }}>
                  <div className="flex items-center justify-between mb-6">
                    <div>
                      <h3 className="text-lg font-bold text-slate-900">Security Score</h3>
                      <p className="text-sm text-slate-600">Higher is better</p>
                    </div>
                    <div className={`px-4 py-2 rounded-full border-2 font-semibold ${getRiskColor(results.risk_level || getRiskLevel(results.security_score || 0))}`}>
                      {(results.risk_level || getRiskLevel(results.security_score || 0)).toUpperCase()}
                    </div>
                  </div>

                  <div className="flex items-center justify-center mb-4">
                    <div className="relative w-32 h-32">
                      <svg className="w-full h-full transform -rotate-90">
                        <circle
                          cx="64"
                          cy="64"
                          r="56"
                          stroke="currentColor"
                          strokeWidth="8"
                          fill="none"
                          className="text-slate-200"
                        />
                        <circle
                          cx="64"
                          cy="64"
                          r="56"
                          stroke="url(#scoreGradient)"
                          strokeWidth="8"
                          fill="none"
                          strokeDasharray={`${((results.security_score || 0) / 100) * 351.86} 351.86`}
                          className="transition-all duration-1000"
                        />
                        <defs>
                          <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" className={`${getScoreGradient(results.security_score || 0).split(' ')[0].replace('from-', 'text-')}`} />
                            <stop offset="100%" className={`${getScoreGradient(results.security_score || 0).split(' ')[1].replace('to-', 'text-')}`} />
                          </linearGradient>
                        </defs>
                      </svg>
                      <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-3xl font-bold text-slate-900">{Math.round(results.security_score || 0)}</span>
                        <span className="text-sm text-slate-600">/ 100</span>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 pt-4 border-t border-slate-200">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-slate-900">{results.vulnerabilities?.length || 0}</div>
                      <div className="text-sm text-slate-600">Vulnerabilities</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-slate-900">{results.evidence_ids?.length || 0}</div>
                      <div className="text-sm text-slate-600">Evidence Used</div>
                    </div>
                  </div>
                </Card>

                {/* Vulnerabilities */}
                {results.vulnerabilities && results.vulnerabilities.length > 0 && (
                  <Card className="animate-slide-up" style={{ animationDelay: '0.3s' }}>
                    <div className="flex items-center gap-3 mb-4">
                      <Bug className="w-5 h-5 text-red-500" />
                      <h3 className="text-lg font-bold text-slate-900">
                        Vulnerabilities Found ({results.vulnerabilities.length})
                      </h3>
                    </div>

                    <div className="space-y-4 max-h-96 overflow-y-auto">
                      {results.vulnerabilities.map((vuln, idx) => (
                        <div
                          key={idx}
                          className="p-4 border border-slate-200 rounded-lg hover:shadow-md transition-shadow"
                        >
                          <div className="flex items-start justify-between mb-2">
                            <div className="flex items-center gap-2">
                              {getSeverityIcon(vuln.severity)}
                              <h4 className="font-semibold text-slate-900">{vuln.issue || 'Security Issue'}</h4>
                            </div>
                            <span className={`px-2 py-1 text-xs rounded-full border ${getRiskColor(vuln.severity)}`}>
                              {vuln.severity ? vuln.severity.toUpperCase() : 'UNKNOWN'}
                            </span>
                          </div>

                          <p className="text-sm text-slate-600 mb-3">{vuln.explanation || 'No details available'}</p>

                          {vuln.line_numbers && vuln.line_numbers.length > 0 && (
                            <div className="flex items-center gap-2 text-xs text-slate-600 mb-3">
                              <FileCode className="w-4 h-4" />
                              <span>Lines: {vuln.line_numbers.join(', ')}</span>
                            </div>
                          )}

                          {vuln.fix_suggestion && (
                            <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                              <div className="flex items-start gap-2">
                                <Lock className="w-4 h-4 text-blue-600 flex-shrink-0 mt-0.5" />
                                <div>
                                  <p className="text-xs font-medium text-blue-900 mb-1">Fix Suggestion:</p>
                                  <p className="text-xs text-blue-700">{vuln.fix_suggestion}</p>
                                </div>
                              </div>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </Card>
                )}

                {/* Summary */}
                {results.summary && (
                  <Card className="animate-slide-up bg-indigo-50/50" style={{ animationDelay: '0.4s' }}>
                    <div className="flex items-center gap-3 mb-4">
                      <Info className="w-5 h-5 text-indigo-600" />
                      <h3 className="text-lg font-bold text-slate-900">Analysis Summary</h3>
                    </div>
                    <p className="text-sm text-slate-700">{results.summary}</p>
                  </Card>
                )}

                {/* Evidence Snippets */}
                {results.evidence_snippets && results.evidence_snippets.length > 0 && (
                  <Card className="animate-slide-up" style={{ animationDelay: '0.5s' }}>
                    <div className="flex items-center gap-3 mb-4">
                      <FileCode className="w-5 h-5 text-purple-600" />
                      <h3 className="text-lg font-bold text-slate-900">RAG Evidence ({results.evidence_snippets.length})</h3>
                    </div>
                    <div className="space-y-3 max-h-64 overflow-y-auto">
                      {results.evidence_snippets.map((evidence, idx) => (
                        <div key={idx} className="p-3 bg-purple-50 border border-purple-200 rounded-lg">
                          <div className="flex items-center gap-2 mb-2">
                            <span className="text-xs font-medium text-purple-700">ID: {evidence.id}</span>
                          </div>
                          <p className="text-xs text-slate-600 font-mono">{evidence.snippet}</p>
                        </div>
                      ))}
                    </div>
                  </Card>
                )}
              </>
            ) : (
              <Card className="text-center py-12">
                <div className="w-20 h-20 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Shield className="w-10 h-10 text-indigo-600" />
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-2">No Analysis Yet</h3>
                <p className="text-slate-600 mb-4">
                  Submit code to detect OWASP vulnerabilities
                </p>
                <div className="flex items-center justify-center gap-4 text-sm text-slate-500">
                  <div className="flex items-center gap-1">
                    <Zap className="w-4 h-4" />
                    Static Analysis
                  </div>
                  <div className="flex items-center gap-1">
                    <Shield className="w-4 h-4" />
                    AI-Powered
                  </div>
                  <div className="flex items-center gap-1">
                    <Lock className="w-4 h-4" />
                    RAG-Enhanced
                  </div>
                </div>
              </Card>
            )}
          </div>
        </div>

        {/* Info Footer */}
        <Card className="mt-8 bg-gradient-to-r from-indigo-50 to-purple-50 border-indigo-200">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center shadow-sm flex-shrink-0">
              <Info className="w-6 h-6 text-indigo-600" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-900 mb-2">About Security Auditor</h3>
              <p className="text-sm text-slate-700 mb-3">
                This tool uses hybrid analysis combining static pattern matching with AI-powered LLM analysis enhanced by RAG (Retrieval-Augmented Generation). 
                It detects 13+ vulnerability types covering OWASP Top 10 (2021) including SQL Injection, XSS, Command Injection, and more.
              </p>
              <div className="flex flex-wrap gap-2">
                <span className="px-3 py-1 bg-white text-indigo-700 text-xs font-medium rounded-full">OWASP Top 10</span>
                <span className="px-3 py-1 bg-white text-purple-700 text-xs font-medium rounded-full">CWE Mapping</span>
                <span className="px-3 py-1 bg-white text-pink-700 text-xs font-medium rounded-full">AI-Enhanced</span>
                <span className="px-3 py-1 bg-white text-blue-700 text-xs font-medium rounded-full">RAG Context</span>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default SecurityAuditor;
