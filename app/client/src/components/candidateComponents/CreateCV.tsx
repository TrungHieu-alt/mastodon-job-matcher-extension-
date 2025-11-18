import { useState } from 'react';
import { Download, Save } from 'lucide-react';

export default function CreateCV() {
  const [template, setTemplate] = useState<'elegant' | 'modern' | 'minimalist'>('modern');
  const [showTemplateSelector, setShowTemplateSelector] = useState(false);

  const [cvData, setCvData] = useState({
    name: 'John Doe',
    title: 'Senior Frontend Developer',
    email: 'john.doe@email.com',
    phone: '+1 (555) 123-4567',
    location: 'San Francisco, CA',
    summary: 'Experienced frontend developer with 5+ years of expertise in building modern web applications using React, TypeScript, and Tailwind CSS. Passionate about creating intuitive user interfaces and writing clean, maintainable code.',
    experience: [
      {
        title: 'Senior Frontend Developer',
        company: 'TechCorp Inc.',
        period: '2021 - Present',
        description: 'Led frontend development for multiple high-traffic web applications. Mentored junior developers and established coding standards.',
      },
      {
        title: 'Frontend Developer',
        company: 'WebSolutions',
        period: '2019 - 2021',
        description: 'Developed responsive web applications using React and modern CSS frameworks. Collaborated with design team to implement pixel-perfect UIs.',
      },
    ],
    education: [
      {
        degree: 'Bachelor of Science in Computer Science',
        school: 'University of Technology',
        year: '2019',
      },
    ],
    skills: ['React', 'TypeScript', 'Tailwind CSS', 'Node.js', 'Git', 'Figma'],
  });

  const templates = {
    elegant: {
      name: 'Elegant',
      primaryColor: 'from-slate-700 to-slate-900',
      accentColor: 'text-slate-700',
      font: 'font-serif',
    },
    modern: {
      name: 'Modern',
      primaryColor: 'from-purple-500 to-purple-700',
      accentColor: 'text-purple-600',
      font: 'font-sans',
    },
    minimalist: {
      name: 'Minimalist',
      primaryColor: 'from-gray-800 to-gray-900',
      accentColor: 'text-gray-800',
      font: 'font-mono',
    },
  };

  const currentTemplate = templates[template];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2>Create CV</h2>
          <p className="text-muted-foreground">Design your professional resume</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => setShowTemplateSelector(true)}
            className="px-6 py-2.5 border border-border rounded-xl hover:bg-muted transition-colors"
          >
            Change Template
          </button>
          <button className="flex items-center gap-2 px-6 py-2.5 border border-border rounded-xl hover:bg-muted transition-colors">
            <Save className="w-4 h-4" />
            Save CV
          </button>
          <button className="flex items-center gap-2 px-6 py-2.5 bg-primary text-primary-foreground rounded-xl hover:opacity-90 transition-opacity">
            <Download className="w-4 h-4" />
            Export PDF
          </button>
        </div>
      </div>

      {/* CV Preview */}
      <div className="flex justify-center">
        <div className={`bg-white shadow-2xl rounded-lg w-[210mm] min-h-[297mm] p-16 ${currentTemplate.font}`}>
          {/* Header */}
          <div className="mb-8">
            <div className={`bg-gradient-to-r ${currentTemplate.primaryColor} text-white p-8 -mx-16 -mt-16 mb-8 rounded-t-lg`}>
              <input
                type="text"
                value={cvData.name}
                onChange={(e) => setCvData({ ...cvData, name: e.target.value })}
                className="bg-transparent border-none outline-none w-full text-4xl mb-2 placeholder-white/70"
                placeholder="Your Name"
              />
              <input
                type="text"
                value={cvData.title}
                onChange={(e) => setCvData({ ...cvData, title: e.target.value })}
                className="bg-transparent border-none outline-none w-full text-xl placeholder-white/70"
                placeholder="Your Title"
              />
            </div>

            <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
              <input
                type="text"
                value={cvData.email}
                onChange={(e) => setCvData({ ...cvData, email: e.target.value })}
                className="bg-transparent border-b border-gray-300 outline-none py-1"
                placeholder="Email"
              />
              <input
                type="text"
                value={cvData.phone}
                onChange={(e) => setCvData({ ...cvData, phone: e.target.value })}
                className="bg-transparent border-b border-gray-300 outline-none py-1"
                placeholder="Phone"
              />
              <input
                type="text"
                value={cvData.location}
                onChange={(e) => setCvData({ ...cvData, location: e.target.value })}
                className="bg-transparent border-b border-gray-300 outline-none py-1 col-span-2"
                placeholder="Location"
              />
            </div>
          </div>

          {/* Summary */}
          <div className="mb-6">
            <h3 className={`text-xl mb-3 ${currentTemplate.accentColor}`}>Professional Summary</h3>
            <textarea
              value={cvData.summary}
              onChange={(e) => setCvData({ ...cvData, summary: e.target.value })}
              className="w-full bg-transparent border border-gray-300 rounded p-3 outline-none text-gray-700 resize-none"
              rows={4}
              placeholder="Write a brief summary about yourself..."
            />
          </div>

          {/* Experience */}
          <div className="mb-6">
            <h3 className={`text-xl mb-3 ${currentTemplate.accentColor}`}>Experience</h3>
            <div className="space-y-4">
              {cvData.experience.map((exp, idx) => (
                <div key={idx} className="border-l-2 border-gray-300 pl-4">
                  <input
                    type="text"
                    value={exp.title}
                    onChange={(e) => {
                      const newExp = [...cvData.experience];
                      newExp[idx].title = e.target.value;
                      setCvData({ ...cvData, experience: newExp });
                    }}
                    className="bg-transparent border-b border-gray-300 outline-none w-full mb-1"
                    placeholder="Job Title"
                  />
                  <div className="flex gap-4 mb-2">
                    <input
                      type="text"
                      value={exp.company}
                      onChange={(e) => {
                        const newExp = [...cvData.experience];
                        newExp[idx].company = e.target.value;
                        setCvData({ ...cvData, experience: newExp });
                      }}
                      className="bg-transparent border-b border-gray-300 outline-none flex-1 text-sm text-gray-600"
                      placeholder="Company"
                    />
                    <input
                      type="text"
                      value={exp.period}
                      onChange={(e) => {
                        const newExp = [...cvData.experience];
                        newExp[idx].period = e.target.value;
                        setCvData({ ...cvData, experience: newExp });
                      }}
                      className="bg-transparent border-b border-gray-300 outline-none w-40 text-sm text-gray-600"
                      placeholder="Period"
                    />
                  </div>
                  <textarea
                    value={exp.description}
                    onChange={(e) => {
                      const newExp = [...cvData.experience];
                      newExp[idx].description = e.target.value;
                      setCvData({ ...cvData, experience: newExp });
                    }}
                    className="w-full bg-transparent border border-gray-300 rounded p-2 outline-none text-sm text-gray-700 resize-none"
                    rows={2}
                    placeholder="Description"
                  />
                </div>
              ))}
            </div>
          </div>

          {/* Education */}
          <div className="mb-6">
            <h3 className={`text-xl mb-3 ${currentTemplate.accentColor}`}>Education</h3>
            <div className="space-y-3">
              {cvData.education.map((edu, idx) => (
                <div key={idx}>
                  <input
                    type="text"
                    value={edu.degree}
                    onChange={(e) => {
                      const newEdu = [...cvData.education];
                      newEdu[idx].degree = e.target.value;
                      setCvData({ ...cvData, education: newEdu });
                    }}
                    className="bg-transparent border-b border-gray-300 outline-none w-full mb-1"
                    placeholder="Degree"
                  />
                  <div className="flex gap-4">
                    <input
                      type="text"
                      value={edu.school}
                      onChange={(e) => {
                        const newEdu = [...cvData.education];
                        newEdu[idx].school = e.target.value;
                        setCvData({ ...cvData, education: newEdu });
                      }}
                      className="bg-transparent border-b border-gray-300 outline-none flex-1 text-sm text-gray-600"
                      placeholder="School"
                    />
                    <input
                      type="text"
                      value={edu.year}
                      onChange={(e) => {
                        const newEdu = [...cvData.education];
                        newEdu[idx].year = e.target.value;
                        setCvData({ ...cvData, education: newEdu });
                      }}
                      className="bg-transparent border-b border-gray-300 outline-none w-24 text-sm text-gray-600"
                      placeholder="Year"
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Skills */}
          <div>
            <h3 className={`text-xl mb-3 ${currentTemplate.accentColor}`}>Skills</h3>
            <div className="flex flex-wrap gap-2">
              {cvData.skills.map((skill, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Template Selector Modal */}
      {showTemplateSelector && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-6">
          <div className="bg-card rounded-2xl max-w-2xl w-full p-6">
            <h3 className="mb-4">Choose Template</h3>
            <div className="grid grid-cols-3 gap-4 mb-6">
              {Object.entries(templates).map(([key, tmpl]) => (
                <button
                  key={key}
                  onClick={() => {
                    setTemplate(key as any);
                    setShowTemplateSelector(false);
                  }}
                  className={`p-4 rounded-xl border-2 transition-all ${
                    template === key
                      ? 'border-primary bg-primary/10'
                      : 'border-border hover:border-primary/50'
                  }`}
                >
                  <div className={`h-32 bg-gradient-to-br ${tmpl.primaryColor} rounded-lg mb-3`}></div>
                  <p className="text-center">{tmpl.name}</p>
                </button>
              ))}
            </div>
            <button
              onClick={() => setShowTemplateSelector(false)}
              className="w-full px-6 py-3 bg-primary text-primary-foreground rounded-xl hover:opacity-90 transition-opacity"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
