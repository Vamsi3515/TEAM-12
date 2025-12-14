import React from "react";
import { Routes, Route } from "react-router-dom";
import Landing from "./components/Landing";
import Home from "./components/Home";
import GitHubAnalyzer from "./components/GitHubAnalyzer";
import RejectionDetector from "./components/Ats-score-with-rejection-detector";
import SecurityAuditor from "./components/SecurityAuditor";
import ExperienceAuthenticityAgent from "./components/ExperienceAuthenticityAgent";
import CodeToUmlDiagram from "./components/CodeToUmlDiagram";
import LearningFlowGenerator from "./components/LearningFlowGenerator";

const App = () => {
  return (
    <div className="min-h-screen bg-pageBg text-sm sm:text-base">
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/home" element={<Home />} />
        <Route path="/Ats-score-with-rejection-detector" element={<RejectionDetector />} />
        <Route path="/github-analyzer" element={<GitHubAnalyzer />} />
        <Route path="/security-auditor" element={<SecurityAuditor />} />
        <Route path="/experience-authenticity" element={<ExperienceAuthenticityAgent />} />
        {/* <Route path="/code-to-uml" element={<CodeToUmlDiagram />} /> */}
        <Route path="/learning-flow" element={<LearningFlowGenerator />} />
      </Routes>
    </div>
  );
};

export default App;
