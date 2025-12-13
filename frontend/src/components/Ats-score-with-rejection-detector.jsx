import React, { useState } from 'react';
import { FileText, Upload, CheckCircle, AlertCircle, TrendingUp, Target } from 'lucide-react';
import Navbar from './Navbar';
import Card from './Card';
import Button from './Button';

const RejectionDetector = () => {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [analyzing, setAnalyzing] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleAnalyze = (e) => {
    e.preventDefault();
    setAnalyzing(true);
    // TODO: Implement ATS analysis
    setTimeout(() => setAnalyzing(false), 2000);
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
                {/* File Upload */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Upload Resume
                  </label>
                  <div className="border-2 border-dashed border-slate-300 rounded-lg p-8 text-center hover:border-purple-400 transition-colors">
                    <input
                      type="file"
                      onChange={handleFileChange}
                      accept=".pdf,.doc,.docx"
                      className="hidden"
                      id="resume-upload"
                      required
                    />
                    <label htmlFor="resume-upload" className="cursor-pointer">
                      <Upload className="w-12 h-12 text-slate-400 mx-auto mb-4" />
                      <p className="text-slate-600 mb-2">
                        {file ? file.name : 'Click to upload or drag and drop'}
                      </p>
                      <p className="text-sm text-slate-500">PDF, DOC, or DOCX (max 5MB)</p>
                    </label>
                  </div>
                </div>

                {/* Job Description */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Job Description (Optional)
                  </label>
                  <textarea
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    placeholder="Paste the job description here for better matching..."
                    rows={6}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all resize-none"
                  />
                </div>

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
            { icon: CheckCircle, title: 'ATS Score', desc: 'Get your compatibility score', color: 'from-green-500 to-emerald-500' },
            { icon: AlertCircle, title: 'Issue Detection', desc: 'Find potential problems', color: 'from-orange-500 to-red-500' },
            { icon: TrendingUp, title: 'Improvement Tips', desc: 'Actionable suggestions', color: 'from-purple-500 to-pink-500' },
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

        {/* Placeholder Results */}
        <Card className="animate-fade-in">
          <div className="text-center py-12">
            <FileText className="w-16 h-16 text-slate-300 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-slate-900 mb-2">Ready to Analyze</h3>
            <p className="text-slate-600">Upload your resume above to get started</p>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default RejectionDetector;
