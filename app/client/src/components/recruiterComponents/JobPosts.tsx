import { useState } from 'react';
import { Card, CardContent } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Textarea } from '../ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../ui/dialog';
import { 
  Plus, 
  Briefcase, 
  Users, 
  Calendar, 
  MoreVertical, 
  Edit, 
  ExternalLink, 
  XCircle, 
  Trash2,
  X,
  Hash,
  ArrowLeft,
  Save,
  Send,
  MessageCircle,
  Repeat2,
  Star
} from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '../ui/dropdown-menu';
import { Separator } from '../ui/separator';

const jobs = [
  { 
    id: 1, 
    title: 'Senior React Developer', 
    department: 'Engineering', 
    description: 'Looking for an experienced React developer to join our team.',
    requiredSkills: ['React', 'TypeScript', 'Node.js'],
    applicants: 24, 
    posted: '2024-10-28', 
    status: 'Active' as const
  },
  { 
    id: 2, 
    title: 'Product Designer', 
    department: 'Design', 
    description: 'Creative product designer with strong UX background.',
    requiredSkills: ['Figma', 'UI/UX', 'Prototyping'],
    applicants: 18, 
    posted: '2024-10-27', 
    status: 'Active' as const
  },
  { 
    id: 3, 
    title: 'DevOps Engineer', 
    department: 'Engineering', 
    description: 'DevOps engineer to manage cloud infrastructure.',
    requiredSkills: ['AWS', 'Kubernetes', 'Docker'],
    applicants: 15, 
    posted: '2024-10-25', 
    status: 'Active' as const
  },
  { 
    id: 4, 
    title: 'UX Researcher', 
    department: 'Design', 
    description: 'UX researcher to conduct user studies and analysis.',
    requiredSkills: ['User Research', 'Data Analysis', 'Figma'],
    applicants: 12, 
    posted: '2024-10-24', 
    status: 'Closed' as const
  },
  { 
    id: 5, 
    title: 'Backend Engineer', 
    department: 'Engineering', 
    description: 'Backend engineer specializing in Python and Django.',
    requiredSkills: ['Python', 'Django', 'PostgreSQL'],
    applicants: 21, 
    posted: '2024-10-22', 
    status: 'Active' as const
  },
];

