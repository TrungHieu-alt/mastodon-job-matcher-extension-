import { Download, Edit, Trash2, Plus, Upload, FileText, ChevronDown, ChevronUp } from 'lucide-react';
import { useState, useEffect } from 'react';
import { toast } from 'sonner';
import { uploadCv, createCv, getCvsByUser } from '../../api/jobs';

type ApiCv = {
  id: number;
  user_id: number;
  title: string;
  location: string;
  experience_years: number;
  skills: string[];
  summary: string;
  full_text: string;
  created_at: string;
};

type CvItem = {
  id: number;
  name: string;
  template?: string;
  lastUpdated?: string;
  thumbnail?: string;
  // detailed fields
  title?: string;
  location?: string;
  experienceYears?: number;
  skills?: string[];
  summary?: string;
  fullText?: string;
};

export default function MyCVs() {
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [showFullText, setShowFullText] = useState(false);
  const [extractedData, setExtractedData] = useState({
    title: '',
    location: '',
    experienceYears: '',
    skills: '',
    summary: '',
    fullText: '',
  });
  const [cvs, setCvs] = useState<CvItem[]>([]);
  const [, setLoadingCvs] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const handleFileSelect = (file: File) => {
    if (file.type === 'application/pdf') {
      setSelectedFile(file);
    } else {
      toast.error('Please select a PDF file');
    }
  };

  const getUserIdFromStorage = (): number | null => {
    const v = localStorage.getItem('user_id');
    if (!v) return null;
    const n = Number(v);
    return Number.isFinite(n) ? n : null;
  };

  useEffect(() => {
    const fetchCvs = async () => {
      const userId = getUserIdFromStorage();
      if (!userId) return;
      setLoadingCvs(true);
      setApiError(null);
      try {
        const res = await getCvsByUser(userId);
        // res is expected to be a list of CV objects matching schema
        const mapped: CvItem[] = res.map((c: ApiCv) => ({
          id: c.id,
          name: c.title || `CV ${c.id}`,
          template: 'Imported',
          lastUpdated: new Date(c.created_at).toLocaleDateString(),
          thumbnail: 'from-purple-500 to-purple-700',
          title: c.title,
          location: c.location,
          experienceYears: c.experience_years,
          skills: c.skills,
          summary: c.summary,
          fullText: c.full_text,
        }));
        setCvs(mapped);
      } catch (err) {
        setApiError('Failed to load CVs');
        toast.error('Failed to load CVs');
      } finally {
        setLoadingCvs(false);
      }
    };
    void fetchCvs();
  }, []);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleContinueUpload = () => {
    const doUpload = async () => {
      if (!selectedFile) return;
      setUploading(true);
      setApiError(null);
      try {
        const form = new FormData();
        form.append('file', selectedFile);
        const res: ApiCv = await uploadCv(form);
        // Map response fields to UI fields
        setExtractedData({
          title: res.title || '',
          location: res.location || '',
          experienceYears: res.experience_years?.toString() ?? '',
          skills: Array.isArray(res.skills) ? res.skills.join(', ') : '',
          summary: res.summary || '',
          fullText: res.full_text || '',
        });
        setShowUploadModal(false);
        setShowReviewModal(true);
      } catch (err) {
        setApiError('Upload failed');
        toast.error('Upload failed');
      } finally {
        setUploading(false);
      }
    };
    void doUpload();
  };

  const handleSaveCV = () => {
    const doSave = async () => {
      setSaving(true);
      setApiError(null);
      try {
        const payload = {
          title: extractedData.title,
          location: extractedData.location,
          experience_years: Number(extractedData.experienceYears) || 0,
          skills: extractedData.skills
            .split(',')
            .map((s) => s.trim())
            .filter((s) => s.length > 0),
          summary: extractedData.summary,
          full_text: extractedData.fullText,
        };
        const created: ApiCv = await createCv(payload);
        const newCv: CvItem = {
          id: created.id,
          name: created.title,
          template: 'Imported',
          lastUpdated: new Date(created.created_at).toLocaleDateString(),
          thumbnail: 'from-purple-500 to-purple-700',
          title: created.title,
          location: created.location,
          experienceYears: created.experience_years,
          skills: created.skills,
          summary: created.summary,
          fullText: created.full_text,
        };
        setCvs((s) => [newCv, ...s]);
        toast.success('CV imported successfully!', {
          description: `"${created.title}" has been added to your CVs`,
          duration: 3000,
        });
        setShowReviewModal(false);
        setSelectedFile(null);
        setExtractedData({
          title: '',
          location: '',
          experienceYears: '',
          skills: '',
          summary: '',
          fullText: '',
        });
      } catch (err) {
        setApiError('Save failed');
        toast.error('Save failed');
      } finally {
        setSaving(false);
      }
    };
    void doSave();
  };

  const handleCancelUpload = () => {
    setShowUploadModal(false);
    setSelectedFile(null);
  };

  const handleCancelReview = () => {
    setShowReviewModal(false);
    setSelectedFile(null);
    setExtractedData({
      title: '',
      location: '',
      experienceYears: '',
      skills: '',
      summary: '',
      fullText: '',
    });
  };

  const defaultCvs = [
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

  // show fetched cvs if available, otherwise fallback to defaults
  const cvsToShow = cvs.length > 0 ? cvs : defaultCvs;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2>My CVs</h2>
          <p className="text-muted-foreground">Manage your professional resumes</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => setShowUploadModal(true)}
            className="flex items-center gap-2 px-6 py-2.5 border border-border rounded-xl hover:bg-muted transition-colors"
          >
            <Upload className="w-4 h-4" />
            Import PDF
          </button>
          <button className="flex items-center gap-2 px-6 py-2.5 bg-primary text-primary-foreground rounded-xl hover:opacity-90 transition-opacity">
            <Plus className="w-4 h-4" />
            Create New CV
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {cvsToShow.map((cv) => (
          <div
            key={cv.id}
            className="bg-card rounded-2xl border border-border shadow-sm hover:shadow-xl transition-all group overflow-hidden"
          >
            {/* CV Thumbnail */}
            <div className={`h-64 bg-linear-to-br ${cv.thumbnail} relative overflow-hidden`}>
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
      </div>

      {/* Upload Modal */}
      {showUploadModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-6">
          <div className="bg-card rounded-2xl max-w-lg w-full border border-border shadow-2xl">
            <div className="p-6 border-b border-border">
              <h3 className="mb-1">Upload CV (PDF)</h3>
              <p className="text-sm text-muted-foreground">Upload your resume to import</p>
            </div>

            <div className="p-6">
              <div
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                className={`border-2 border-dashed rounded-xl p-12 transition-all cursor-pointer ${
                  isDragging
                    ? 'border-primary bg-primary/5'
                    : selectedFile
                    ? 'border-primary bg-primary/5'
                    : 'border-border hover:border-primary/50 hover:bg-muted/50'
                }`}
                onClick={() => document.getElementById('pdf-upload')?.click()}
              >
                <input
                  id="pdf-upload"
                  type="file"
                  accept="application/pdf"
                  onChange={handleFileInputChange}
                  className="hidden"
                />
                <div className="flex flex-col items-center text-center">
                  <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mb-4">
                    {selectedFile ? (
                      <FileText className="w-8 h-8 text-primary" />
                    ) : (
                      <Upload className="w-8 h-8 text-primary" />
                    )}
                  </div>
                  {selectedFile ? (
                    <>
                      <p className="mb-1">{selectedFile.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {(selectedFile.size / 1024).toFixed(1)} KB
                      </p>
                    </>
                  ) : (
                    <>
                      <p className="mb-2">Drag & drop your PDF here or click to upload</p>
                      <p className="text-sm text-muted-foreground">PDF only</p>
                    </>
                  )}
                </div>
              </div>
            </div>

            <div className="p-6 border-t border-border flex flex-col sm:flex-row gap-3">
              <button
                onClick={handleCancelUpload}
                className="flex-1 px-6 py-2.5 border border-border rounded-xl hover:bg-muted transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleContinueUpload}
                disabled={!selectedFile || uploading}
                className={`flex-1 px-6 py-2.5 rounded-xl transition-opacity ${
                  selectedFile
                    ? 'bg-primary text-primary-foreground hover:opacity-90'
                    : 'bg-muted text-muted-foreground cursor-not-allowed'
                }`}
              >
                {uploading ? 'Uploading...' : 'Continue'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Review Extracted Information Modal */}
      {showReviewModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-6">
          <div className="bg-card rounded-2xl max-w-2xl w-full border border-border shadow-2xl max-h-[90vh] overflow-hidden flex flex-col">
            <div className="p-6 border-b border-border">
              <h3 className="mb-1">Review Extracted Information</h3>
              <p className="text-sm text-muted-foreground">Confirm or edit the information extracted from your PDF</p>
            </div>

            <div className="p-6 space-y-6 overflow-y-auto flex-1">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm mb-2 text-muted-foreground">Title</label>
                  <input
                    type="text"
                    value={extractedData.title}
                    onChange={(e) => setExtractedData({ ...extractedData, title: e.target.value })}
                    className="w-full px-4 py-2.5 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none"
                    placeholder="e.g., Senior Frontend Developer"
                  />
                </div>

                <div>
                  <label className="block text-sm mb-2 text-muted-foreground">Location</label>
                  <input
                    type="text"
                    value={extractedData.location}
                    onChange={(e) => setExtractedData({ ...extractedData, location: e.target.value })}
                    className="w-full px-4 py-2.5 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none"
                    placeholder="e.g., San Francisco, CA"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm mb-2 text-muted-foreground">Experience Years</label>
                <input
                  type="number"
                  value={extractedData.experienceYears}
                  onChange={(e) => setExtractedData({ ...extractedData, experienceYears: e.target.value })}
                  className="w-full px-4 py-2.5 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none"
                  placeholder="e.g., 5"
                />
              </div>

              <div>
                <label className="block text-sm mb-2 text-muted-foreground">Skills</label>
                <textarea
                  value={extractedData.skills}
                  onChange={(e) => setExtractedData({ ...extractedData, skills: e.target.value })}
                  className="w-full px-4 py-2.5 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none resize-none"
                  rows={3}
                  placeholder="e.g., React, TypeScript, Tailwind CSS"
                />
              </div>

              <div>
                <label className="block text-sm mb-2 text-muted-foreground">Summary</label>
                <textarea
                  value={extractedData.summary}
                  onChange={(e) => setExtractedData({ ...extractedData, summary: e.target.value })}
                  className="w-full px-4 py-2.5 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none resize-none"
                  rows={4}
                  placeholder="Professional summary"
                />
              </div>

              {/* Collapsible Full Text Section */}
              <div className="border border-border rounded-xl overflow-hidden">
                <button
                  onClick={() => setShowFullText(!showFullText)}
                  className="w-full px-4 py-3 bg-muted/50 hover:bg-muted transition-colors flex items-center justify-between"
                >
                  <span className="text-sm">Full Text (optional)</span>
                  {showFullText ? (
                    <ChevronUp className="w-4 h-4" />
                  ) : (
                    <ChevronDown className="w-4 h-4" />
                  )}
                </button>
                {showFullText && (
                  <div className="p-4">
                    <textarea
                      value={extractedData.fullText}
                      readOnly
                      className="w-full px-4 py-2.5 bg-input-background rounded-xl border border-transparent resize-none text-sm"
                      rows={10}
                    />
                  </div>
                )}
              </div>
            </div>

            <div className="p-6 border-t border-border flex flex-col sm:flex-row gap-3">
              <button
                onClick={handleCancelReview}
                className="flex-1 px-6 py-2.5 border border-border rounded-xl hover:bg-muted transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleSaveCV}
                disabled={saving}
                className="flex-1 px-6 py-2.5 bg-primary text-primary-foreground rounded-xl hover:opacity-90 transition-opacity"
              >
                {saving ? 'Saving...' : 'Save CV'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}