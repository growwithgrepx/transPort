import type { Job, JobFilters } from '@/types/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:5000';

function buildUrl(endpoint: string, params?: URLSearchParams): string {
  const url = `${API_BASE_URL}${endpoint}`;
  if (params && params.toString()) {
    return `${url}?${params.toString()}`;
  }
  return url;
}

export async function getJobs(filters: JobFilters = {}): Promise<Job[]> {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      params.append(key, String(value));
    }
  });
  const response = await fetch(buildUrl('/api/jobs/table', params), {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!response.ok) {
    throw new Error(`Failed to fetch jobs: ${response.status}`);
  }
  const data = await response.json();
  return data.items || [];
}

export async function getJobById(id: number): Promise<Job> {
  const response = await fetch(buildUrl(`/jobs/view/${id}`), {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!response.ok) {
    throw new Error(`Failed to fetch job: ${response.status}`);
  }
  return response.json();
}

export async function createJob(jobData: Partial<Job>): Promise<Job> {
  const response = await fetch('/jobs/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(jobData),
  });
  if (!response.ok) {
    throw new Error(`Failed to create job: ${response.status}`);
  }
  return response.json();
}

export async function updateJob(id: number, jobData: Partial<Job>): Promise<Job> {
  const response = await fetch(`/jobs/edit/${id}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(jobData),
  });
  if (!response.ok) {
    throw new Error(`Failed to update job: ${response.status}`);
  }
  return response.json();
}

export async function deleteJob(id: number): Promise<void> {
  const response = await fetch(`/jobs/delete/${id}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!response.ok) {
    throw new Error(`Failed to delete job: ${response.status}`);
  }
} 