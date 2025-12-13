import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Github, FileText, ArrowRight, Sparkles, TrendingUp, Users } from 'lucide-react';
import Navbar from './Navbar';
import Card from './Card';
import Button from './Button';

const Home = () => {
  const navigate = useNavigate();

  const features = [
    {
      id: 'github-analyzer',
      icon: Github,
      title: 'GitHub Profile Analyzer',
      description: 'Analyze GitHub profiles, repositories, and contributions with AI-powered insights',
      gradient: 'from-blue-500 to-cyan-500',
      route: '/github-analyzer',
      stats: [
        { label: 'Repositories', value: '50+' },
        { label: 'Contributors', value: '1K+' },
        { label: 'Languages', value: '20+' }
      ]
    },
    {
      id: 'ats-detector',
      icon: FileText,
      title: 'ATS Score & Rejection Detector',
      description: 'Optimize your resume for ATS systems and detect potential rejection reasons',
      gradient: 'from-purple-500 to-pink-500',
      route: '/Ats-score-with-rejection-detector',
      stats: [
        { label: 'Success Rate', value: '95%' },
        { label: 'Analyzed', value: '10K+' },
        { label: 'Keywords', value: '500+' }
      ]
    }
  ];

  const handleCardClick = (route) => {
    navigate(route);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/30">
      <Navbar />
      
      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-12 pb-8">
        <div className="text-center animate-slide-up">
          <div className="inline-flex items-center gap-2 bg-gradient-to-r from-primary-100 to-secondary-100 text-primary-700 px-4 py-2 rounded-full text-sm font-medium mb-4 shadow-sm">
            <Sparkles className="w-4 h-4 animate-pulse" />
            <span>Welcome to Your Dashboard</span>
          </div>
          
          <h1 className="text-4xl sm:text-5xl font-bold text-slate-900 mb-4">
            Choose Your
            <span className="block bg-gradient-to-r from-primary-600 via-secondary-600 to-purple-600 bg-clip-text text-transparent">
              Analysis Tool
            </span>
          </h1>
          
          <p className="text-lg text-slate-600 max-w-2xl mx-auto mb-8">
            Select from our powerful AI-driven tools to accelerate your career growth
          </p>
        </div>
      </section>

      {/* Main Cards Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        <div className="grid md:grid-cols-2 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <Card 
                key={feature.id}
                hover
                className="group cursor-pointer animate-slide-up overflow-hidden"
                style={{ animationDelay: `${index * 0.1}s` }}
                onClick={() => handleCardClick(feature.route)}
              >
                {/* Header with Icon */}
                <div className="relative mb-6">
                  <div className={`absolute inset-0 bg-gradient-to-r ${feature.gradient} opacity-10 rounded-xl blur-xl group-hover:opacity-20 transition-opacity`}></div>
                  <div className={`relative w-16 h-16 bg-gradient-to-r ${feature.gradient} rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300 shadow-lg`}>
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h2 className="text-2xl font-bold text-slate-900 mb-2 group-hover:text-primary-600 transition-colors">
                    {feature.title}
                  </h2>
                  <p className="text-slate-600">
                    {feature.description}
                  </p>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-3 gap-4 mb-6">
                  {feature.stats.map((stat, idx) => (
                    <div key={idx} className="text-center p-3 bg-slate-50 rounded-lg group-hover:bg-white transition-colors">
                      <div className="text-2xl font-bold text-slate-900 mb-1">
                        {stat.value}
                      </div>
                      <div className="text-xs text-slate-600">
                        {stat.label}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Action Button */}
                <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                  <span className="text-sm font-medium text-slate-600 group-hover:text-primary-600 transition-colors">
                    Start Analysis
                  </span>
                  <div className="w-10 h-10 bg-slate-100 group-hover:bg-primary-600 rounded-lg flex items-center justify-center transition-all duration-300 group-hover:shadow-lg">
                    <ArrowRight className="w-5 h-5 text-slate-600 group-hover:text-white transition-colors" />
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      </section>

      {/* Quick Stats Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        <Card className="bg-gradient-to-br from-primary-600 to-secondary-600 border-none animate-fade-in">
          <div className="text-white">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="w-6 h-6" />
              <h3 className="text-2xl font-bold">Your Impact</h3>
            </div>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
                <div className="flex items-center gap-3 mb-2">
                  <Users className="w-5 h-5" />
                  <span className="text-sm font-medium">Total Analyses</span>
                </div>
                <div className="text-3xl font-bold">24</div>
                <div className="text-sm opacity-90 mt-1">↑ 12% from last week</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
                <div className="flex items-center gap-3 mb-2">
                  <Sparkles className="w-5 h-5" />
                  <span className="text-sm font-medium">Success Rate</span>
                </div>
                <div className="text-3xl font-bold">98%</div>
                <div className="text-sm opacity-90 mt-1">Outstanding performance</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
                <div className="flex items-center gap-3 mb-2">
                  <TrendingUp className="w-5 h-5" />
                  <span className="text-sm font-medium">Time Saved</span>
                </div>
                <div className="text-3xl font-bold">45h</div>
                <div className="text-sm opacity-90 mt-1">Compared to manual analysis</div>
              </div>
            </div>
          </div>
        </Card>
      </section>

      {/* Coming Soon Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-slate-900 mb-2">Coming Soon</h2>
          <p className="text-slate-600">More powerful tools are on the way</p>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          {['Interview Prep AI', 'Skill Gap Analysis', 'Career Path Planner'].map((title, idx) => (
            <Card key={idx} className="text-center opacity-60 cursor-not-allowed">
              <div className="w-12 h-12 bg-slate-200 rounded-xl mx-auto mb-4"></div>
              <h3 className="font-semibold text-slate-900 mb-2">{title}</h3>
              <p className="text-sm text-slate-600">Coming in Q1 2026</p>
            </Card>
          ))}
        </div>
      </section>
    </div>
  );
};

export default Home;