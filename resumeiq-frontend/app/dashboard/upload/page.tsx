'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import api from '@/lib/api';
import { Upload } from 'lucide-react';

export default function UploadResume() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const { register, handleSubmit } = useForm();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (selectedFile.size > 10 * 1024 * 1024) {
        toast.error('File size must be less than 10MB');
        return;
      }
      setFile(selectedFile);
    }
  };

  const onSubmit = async (data: any) => {
    if (!file) {
      toast.error('Please select a file');
      return;
    }

    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      if (data.position_applied) {
        formData.append('position_applied', data.position_applied);
      }

      const response = await api.post('/resumes/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      const resumeId = response.data.id;
      toast.success('Resume uploaded successfully!');

      // Analyze the resume
      setAnalyzing(true);
      try {
        await api.post(`/ai/analyze/${resumeId}`);
        toast.success('Analysis complete!');
        router.push(`/dashboard/resumes/${resumeId}`);
      } catch (error) {
        toast.error('Analysis failed, but resume was saved');
        router.push(`/dashboard/resumes/${resumeId}`);
      }
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Upload failed');
    } finally {
      setUploading(false);
      setAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-3xl mx-auto px-4">
        <h1 className="text-3xl text-gray-700 font-bold mb-8">Upload Resume</h1>

        <div className="bg-white rounded-lg shadow p-6">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Resume File (PDF or TXT)
              </label>
              <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                <div className="space-y-1 text-center">
                  <Upload className="mx-auto h-12 w-12 text-gray-400" />
                  <div className="flex text-sm text-gray-600">
                    <label className="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500">
                      <span>Upload a file</span>
                      <input
                        type="file"
                        className="sr-only"
                        accept=".pdf,.txt"
                        onChange={handleFileChange}
                      />
                    </label>
                  </div>
                  <p className="text-xs text-gray-500">PDF or TXT up to 10MB</p>
                  {file && (
                    <p className="text-sm text-green-600 mt-2">
                      Selected: {file.name}
                    </p>
                  )}
                </div>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Position Applying For (Optional)
              </label>
              <input
                {...register('position_applied')}
                type="text"
                className="mt-1 block w-full px-3 py-2 border border-gray-300 text-gray-700 rounded-md"
                placeholder="e.g., Senior Software Engineer"
              />
            </div>

            <button
              type="submit"
              disabled={uploading || analyzing}
              className="w-full py-2 px-4 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
            >
              {uploading ? 'Uploading...' : analyzing ? 'Analyzing...' : 'Upload & Analyze'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}