import { FileText, Briefcase, Send, Star, TrendingUp } from 'lucide-react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const stats = [
    { label: 'Total CVs Created', value: '12', icon: FileText, color: 'from-purple-400 to-purple-600' },
    { label: 'Jobs Matched', value: '47', icon: Briefcase, color: 'from-violet-400 to-violet-600' },
    { label: 'Applications Sent', value: '23', icon: Send, color: 'from-indigo-400 to-indigo-600' },
    { label: 'Saved Jobs', value: '15', icon: Star, color: 'from-purple-500 to-purple-700' },
  ];

  const matchScoreData = [
    { month: 'Jan', score: 65 },
    { month: 'Feb', score: 72 },
    { month: 'Mar', score: 68 },
    { month: 'Apr', score: 78 },
    { month: 'May', score: 85 },
    { month: 'Jun', score: 88 },
  ];

  const recommendedJobs = [
    {
      id: 1,
      title: 'Senior Frontend Developer',
      company: 'TechCorp Inc.',
      matchScore: 92,
      skills: 'React, TypeScript, Tailwind',
      status: 'New',
    },
    {
      id: 2,
      title: 'Full Stack Engineer',
      company: 'StartupXYZ',
      matchScore: 88,
      skills: 'Node.js, React, PostgreSQL',
      status: 'New',
    },
    {
      id: 3,
      title: 'UI/UX Developer',
      company: 'DesignHub',
      matchScore: 85,
      skills: 'Figma, React, CSS',
      status: 'Viewed',
    },
    {
      id: 4,
      title: 'React Developer',
      company: 'WebSolutions',
      matchScore: 82,
      skills: 'React, Redux, Jest',
      status: 'New',
    },
    {
      id: 5,
      title: 'Frontend Architect',
      company: 'Enterprise Corp',
      matchScore: 80,
      skills: 'JavaScript, Architecture, Leadership',
      status: 'Viewed',
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2>Welcome Back!</h2>
        <p className="text-muted-foreground">Here's what's happening with your job search today</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div
              key={index}
              className="bg-card rounded-2xl p-6 border border-border shadow-sm hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${stat.color} flex items-center justify-center shadow-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
              <div className="space-y-1">
                <p className="text-muted-foreground text-sm">{stat.label}</p>
                <h3 className="text-3xl">{stat.value}</h3>
              </div>
            </div>
          );
        })}
      </div>

      {/* Chart Section */}
      <div className="bg-card rounded-2xl p-6 border border-border shadow-sm">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3>Average Match Score Over Time</h3>
            <p className="text-muted-foreground text-sm">Your matching performance trend</p>
          </div>
          <div className="flex items-center gap-2 text-green-600">
            <TrendingUp className="w-5 h-5" />
            <span>+12% this month</span>
          </div>
        </div>

        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={matchScoreData}>
            <defs>
              <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#a78bfa" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#a78bfa" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e8e5f5" />
            <XAxis dataKey="month" stroke="#8b86a3" />
            <YAxis stroke="#8b86a3" />
            <Tooltip
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #e8e5f5',
                borderRadius: '12px',
                boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
              }}
            />
            <Line
              type="monotone"
              dataKey="score"
              stroke="#6c5dd3"
              strokeWidth={3}
              fill="url(#colorScore)"
              dot={{ fill: '#6c5dd3', r: 6 }}
              activeDot={{ r: 8 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Recommended Jobs Table */}
      <div className="bg-card rounded-2xl border border-border shadow-sm overflow-hidden">
        <div className="p-6 border-b border-border">
          <h3>Recommended Jobs</h3>
          <p className="text-muted-foreground text-sm">Top matches based on your profile</p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-muted/50">
              <tr>
                <th className="text-left px-6 py-4 text-sm text-muted-foreground">Job Title</th>
                <th className="text-left px-6 py-4 text-sm text-muted-foreground">Company</th>
                <th className="text-left px-6 py-4 text-sm text-muted-foreground">Match Score</th>
                <th className="text-left px-6 py-4 text-sm text-muted-foreground">Skills Matched</th>
                <th className="text-left px-6 py-4 text-sm text-muted-foreground">Status</th>
              </tr>
            </thead>
            <tbody>
              {recommendedJobs.map((job) => (
                <tr
                  key={job.id}
                  className="border-t border-border hover:bg-muted/30 cursor-pointer transition-colors"
                >
                  <td className="px-6 py-4">{job.title}</td>
                  <td className="px-6 py-4 text-muted-foreground">{job.company}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 max-w-[100px] h-2 bg-muted rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-purple-500 to-purple-600 rounded-full"
                          style={{ width: `${job.matchScore}%` }}
                        ></div>
                      </div>
                      <span className="text-sm">{job.matchScore}%</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-muted-foreground text-sm">{job.skills}</td>
                  <td className="px-6 py-4">
                    <span
                      className={`px-3 py-1 rounded-full text-xs ${
                        job.status === 'New'
                          ? 'bg-purple-100 text-purple-700'
                          : 'bg-gray-100 text-gray-700'
                      }`}
                    >
                      {job.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
