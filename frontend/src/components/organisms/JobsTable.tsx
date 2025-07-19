"use client";
import React, { useState } from 'react';
import { Badge } from '@/components/atoms/Badge';
import type { Job } from '@/types/types';
import { HiChevronDown, HiChevronRight } from 'react-icons/hi2';

function getStatusVariant(status: string) {
  switch (status?.toLowerCase()) {
    case 'completed':
    case 'paid':
      return 'success';
    case 'pending':
    case 'unpaid':
      return 'warning';
    case 'cancelled':
    case 'failed':
      return 'danger';
    default:
      return 'info';
  }
}

export function JobsTable({ jobs, selectedJobIds = [], onSelectionChange, columnFilters = {}, onColumnFilterChange }: {
  jobs: Job[];
  selectedJobIds?: number[];
  onSelectionChange?: (ids: number[]) => void;
  columnFilters?: Record<string, string>;
  onColumnFilterChange?: (key: string, value: string) => void;
}) {
  const [expandedJobId, setExpandedJobId] = useState<number | null>(null);
  const allSelected = jobs.length > 0 && selectedJobIds && selectedJobIds.length === jobs.length;
  const toggleAll = () => {
    if (!onSelectionChange) return;
    if (allSelected) {
      onSelectionChange([]);
    } else {
      onSelectionChange(jobs.map(j => j.id));
    }
  };
  const toggleOne = (id: number) => {
    if (!onSelectionChange) return;
    if (selectedJobIds?.includes(id)) {
      onSelectionChange(selectedJobIds.filter(jid => jid !== id));
    } else {
      onSelectionChange([...(selectedJobIds || []), id]);
    }
  };
  if (!jobs || jobs.length === 0) {
    return <div className="text-center text-gray-400 dark:text-gray-500 py-8">No jobs found.</div>;
  }
  return (
    <div className="overflow-x-auto card shadow mt-6">
      <table className="min-w-full text-sm align-middle">
        <thead>
          <tr className="bg-gray-800 text-gray-100 border-b border-gray-700 text-base font-bold">
            <th className="px-2 py-2 text-left w-8"></th>
            <th className="px-3 py-2 text-left">
              <input
                type="checkbox"
                aria-label="Select all jobs"
                checked={allSelected}
                onChange={toggleAll}
                className="accent-blue-600 w-4 h-4 rounded focus:ring-2 focus:ring-blue-400 bg-gray-700 border-gray-600"
              />
            </th>
            <th className="px-3 py-2 text-left">Customer Name</th>
            <th className="px-3 py-2 text-left">Type of Service</th>
            <th className="px-3 py-2 text-left">Date</th>
            <th className="px-3 py-2 text-left">Pickup</th>
            <th className="px-3 py-2 text-left">Drop-off</th>
            <th className="px-3 py-2 text-left">Final Price</th>
            <th className="px-3 py-2 text-left">Job Status</th>
            <th className="px-3 py-2 text-left">Actions</th>
          </tr>
          {/* Filter row for visible columns */}
          {onColumnFilterChange && (
            <tr className="bg-gray-900 border-b border-gray-800">
              <th className="px-2 py-1"></th>
              <th className="px-3 py-1"></th>
              <th className="px-3 py-1"><input type="text" className="form-input w-full bg-gray-800 border-gray-700 text-white text-xs rounded" placeholder="Filter" value={columnFilters.customer_name || ''} onChange={e => onColumnFilterChange('customer_name', e.target.value)} /></th>
              <th className="px-3 py-1"><input type="text" className="form-input w-full bg-gray-800 border-gray-700 text-white text-xs rounded" placeholder="Filter" value={columnFilters.type_of_service || ''} onChange={e => onColumnFilterChange('type_of_service', e.target.value)} /></th>
              <th className="px-3 py-1"><input type="text" className="form-input w-full bg-gray-800 border-gray-700 text-white text-xs rounded" placeholder="Filter" value={columnFilters.pickup_date || ''} onChange={e => onColumnFilterChange('pickup_date', e.target.value)} /></th>
              <th className="px-3 py-1"><input type="text" className="form-input w-full bg-gray-800 border-gray-700 text-white text-xs rounded" placeholder="Filter" value={columnFilters.pickup_location || ''} onChange={e => onColumnFilterChange('pickup_location', e.target.value)} /></th>
              <th className="px-3 py-1"><input type="text" className="form-input w-full bg-gray-800 border-gray-700 text-white text-xs rounded" placeholder="Filter" value={columnFilters.dropoff_location || ''} onChange={e => onColumnFilterChange('dropoff_location', e.target.value)} /></th>
              <th className="px-3 py-1"><input type="text" className="form-input w-full bg-gray-800 border-gray-700 text-white text-xs rounded" placeholder="Filter" value={columnFilters.final_price || ''} onChange={e => onColumnFilterChange('final_price', e.target.value)} /></th>
              <th className="px-3 py-1"><input type="text" className="form-input w-full bg-gray-800 border-gray-700 text-white text-xs rounded" placeholder="Filter" value={columnFilters.status || ''} onChange={e => onColumnFilterChange('status', e.target.value)} /></th>
              <th className="px-3 py-1"></th>
            </tr>
          )}
        </thead>
        <tbody>
          {jobs.map((job: Job) => (
            <React.Fragment key={job.id}>
              <tr className="even:bg-gray-900 hover:bg-gray-800 transition">
                <td className="px-2 py-2 align-top">
                  <button
                    aria-label={expandedJobId === job.id ? 'Collapse details' : 'Expand details'}
                    onClick={() => setExpandedJobId(expandedJobId === job.id ? null : job.id)}
                    className="focus:outline-none text-gray-400 hover:text-blue-400"
                  >
                    {expandedJobId === job.id ? <HiChevronDown className="w-5 h-5" /> : <HiChevronRight className="w-5 h-5" />}
                  </button>
                </td>
                <td className="px-3 py-2 align-top">
                  <input
                    type="checkbox"
                    aria-label={`Select job ${job.customer_name}`}
                    checked={selectedJobIds?.includes(job.id) || false}
                    onChange={() => toggleOne(job.id)}
                    className="accent-blue-600 w-4 h-4 rounded focus:ring-2 focus:ring-blue-400 bg-gray-700 border-gray-600"
                  />
                </td>
                <td className="px-3 py-2 whitespace-nowrap align-top">{job.customer_name}</td>
                <td className="px-3 py-2 whitespace-nowrap align-top">{job.type_of_service}</td>
                <td className="px-3 py-2 whitespace-nowrap align-top">{job.pickup_date}</td>
                <td className="px-3 py-2 whitespace-nowrap align-top">{job.pickup_location}</td>
                <td className="px-3 py-2 whitespace-nowrap align-top">{job.dropoff_location}</td>
                <td className="px-3 py-2 whitespace-nowrap align-top">{job.final_price?.toFixed(2)}</td>
                <td className="px-3 py-2 whitespace-nowrap align-top"><Badge variant={getStatusVariant(job.status)}>{job.status}</Badge></td>
                <td className="px-3 py-2 whitespace-nowrap align-top">
                  <button className="px-2 py-1 text-xs rounded bg-blue-600 hover:bg-blue-500 text-white focus:ring-2 focus:ring-blue-400 transition">View</button>
                </td>
              </tr>
              {expandedJobId === job.id && (
                <tr>
                  <td colSpan={10} className="bg-gray-950 border-t border-gray-800 px-0 py-0">
                    <div className="m-2 md:m-4 rounded-lg bg-gray-900 border border-gray-700 shadow-lg p-4 md:p-6 grid grid-cols-1 md:grid-cols-2 gap-6 text-sm text-gray-200">
                      <div>
                        <div className="flex items-center gap-2 font-semibold text-blue-300 mb-2"><span className="inline-block w-4 h-4 bg-blue-400 rounded-full"></span>Customer Info</div>
                        <div className="mb-1"><span className="font-medium">Name:</span> {job.customer_name}</div>
                        <div className="mb-1"><span className="font-medium">Mobile:</span> {job.customer_mobile}</div>
                        <div className="mb-1"><span className="font-medium">Email:</span> {job.customer_email}</div>
                        <div className="mb-1"><span className="font-medium">Reference:</span> {job.customer_reference}</div>
                      </div>
                      <div>
                        <div className="flex items-center gap-2 font-semibold text-blue-300 mb-2"><span className="inline-block w-4 h-4 bg-blue-400 rounded-full"></span>Passenger Info</div>
                        <div className="mb-1"><span className="font-medium">Name:</span> {job.passenger_name}</div>
                        <div className="mb-1"><span className="font-medium">Mobile:</span> {job.passenger_mobile}</div>
                        <div className="mb-1"><span className="font-medium">Email:</span> {job.passenger_email}</div>
                      </div>
                      <div>
                        <div className="flex items-center gap-2 font-semibold text-green-300 mb-2"><span className="inline-block w-4 h-4 bg-green-400 rounded-full"></span>Trip Details</div>
                        <div className="mb-1"><span className="font-medium">Type of Service:</span> {job.type_of_service}</div>
                        <div className="mb-1"><span className="font-medium">Pickup Date:</span> {job.pickup_date}</div>
                        <div className="mb-1"><span className="font-medium">Pickup Time:</span> {job.pickup_time}</div>
                        <div className="mb-1"><span className="font-medium">Pickup Location:</span> {job.pickup_location}</div>
                        <div className="mb-1"><span className="font-medium">Drop-off Location:</span> {job.dropoff_location}</div>
                        <div className="mb-1"><span className="font-medium">Vehicle:</span> {`${job.vehicle_type} ${job.vehicle_number || ''}`.trim()}</div>
                        <div className="mb-1"><span className="font-medium">Driver Contact:</span> {job.driver_contact}</div>
                      </div>
                      <div>
                        <div className="flex items-center gap-2 font-semibold text-yellow-300 mb-2"><span className="inline-block w-4 h-4 bg-yellow-400 rounded-full"></span>Pricing & Status</div>
                        <div className="mb-1"><span className="font-medium">Base Price:</span> {job.base_price?.toFixed(2)}</div>
                        <div className="mb-1"><span className="font-medium">Discounts:</span> {((job.base_discount_percent || 0) + (job.agent_discount_percent || 0) + (job.additional_discount_percent || 0)).toFixed(2)}%</div>
                        <div className="mb-1"><span className="font-medium">Additional Charges:</span> {job.additional_charges?.toFixed(2)}</div>
                        <div className="mb-1"><span className="font-medium">Final Price:</span> {job.final_price?.toFixed(2)}</div>
                        <div className="mb-1"><span className="font-medium">Payment Status:</span> <Badge variant={getStatusVariant(job.payment_status)}>{job.payment_status}</Badge></div>
                        <div className="mb-1"><span className="font-medium">Job Status:</span> <Badge variant={getStatusVariant(job.status)}>{job.status}</Badge></div>
                      </div>
                      <div className="md:col-span-2">
                        <div className="flex items-center gap-2 font-semibold text-purple-300 mb-2"><span className="inline-block w-4 h-4 bg-purple-400 rounded-full"></span>Other</div>
                        <div className="mb-1"><span className="font-medium">Order Status:</span> {job.order_status}</div>
                        <div className="mb-1"><span className="font-medium">Reference:</span> {job.reference}</div>
                        <div className="mb-1"><span className="font-medium">Remarks:</span> {job.remarks}</div>
                        <div className="mb-1"><span className="font-medium">Message:</span> {job.message}</div>
                        <div className="mb-1"><span className="font-medium">Invoice Number:</span> {job.invoice_number}</div>
                      </div>
                    </div>
                  </td>
                </tr>
              )}
            </React.Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );
} 