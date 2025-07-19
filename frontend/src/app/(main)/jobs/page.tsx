"use client";
import React, { useState } from 'react';
import { useJobs } from '@/hooks/useJobs';
import { JobsTable } from '@/components/organisms/JobsTable';
import { HiOutlineBriefcase, HiOutlineArrowDownTray, HiOutlinePlusCircle, HiOutlineListBullet } from 'react-icons/hi2';

function JobsHeader() {
  return (
    <header className="sticky top-0 z-20 bg-gray-950 shadow-sm flex items-center justify-between max-w-7xl mx-auto px-0 sm:px-0 py-4 border-b border-gray-800">
      <div className="flex items-center gap-2">
        <HiOutlineBriefcase className="w-7 h-7 text-white" />
        <h1 className="text-2xl font-bold text-white">Manage Jobs</h1>
      </div>
      <div className="flex gap-3">
        <button
          className="flex items-center gap-2 px-4 py-2 rounded-lg text-white bg-gray-700 hover:bg-gray-600 focus:ring-2 focus:ring-blue-400 transition disabled:opacity-60"
          aria-label="Download Selected"
          disabled
        >
          <HiOutlineArrowDownTray className="w-5 h-5" />
          Download Selected
        </button>
        <button
          className="flex items-center gap-2 px-4 py-2 rounded-lg text-white bg-blue-600 hover:bg-blue-500 focus:ring-2 focus:ring-blue-400 transition"
          aria-label="Create Job"
        >
          <HiOutlinePlusCircle className="w-5 h-5" />
          Create Job
        </button>
        <button
          className="flex items-center gap-2 px-4 py-2 rounded-lg text-white bg-blue-500 hover:bg-blue-400 focus:ring-2 focus:ring-blue-300 transition"
          aria-label="Create Bulk Jobs"
        >
          <HiOutlineListBullet className="w-5 h-5" />
          Create Bulk Jobs
        </button>
      </div>
    </header>
  );
}

export default function JobsPage() {
  const { jobsQuery, jobs, filters, setFilters } = useJobs();
  const [selectedJobIds, setSelectedJobIds] = useState<number[]>([]);

  // Per-column filter state
  const [columnFilters, setColumnFilters] = useState({
    customer_name: '',
    customer_mobile: '',
    passenger_name: '',
    type_of_service: '',
    pickup_date: '',
    pickup_time: '',
    pickup_location: '',
    dropoff_location: '',
    vehicle_type: '',
    vehicle_number: '',
    driver_contact: '',
    base_price: '',
    discounts: '',
    additional_charges: '',
    final_price: '',
    payment_status: '',
    status: '',
  });

  // Sync column filters to main filters
  function handleColumnFilterChange(key: string, value: string) {
    setColumnFilters(f => ({ ...f, [key]: value }));
    setFilters(f => ({ ...f, [key]: value }));
  }

  // Only update selectedJobIds if jobs list actually changes (by ID)
  React.useEffect(() => {
    setSelectedJobIds(ids => ids.filter(id => jobs.some(j => j.id === id)));
  }, [jobs.map(j => j.id).join(",")]);

  return (
    <main className="min-h-screen bg-gray-950">
      <JobsHeader />
      <div className="max-w-7xl mx-auto px-0 sm:px-0 py-8">
        {/* Quick search bar, full width, minimal padding */}
        <form className="mb-2" onSubmit={e => e.preventDefault()} role="search">
          <input
            type="text"
            placeholder="Quick search (all columns)..."
            value={filters.search || ''}
            onChange={e => setFilters({ ...filters, search: e.target.value })}
            className="form-input w-full bg-gray-800 border-gray-700 text-white placeholder-gray-400 focus:ring-2 focus:ring-blue-400 rounded-lg px-3 py-2"
            aria-label="Quick search jobs"
          />
        </form>
        <div className="bg-gray-900 rounded-xl shadow border border-gray-800 overflow-x-auto">
          <JobsTable
            jobs={jobs}
            selectedJobIds={selectedJobIds}
            onSelectionChange={setSelectedJobIds}
            columnFilters={columnFilters}
            onColumnFilterChange={handleColumnFilterChange}
          />
        </div>
      </div>
    </main>
  );
}

import type { JobFilters } from '@/types/types';
function JobsFilterBar({ filters, setFilters }: { filters: JobFilters; setFilters: (f: JobFilters) => void }) {
  return (
    <form
      className="flex w-full md:w-auto items-center gap-2 md:gap-4"
      onSubmit={e => e.preventDefault()}
      role="search"
    >
      <input
        type="text"
        placeholder="Quick search (all columns)..."
        value={filters.search || ''}
        onChange={e => setFilters({ ...filters, search: e.target.value })}
        className="form-input w-full md:w-80 bg-gray-800 border-gray-700 text-white placeholder-gray-400 focus:ring-2 focus:ring-blue-400 rounded-lg px-3 py-2"
        aria-label="Quick search jobs"
      />
    </form>
  );
} 