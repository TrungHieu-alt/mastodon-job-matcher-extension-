import { Search, Bell, User, LogOut, Moon, Sun } from 'lucide-react';
import { useState } from 'react';

interface TopbarProps {
  isDark: boolean;
  onToggleTheme: () => void;
}

export default function Topbar({ isDark, onToggleTheme }: TopbarProps) {
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [hasNotifications] = useState(true);

  return (
    <header className="h-16 bg-card border-b border-border fixed top-0 right-0 left-64 z-10 px-6 flex items-center justify-between">
      <div className="flex-1 max-w-xl">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search Job, Company, or Skill..."
            className="w-full pl-12 pr-4 py-2.5 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none transition-colors"
          />
        </div>
      </div>

      <div className="flex items-center gap-4">
        <button
          onClick={onToggleTheme}
          className="w-10 h-10 rounded-xl hover:bg-muted flex items-center justify-center transition-colors"
        >
          {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
        </button>

        <button className="relative w-10 h-10 rounded-xl hover:bg-muted flex items-center justify-center transition-colors">
          <Bell className="w-5 h-5" />
          {hasNotifications && (
            <span className="absolute top-2 right-2 w-2 h-2 bg-destructive rounded-full"></span>
          )}
        </button>

        <div className="relative">
          <button
            onClick={() => setShowUserMenu(!showUserMenu)}
            className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center text-white hover:shadow-lg transition-shadow"
          >
            <User className="w-5 h-5" />
          </button>

          {showUserMenu && (
            <div className="absolute right-0 top-12 w-48 bg-popover border border-border rounded-xl shadow-lg overflow-hidden">
              <button className="w-full px-4 py-3 text-left hover:bg-muted flex items-center gap-3 transition-colors">
                <User className="w-4 h-4" />
                <span>My Profile</span>
              </button>
              <button className="w-full px-4 py-3 text-left hover:bg-muted flex items-center gap-3 text-destructive transition-colors">
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
