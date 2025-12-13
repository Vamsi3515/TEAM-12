import React, { useState, useEffect, useRef } from 'react';
import { 
  Code, 
  GitBranch, 
  Loader, 
  Download, 
  ZoomIn, 
  ZoomOut, 
  Maximize2,
  Eye,
  EyeOff,
  FileCode,
  CheckCircle,
  AlertTriangle,
  Copy,
  Check
} from 'lucide-react';
import Navbar from './Navbar';
import Card from './Card';
import Button from './Button';
import mermaid from 'mermaid';

const CodeToUmlDiagram = () => {
  const [inputType, setInputType] = useState('code'); // 'code' or 'repository'
  const [codeInput, setCodeInput] = useState('');
  const [repositoryUrl, setRepositoryUrl] = useState('');
  const [language, setLanguage] = useState('python');
  const [generating, setGenerating] = useState(false);
  const [diagrams, setDiagrams] = useState(null);
  const [activeDiagramTab, setActiveDiagramTab] = useState(0);
  const [error, setError] = useState(null);
  const [showCode, setShowCode] = useState(false);
  const [zoom, setZoom] = useState(1);
  const [copied, setCopied] = useState(false);
  
  const diagramRef = useRef(null);
  const containerRef = useRef(null);

  // Initialize Mermaid
  useEffect(() => {
    mermaid.initialize({ 
      startOnLoad: true,
      theme: 'default',
      securityLevel: 'loose',
      flowchart: { 
        useMaxWidth: true, 
        htmlLabels: true,
        curve: 'basis'
      }
    });
  }, []);

  // Render Mermaid diagram
  useEffect(() => {
    if (diagrams && diagrams.length > 0 && diagramRef.current) {
      const currentDiagram = diagrams[activeDiagramTab];
      if (currentDiagram && currentDiagram.mermaid_code) {
        try {
          const id = `mermaid-${Date.now()}`;
          mermaid.render(id, currentDiagram.mermaid_code).then(({ svg }) => {
            if (diagramRef.current) {
              diagramRef.current.innerHTML = svg;
            }
          }).catch(err => {
            console.error('Mermaid rendering error:', err);
            setError('Failed to render diagram. Invalid Mermaid syntax.');
          });
        } catch (err) {
          console.error('Mermaid error:', err);
          setError('Failed to render diagram');
        }
      }
    }
  }, [diagrams, activeDiagramTab]);

  // Handle form submission
  const handleGenerate = async () => {
    // Validation
    if (inputType === 'code' && !codeInput.trim()) {
      setError('Please enter code to analyze');
      return;
    }
    if (inputType === 'repository' && !repositoryUrl.trim()) {
      setError('Please enter a repository URL');
      return;
    }

    setGenerating(true);
    setError(null);

    try {
      const payload = inputType === 'code' 
        ? { code: codeInput, language, inputType: 'code' }
        : { repoUrl: repositoryUrl, inputType: 'repo' };

      const response = await fetch('http://localhost:8000/api/generate-code-diagrams', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error('Failed to generate diagrams. Please try again.');
      }

      const data = await response.json();
      console.log('API Response:', data); // Debug
      
      // Map response to expected format
      if (data.diagrams && data.diagrams.length > 0) {
        const mappedDiagrams = data.diagrams.map(d => ({
          type: d.type || d.title || 'Diagram',
          mermaid_code: d.mermaid || d.mermaid_code || '',
          description: d.description || ''
        }));
        setDiagrams(mappedDiagrams);
        setActiveDiagramTab(0);
        setZoom(1);
      } else {
        throw new Error('No diagrams generated from code');
      }
    } catch (err) {
      setError(err.message || 'An error occurred while generating diagrams');
      console.error('Error:', err);
    } finally {
      setGenerating(false);
    }
  };

  // Load sample code
  const loadSampleCode = () => {
    const sampleCode = `class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.orders = []
    
    def place_order(self, order):
        self.orders.append(order)
        order.assign_user(self)

class Order:
    def __init__(self, order_id, total):
        self.order_id = order_id
        self.total = total
        self.user = None
        self.items = []
    
    def assign_user(self, user):
        self.user = user
    
    def add_item(self, item):
        self.items.append(item)

class OrderItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price`;

    setCodeInput(sampleCode);
    setLanguage('python');
    setInputType('code');
  };

  // Load sample diagrams
  const loadSampleDiagrams = () => {
    setDiagrams([
      {
        type: 'Class Diagram',
        mermaid_code: `classDiagram
    class User {
        +String name
        +String email
        +List~Order~ orders
        +place_order(order)
    }
    class Order {
        +String order_id
        +Float total
        +User user
        +List~OrderItem~ items
        +assign_user(user)
        +add_item(item)
    }
    class OrderItem {
        +String product
        +Int quantity
        +Float price
    }
    User "1" --> "*" Order : places
    Order "1" --> "*" OrderItem : contains`,
        description: 'Class structure and relationships'
      },
      {
        type: 'Sequence Diagram',
        mermaid_code: `sequenceDiagram
    participant U as User
    participant O as Order
    participant OI as OrderItem
    U->>O: place_order(order)
    O->>U: assign_user(user)
    U->>O: add_item(item)
    O->>OI: create OrderItem`,
        description: 'Method call flow and interactions'
      },
      {
        type: 'Flowchart',
        mermaid_code: `flowchart TD
    A[Start] --> B{User Exists?}
    B -->|Yes| C[Load User]
    B -->|No| D[Create User]
    C --> E[Create Order]
    D --> E
    E --> F[Add Items]
    F --> G{More Items?}
    G -->|Yes| F
    G -->|No| H[Calculate Total]
    H --> I[Save Order]
    I --> J[End]`,
        description: 'Process flow and decision points'
      }
    ]);
    setActiveDiagramTab(0);
    setZoom(1);
  };

  // Zoom controls
  const handleZoomIn = () => setZoom(prev => Math.min(prev + 0.2, 3));
  const handleZoomOut = () => setZoom(prev => Math.max(prev - 0.2, 0.5));
  const handleResetZoom = () => setZoom(1);

  // Download SVG
  const handleDownloadSVG = () => {
    if (diagramRef.current && diagrams) {
      const svgElement = diagramRef.current.querySelector('svg');
      if (svgElement) {
        const svgData = new XMLSerializer().serializeToString(svgElement);
        const blob = new Blob([svgData], { type: 'image/svg+xml' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${diagrams[activeDiagramTab].type.replace(/\s+/g, '_')}.svg`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      }
    }
  };

  // Copy Mermaid code
  const handleCopyCode = () => {
    if (diagrams && diagrams[activeDiagramTab]) {
      navigator.clipboard.writeText(diagrams[activeDiagramTab].mermaid_code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-indigo-50/30 to-purple-50/30">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-8 animate-slide-up">
          <div className="inline-flex items-center gap-2 bg-gradient-to-r from-indigo-100 to-purple-100 text-indigo-700 px-4 py-2 rounded-full text-sm font-medium mb-4 shadow-sm">
            <Code className="w-4 h-4" />
            <span>AI-Powered Diagram Generation</span>
          </div>
          
          <h1 className="text-4xl font-bold text-slate-900 mb-3">
            Code to 
            <span className="block bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
              UML Diagrams
            </span>
          </h1>
          
          <p className="text-lg text-slate-600 max-w-3xl mx-auto">
            Transform your code into interactive UML diagrams with AI-powered analysis
          </p>
        </div>

        {/* Input Section */}
        <Card className="mb-8 animate-slide-up" style={{ animationDelay: '0.1s' }}>
          {/* Input Type Toggle */}
          <div className="flex items-center gap-4 mb-6 p-1 bg-slate-100 rounded-lg w-fit">
            <button
              onClick={() => setInputType('code')}
              className={`flex items-center gap-2 px-6 py-2.5 rounded-lg font-medium transition-all ${
                inputType === 'code'
                  ? 'bg-white text-indigo-600 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Code className="w-4 h-4" />
              Code Input
            </button>
            <button
              onClick={() => setInputType('repository')}
              className={`flex items-center gap-2 px-6 py-2.5 rounded-lg font-medium transition-all ${
                inputType === 'repository'
                  ? 'bg-white text-indigo-600 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <GitBranch className="w-4 h-4" />
              Repository URL
            </button>
          </div>

          {/* Code Input */}
          {inputType === 'code' && (
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Source Code
              </label>
              <textarea
                value={codeInput}
                onChange={(e) => setCodeInput(e.target.value)}
                placeholder="Paste your code here..."
                className="w-full h-64 px-4 py-3 border border-slate-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all resize-none"
              />
            </div>
          )}

          {/* Repository Input */}
          {inputType === 'repository' && (
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                GitHub Repository URL
              </label>
              <input
                type="url"
                value={repositoryUrl}
                onChange={(e) => setRepositoryUrl(e.target.value)}
                placeholder="https://github.com/username/repository"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              />
              <p className="mt-2 text-sm text-slate-500">
                Enter a public GitHub repository URL to analyze its structure
              </p>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          {/* Action Button */}
          <div className="mt-6">
            <Button
              onClick={handleGenerate}
              disabled={generating}
              className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold py-3 rounded-lg transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {generating ? (
                <>
                  <Loader className="w-5 h-5 animate-spin" />
                  Generating Diagrams...
                </>
              ) : (
                <>
                  <Code className="w-5 h-5" />
                  Generate UML Diagrams
                </>
              )}
            </Button>
          </div>
        </Card>

        {/* Results Section */}
        {diagrams && diagrams.length > 0 && (
          <div className="animate-slide-up" style={{ animationDelay: '0.2s' }}>
            {/* Diagram Tabs */}
            <Card className="mb-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-slate-900">Generated Diagrams</h3>
                <div className="flex items-center gap-2 text-sm text-slate-600">
                  <CheckCircle className="w-4 h-4 text-green-600" />
                  <span>{diagrams.length} diagram{diagrams.length !== 1 ? 's' : ''} generated</span>
                </div>
              </div>

              <div className="flex gap-2 overflow-x-auto pb-2">
                {diagrams.map((diagram, index) => (
                  <button
                    key={index}
                    onClick={() => {
                      setActiveDiagramTab(index);
                      setZoom(1);
                    }}
                    className={`flex items-center gap-2 px-4 py-2.5 rounded-lg font-medium whitespace-nowrap transition-all ${
                      activeDiagramTab === index
                        ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    <FileCode className="w-4 h-4" />
                    {diagram.type}
                  </button>
                ))}
              </div>
            </Card>

            {/* Diagram Viewer */}
            <Card>
              {/* Toolbar */}
              <div className="flex flex-wrap items-center justify-between gap-4 mb-6 pb-4 border-b border-slate-200">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-slate-700">
                    {diagrams[activeDiagramTab].type}
                  </span>
                  {diagrams[activeDiagramTab].description && (
                    <span className="text-sm text-slate-500">
                      • {diagrams[activeDiagramTab].description}
                    </span>
                  )}
                </div>

                <div className="flex items-center gap-2">
                  {/* Zoom Controls */}
                  <div className="flex items-center gap-1 bg-slate-100 rounded-lg p-1">
                    <button
                      onClick={handleZoomOut}
                      className="p-2 hover:bg-white rounded transition-colors"
                      title="Zoom Out"
                    >
                      <ZoomOut className="w-4 h-4 text-slate-600" />
                    </button>
                    <span className="px-3 text-sm font-medium text-slate-700 min-w-[60px] text-center">
                      {Math.round(zoom * 100)}%
                    </span>
                    <button
                      onClick={handleZoomIn}
                      className="p-2 hover:bg-white rounded transition-colors"
                      title="Zoom In"
                    >
                      <ZoomIn className="w-4 h-4 text-slate-600" />
                    </button>
                    <button
                      onClick={handleResetZoom}
                      className="p-2 hover:bg-white rounded transition-colors"
                      title="Reset Zoom"
                    >
                      <Maximize2 className="w-4 h-4 text-slate-600" />
                    </button>
                  </div>

                  {/* View Toggle */}
                  <button
                    onClick={() => setShowCode(!showCode)}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
                      showCode
                        ? 'bg-indigo-100 text-indigo-600'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    {showCode ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    {showCode ? 'Hide Code' : 'Show Code'}
                  </button>

                  {/* Download Button */}
                  <button
                    onClick={handleDownloadSVG}
                    className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-medium hover:from-indigo-700 hover:to-purple-700 transition-all shadow-sm"
                  >
                    <Download className="w-4 h-4" />
                    Download SVG
                  </button>
                </div>
              </div>

              {/* Mermaid Code View */}
              {showCode && (
                <div className="mb-6 relative">
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-sm font-medium text-slate-700">Mermaid Source Code</label>
                    <button
                      onClick={handleCopyCode}
                      className="flex items-center gap-2 px-3 py-1.5 text-sm bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg transition-colors"
                    >
                      {copied ? (
                        <>
                          <Check className="w-4 h-4 text-green-600" />
                          Copied!
                        </>
                      ) : (
                        <>
                          <Copy className="w-4 h-4" />
                          Copy Code
                        </>
                      )}
                    </button>
                  </div>
                  <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto text-sm font-mono">
                    {diagrams[activeDiagramTab].mermaid_code}
                  </pre>
                </div>
              )}

              {/* Diagram Container */}
              <div 
                ref={containerRef}
                className="bg-white border-2 border-slate-200 rounded-lg overflow-auto"
                style={{ minHeight: '500px', maxHeight: '700px' }}
              >
                <div 
                  className="p-8 inline-block min-w-full"
                  style={{ 
                    transform: `scale(${zoom})`,
                    transformOrigin: 'top left',
                    transition: 'transform 0.2s ease'
                  }}
                >
                  <div ref={diagramRef} className="flex items-center justify-center" />
                </div>
              </div>

              {/* Diagram Info */}
              <div className="mt-4 p-4 bg-blue-50 border border-blue-100 rounded-lg">
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-blue-900 mb-1">
                      Interactive Diagram Controls
                    </p>
                    <p className="text-sm text-blue-700">
                      Use the zoom controls to adjust view • Toggle code view to see Mermaid syntax • Download as SVG for high-quality export
                    </p>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        )}

        {/* Empty State */}
        {!diagrams && !generating && (
          <Card className="text-center py-12 animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <div className="w-20 h-20 bg-gradient-to-r from-indigo-100 to-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Code className="w-10 h-10 text-indigo-600" />
            </div>
            <h3 className="text-xl font-bold text-slate-900 mb-2">Ready to Generate Diagrams</h3>
            <p className="text-slate-600 mb-6">
              Enter your code or repository URL above to generate UML diagrams
            </p>
            <div className="flex flex-wrap justify-center gap-4 text-sm text-slate-500">
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span>Class Diagrams</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span>Sequence Diagrams</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span>Flowcharts</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span>Interactive Viewer</span>
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};

export default CodeToUmlDiagram;
