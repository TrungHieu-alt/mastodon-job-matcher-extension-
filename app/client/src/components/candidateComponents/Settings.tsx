import { User, Bell, Shield, Globe, Palette } from 'lucide-react';
import { useState } from 'react';

export default function Settings() {
  const [notifications, setNotifications] = useState({
    email: true,
    push: true,
    jobMatches: true,
    messages: true,
  });

  return (
    <div className="space-y-6">
      <div>
        <h2>Settings</h2>
        <p className="text-muted-foreground">Manage your account preferences</p>
      </div>

      <div className="space-y-6">
        {/* Profile Settings */}
        <div className="bg-card rounded-2xl border border-border shadow-sm overflow-hidden">
          <div className="p-6 border-b border-border flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
              <User className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            </div>
            <div>
              <h3>Profile Settings</h3>
              <p className="text-muted-foreground text-sm">Update your personal information</p>
            </div>
          </div>
          <div className="p-6 space-y-4">
            <div>
              <label className="text-sm mb-2 block">Full Name</label>
              <input
                type="text"
                defaultValue="John Doe"
                className="w-full px-4 py-2.5 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none"
              />
            </div>
            <div>
              <label className="text-sm mb-2 block">Email Address</label>
              <input
                type="email"
                defaultValue="john.doe@email.com"
                className="w-full px-4 py-2.5 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none"
              />
            </div>
            <div>
              <label className="text-sm mb-2 block">Phone Number</label>
              <input
                type="tel"
                defaultValue="+1 (555) 123-4567"
                className="w-full px-4 py-2.5 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none"
              />
            </div>
            <div>
              <label className="text-sm mb-2 block">Location</label>
              <input
                type="text"
                defaultValue="San Francisco, CA"
                className="w-full px-4 py-2.5 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none"
              />
            </div>
            <button className="px-6 py-2.5 bg-primary text-primary-foreground rounded-xl hover:opacity-90 transition-opacity">
              Save Changes
            </button>
          </div>
        </div>

        {/* Notification Settings */}
        <div className="bg-card rounded-2xl border border-border shadow-sm overflow-hidden">
          <div className="p-6 border-b border-border flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
              <Bell className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <h3>Notification Preferences</h3>
              <p className="text-muted-foreground text-sm">Choose how you want to be notified</p>
            </div>
          </div>
          <div className="p-6 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p>Email Notifications</p>
                <p className="text-sm text-muted-foreground">Receive updates via email</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={notifications.email}
                  onChange={(e) => setNotifications({ ...notifications, email: e.target.checked })}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-muted peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-primary rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
              </label>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p>Push Notifications</p>
                <p className="text-sm text-muted-foreground">Get instant notifications</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={notifications.push}
                  onChange={(e) => setNotifications({ ...notifications, push: e.target.checked })}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-muted peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-primary rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
              </label>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p>Job Match Alerts</p>
                <p className="text-sm text-muted-foreground">Notify when new jobs match your profile</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={notifications.jobMatches}
                  onChange={(e) => setNotifications({ ...notifications, jobMatches: e.target.checked })}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-muted peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-primary rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
              </label>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p>Message Notifications</p>
                <p className="text-sm text-muted-foreground">Alerts for new chat messages</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={notifications.messages}
                  onChange={(e) => setNotifications({ ...notifications, messages: e.target.checked })}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-muted peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-primary rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
              </label>
            </div>
          </div>
        </div>

        {/* Privacy Settings */}
        <div className="bg-card rounded-2xl border border-border shadow-sm overflow-hidden">
          <div className="p-6 border-b border-border flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
              <Shield className="w-5 h-5 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <h3>Privacy & Security</h3>
              <p className="text-muted-foreground text-sm">Manage your privacy settings</p>
            </div>
          </div>
          <div className="p-6 space-y-4">
            <button className="w-full px-4 py-3 text-left hover:bg-muted rounded-xl transition-colors">
              Change Password
            </button>
            <button className="w-full px-4 py-3 text-left hover:bg-muted rounded-xl transition-colors">
              Two-Factor Authentication
            </button>
            <button className="w-full px-4 py-3 text-left hover:bg-muted rounded-xl transition-colors">
              Connected Accounts
            </button>
            <button className="w-full px-4 py-3 text-left hover:bg-muted rounded-xl transition-colors">
              Privacy Policy
            </button>
          </div>
        </div>

        {/* Preferences */}
        <div className="bg-card rounded-2xl border border-border shadow-sm overflow-hidden">
          <div className="p-6 border-b border-border flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-orange-100 dark:bg-orange-900/30 flex items-center justify-center">
              <Palette className="w-5 h-5 text-orange-600 dark:text-orange-400" />
            </div>
            <div>
              <h3>Preferences</h3>
              <p className="text-muted-foreground text-sm">Customize your experience</p>
            </div>
          </div>
          <div className="p-6 space-y-4">
            <div>
              <label className="text-sm mb-2 block">Language</label>
              <select className="w-full px-4 py-2.5 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none">
                <option>English (US)</option>
                <option>Spanish</option>
                <option>French</option>
                <option>German</option>
              </select>
            </div>
            <div>
              <label className="text-sm mb-2 block">Time Zone</label>
              <select className="w-full px-4 py-2.5 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none">
                <option>Pacific Time (PT)</option>
                <option>Eastern Time (ET)</option>
                <option>Central Time (CT)</option>
                <option>Mountain Time (MT)</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
