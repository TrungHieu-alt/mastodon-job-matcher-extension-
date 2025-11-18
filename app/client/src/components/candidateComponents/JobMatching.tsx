import { useState } from 'react';
import { MapPin, DollarSign, Briefcase, Star, X, CheckCircle, XCircle } from 'lucide-react';

export default function JobMatching() {
  const [selectedJob, setSelectedJob] = useState<number | null>(null);
  const [filters, setFilters] = useState({
    skill: '',
    location: '',
    salary: '',
    matchScore: '',
  });

  const jobs = [
    {
      id: 1,
      title: 'Senior Frontend Developer',
      company: 'TechCorp Inc.',
      location: 'San Francisco, CA',
      salary: '$120k - $160k',
      matchScore: 92,
      logo: '🏢',
      skills: ['React', 'TypeScript', 'Tailwind CSS', 'Node.js'],
      description: 'We are looking for a talented Senior Frontend Developer to join our growing team. You will be responsible for building modern, scalable web applications using React and TypeScript.',
      requirements: [
        '5+ years of experience with React',
        'Strong TypeScript skills',
        'Experience with modern CSS frameworks',
        'Good understanding of RESTful APIs',
      ],
      matchedSkills: ['React', 'TypeScript', 'Tailwind CSS'],
      missingSkills: ['GraphQL', 'Docker'],
    },
    {
      id: 2,
      title: 'Full Stack Engineer',
      company: 'StartupXYZ',
      location: 'Remote',
      salary: '$100k - $140k',
      matchScore: 88,
      logo: '🚀',
      skills: ['React', 'Node.js', 'PostgreSQL', 'AWS'],
      description: 'Join our fast-growing startup as a Full Stack Engineer. Build features end-to-end and work with cutting-edge technologies.',
      requirements: [
        '3+ years full stack development',
        'Experience with React and Node.js',
        'Database design knowledge',
        'Cloud platform experience',
      ],
      matchedSkills: ['React', 'Node.js', 'PostgreSQL'],
      missingSkills: ['AWS', 'Kubernetes'],
    },
    {
      id: 3,
      title: 'UI/UX Developer',
      company: 'DesignHub',
      location: 'New York, NY',
      salary: '$90k - $120k',
      matchScore: 85,
      logo: '🎨',
      skills: ['Figma', 'React', 'CSS', 'Animation'],
      description: 'Create beautiful, user-friendly interfaces that delight our customers. Work closely with designers to bring mockups to life.',
      requirements: [
        'Strong CSS and design skills',
        'Proficiency in Figma',
        'React experience',
        'Eye for detail and aesthetics',
      ],
      matchedSkills: ['React', 'CSS', 'Figma'],
      missingSkills: ['After Effects'],
    },
    {
      id: 4,
      title: 'React Developer',
      company: 'WebSolutions',
      location: 'Austin, TX',
      salary: '$95k - $125k',
      matchScore: 82,
      logo: '💻',
      skills: ['React', 'Redux', 'Jest', 'Webpack'],
      description: 'Build and maintain enterprise-level React applications for our clients. Focus on code quality and performance.',
      requirements: [
        '3+ years React development',
        'State management expertise',
        'Testing experience',
        'Performance optimization skills',
      ],
      matchedSkills: ['React', 'Redux', 'Jest'],
      missingSkills: ['Webpack'],
    },
    {
      id: 5,
      title: 'Frontend Architect',
      company: 'Enterprise Corp',
      location: 'Seattle, WA',
      salary: '$150k - $200k',
      matchScore: 80,
      logo: '🏛️',
      skills: ['JavaScript', 'Architecture', 'Leadership', 'React'],
      description: 'Lead frontend architecture decisions for our enterprise platform. Mentor junior developers and establish best practices.',
      requirements: [
        '8+ years frontend experience',
        'Architecture design experience',
        'Team leadership skills',
        'Strong communication',
      ],
      matchedSkills: ['JavaScript', 'React'],
      missingSkills: ['Microservices', 'System Design'],
    },
  ];

  const selectedJobData = jobs.find(job => job.id === selectedJob);

  return (
    <div className="space-y-6">
      <div>
        <h2>Job Matching</h2>
        <p className="text-muted-foreground">AI-powered job recommendations based on your profile</p>
      </div>

      {/* Filter Bar */}
      <div className="bg-card rounded-2xl p-6 border border-border shadow-sm">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <input
            type="text"
            placeholder="Filter by skill..."
            value={filters.skill}
            onChange={(e) => setFilters({ ...filters, skill: e.target.value })}
            className="px-4 py-2.5 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none"
          />
          <input
            type="text"
            placeholder="Location..."
            value={filters.location}
            onChange={(e) => setFilters({ ...filters, location: e.target.value })}
            className="px-4 py-2.5 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none"
          />
          <input
            type="text"
            placeholder="Salary range..."
            value={filters.salary}
            onChange={(e) => setFilters({ ...filters, salary: e.target.value })}
            className="px-4 py-2.5 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none"
          />
          <input
            type="text"
            placeholder="Min match score..."
            value={filters.matchScore}
            onChange={(e) => setFilters({ ...filters, matchScore: e.target.value })}
            className="px-4 py-2.5 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none"
          />
        </div>
      </div>

      {/* Job List */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {jobs.map((job) => (
          <div
            key={job.id}
            className="bg-card rounded-2xl p-6 border border-border shadow-sm hover:shadow-md transition-all cursor-pointer"
            onClick={() => setSelectedJob(job.id)}
          >
            <div className="flex items-start gap-4 mb-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center text-2xl">
                {job.logo}
              </div>
              <div className="flex-1">
                <h4 className="mb-1">{job.title}</h4>
                <p className="text-muted-foreground text-sm">{job.company}</p>
              </div>
              <div className="flex items-center gap-1 bg-purple-100 dark:bg-purple-900/30 px-3 py-1 rounded-full">
                <Star className="w-4 h-4 text-purple-600 dark:text-purple-400 fill-purple-600 dark:fill-purple-400" />
                <span className="text-purple-700 dark:text-purple-300">{job.matchScore}%</span>
              </div>
            </div>

            <div className="space-y-3 mb-4">
              <div className="flex items-center gap-2 text-muted-foreground text-sm">
                <MapPin className="w-4 h-4" />
                <span>{job.location}</span>
              </div>
              <div className="flex items-center gap-2 text-muted-foreground text-sm">
                <DollarSign className="w-4 h-4" />
                <span>{job.salary}</span>
              </div>
            </div>

            <div className="flex flex-wrap gap-2 mb-4">
              {job.skills.slice(0, 4).map((skill, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 rounded-full text-xs"
                >
                  {skill}
                </span>
              ))}
            </div>

            <div className="flex gap-3">
              <button className="flex-1 px-4 py-2 bg-primary text-primary-foreground rounded-xl hover:opacity-90 transition-opacity">
                View Details
              </button>
              <button className="px-4 py-2 border border-border rounded-xl hover:bg-muted transition-colors">
                <Star className="w-5 h-5" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Job Detail Panel */}
      {selectedJob && selectedJobData && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-6">
          <div className="bg-card rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-card border-b border-border p-6 flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center text-2xl">
                  {selectedJobData.logo}
                </div>
                <div>
                  <h3>{selectedJobData.title}</h3>
                  <p className="text-muted-foreground text-sm">{selectedJobData.company}</p>
                </div>
              </div>
              <button
                onClick={() => setSelectedJob(null)}
                className="w-8 h-8 rounded-lg hover:bg-muted flex items-center justify-center transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 space-y-6">
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <MapPin className="w-4 h-4 text-muted-foreground" />
                  <span className="text-sm">{selectedJobData.location}</span>
                </div>
                <div className="flex items-center gap-2">
                  <DollarSign className="w-4 h-4 text-muted-foreground" />
                  <span className="text-sm">{selectedJobData.salary}</span>
                </div>
              </div>

              <div>
                <h4 className="mb-2">Description</h4>
                <p className="text-muted-foreground">{selectedJobData.description}</p>
              </div>

              <div>
                <h4 className="mb-2">Requirements</h4>
                <ul className="space-y-2">
                  {selectedJobData.requirements.map((req, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-muted-foreground">
                      <Briefcase className="w-4 h-4 mt-1 flex-shrink-0" />
                      <span>{req}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h4 className="mb-3">AI Match Summary</h4>
                <div className="space-y-3">
                  <div>
                    <p className="text-sm text-muted-foreground mb-2">Matched Skills</p>
                    <div className="flex flex-wrap gap-2">
                      {selectedJobData.matchedSkills.map((skill, idx) => (
                        <span
                          key={idx}
                          className="flex items-center gap-1 px-3 py-1 bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300 rounded-full text-sm"
                        >
                          <CheckCircle className="w-3 h-3" />
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground mb-2">Skills to Learn</p>
                    <div className="flex flex-wrap gap-2">
                      {selectedJobData.missingSkills.map((skill, idx) => (
                        <span
                          key={idx}
                          className="flex items-center gap-1 px-3 py-1 bg-orange-50 dark:bg-orange-900/20 text-orange-700 dark:text-orange-300 rounded-full text-sm"
                        >
                          <XCircle className="w-3 h-3" />
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex gap-3 pt-4 border-t border-border">
                <button className="flex-1 px-6 py-3 bg-primary text-primary-foreground rounded-xl hover:opacity-90 transition-opacity">
                  Apply Now
                </button>
                <button className="flex-1 px-6 py-3 border border-border rounded-xl hover:bg-muted transition-colors">
                  Chat with Employer
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
