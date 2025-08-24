'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function Home() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <h1 className="text-2xl font-bold text-indigo-600">ResumeIQ</h1>
            <div className="space-x-4">
              <Link href="/login" className="text-gray-700 hover:text-indigo-600">
                Login
              </Link>
              <Link
                href="/register"
                className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            AI-Powered Resume Analysis
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Upload resumes, extract skills automatically, and match candidates to jobs
            using advanced AI models. Streamline your hiring process with intelligent matching.
          </p>
          <div className="space-x-4">
            <Link
              href="/register"
              className="inline-block bg-indigo-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-indigo-700"
            >
              Start Free Trial
            </Link>
            <Link
              href="/login"
              className="inline-block bg-white text-indigo-600 px-8 py-3 rounded-lg text-lg font-semibold border-2 border-indigo-600 hover:bg-indigo-50"
            >
              Login
            </Link>
          </div>
        </div>

        <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-3">📄 Smart Parsing</h3>
            <p className="text-gray-600">
              Extract skills, experience, and contact info from PDFs automatically
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-3">🎯 Job Matching</h3>
            <p className="text-gray-600">
              AI-powered matching with skill gap analysis and scoring
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-3">⚡ Fast Analysis</h3>
            <p className="text-gray-600">
              Process hundreds of resumes in seconds with transformer models
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
