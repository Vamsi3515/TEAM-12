import React, { useState } from 'react';
import { 
  BookOpen, 
  Clock, 
  TrendingUp, 
  Lightbulb,
  CheckCircle,
  Play,
  Target,
  Award,
  Users,
  ExternalLink,
  Video,
  FileText,
  Loader,
  AlertTriangle,
  Code,
  Zap
} from 'lucide-react';
import Navbar from './Navbar';
import Card from './Card';
import Button from './Button';

const LearningFlowGenerator = () => {
  const [topic, setTopic] = useState('');
  const [experienceLevel, setExperienceLevel] = useState('beginner');
  const [weeklyHours, setWeeklyHours] = useState('5-10');
  const [generating, setGenerating] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  // Calculate timeline estimates
  const calculateTimeline = () => {
    const baseWeeks = 12;
    const multipliers = {
      beginner: 1.5,
      intermediate: 1.0,
      advanced: 0.7
    };
    
    const hoursMap = {
      '1-5': 3,
      '5-10': 7.5,
      '10-20': 15,
      '20+': 25
    };
    
    const weeks = Math.ceil(baseWeeks * multipliers[experienceLevel]);
    const avgHours = hoursMap[weeklyHours];
    const totalHours = weeks * avgHours;
    
    return { weeks, totalHours, avgHours };
  };

  // Handle form submission
  const handleGenerate = async () => {
    if (!topic.trim()) {
      setError('Please enter a topic to learn');
      return;
    }

    setGenerating(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/learning-flow/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          topic: topic.trim(),
          experience_level: experienceLevel,
          weekly_hours: weeklyHours
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate learning flow. Please try again.');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message || 'An error occurred while generating learning flow');
    } finally {
      setGenerating(false);
    }
  };

  // Load sample data
  const loadSampleData = () => {
    const timeline = calculateTimeline();
    
    setResults({
      phases: [
        {
          name: 'Foundation',
          duration: '4 weeks',
          description: 'Build core fundamentals and setup development environment',
          keyTopics: [
            'Introduction to React concepts',
            'JavaScript ES6+ essentials',
            'Component-based architecture',
            'JSX syntax and rendering',
            'Props and state management'
          ]
        },
        {
          name: 'Core Concepts',
          duration: '4 weeks',
          description: 'Master essential React patterns and lifecycle',
          keyTopics: [
            'React Hooks (useState, useEffect)',
            'Event handling and forms',
            'Conditional rendering',
            'Lists and keys',
            'Component composition'
          ]
        },
        {
          name: 'Advanced Topics',
          duration: '3 weeks',
          description: 'Explore advanced patterns and state management',
          keyTopics: [
            'Context API and useContext',
            'Custom Hooks',
            'Performance optimization',
            'React Router for navigation',
            'API integration with fetch/axios'
          ]
        },
        {
          name: 'Real-World Projects',
          duration: '3 weeks',
          description: 'Apply knowledge through hands-on projects',
          keyTopics: [
            'Build a task management app',
            'Create a weather dashboard',
            'Develop an e-commerce frontend',
            'Testing with Jest and React Testing Library',
            'Deployment to production'
          ]
        }
      ],
      mermaidDiagram: `graph LR
    A[Start Learning] --> B[Foundation Phase]
    B --> C[Core Concepts]
    C --> D[Advanced Topics]
    D --> E[Real-World Projects]
    E --> F[React Developer!]
    
    B -.4 weeks.-> C
    C -.4 weeks.-> D
    D -.3 weeks.-> E
    E -.3 weeks.-> F`,
      youtubeChannels: [
        {
          name: 'Traversy Media',
          url: 'https://youtube.com/@TraversyMedia',
          focus: 'Practical web development tutorials',
          recommendedPlaylists: ['React Crash Course', 'React Projects']
        },
        {
          name: 'Codevolution',
          url: 'https://youtube.com/@Codevolution',
          focus: 'In-depth React tutorials',
          recommendedPlaylists: ['React Tutorial for Beginners', 'React Hooks Tutorial']
        },
        {
          name: 'Web Dev Simplified',
          url: 'https://youtube.com/@WebDevSimplified',
          focus: 'Simple explanations of complex topics',
          recommendedPlaylists: ['Learn React In 30 Minutes', 'React Projects']
        }
      ],
      projects: [
        {
          name: 'Todo App with Local Storage',
          description: 'Build a task management app with CRUD operations',
          difficulty: 'beginner',
          estimatedHours: 8
        },
        {
          name: 'Weather Dashboard',
          description: 'Fetch and display weather data from an API',
          difficulty: 'intermediate',
          estimatedHours: 12
        },
        {
          name: 'E-commerce Product Catalog',
          description: 'Create a product listing with cart functionality',
          difficulty: 'intermediate',
          estimatedHours: 20
        },
        {
          name: 'Social Media Dashboard',
          description: 'Full-featured app with authentication and real-time updates',
          difficulty: 'advanced',
          estimatedHours: 40
        }
      ],
      timeline: `${timeline.weeks} weeks (${timeline.totalHours} total hours)`,
      prerequisites: [
        'Basic HTML and CSS knowledge',
        'JavaScript fundamentals (variables, functions, arrays)',
        'Understanding of DOM manipulation',
        'Familiarity with ES6+ syntax (arrow functions, destructuring)'
      ],
      resources: {
        books: [
          'React - The Complete Guide by Maximilian Schwarzmüller',
          'Learning React by Alex Banks & Eve Porcello',
          'Fullstack React by Anthony Accomazzo'
        ],
        websites: [
          'Official React Documentation (react.dev)',
          'FreeCodeCamp React Course',
          'React Patterns (reactpatterns.com)',
          'Scrimba Interactive React Course'
        ],
        communities: [
          'Reactiflux Discord',
          'Reddit r/reactjs',
          'Stack Overflow React Tag',
          'Dev.to React Community'
        ]
      }
    });
    setTopic('React.js');
  };

  // Get difficulty color
  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 text-green-700';
      case 'intermediate': return 'bg-yellow-100 text-yellow-700';
      case 'advanced': return 'bg-red-100 text-red-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  // Get experience level description
  const getExperienceLevelDesc = (level) => {
    switch (level) {
      case 'beginner': return 'New to programming';
      case 'intermediate': return 'Some experience';
      case 'advanced': return 'Looking to specialize';
      default: return '';
    }
  };

  // Get weekly hours description
  const getWeeklyHoursDesc = (hours) => {
    switch (hours) {
      case '1-5': return 'Casual learning';
      case '5-10': return 'Regular practice';
      case '10-20': return 'Intensive study';
      case '20+': return 'Full-time learning';
      default: return '';
    }
  };

  const timeline = calculateTimeline();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/30">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-8 animate-slide-up">
          <div className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-700 px-4 py-2 rounded-full text-sm font-medium mb-4 shadow-sm">
            <BookOpen className="w-4 h-4" />
            <span>AI-Powered Learning Path</span>
          </div>
          
          <h1 className="text-4xl font-bold text-slate-900 mb-3">
            Learning Flow
            <span className="block bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
              Generator
            </span>
          </h1>
          
          <p className="text-lg text-slate-600 max-w-3xl mx-auto">
            Create personalized learning roadmaps with AI-curated resources and projects
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* LEFT COLUMN - Input Form */}
          <div className="lg:col-span-1 space-y-6">
            <Card className="animate-slide-up" style={{ animationDelay: '0.1s' }}>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-lg flex items-center justify-center">
                  <Target className="w-5 h-5 text-white" />
                </div>
                <h2 className="text-xl font-bold text-slate-900">Learning Goals</h2>
              </div>

              {/* Topic Input */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  What do you want to learn? <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="e.g., React.js, Python, Machine Learning"
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                />
              </div>

              {/* Experience Level */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Experience Level
                </label>
                <select
                  value={experienceLevel}
                  onChange={(e) => setExperienceLevel(e.target.value)}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                >
                  <option value="beginner">Beginner - New to programming</option>
                  <option value="intermediate">Intermediate - Some experience</option>
                  <option value="advanced">Advanced - Looking to specialize</option>
                </select>
                <p className="mt-2 text-sm text-slate-500">
                  {getExperienceLevelDesc(experienceLevel)}
                </p>
              </div>

              {/* Weekly Hours */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Weekly Time Commitment
                </label>
                <select
                  value={weeklyHours}
                  onChange={(e) => setWeeklyHours(e.target.value)}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                >
                  <option value="1-5">1-5 hours - Casual learning</option>
                  <option value="5-10">5-10 hours - Regular practice</option>
                  <option value="10-20">10-20 hours - Intensive study</option>
                  <option value="20+">20+ hours - Full-time learning</option>
                </select>
                <p className="mt-2 text-sm text-slate-500">
                  {getWeeklyHoursDesc(weeklyHours)}
                </p>
              </div>

              {/* Timeline Preview */}
              <div className="mb-6 p-4 bg-blue-50 border border-blue-100 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <Clock className="w-4 h-4 text-blue-600" />
                  <span className="text-sm font-medium text-blue-900">Estimated Timeline</span>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <div className="text-2xl font-bold text-blue-600">{timeline.weeks}</div>
                    <div className="text-xs text-blue-700">weeks</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-blue-600">{timeline.totalHours}</div>
                    <div className="text-xs text-blue-700">total hours</div>
                  </div>
                </div>
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
                  onClick={handleGenerate}
                  disabled={generating || !topic.trim()}
                  className="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-3 rounded-lg transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {generating ? (
                    <>
                      <Loader className="w-5 h-5 animate-spin" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Play className="w-5 h-5" />
                      Generate Path
                    </>
                  )}
                </Button>
                
                <Button
                  onClick={loadSampleData}
                  className="px-6 bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium py-3 rounded-lg transition-all"
                >
                  Sample
                </Button>
              </div>
            </Card>
          </div>

          {/* RIGHT COLUMN - Results */}
          <div className="lg:col-span-2 space-y-6">
            {results ? (
              <>
                {/* Learning Phases */}
                <Card className="animate-slide-up" style={{ animationDelay: '0.2s' }}>
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg flex items-center justify-center">
                        <TrendingUp className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <h3 className="text-xl font-bold text-slate-900">Learning Phases</h3>
                        <p className="text-sm text-slate-600">
                          {results.timeline && typeof results.timeline === 'object' 
                            ? `${results.timeline.weeks} weeks (${results.timeline.total_hours} hours total, ${results.timeline.avg_hours_per_week}h/week)`
                            : results.timeline || 'Timeline not available'}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-4">
                    {results.phases?.map((phase, index) => (
                      <div key={index} className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-100">
                        <div className="flex items-start justify-between mb-3">
                          <div>
                            <div className="flex items-center gap-2 mb-1">
                              <span className="text-lg font-bold text-slate-900">{phase.name}</span>
                              <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-medium rounded">
                                {phase.duration}
                              </span>
                            </div>
                            <p className="text-sm text-slate-600">{phase.description}</p>
                          </div>
                          <div className="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold text-sm">
                            {index + 1}
                          </div>
                        </div>
                        
                        <div className="space-y-2">
                          {(phase.keyTopics || phase.topics || []).map((topic, idx) => (
                            <div key={idx} className="flex items-start gap-2">
                              <CheckCircle className="w-4 h-4 text-green-600 flex-shrink-0 mt-0.5" />
                              <span className="text-sm text-slate-700">{topic}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>

                {/* Prerequisites */}
                <Card className="animate-slide-up" style={{ animationDelay: '0.3s' }}>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 bg-gradient-to-r from-orange-500 to-red-500 rounded-lg flex items-center justify-center">
                      <Zap className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-900">Prerequisites</h3>
                  </div>
                  <div className="grid md:grid-cols-2 gap-3">
                    {(results.prerequisites || []).map((prereq, index) => (
                      <div key={index} className="flex items-start gap-2 p-3 bg-orange-50 rounded-lg border border-orange-100">
                        <Lightbulb className="w-4 h-4 text-orange-600 flex-shrink-0 mt-0.5" />
                        <span className="text-sm text-slate-700">{prereq}</span>
                      </div>
                    ))}
                  </div>
                </Card>

                {/* YouTube Channels */}
                <Card className="animate-slide-up" style={{ animationDelay: '0.4s' }}>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 bg-gradient-to-r from-red-500 to-pink-500 rounded-lg flex items-center justify-center">
                      <Video className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-900">YouTube Channels</h3>
                  </div>
                  <div className="space-y-3">
                    {(results.youtubeChannels || results.youtube_channels || []).map((channel, index) => (
                      <div key={index} className="p-4 bg-slate-50 rounded-lg border border-slate-200 hover:border-blue-300 transition-colors">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <a 
                                href={channel.url} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="text-base font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1"
                              >
                                {channel.name}
                                <ExternalLink className="w-4 h-4" />
                              </a>
                            </div>
                            <p className="text-sm text-slate-600 mb-2">{channel.focus}</p>
                            {(channel.recommendedPlaylists || channel.recommended_playlists || []).length > 0 && (
                              <div className="flex flex-wrap gap-2">
                                {(channel.recommendedPlaylists || channel.recommended_playlists || []).map((playlist, idx) => (
                                  <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded">
                                    {playlist}
                                  </span>
                                ))}
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>

                {/* Projects */}
                <Card className="animate-slide-up" style={{ animationDelay: '0.5s' }}>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-lg flex items-center justify-center">
                      <Code className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-900">Hands-On Projects</h3>
                  </div>
                  <div className="grid md:grid-cols-2 gap-4">
                    {(results.projects || []).map((project, index) => (
                      <div key={index} className="p-4 bg-slate-50 rounded-lg border border-slate-200">
                        <div className="flex items-start justify-between mb-2">
                          <h4 className="font-bold text-slate-900">{project.name}</h4>
                          <span className={`px-2 py-1 text-xs font-medium rounded ${getDifficultyColor(project.difficulty)}`}>
                            {project.difficulty}
                          </span>
                        </div>
                        <p className="text-sm text-slate-600 mb-3">{project.description}</p>
                        <div className="flex items-center gap-2 text-sm text-slate-500">
                          <Clock className="w-4 h-4" />
                          <span>{project.estimated_hours || project.estimatedHours} hours</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>

                {/* Resources */}
                <Card className="animate-slide-up" style={{ animationDelay: '0.6s' }}>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 bg-gradient-to-r from-teal-500 to-cyan-500 rounded-lg flex items-center justify-center">
                      <FileText className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-900">Additional Resources</h3>
                  </div>
                  
                  <div className="grid md:grid-cols-3 gap-6">
                    {/* Books */}
                    <div>
                      <h4 className="font-semibold text-slate-900 mb-3 flex items-center gap-2">
                        <BookOpen className="w-4 h-4" />
                        Books
                      </h4>
                      <ul className="space-y-2">
                        {(results.resources?.books || []).map((book, index) => (
                          <li key={index} className="text-sm text-slate-600 flex items-start gap-2">
                            <span className="text-blue-500 mt-1">•</span>
                            <span>{book}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Websites */}
                    <div>
                      <h4 className="font-semibold text-slate-900 mb-3 flex items-center gap-2">
                        <ExternalLink className="w-4 h-4" />
                        Websites
                      </h4>
                      <ul className="space-y-2">
                        {(results.resources?.websites || []).map((website, index) => (
                          <li key={index} className="text-sm text-slate-600 flex items-start gap-2">
                            <span className="text-blue-500 mt-1">•</span>
                            <span>{website}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Communities */}
                    <div>
                      <h4 className="font-semibold text-slate-900 mb-3 flex items-center gap-2">
                        <Users className="w-4 h-4" />
                        Communities
                      </h4>
                      <ul className="space-y-2">
                        {(results.resources?.communities || []).map((community, index) => (
                          <li key={index} className="text-sm text-slate-600 flex items-start gap-2">
                            <span className="text-blue-500 mt-1">•</span>
                            <span>{community}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </Card>
              </>
            ) : (
              <Card className="text-center py-12 animate-slide-up" style={{ animationDelay: '0.2s' }}>
                <div className="w-20 h-20 bg-gradient-to-r from-blue-100 to-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <BookOpen className="w-10 h-10 text-blue-600" />
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-2">Ready to Start Learning</h3>
                <p className="text-slate-600 mb-6">
                  Enter your learning goals and get a personalized roadmap
                </p>
                <div className="flex flex-wrap justify-center gap-4 text-sm text-slate-500">
                  <div className="flex items-center gap-2">
                    <Award className="w-4 h-4 text-blue-500" />
                    <span>Curated Resources</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Target className="w-4 h-4 text-blue-500" />
                    <span>Structured Phases</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Clock className="w-4 h-4 text-blue-500" />
                    <span>Time Estimates</span>
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

export default LearningFlowGenerator;
