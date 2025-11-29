import { useState, useEffect } from 'react';
import { Sidebar } from './recruiterComponents/Sidebar';
import { Topbar } from './recruiterComponents/Topbar';
import { Dashboard } from './recruiterComponents/Dashboard';
import { JobPosts } from './recruiterComponents/JobPosts';
import { MatchingTracker } from './recruiterComponents/MatchingTracker';
import { CandidateManager } from './recruiterComponents/CandidateManager';
import { Analytics } from './recruiterComponents/Analytics';
import { Settings } from './recruiterComponents/Settings';

export default function RecruiterPage() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />;
      case 'jobs':
        return <JobPosts />;
      case 'matching':
        return <MatchingTracker />;
      case 'candidates':
        return <CandidateManager />;
      case 'analytics':
        return <Analytics />;
      case 'settings':
        return <Settings />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <Sidebar currentPage={currentPage} onNavigate={setCurrentPage} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Topbar */}
        <Topbar isDarkMode={isDarkMode} onToggleTheme={() => setIsDarkMode(!isDarkMode)} />

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto p-8">
          {renderPage()}
        </main>
      </div>
    </div>
  );
}
