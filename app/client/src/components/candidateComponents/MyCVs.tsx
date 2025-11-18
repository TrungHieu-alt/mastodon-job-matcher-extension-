import { Download, Edit, Trash2, Plus } from 'lucide-react';

export default function MyCVs() {
  const cvs = [
    {
      id: 1,
      name: 'Senior Developer CV',
      template: 'Modern',
      lastUpdated: '2 days ago',
      thumbnail: 'from-purple-500 to-purple-700',
    },
    {
      id: 2,
      name: 'Full Stack Engineer Resume',
      template: 'Elegant',
      lastUpdated: '1 week ago',
      thumbnail: 'from-slate-700 to-slate-900',
    },
    {
      id: 3,
      name: 'UI Developer Portfolio',
      template: 'Minimalist',
      lastUpdated: '2 weeks ago',
      thumbnail: 'from-gray-800 to-gray-900',
    },
    {
      id: 4,
      name: 'Frontend Specialist CV',
      template: 'Modern',
      lastUpdated: '1 month ago',
      thumbnail: 'from-purple-500 to-purple-700',
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2>My CVs</h2>
          <p className="text-muted-foreground">Manage your professional resumes</p>
        </div>
        <button className="flex items-center gap-2 px-6 py-2.5 bg-primary text-primary-foreground rounded-xl hover:opacity-90 transition-opacity">
          <Plus className="w-4 h-4" />
          Create New CV
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {cvs.map((cv) => (
          <div
            key={cv.id}
            className="bg-card rounded-2xl border border-border shadow-sm hover:shadow-xl transition-all group overflow-hidden"
          >
            {/* CV Thumbnail */}
            <div className={`h-64 bg-gradient-to-br ${cv.thumbnail} relative overflow-hidden`}>
              <div className="absolute inset-0 bg-white/10 backdrop-blur-[1px]">
                <div className="p-8 text-white">
                  <div className="h-3 bg-white/30 rounded mb-3 w-3/4"></div>
                  <div className="h-2 bg-white/20 rounded mb-2 w-full"></div>
                  <div className="h-2 bg-white/20 rounded mb-2 w-5/6"></div>
                  <div className="h-2 bg-white/20 rounded mb-6 w-4/6"></div>
                  
                  <div className="space-y-4 mt-8">
                    <div>
                      <div className="h-2 bg-white/30 rounded mb-2 w-1/2"></div>
                      <div className="h-2 bg-white/20 rounded mb-1 w-full"></div>
                      <div className="h-2 bg-white/20 rounded w-4/5"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* CV Info */}
            <div className="p-6">
              <div className="mb-4">
                <h4 className="mb-1">{cv.name}</h4>
                <div className="flex items-center gap-3 text-sm text-muted-foreground">
                  <span>{cv.template} Template</span>
                  <span>•</span>
                  <span>Updated {cv.lastUpdated}</span>
                </div>
              </div>

              <div className="flex gap-2">
                <button className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-xl hover:opacity-90 transition-opacity">
                  <Edit className="w-4 h-4" />
                  Edit
                </button>
                <button className="px-4 py-2 border border-border rounded-xl hover:bg-muted transition-colors">
                  <Download className="w-4 h-4" />
                </button>
                <button className="px-4 py-2 border border-border rounded-xl hover:bg-destructive hover:text-destructive-foreground hover:border-destructive transition-colors">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}

        {/* Create New Card */}
        <div className="bg-card rounded-2xl border-2 border-dashed border-border hover:border-primary transition-colors cursor-pointer group">
          <div className="h-full flex flex-col items-center justify-center p-12 min-h-[400px]">
            <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
              <Plus className="w-8 h-8 text-primary" />
            </div>
            <h4 className="mb-2">Create New CV</h4>
            <p className="text-muted-foreground text-sm text-center">
              Start building your professional resume
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
