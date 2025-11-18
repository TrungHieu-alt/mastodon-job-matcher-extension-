import { Trash2, Send, Star } from 'lucide-react';

export default function SavedJobs() {
  const savedJobs = [
    {
      id: 1,
      title: 'Senior Frontend Developer',
      company: 'TechCorp Inc.',
      dateSaved: 'Jan 15, 2025',
      matchPercent: 92,
      logo: '🏢',
    },
    {
      id: 2,
      title: 'Full Stack Engineer',
      company: 'StartupXYZ',
      dateSaved: 'Jan 12, 2025',
      matchPercent: 88,
      logo: '🚀',
    },
    {
      id: 3,
      title: 'UI/UX Developer',
      company: 'DesignHub',
      dateSaved: 'Jan 10, 2025',
      matchPercent: 85,
      logo: '🎨',
    },
    {
      id: 4,
      title: 'React Developer',
      company: 'WebSolutions',
      dateSaved: 'Jan 8, 2025',
      matchPercent: 82,
      logo: '💻',
    },
    {
      id: 5,
      title: 'Frontend Architect',
      company: 'Enterprise Corp',
      dateSaved: 'Jan 5, 2025',
      matchPercent: 80,
      logo: '🏛️',
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2>Saved Jobs</h2>
        <p className="text-muted-foreground">Jobs you've bookmarked for later review</p>
      </div>

      <div className="bg-card rounded-2xl border border-border shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-muted/50 border-b border-border">
              <tr>
                <th className="text-left px-6 py-4 text-muted-foreground">Job Title</th>
                <th className="text-left px-6 py-4 text-muted-foreground">Company</th>
                <th className="text-left px-6 py-4 text-muted-foreground">Date Saved</th>
                <th className="text-left px-6 py-4 text-muted-foreground">Match</th>
                <th className="text-left px-6 py-4 text-muted-foreground">Actions</th>
              </tr>
            </thead>
            <tbody>
              {savedJobs.map((job) => (
                <tr
                  key={job.id}
                  className="border-b border-border hover:bg-muted/30 transition-colors"
                >
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center text-xl">
                        {job.logo}
                      </div>
                      <span>{job.title}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-muted-foreground">{job.company}</td>
                  <td className="px-6 py-4 text-muted-foreground">{job.dateSaved}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 max-w-[120px] h-2 bg-muted rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-purple-500 to-purple-600 rounded-full"
                          style={{ width: `${job.matchPercent}%` }}
                        ></div>
                      </div>
                      <span className="text-sm">{job.matchPercent}%</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-xl hover:opacity-90 transition-opacity">
                        <Send className="w-4 h-4" />
                        Apply
                      </button>
                      <button className="px-3 py-2 border border-border rounded-xl hover:bg-destructive hover:text-destructive-foreground hover:border-destructive transition-colors">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {savedJobs.length === 0 && (
        <div className="bg-card rounded-2xl border border-border p-12 text-center">
          <div className="w-16 h-16 rounded-2xl bg-muted mx-auto mb-4 flex items-center justify-center">
            <Star className="w-8 h-8 text-muted-foreground" />
          </div>
          <h3 className="mb-2">No saved jobs yet</h3>
          <p className="text-muted-foreground mb-6">
            Start exploring jobs and save the ones you're interested in
          </p>
          <button className="px-6 py-2.5 bg-primary text-primary-foreground rounded-xl hover:opacity-90 transition-opacity">
            Browse Jobs
          </button>
        </div>
      )}
    </div>
  );
}
