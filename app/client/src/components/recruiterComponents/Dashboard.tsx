import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Briefcase, Users, MessageSquare, CheckCircle } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Badge } from '../ui/badge';

const performanceData = [
  { month: 'Jan', matches: 45, offers: 12 },
  { month: 'Feb', matches: 52, offers: 15 },
  { month: 'Mar', matches: 68, offers: 20 },
  { month: 'Apr', matches: 75, offers: 22 },
  { month: 'May', matches: 89, offers: 28 },
  { month: 'Jun', matches: 95, offers: 32 },
];

const recentJobs = [
  { title: 'Senior React Developer', posted: '2024-10-28', status: 'Active', matchScore: 94 },
  { title: 'Product Designer', posted: '2024-10-27', status: 'Active', matchScore: 88 },
  { title: 'DevOps Engineer', posted: '2024-10-25', status: 'Active', matchScore: 91 },
  { title: 'UX Researcher', posted: '2024-10-24', status: 'Closed', matchScore: 85 },
  { title: 'Backend Engineer', posted: '2024-10-22', status: 'Active', matchScore: 92 },
];

export function Dashboard() {
  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="rounded-2xl border-border shadow-sm bg-linear-to-br from-purple-50 to-white dark:from-purple-950/20 dark:to-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm text-muted-foreground">Jobs Posted</CardTitle>
            <Briefcase className="w-5 h-5 text-purple-500" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl">24</div>
            <p className="text-xs text-muted-foreground mt-1">+3 this week</p>
          </CardContent>
        </Card>

        <Card className="rounded-2xl border-border shadow-sm bg-linear-to-br from-blue-50 to-white dark:from-blue-950/20 dark:to-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm text-muted-foreground">Candidates Matched</CardTitle>
            <Users className="w-5 h-5 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl">156</div>
            <p className="text-xs text-muted-foreground mt-1">+12 this week</p>
          </CardContent>
        </Card>

        <Card className="rounded-2xl border-border shadow-sm bg-linear-to-br from-pink-50 to-white dark:from-pink-950/20 dark:to-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm text-muted-foreground">Messages Sent</CardTitle>
            <MessageSquare className="w-5 h-5 text-pink-500" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl">89</div>
            <p className="text-xs text-muted-foreground mt-1">+8 this week</p>
          </CardContent>
        </Card>

        <Card className="rounded-2xl border-border shadow-sm bg-linear-to-br from-green-50 to-white dark:from-green-950/20 dark:to-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm text-muted-foreground">Offers Accepted</CardTitle>
            <CheckCircle className="w-5 h-5 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl">32</div>
            <p className="text-xs text-muted-foreground mt-1">+5 this week</p>
          </CardContent>
        </Card>
      </div>

      {/* Performance Chart */}
      <Card className="rounded-2xl border-border shadow-sm">
        <CardHeader>
          <CardTitle>Matching Performance Over Time</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(99, 100, 255, 0.1)" />
              <XAxis dataKey="month" stroke="#6b6b7b" />
              <YAxis stroke="#6b6b7b" />
              <Tooltip 
                contentStyle={{ 
                  background: 'var(--card)', 
                  border: '1px solid var(--border)',
                  borderRadius: '12px'
                }} 
              />
              <Line 
                type="monotone" 
                dataKey="matches" 
                stroke="#6364FF" 
                strokeWidth={3}
                dot={{ fill: '#6364FF', r: 5 }}
                name="Matches"
              />
              <Line 
                type="monotone" 
                dataKey="offers" 
                stroke="#9b87f5" 
                strokeWidth={3}
                dot={{ fill: '#9b87f5', r: 5 }}
                name="Offers"
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Recent Job Posts */}
      <Card className="rounded-2xl border-border shadow-sm">
        <CardHeader>
          <CardTitle>Recent Job Posts</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-3 px-4 text-muted-foreground">Title</th>
                  <th className="text-left py-3 px-4 text-muted-foreground">Posted Date</th>
                  <th className="text-left py-3 px-4 text-muted-foreground">Status</th>
                  <th className="text-left py-3 px-4 text-muted-foreground">Top Match Score</th>
                </tr>
              </thead>
              <tbody>
                {recentJobs.map((job, idx) => (
                  <tr key={idx} className="border-b border-border hover:bg-accent/50 transition-colors">
                    <td className="py-3 px-4">{job.title}</td>
                    <td className="py-3 px-4 text-muted-foreground">{job.posted}</td>
                    <td className="py-3 px-4">
                      <Badge 
                        variant={job.status === 'Active' ? 'default' : 'secondary'}
                        className={job.status === 'Active' ? 'bg-linear-to-r from-purple-500 to-purple-600' : ''}
                      >
                        {job.status}
                      </Badge>
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        <div className="flex-1 bg-accent rounded-full h-2 max-w-[100px]">
                          <div 
                            className="bg-linear-to-r from-purple-500 to-purple-600 h-2 rounded-full" 
                            style={{ width: `${job.matchScore}%` }}
                          />
                        </div>
                        <span className="text-sm">{job.matchScore}%</span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
