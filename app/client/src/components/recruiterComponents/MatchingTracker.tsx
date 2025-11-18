import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Search, Users, TrendingUp, Calendar } from 'lucide-react';
import { CandidateListModal } from './CandidateListModel';

const jobPosts = [
  {
    id: 1,
    title: 'Senior React Developer',
    tags: ['React', 'TypeScript', 'Node.js', 'Remote'],
    matchCount: 24,
    topSkills: ['React Hooks', 'Redux', 'Jest'],
    matchPercentage: 94,
    posted: '2024-10-28',
  },
  {
    id: 2,
    title: 'Product Designer',
    tags: ['Figma', 'UI/UX', 'Design Systems', 'Remote'],
    matchCount: 18,
    topSkills: ['Figma', 'Prototyping', 'User Research'],
    matchPercentage: 88,
    posted: '2024-10-27',
  },
  {
    id: 3,
    title: 'DevOps Engineer',
    tags: ['AWS', 'Kubernetes', 'Docker', 'CI/CD'],
    matchCount: 15,
    topSkills: ['AWS', 'Terraform', 'GitHub Actions'],
    matchPercentage: 91,
    posted: '2024-10-25',
  },
  {
    id: 4,
    title: 'Backend Engineer',
    tags: ['Python', 'Django', 'PostgreSQL', 'Remote'],
    matchCount: 21,
    topSkills: ['Python', 'REST APIs', 'Database Design'],
    matchPercentage: 92,
    posted: '2024-10-22',
  },
  {
    id: 5,
    title: 'Mobile Developer (React Native)',
    tags: ['React Native', 'iOS', 'Android', 'Remote'],
    matchCount: 12,
    topSkills: ['React Native', 'Mobile UI', 'App Store'],
    matchPercentage: 86,
    posted: '2024-10-20',
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
        <div className="relative w-full md:w-80">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <Input
            placeholder="Filter by hashtag / date / skill..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 bg-input-background border-border rounded-xl"
          />
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
                  <CardTitle className="mb-2">{job.title}</CardTitle>
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <Calendar className="w-4 h-4" />
                    <span>Posted {job.posted}</span>
                  </div>
                </div>
                <div className="flex flex-col items-end gap-1">
                  <div className="flex items-center gap-2 text-sm">
                    <Users className="w-4 h-4 text-purple-500" />
                    <span>{job.matchCount} matches</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <TrendingUp className="w-4 h-4 text-green-500" />
                    <span className="font-medium">{job.matchPercentage}%</span>
                  </div>
                </div>
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
                      className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg"
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
                    className="bg-gradient-to-r from-purple-500 to-purple-600 h-2 rounded-full transition-all" 
                    style={{ width: `${job.matchPercentage}%` }}
                  />
                </div>
              </div>

              {/* Action Button */}
              <Button 
                className="w-full bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 rounded-xl"
                onClick={() => setSelectedCandidate(true)}
              >
                View {job.matchCount} Matches
              </Button>
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
