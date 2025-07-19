"use client";
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import type { Job, JobFilters } from '@/types/types';
import { getJobs, deleteJob } from '@/services/api';

export function useJobs() {
  const [filters, setFilters] = useState<JobFilters>({});
  const queryClient = useQueryClient();

  // Fetch jobs with filters
  const jobsQuery = useQuery<Job[], Error>({
    queryKey: ['jobs', filters],
    queryFn: () => getJobs(filters),
  });

  // Delete job mutation
  const deleteJobMutation = useMutation<void, Error, number>({
    mutationFn: (id: number) => deleteJob(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
    },
  });

  return {
    jobsQuery, // { data, isLoading, isError, ... }
    jobs: jobsQuery.data ?? [],
    filters,
    setFilters,
    deleteJobMutation,
  };
} 