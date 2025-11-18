import { useState, useEffect } from 'react';
import Sidebar from './candidateComponents/Sidebar';
import Topbar from './candidateComponents/Topbar';
import Dashboard from './candidateComponents/Dashboard';
import JobMatching from './candidateComponents/JobMatching';
import CreateCV from './candidateComponents/CreateCV';
import MyCVs from './candidateComponents/MyCVs';
import SavedJobs from './candidateComponents/SavedJobs';
import AppliedJobs from './candidateComponents/AppliedJobs';
import CompanyChat from './candidateComponents/CompanyChat';
import Settings from './candidateComponents/Settings';

export default function CandidatePage() {
  const [activePage, setActivePage] = useState('dashboard');
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const darkModePreference = window.matchMedia('(prefers-color-scheme: dark)').matches;
    setIsDark(darkModePreference);
  }, []);

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  const toggleTheme = () => {
    setIsDark(!isDark);
  };

  const renderPage = () => {
    switch (activePage) {
      case 'dashboard':
        return <Dashboard />;
      case 'job-matching':
        return <JobMatching />;
      case 'create-cv':
        return <CreateCV />;
      case 'my-cvs':
        return <MyCVs />;
      case 'saved-jobs':
        return <SavedJobs />;
      case 'applied-jobs':
        return <AppliedJobs />;
      case 'company-chat':
        return <CompanyChat />;
      case 'settings':
        return <Settings />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Sidebar activePage={activePage} onNavigate={setActivePage} />
      <Topbar isDark={isDark} onToggleTheme={toggleTheme} />
      
      <main className="ml-64 pt-16 p-6">
        <div className="max-w-7xl mx-auto">
          {renderPage()}
        </div>
      </main>
    </div>
  );
}
