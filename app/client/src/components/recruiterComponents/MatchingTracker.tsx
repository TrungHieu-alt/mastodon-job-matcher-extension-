import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Search, Users, Calendar, Plus, MoreVertical, Edit, ExternalLink, XCircle, Trash2, Sparkles } from 'lucide-react';
import { CandidateListModal } from './CandidateListModel';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '../ui/dropdown-menu';

const jobPosts = [
  {
    id: 1,
    title: 'Senior React Developer',
    tags: ['React', 'TypeScript', 'Node.js', 'Remote'],
    matchCount: 18,
    applicants: 24,
    topSkills: ['React Hooks', 'Redux', 'Jest'],
    matchPercentage: 94,
    posted: '2024-10-28',
    status: 'Open' as const,
  },
  {
    id: 2,
    title: 'Product Designer',
    tags: ['Figma', 'UI/UX', 'Design Systems', 'Remote'],
    matchCount: 12,
    applicants: 18,
    topSkills: ['Figma', 'Prototyping', 'User Research'],
    matchPercentage: 88,
    posted: '2024-10-27',
    status: 'Open' as const,
  },
  {
    id: 3,
    title: 'DevOps Engineer',
    tags: ['AWS', 'Kubernetes', 'Docker', 'CI/CD'],
    matchCount: 11,
    applicants: 15,
    topSkills: ['AWS', 'Terraform', 'GitHub Actions'],
    matchPercentage: 91,
    posted: '2024-10-25',
    status: 'Closed' as const,
  },
  {
    id: 4,
    title: 'Backend Engineer',
    tags: ['Python', 'Django', 'PostgreSQL', 'Remote'],
    matchCount: 16,
    applicants: 21,
    topSkills: ['Python', 'REST APIs', 'Database Design'],
    matchPercentage: 92,
    posted: '2024-10-22',
    status: 'Open' as const,
  },
  {
    id: 5,
    title: 'Mobile Developer (React Native)',
    tags: ['React Native', 'iOS', 'Android', 'Remote'],
    matchCount: 9,
    applicants: 12,
    topSkills: ['React Native', 'Mobile UI', 'App Store'],
    matchPercentage: 86,
    posted: '2024-10-20',
    status: 'Closed' as const,
  },
];

export function MatchingTracker() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCandidate, setSelectedCandidate] = useState<boolean>(false);

  const filteredJobs = jobPosts.filter(job =>
    job.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    job.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase())) ||
    job.topSkills.some(skill => skill.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <div className="space-y-6">
      {/* Header & Filters */}
      <div className="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
        <div>
          <h2>Matching Tracker</h2>
          <p className="text-muted-foreground">Track candidate matches across all active job posts</p>
        </div>
        <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
          <div className="relative w-full md:w-80">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Filter by hashtag / date / skill..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 bg-input-background border-border rounded-xl"
            />
          </div>
          <Button 
            onClick={() => {/* Navigation to job editor will be handled by parent */}}
            className="bg-linear-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 rounded-xl whitespace-nowrap"
          >
            <Plus className="w-4 h-4 mr-2" />
            Create New Job Post
          </Button>
        </div>
      </div>

      {/* Job Cards Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {filteredJobs.map((job) => (
          <Card 
            key={job.id} 
            className="rounded-2xl border-border shadow-sm hover:shadow-md transition-all hover:border-purple-500/50"
          >
            <CardHeader>
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <CardTitle className="mb-1">{job.title}</CardTitle>
                  {/* Status Badge */}
                  <Badge 
                    className={`h-5 px-2 text-[11px] rounded-md ${
                      job.status === 'Open'
                        ? 'bg-linear-to-r from-purple-500 to-purple-600 text-white'
                        : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                    }`}
                  >
                    {job.status}
                  </Badge>
                  <div className="flex items-center gap-4 text-sm text-muted-foreground mt-2">
                    <div className="flex items-center gap-2">
                      <Calendar className="w-4 h-4" />
                      <span>Posted {job.posted}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Users className="w-4 h-4 text-purple-500" />
                      <span>{job.applicants} Applicants</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-purple-500" />
                      <span>{job.matchCount} Matches</span>
                    </div>
                  </div>
                </div>
                {/* Dropdown Menu */}
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon" className="rounded-xl">
                      <MoreVertical className="w-4 h-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end" className="w-48 rounded-xl">
                    <DropdownMenuItem className="rounded-lg cursor-pointer">
                      <Edit className="w-4 h-4 mr-2" />
                      Edit Post
                    </DropdownMenuItem>
                    <DropdownMenuItem className="rounded-lg cursor-pointer">
                      <ExternalLink className="w-4 h-4 mr-2" />
                      View on Mastodon
                    </DropdownMenuItem>
                    <DropdownMenuItem className="rounded-lg cursor-pointer">
                      <XCircle className="w-4 h-4 mr-2" />
                      Close Post
                    </DropdownMenuItem>
                    <DropdownMenuItem className="rounded-lg cursor-pointer text-red-600 dark:text-red-400">
                      <Trash2 className="w-4 h-4 mr-2" />
                      Delete Post
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Tags */}
              <div className="flex flex-wrap gap-2">
                {job.tags.map((tag, idx) => (
                  <Badge 
                    key={idx} 
                    variant="secondary"
                    className="rounded-lg bg-purple-50 text-purple-700 dark:bg-purple-950/50 dark:text-purple-300"
                  >
                    #{tag}
                  </Badge>
                ))}
              </div>

              {/* Top Skills */}
              <div>
                <div className="text-sm text-muted-foreground mb-2">Top Matching Skills:</div>
                <div className="flex flex-wrap gap-2">
                  {job.topSkills.map((skill, idx) => (
                    <Badge 
                      key={idx}
                      className="bg-linear-to-r from-purple-500 to-purple-600 rounded-lg"
                    >
                      {skill}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Match Progress */}
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-muted-foreground">Match Quality</span>
                  <span>{job.matchPercentage}%</span>
                </div>
                <div className="bg-accent rounded-full h-2">
                  <div 
                    className="bg-linear-to-r from-purple-500 to-purple-600 h-2 rounded-full transition-all" 
                    style={{ width: `${job.matchPercentage}%` }}
                  />
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3">
                <Button 
                  variant="outline"
                  className="flex-1 rounded-xl"
                  onClick={() => setSelectedCandidate(true)}
                >
                  View Applicants ({job.applicants})
                </Button>
                <Button 
                  className="flex-1 bg-linear-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 rounded-xl"
                  onClick={() => setSelectedCandidate(true)}
                >
                  View Matching ({job.matchCount})
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Empty State */}
      {filteredJobs.length === 0 && (
        <Card className="rounded-2xl border-border shadow-sm">
          <CardContent className="py-12 text-center">
            <Users className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="mb-2">No matches found</h3>
            <p className="text-muted-foreground">
              Try adjusting your search filters
            </p>
          </CardContent>
        </Card>
      )}

      {/* Candidate List Modal */}
      <CandidateListModal 
        open={selectedCandidate} 
        onOpenChange={setSelectedCandidate}
      />
    </div>
  );
}