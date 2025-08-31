'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import api from '@/lib/api';
import { FileText, Mail, Phone, Briefcase, Award, Target, ArrowLeft, Trash2} from 'lucide-react';
import Link from 'next/link';

export default function ResumeAnalysis() {
  const params = useParams();
  const [resume, setResume] = useState<any>(null);
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadResume();
  }, [params.id]);

  const loadResume = async () => {
    try {
      const resumeRes = await api.get(`/resumes/${params.id}`);
      setResume(resumeRes.data);

      // Try to get analysis
      try {
        const analysisRes = await api.get(`/resumes/${params.id}/analysis`);
        setAnalysis(analysisRes.data);
      } catch (error) {
        console.log('No analysis available');
      }
    } catch (error) {
      console.error('Failed to load resume');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this resume?")) return;

    try {
      await api.delete(`/resumes/${params.id}`);
      
      // Redirect back to dashboard after deletion
      window.location.href = "/dashboard";
    } catch (err: any) {
      console.error(err);
      alert(err.response?.data?.detail || "Error deleting resume");
    }
  };

  if (loading) return <div>Loading...</div>;
  if (!resume) return <div>Resume not found</div>;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <Link 
          href="/dashboard" 
          className="flex items-center text-indigo-600 hover:text-indigo-800 mb-6"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Dashboard
        </Link>
        <h1 className="text-3xl font-bold mb-8 text-gray-900">Resume Analysis</h1>

        {/* Resume Info */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex items-center mb-4">
            <FileText className="w-6 h-6 text-indigo-600 mr-2" />
            <h2 className="text-xl font-semibold text-gray-900">{resume.filename}</h2>
          </div>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <h2 className="text-gray-600">Status: {'Completed'}</h2>
            </div>
            <div>
              <h2 className="text-gray-600">Uploaded: {' '}
                {new Date(resume.uploaded_at).toLocaleDateString()}
              </h2>
            </div>
          </div>
        </div>

        {analysis && (
          <>
            {/* Contact Info */}
            {analysis.contact_info && (
              <div className="bg-white rounded-lg shadow p-6 mb-6">
                <h3 className="text-lg font-semibold mb-4 text-gray-900">Contact Information</h3>
                <div className="space-y-2">
                  {analysis.contact_info.email && (
                    <div className="flex items-center">
                      <Mail className="w-4 h-4 text-gray-400 mr-2" />
                      <h3 className="text-gray-600">{analysis.contact_info.email}</h3>
                    </div>
                  )}
                  {analysis.contact_info.phone && (
                    <div className="flex items-center">
                      <Phone className="w-4 h-4 text-gray-400 mr-2" />
                      <h3 className="text-gray-600">{analysis.contact_info.phone}</h3>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Skills */}
            <div className="bg-white rounded-lg shadow p-6 mb-6">
              <h3 className="text-lg font-semibold mb-4 text-gray-900">Extracted Skills</h3>
              <div className="flex flex-wrap gap-2">
                {analysis.extracted_skills?.map((skill: string) => (
                  <span
                    key={skill}
                    className="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            {/* Experience */}
            <div className="bg-white rounded-lg shadow p-6 mb-6">
              <h3 className="text-lg font-semibold mb-4 text-gray-900">Experience Analysis</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <span className="text-gray-600">Experience Level:</span>{' '}
                  <span className="font-medium text-gray-900">{analysis.experience_level}</span>
                </div>
                <div>
                  <span className="text-gray-600">Years of Experience:</span>{' '}
                  <span className="font-medium text-gray-900">{analysis.total_experience_years || 'N/A'}</span>
                </div>
              </div>
            </div>

            {/* ATS Score */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4 text-gray-900">ATS Compatibility Score</h3>
              <div className="flex items-center">
                <div className="text-3xl font-bold text-indigo-600">
                  {analysis.ats_score || 0}/100
                </div>
                <div className="ml-4 text-gray-600">
                  {analysis.ats_score >= 80 ? 'Excellent' : 
                   analysis.ats_score >= 60 ? 'Good' : 'Needs Improvement'}
                </div>
              </div>
            </div>

            <div className="flex justify-between items-center p-7">
              <button
                onClick={handleDelete}
                className="flex items-center px-3 py-1 bg-red-100 text-red-700 rounded hover:bg-red-200"
              >
                <Trash2 className="w-4 h-4 mr-1" />
                Delete
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
