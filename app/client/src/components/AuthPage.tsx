import { useState } from 'react';
import { Briefcase, ChevronDown, Check } from 'lucide-react';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from './ui/collapsible';

export default function AuthPage() {
  const [isPermissionsOpen, setIsPermissionsOpen] = useState(false);

  const permissions = [
    'Read your public profile',
    'Access basic social graph (followers / following)',
    'Send messages only to deliver job matches'
  ];

  return (
    <div className="min-h-screen w-full flex items-center justify-center p-6 relative overflow-hidden bg-linear-to-br from-[#A78BFA] to-[#C7D2FE]">
      {/* Background decorative elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-20 w-64 h-64 bg-white/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-32 right-32 w-96 h-96 bg-purple-300/20 rounded-full blur-3xl"></div>
      </div>

      {/* Main Card */}
      <div className="relative w-full max-w-md">
        <div 
          className="bg-white/25 backdrop-blur-2xl rounded-3xl p-10 shadow-2xl shadow-purple-900/10"
          style={{
            boxShadow: '0 8px 32px 0 rgba(139, 92, 246, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.3)'
          }}
        >
          {/* Logo */}
          <div className="flex justify-center mb-8">
            <div className="w-20 h-20 bg-linear-to-br from-purple-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg shadow-purple-500/30">
              <Briefcase className="w-10 h-10 text-white" strokeWidth={2.5} />
            </div>
          </div>

          {/* Title */}
          <h1 className="text-center text-gray-900 mb-3">
            Connect Your Mastodon Profile
          </h1>

          {/* Subtitle */}
          <p className="text-center text-gray-700 mb-8">
            We'll use your profile and public activity to help recommend relevant jobs and opportunities.
          </p>

          {/* Primary Button */}
          <button className="w-full bg-linear-to-r from-purple-600 to-purple-500 text-white py-4 rounded-2xl mb-4 shadow-lg shadow-purple-500/30 hover:shadow-xl hover:shadow-purple-500/40 transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]">
            Authorize with Mastodon
          </button>

          {/* View Permissions Toggle */}
          <Collapsible open={isPermissionsOpen} onOpenChange={setIsPermissionsOpen}>
            <CollapsibleTrigger asChild>
              <button className="w-full text-purple-900 text-center py-2 mb-6 flex items-center justify-center gap-2 hover:text-purple-950 transition-colors">
                <span className="underline decoration-1 underline-offset-4">View Permissions</span>
                <ChevronDown 
                  className={`w-4 h-4 transition-transform duration-200 ${isPermissionsOpen ? 'rotate-180' : ''}`} 
                />
              </button>
            </CollapsibleTrigger>

            <CollapsibleContent className="mb-6">
              <div className="bg-white/40 backdrop-blur-sm rounded-2xl p-5 space-y-3">
                {permissions.map((permission, index) => (
                  <div key={index} className="flex gap-3 items-start">
                    <div className="shrink-0 mt-0.5">
                      <div className="w-5 h-5 rounded-full bg-purple-500 flex items-center justify-center">
                        <Check className="w-3 h-3 text-white" strokeWidth={3} />
                      </div>
                    </div>
                    <div className="text-gray-900">{permission}</div>
                  </div>
                ))}
              </div>
            </CollapsibleContent>
          </Collapsible>

          {/* Legal Notice */}
          <div className="text-center text-gray-600">
            Your data will never be sold. You can revoke access at any time from your Mastodon account settings.
          </div>
        </div>
      </div>
    </div>
  );
}