export function JobPosts() {
  const [jobType, setJobType] = useState<'remote' | 'onsite' | 'hybrid'>('remote');
  const [status, setStatus] = useState<'Open' | 'Closed'>('Open');
  
  // Form state
  const [formData, setFormData] = useState({
    title: '',
    roleSummary: '',
    responsibilities: '',
    requirements: '',
    benefits: '',
    workingTime: '',
    probationaryPeriod: '',
    location: '',
    dueDate: '',
  });

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };



  return (
    <div className="max-w-[900px] mx-auto space-y-6 pb-4">
      {/* Header */}
      <div className="space-y-1">
        <h2>Job Post Editor</h2>
        <p className="text-muted-foreground">Create or edit a job posting</p>
      </div>

      {/* Form Container */}
      <Card className="rounded-2xl border-border shadow-sm">
        <CardContent className="p-8  space-y-8">
          {/* Basic Information Section */}
          <div className="space-y-6">
            <div>
              <h3 className="mb-4">Basic Information</h3>
              <Separator className="mb-6" />
            </div>

            {/* Job Title */}
            <div className="space-y-2">
              <Label htmlFor="title" className="text-sm">Job Title *</Label>
              <Input
                id="title"
                placeholder="e.g. Senior React Developer"
                value={formData.title}
                onChange={(e) => handleInputChange('title', e.target.value)}
                className="rounded-xl h-11"
              />
            </div>

            {/* Role Summary */}
            <div className="space-y-2">
              <Label htmlFor="role-summary" className="text-sm">Role Summary *</Label>
              <Textarea
                id="role-summary"
                placeholder="Briefly describe the role and what you're looking for..."
                value={formData.roleSummary}
                onChange={(e) => handleInputChange('roleSummary', e.target.value)}
                className="rounded-xl min-h-[100px] resize-none"
              />
              <p className="text-xs text-muted-foreground">
                This will be the main text of your Mastodon post
              </p>
            </div>

            {/* Status */}
            <div className="space-y-3">
              <Label className="text-sm">Status *</Label>
              <div className="grid grid-cols-2 gap-3 max-w-xs">
                <Button
                  type="button"
                  variant={status === 'Open' ? 'default' : 'outline'}
                  onClick={() => setStatus('Open')}
                  className={`rounded-xl h-11 ${
                    status === 'Open' 
                      ? 'bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700' 
                      : ''
                  }`}
                >
                  Open
                </Button>
                <Button
                  type="button"
                  variant={status === 'Closed' ? 'default' : 'outline'}
                  onClick={() => setStatus('Closed')}
                  className={`rounded-xl h-11 ${
                    status === 'Closed' 
                      ? 'bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700' 
                      : ''
                  }`}
                >
                  Closed
                </Button>
              </div>
            </div>
          </div>

          {/* Responsibilities Section */}
          <div className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="responsibilities" className="text-sm">Responsibilities *</Label>
              <Textarea
                id="responsibilities"
                placeholder="Enter each responsibility on a new line...&#10;Example:&#10;Lead frontend development&#10;Mentor junior developers&#10;Review code and design"
                value={formData.responsibilities}
                onChange={(e) => handleInputChange('responsibilities', e.target.value)}
                className="rounded-xl min-h-[140px] resize-none"
              />
              <p className="text-xs text-muted-foreground">
                Each line will be formatted as a bullet point in the preview
              </p>
            </div>
          </div>

          {/* Requirements Section */}
          <div className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="requirements" className="text-sm">Requirements *</Label>
              <Textarea
                id="requirements"
                placeholder="Enter each requirement on a new line...&#10;Example:&#10;5+ years React experience&#10;Strong TypeScript skills&#10;Experience with Node.js"
                value={formData.requirements}
                onChange={(e) => handleInputChange('requirements', e.target.value)}
                className="rounded-xl min-h-[140px] resize-none"
              />
              <p className="text-xs text-muted-foreground">
                Each line will be formatted as a bullet point in the preview
              </p>
            </div>
          </div>

          {/* Benefits Section */}
          <div className="space-y-6"> 
            <div className="grid gap-6">
              {/* Benefits */}
              <div className="space-y-2">
                <Label htmlFor="benefits" className="text-sm">Benefits *</Label>
                <Textarea
                  id="benefits"
                  placeholder="Describe the benefits and perks offered..."
                  value={formData.benefits}
                  onChange={(e) => handleInputChange('benefits', e.target.value)}
                  className="rounded-xl min-h-[100px] resize-none"
                />
              </div>

              {/* Working Time & Probation */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="working-time" className="text-sm">Working Time</Label>
                  <Input
                    id="working-time"
                    placeholder="e.g. 9:00 AM - 5:00 PM"
                    value={formData.workingTime}
                    onChange={(e) => handleInputChange('workingTime', e.target.value)}
                    className="rounded-xl h-11"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="probation" className="text-sm">Probationary Period</Label>
                  <Input
                    id="probation"
                    placeholder="e.g. 3 months"
                    value={formData.probationaryPeriod}
                    onChange={(e) => handleInputChange('probationaryPeriod', e.target.value)}
                    className="rounded-xl h-11"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Job Settings Section */}
          <div className="space-y-6">
            <div className="grid gap-6">
              {/* Job Type */}
              <div className="space-y-3">
                <Label className="text-sm">Job Type *</Label>
                <div className="grid grid-cols-3 gap-3">
                  <Button
                    type="button"
                    variant={jobType === 'remote' ? 'default' : 'outline'}
                    onClick={() => setJobType('remote')}
                    className={`rounded-xl h-11 ${
                      jobType === 'remote' 
                        ? 'bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700' 
                        : ''
                    }`}
                  >
                    Remote
                  </Button>
                  <Button
                    type="button"
                    variant={jobType === 'onsite' ? 'default' : 'outline'}
                    onClick={() => setJobType('onsite')}
                    className={`rounded-xl h-11 ${
                      jobType === 'onsite' 
                        ? 'bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700' 
                        : ''
                    }`}
                  >
                    Onsite
                  </Button>
                  <Button
                    type="button"
                    variant={jobType === 'hybrid' ? 'default' : 'outline'}
                    onClick={() => setJobType('hybrid')}
                    className={`rounded-xl h-11 ${
                      jobType === 'hybrid' 
                        ? 'bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700' 
                        : ''
                    }`}
                  >
                    Hybrid
                  </Button>
                </div>
              </div>

              {/* Application Deadline */}
              <div className="space-y-2">
                <Label htmlFor="due-date" className="text-sm">Application Deadline</Label>
                <Input
                  id="due-date"
                  type="date"
                  value={formData.dueDate}
                  onChange={(e) => handleInputChange('dueDate', e.target.value)}
                  className="rounded-xl h-11 max-w-xs"
                />
                <p className="text-xs text-muted-foreground">
                  Last date to accept applications for this position
                </p>
              </div>

              {/* Location */}
              <div className="space-y-2">
                <Label htmlFor="location" className="text-sm">Location</Label>
                <Input
                  id="location"
                  placeholder="e.g. San Francisco, CA or Remote"
                  value={formData.location}
                  onChange={(e) => handleInputChange('location', e.target.value)}
                  className="rounded-xl h-11"
                />
                <p className="text-xs text-muted-foreground">
                  Physical location or specify if remote
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>


      {/* Action Buttons */}
      <Card className="rounded-2xl shadow-sm sticky bottom-0  backdrop-blur-sm">
        <CardContent className="p-4">
          <div className="flex gap-3">
            <Button
              type="button"
              onClick={() => {/* Navigation will be handled by parent */}}
              variant="outline"
              className="rounded-xl h-11 px-6"
            >
              Cancel
            </Button>
            <Button
              type="button"
              variant="outline"
              className="rounded-xl h-11 px-6 flex-1"
              onClick={() => {/* Save draft logic */}}
            >
              <Save className="w-4 h-4 mr-2" />
              Save Draft
            </Button>
            <Button
              type="submit"
              className="bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 rounded-xl h-11 px-6 flex-1"
            >
              <Send className="w-4 h-4 mr-2" />
              Publish to Mastodon
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}