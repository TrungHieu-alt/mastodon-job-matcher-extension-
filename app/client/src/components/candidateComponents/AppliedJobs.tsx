import { Eye, MessageSquare } from 'lucide-react';

export default function AppliedJobs() {
  const appliedJobs = [
    {
      id: 1,
      title: 'Senior Frontend Developer',
      company: 'TechCorp Inc.',
      appliedDate: 'Jan 15, 2025',
      status: 'Interview',
      logo: '🏢',
    },
    {
      id: 2,
      title: 'Full Stack Engineer',
      company: 'StartupXYZ',
      appliedDate: 'Jan 12, 2025',
      status: 'Under Review',
      logo: '🚀',
    },
    {
      id: 3,
      title: 'UI/UX Developer',
      company: 'DesignHub',
      appliedDate: 'Jan 10, 2025',
      status: 'Offer',
      logo: '🎨',
    },
    {
      id: 4,
      title: 'React Developer',
      company: 'WebSolutions',
      appliedDate: 'Jan 8, 2025',
      status: 'Rejected',
      logo: '💻',
    },
    {
      id: 5,
      title: 'Frontend Architect',
      company: 'Enterprise Corp',
      appliedDate: 'Jan 5, 2025',
      status: 'Under Review',
      logo: '🏛️',
    },
  ];

  const getStatusStyle = (status: string) => {
    switch (status) {
      case 'Interview':
        return 'bg-gradient-to-r from-blue-500 to-blue-600 text-white';
      case 'Under Review':
        return 'bg-gradient-to-r from-purple-500 to-purple-600 text-white';
      case 'Offer':
        return 'bg-gradient-to-r from-green-500 to-green-600 text-white';
      case 'Rejected':
        return 'bg-gradient-to-r from-red-500 to-red-600 text-white';
      default:
        return 'bg-gradient-to-r from-gray-500 to-gray-600 text-white';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2>Applied Jobs</h2>
        <p className="text-muted-foreground">Track the status of your job applications</p>
      </div>

      <div className="bg-card rounded-2xl border border-border shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-muted/50 border-b border-border">
              <tr>
                <th className="text-left px-6 py-4 text-muted-foreground">Job Title</th>
                <th className="text-left px-6 py-4 text-muted-foreground">Company</th>
                <th className="text-left px-6 py-4 text-muted-foreground">Applied Date</th>
                <th className="text-left px-6 py-4 text-muted-foreground">Status</th>
                <th className="text-left px-6 py-4 text-muted-foreground">Actions</th>
              </tr>
            </thead>
            <tbody>
              {appliedJobs.map((job) => (
                <tr
                  key={job.id}
                  className="border-b border-border hover:bg-muted/30 transition-colors"
                >
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-lg bg-linear-to-br from-purple-400 to-purple-600 flex items-center justify-center text-xl">
                        {job.logo}
                      </div>
                      <span>{job.title}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-muted-foreground">{job.company}</td>
                  <td className="px-6 py-4 text-muted-foreground">{job.appliedDate}</td>
                  <td className="px-6 py-4">
                    <span className={`px-4 py-1.5 rounded-full text-sm shadow-sm ${getStatusStyle(job.status)}`}>
                      {job.status}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <button className="flex items-center gap-2 px-4 py-2 border border-border rounded-xl hover:bg-muted transition-colors">
                        <Eye className="w-4 h-4" />
                        View
                      </button>
                      {job.status !== 'Rejected' && (
                        <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-xl hover:opacity-90 transition-opacity">
                          <MessageSquare className="w-4 h-4" />
                          Chat
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Stats Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-card rounded-2xl p-6 border border-border shadow-sm">
          <p className="text-muted-foreground text-sm mb-1">Total Applications</p>
          <h3 className="text-3xl">{appliedJobs.length}</h3>
        </div>
        <div className="bg-card rounded-2xl p-6 border border-border shadow-sm">
          <p className="text-muted-foreground text-sm mb-1">Under Review</p>
          <h3 className="text-3xl text-purple-600">
            {appliedJobs.filter(j => j.status === 'Under Review').length}
          </h3>
        </div>
        <div className="bg-card rounded-2xl p-6 border border-border shadow-sm">
          <p className="text-muted-foreground text-sm mb-1">Interviews</p>
          <h3 className="text-3xl text-blue-600">
            {appliedJobs.filter(j => j.status === 'Interview').length}
          </h3>
        </div>
        <div className="bg-card rounded-2xl p-6 border border-border shadow-sm">
          <p className="text-muted-foreground text-sm mb-1">Offers</p>
          <h3 className="text-3xl text-green-600">
            {appliedJobs.filter(j => j.status === 'Offer').length}
          </h3>
        </div>
      </div>
    </div>
  );
}
