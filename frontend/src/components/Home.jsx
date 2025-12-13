import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Github, FileText, Shield, ArrowRight, Sparkles, TrendingUp, Users, Award, Workflow, BookOpen } from 'lucide-react';
import Navbar from './Navbar';
import Card from './Card';
import Button from './Button';

const Home = () => {
  const navigate = useNavigate();

  const superAgents = [
    {
      id: 'ats-detector',
      icon: FileText,
      title: 'ATS Score & Rejection Detector',
      description: 'Optimize your resume for ATS systems and detect potential rejection reasons',
      gradient: 'from-purple-500 to-pink-500',
      route: '/Ats-score-with-rejection-detector',
      isSuperAgent: true
    },
    {
      id: 'experience-authenticity',
      icon: Award,
      title: 'Experience Authenticity Agent',
      description: 'Verify resume claims with AI analysis of GitHub, LeetCode, and online presence',
      gradient: 'from-emerald-500 to-teal-600',
      route: '/experience-authenticity',
      isSuperAgent: true
    }
  ];

  const otherAgents = [
    {
      id: 'github-analyzer',
      icon: Github,
      title: 'GitHub Profile Analyzer',
      description: 'Analyze GitHub profiles, repositories, and contributions with AI-powered insights',
      gradient: 'from-blue-500 to-cyan-500',
      route: '/github-analyzer'
    },
    {
      id: 'security-auditor',
      icon: Shield,
      title: 'Security Auditor',
      description: 'Detect OWASP vulnerabilities using hybrid AI analysis with static patterns and RAG',
      gradient: 'from-indigo-500 to-purple-600',
      route: '/security-auditor'
    },
    {
      id: 'code-to-uml',
      icon: Workflow,
      title: 'Code to UML Diagrams',
      description: 'Transform code into interactive UML diagrams with AI-powered analysis',
      gradient: 'from-violet-500 to-fuchsia-600',
      route: '/code-to-uml'
    },
    {
      id: 'learning-flow',
      icon: BookOpen,
      title: 'Learning Flow Generator',
      description: 'Create personalized learning roadmaps with AI-curated resources',
      gradient: 'from-sky-500 to-cyan-600',
      route: '/learning-flow'
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
        {/* Super Agents */}
        <div className="mb-12">
          <div className="flex items-center justify-center gap-2 mb-6">
            <Sparkles className="w-5 h-5 text-primary-600" />
            <h2 className="text-3xl font-bold text-slate-900">Super Agents</h2>
          </div>
          <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            {superAgents.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <Card 
                  key={feature.id}
                  hover
                  className="group cursor-pointer animate-slide-up overflow-hidden bg-gradient-to-br from-white to-primary-50 border-2 border-primary-200 hover:border-primary-400"
                  style={{ animationDelay: `${index * 0.1}s` }}
                  onClick={() => handleCardClick(feature.route)}
                >
                  {/* Header with Icon */}
                  <div className="relative mb-6">
                    <div className="absolute -top-4 -right-4 bg-primary-600 text-white text-xs font-bold px-3 py-1 rounded-full shadow-lg z-10">
                      SUPER AGENT
                    </div>
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

                  {/* Action Button */}
                  <div className="flex items-center justify-between pt-4 border-t border-primary-200">
                    <span className="text-sm font-medium text-slate-600 group-hover:text-primary-600 transition-colors">
                      Start Analysis
                    </span>
                    <div className="w-10 h-10 bg-primary-100 group-hover:bg-primary-600 rounded-lg flex items-center justify-center transition-all duration-300 group-hover:shadow-lg">
                      <ArrowRight className="w-5 h-5 text-primary-600 group-hover:text-white transition-colors" />
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        </div>

        {/* Other Agents */}
        <div>
          <div className="text-center mb-6">
            <h2 className="text-3xl font-bold text-slate-900">Other Agents</h2>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {otherAgents.map((feature, index) => {
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
        </div>
      </section>

    </div>
  );
};

export default Home;