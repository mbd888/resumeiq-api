'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import toast from 'react-hot-toast';
import { auth, User } from '@/lib/auth';
import api from '@/lib/api';
import { Upload, FileText, BriefcaseBusiness, LogOut, BarChart } from 'lucide-react';

export default function Dashboard() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [resumes, setResumes] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const userData = await auth.getCurrentUser();
      setUser(userData);

      // Load resumes
      const resumesRes = await api.get('/resumes/');
      setResumes(resumesRes.data.resumes);

      // Load jobs if recruiter
      if (userData.user_type === 'recruiter') {
        const jobsRes = await api.get('/jobs/?my_jobs_only=true');
        setJobs(jobsRes.data.jobs);
      }
    } catch (error) {
      toast.error('Failed to load dashboard');
      router.push('/login');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <h1 className="text-2xl font-bold text-indigo-600">ResumeIQ</h1>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">
                {user?.full_name} ({user?.user_type})
              </span>
              <button
                onClick={() => auth.logout()}
                className="flex items-center text-gray-700 hover:text-red-600"
              >
                <LogOut className="w-5 h-5 mr-1" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h2 className="text-3xl font-bold mb-8 text-gray-700">Dashboard</h2>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 text-gray-600">
          <Link
            href="/dashboard/upload"
            className="bg-white p-6 rounded-lg shadow hover:shadow-md transition flex items-center"
          >
            <Upload className="w-8 h-8 text-indigo-600 mr-4" />
            <div>
              <h3 className="font-semibold">Upload Resume</h3>
              <p className="text-sm text-gray-600">Upload and analyze</p>
            </div>
          </Link>

          {user?.user_type === 'recruiter' && (
            <Link
              href="/dashboard/jobs/create"
              className="bg-white p-6 rounded-lg shadow hover:shadow-md transition flex items-center"
            >
              <BriefcaseBusiness className="w-8 h-8 text-indigo-600 mr-4" />
              <div>
                <h3 className="font-semibold">Post Job</h3>
                <p className="text-sm text-gray-600">Create job listing</p>
              </div>
            </Link>
          )}

          <Link
            href="/dashboard/jobs"
            className="bg-white p-6 rounded-lg shadow hover:shadow-md transition flex items-center"
          >
            <BriefcaseBusiness className="w-8 h-8 text-indigo-600 mr-4" />
            <div>
              <h3 className="font-semibold">Job Tracker</h3>
              <p className="text-sm text-gray-600">[check what you've applied to]</p>
            </div>
          </Link>

          <Link
            href="/dashboard/analysis"
            className="bg-white p-6 rounded-lg shadow hover:shadow-md transition flex items-center"
          >
            <BarChart className="w-8 h-8 text-indigo-600 mr-4" />
            <div>
              <h3 className="font-semibold">Analysis</h3>
              <p className="text-sm text-gray-600">[track your applications]</p>
            </div>
          </Link>
        </div>

        {/* Recent Resumes */}
        <div className="bg-white rounded-lg shadow p-6 mb-8 text-gray-700">
          <h3 className="text-xl font-semibold mb-4">My Resumes</h3>
          {resumes.length === 0 ? (
            <p className="text-gray-600">No resumes uploaded yet</p>
          ) : (
            <div className="space-y-4">
              {resumes.slice(0, 5).map((resume: any) => (
                <div key={resume.id} className="flex items-center justify-between p-4 border rounded">
                  <div className="flex items-center">
                    <FileText className="w-5 h-5 text-gray-400 mr-3" />
                    <div>
                      <p className="font-medium">{resume.filename}</p>
                      <p className="text-sm text-gray-600">
                        Uploaded {new Date(resume.uploaded_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <Link
                    href={`/dashboard/resumes/${resume.id}`}
                    className="text-indigo-600 hover:text-indigo-800"
                  >
                    View Analysis
                  </Link>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Jobs (for recruiters) */}
        {user?.user_type === 'recruiter' && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-semibold mb-4">My Job Postings</h3>
            {jobs.length === 0 ? (
              <p className="text-gray-600">No jobs posted yet</p>
            ) : (
              <div className="space-y-4">
                {jobs.slice(0, 5).map((job: any) => (
                  <div key={job.id} className="flex items-center justify-between p-4 border rounded">
                    <div>
                      <p className="font-medium">{job.title}</p>
                      <p className="text-sm text-gray-600">{job.company} • {job.location}</p>
                    </div>
                    <Link
                      href={`/dashboard/jobs/${job.id}/match`}
                      className="text-indigo-600 hover:text-indigo-800"
                    >
                      Find Matches
                    </Link>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}