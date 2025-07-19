"use client";
import React from 'react';
import { Badge } from '@/components/atoms/Badge';
import type { Job } from '@/types/types';

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

export function JobsTable({ jobs }: { jobs: Job[] }) {
  if (!jobs || jobs.length === 0) {
    return <div className="text-center text-gray-400 dark:text-gray-500 py-8">No jobs found.</div>;
  }

  return (
    <div className="overflow-x-auto card shadow mt-6">
      <table className="table">
        <thead>
          <tr>
            <th>Customer</th>
            <th>Pickup</th>
            <th>Dropoff</th>
            <th>Status</th>
            <th>Payment</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map((job: Job) => (
            <tr key={job.id}>
              <td>{job.customer_name}</td>
              <td>{job.pickup_location}</td>
              <td>{job.dropoff_location}</td>
              <td>
                <Badge variant={getStatusVariant(job.status)}>{job.status}</Badge>
              </td>
              <td>
                <Badge variant={getStatusVariant(job.payment_status)}>{job.payment_status}</Badge>
              </td>
              <td>{job.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
} 