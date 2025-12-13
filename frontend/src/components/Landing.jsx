import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, Sparkles, Zap, Shield, Star, TrendingUp, Github, BarChart3, Code, Award, BookOpen, Workflow } from 'lucide-react';
import Button from './Button';

const Landing = () => {
  const navigate = useNavigate();

  const superAgents = [
    {
      icon: BarChart3,
      title: 'ATS Score & Rejection Detector',
      description: 'Get instant ATS optimization scores and receive detailed rejection analysis directly via email',
      color: 'from-purple-500 to-pink-500',
      isSuperAgent: true,
    },
    {
      icon: Award,
      title: 'Experience Authenticity Agent',
      description: 'AI-powered verification of resume claims through GitHub, LeetCode, and professional presence analysis',
      color: 'from-emerald-500 to-teal-600',
      isSuperAgent: true,
    },
  ];

  const otherFeatures = [
    {
      icon: Github,
      title: 'GitHub Analytics',
      description: 'Comprehensive analysis of repositories and contribution patterns',
      color: 'from-blue-500 to-cyan-500',
    },
    {
      icon: Shield,
      title: 'Security Auditor',
      description: 'OWASP vulnerability detection with hybrid AI analysis',
      color: 'from-indigo-500 to-purple-600',
    },
    {
      icon: Workflow,
      title: 'Code to UML',
      description: 'Transform code into interactive UML diagrams',
      color: 'from-violet-500 to-fuchsia-600',
    },
    {
      icon: BookOpen,
      title: 'Learning Flow',
      description: 'Personalized learning roadmaps with curated resources',
      color: 'from-sky-500 to-cyan-600',
    },
  ];

  const stats = [
    { value: '10K+', label: 'Active Users' },
    { value: '50K+', label: 'Resumes Analyzed' },
    { value: '99.9%', label: 'Uptime' },
    { value: '4.9/5', label: 'User Rating' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
      {/* Navbar */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-secondary-600 rounded-lg flex items-center justify-center shadow-lg">
                <span className="text-white font-bold text-xl">M</span>
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
                Mirai
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="sm" onClick={() => navigate('/home')}>
                Features
              </Button>
              <Button variant="ghost" size="sm">
                About
              </Button>
              <Button variant="primary" size="sm" onClick={() => navigate('/home')}>
                Get Started
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-20">
        {/* Background Decoration */}
        <div className="absolute inset-0 -z-10 overflow-hidden">
          <div className="absolute top-20 left-10 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float"></div>
          <div className="absolute top-40 right-10 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float" style={{animationDelay: '2s'}}></div>
          <div className="absolute bottom-20 left-1/2 w-72 h-72 bg-blue-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float" style={{animationDelay: '4s'}}></div>
        </div>

        <div className="text-center animate-slide-up">
          <div className="inline-flex items-center gap-2 bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 px-5 py-2.5 rounded-full text-sm font-semibold mb-6 shadow-sm border border-purple-200">
            <Star className="w-4 h-4 fill-current" />
            <span>AI-Powered Career Intelligence Platform</span>
          </div>
          
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold text-slate-900 mb-6 leading-tight tracking-tight">
            Transform Your
            <span className="block mt-2 bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">
              Career Journey
            </span>
          </h1>
          
          <p className="text-xl text-slate-600 mb-10 max-w-3xl mx-auto leading-relaxed">
            Leverage cutting-edge AI agents to optimize resumes, verify experience authenticity, 
            analyze GitHub profiles, and accelerate your professional growth.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-8">
            <Button 
              variant="primary" 
              size="lg" 
              icon={ArrowRight}
              onClick={() => navigate('/home')}
              className="shadow-2xl hover:shadow-purple-500/50 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 px-8 py-4 text-lg"
            >
              Get Started Free
            </Button>
            <Button 
              variant="outline" 
              size="lg" 
              icon={Sparkles}
              onClick={() => navigate('/home')}
              className="px-8 py-4 text-lg border-2 border-slate-300 hover:border-purple-500 hover:bg-purple-50"
            >
              Explore Agents
            </Button>
          </div>

          {/* Trust Indicators */}
          <div className="flex flex-wrap items-center justify-center gap-8 text-sm text-slate-600 mt-12">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>100% Free</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>No Credit Card Required</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>Instant Results</span>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <div key={index} className="text-center animate-scale-in" style={{ animationDelay: `${index * 0.1}s` }}>
              <div className="text-4xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent mb-2">
                {stat.value}
              </div>
              <div className="text-slate-600 font-medium">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl sm:text-5xl font-bold text-slate-900 mb-4">
            Powerful AI Agents at Your Service
          </h2>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            Choose from our suite of specialized AI agents designed to accelerate your career
          </p>
        </div>

        {/* Super Agents Section */}
        <div className="mb-16">
          <div className="flex items-center justify-center gap-3 mb-8">
            <div className="flex items-center gap-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-4 py-2 rounded-full font-bold text-sm shadow-lg">
              <Star className="w-4 h-4 fill-current" />
              SUPER AGENTS
            </div>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
            {superAgents.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div
                  key={index}
                  onClick={() => navigate('/home')}
                  className="group relative bg-white rounded-3xl p-8 border-2 border-purple-200 hover:border-purple-400 hover:shadow-2xl transition-all duration-300 cursor-pointer animate-slide-up overflow-hidden"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  {/* Background Gradient */}
                  <div className="absolute inset-0 bg-gradient-to-br from-purple-50 to-pink-50 opacity-50 group-hover:opacity-100 transition-opacity"></div>
                  
                  {/* Content */}
                  <div className="relative">
                    <div className="flex items-start justify-between mb-4">
                      <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${feature.color} flex items-center justify-center shadow-lg group-hover:scale-110 group-hover:rotate-3 transition-transform duration-300`}>
                        <Icon className="w-8 h-8 text-white" />
                      </div>
                      <div className="bg-purple-600 text-white text-xs font-bold px-3 py-1.5 rounded-full shadow-lg">
                        FEATURED
                      </div>
                    </div>
                    
                    <h3 className="text-2xl font-bold text-slate-900 mb-3 group-hover:text-purple-600 transition-colors">
                      {feature.title}
                    </h3>
                    <p className="text-slate-600 leading-relaxed mb-4">
                      {feature.description}
                    </p>
                    
                    <div className="flex items-center text-purple-600 font-semibold group-hover:gap-2 transition-all">
                      <span>Get Started</span>
                      <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Other Agents Section */}
        <div>
          <h3 className="text-2xl font-bold text-slate-900 text-center mb-8">Additional Specialized Agents</h3>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {otherFeatures.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div
                  key={index}
                  onClick={() => navigate('/home')}
                  className="group bg-white rounded-2xl p-6 border border-slate-200 hover:border-slate-300 hover:shadow-lg transition-all duration-300 cursor-pointer animate-fade-in"
                  style={{ animationDelay: `${(index + 2) * 0.1}s` }}
                >
                  <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-4 group-hover:scale-105 transition-transform duration-300 shadow-md`}>
                    <Icon className="w-7 h-7 text-white" />
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors">
                    {feature.title}
                  </h3>
                  <p className="text-slate-600 text-sm leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 mb-20">
        <div className="relative overflow-hidden bg-gradient-to-br from-purple-600 via-pink-600 to-blue-600 rounded-3xl p-16 text-center shadow-2xl">
          {/* Animated Background */}
          <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS1vcGFjaXR5PSIwLjEiIHN0cm9rZS13aWR0aD0iMSIvPjwvcGF0dGVybj48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNncmlkKSIvPjwvc3ZnPg==')] opacity-30"></div>
          
          <div className="relative z-10">
            <div className="inline-block bg-white/20 backdrop-blur-sm text-white px-4 py-2 rounded-full text-sm font-semibold mb-6">
              🚀 Start Your Journey Today
            </div>
            
            <h2 className="text-4xl sm:text-5xl font-bold text-white mb-6">
              Ready to Elevate Your Career?
            </h2>
            <p className="text-xl text-white/90 mb-10 max-w-2xl mx-auto leading-relaxed">
              Join professionals leveraging AI to optimize resumes, verify credentials, and accelerate growth
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                variant="outline" 
                size="lg" 
                icon={ArrowRight}
                onClick={() => navigate('/home')}
                className="bg-white hover:bg-gray-50 text-purple-600 border-white font-bold px-8 py-4 shadow-xl hover:shadow-2xl hover:scale-105 transition-all"
              >
                Get Started Free
              </Button>
              <Button 
                variant="outline" 
                size="lg" 
                icon={Sparkles}
                onClick={() => navigate('/home')}
                className="bg-transparent hover:bg-white/10 text-white border-2 border-white px-8 py-4"
              >
                View All Agents
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-300">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-secondary-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold">M</span>
                </div>
                <span className="text-xl font-bold text-white">Mirai</span>
              </div>
              <p className="text-sm">
                Empowering professionals with AI-driven insights and analytics.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Product</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-white transition-colors">FAQ</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Company</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Legal</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">Privacy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Terms</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Security</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-slate-800 mt-8 pt-8 text-sm text-center">
            <p>&copy; 2025 Mirai. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
