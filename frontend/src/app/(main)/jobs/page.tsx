"use client";
import React from 'react';
import { useJobs } from '@/hooks/useJobs';
import { JobsTable } from '@/components/organisms/JobsTable';
import type { JobFilters } from '@/types/types';

// Placeholder for JobsFilterBar organism
function JobsFilterBar({ filters, setFilters }: { filters: JobFilters; setFilters: (f: JobFilters) => void }) {
  return (
    <div className="mb-6 p-4 bg-white dark:bg-gray-800 rounded shadow flex items-center gap-4">
      {/* Example filter: search by customer name */}
      <input
        type="text"
        placeholder="Search customer name..."
        value={filters.customer_name || ''}
        onChange={e => setFilters({ ...filters, customer_name: e.target.value })}
        className="border rounded px-3 py-2 w-64"
      />
      {/* Add more filter controls here */}
    </div>
  );
}

export default function JobsPage() {
  const { jobsQuery, jobs, filters, setFilters } = useJobs();

  return (
    <section>
      <h1 className="text-2xl font-bold mb-6">Jobs</h1>
      <JobsFilterBar filters={filters} setFilters={setFilters} />
      {jobsQuery.isLoading && (
        <div className="py-8 text-center text-gray-500">Loading jobs...</div>
      )}
      {jobsQuery.isError && (
        <div className="py-8 text-center text-red-500">Error loading jobs. Please try again.</div>
      )}
      {!jobsQuery.isLoading && !jobsQuery.isError && (
        <JobsTable
          jobs={jobs}
        />
      )}
    </section>
  );
} 