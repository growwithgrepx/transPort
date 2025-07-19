// // ============================================================================
// // API SERVICE USAGE EXAMPLES
// // ============================================================================
// // This file demonstrates how to use the API service functions
// // with TanStack Query, React hooks, and other patterns.

// import {
//   getJobs,
//   getJobById,
//   createJob,
//   updateJob,
//   deleteJob,
//   getDashboardStats,
//   calculatePricing,
//   sendChatMessage,
// } from './api';
// import type { JobFormData, JobSearchParams } from '@/types/types';

// // ============================================================================
// // EXAMPLE 1: Basic API Calls
// // ============================================================================

// // Get all jobs
// async function fetchAllJobs() {
//   try {
//     const response = await getJobs();
//     console.log('Jobs:', response.items);
//     console.log('Total:', response.total);
//     console.log('Pages:', response.pages);
//   } catch (error) {
//     console.error('Error fetching jobs:', error);
//   }
// }

// // Get jobs with filters
// async function fetchFilteredJobs() {
//   try {
//     const params: JobSearchParams = {
//       status: 'Active',
//       payment_status: 'Pending',
//       page: 1,
//       per_page: 20,
//       sort_by: 'date',
//       sort_order: 'desc',
//     };
    
//     const response = await getJobs(params);
//     console.log('Filtered jobs:', response.items);
//   } catch (error) {
//     console.error('Error fetching filtered jobs:', error);
//   }
// }

// // Get a single job
// async function fetchJobDetails(jobId: number) {
//   try {
//     const job = await getJobById(jobId);
//     console.log('Job details:', job);
//   } catch (error) {
//     console.error('Error fetching job:', error);
//   }
// }

// // Create a new job
// async function createNewJob() {
//   try {
//     const jobData: JobFormData = {
//       customer_name: 'John Doe',
//       customer_email: 'john@example.com',
//       customer_mobile: '+1234567890',
//       customer_reference: 'REF001',
//       passenger_name: 'Jane Doe',
//       passenger_email: 'jane@example.com',
//       passenger_mobile: '+1234567891',
//       type_of_service: 'Airport Transfer',
//       service_id: 1,
//       pickup_date: '2024-01-15',
//       pickup_time: '14:00',
//       pickup_location: 'Airport Terminal 1',
//       dropoff_location: 'Downtown Hotel',
//       vehicle_type: 'Sedan',
//       vehicle_number: 'ABC123',
//       driver_contact: '+1234567892',
//       payment_mode: 'Credit Card',
//       has_additional_stop: false,
//       has_request: false,
//     };
    
//     const response = await createJob(jobData);
//     console.log('Job created:', response.data);
//   } catch (error) {
//     console.error('Error creating job:', error);
//   }
// }

// // ============================================================================
// // EXAMPLE 2: TanStack Query Integration
// // ============================================================================

// // Note: These would typically be in custom hooks
// // import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// /*
// // Jobs query hook
// export function useJobs(params?: JobSearchParams) {
//   return useQuery({
//     queryKey: ['jobs', params],
//     queryFn: () => getJobs(params),
//     staleTime: 5 * 60 * 1000, // 5 minutes
//   });
// }

// // Single job query hook
// export function useJob(id: number) {
//   return useQuery({
//     queryKey: ['job', id],
//     queryFn: () => getJobById(id),
//     enabled: !!id,
//   });
// }

// // Create job mutation hook
// export function useCreateJob() {
//   const queryClient = useQueryClient();
  
//   return useMutation({
//     mutationFn: createJob,
//     onSuccess: () => {
//       // Invalidate and refetch jobs
//       queryClient.invalidateQueries({ queryKey: ['jobs'] });
//     },
//   });
// }

// // Update job mutation hook
// export function useUpdateJob() {
//   const queryClient = useQueryClient();
  
//   return useMutation({
//     mutationFn: ({ id, data }: { id: number; data: Partial<JobFormData> }) =>
//       updateJob(id, data),
//     onSuccess: (_, { id }) => {
//       // Invalidate specific job and jobs list
//       queryClient.invalidateQueries({ queryKey: ['job', id] });
//       queryClient.invalidateQueries({ queryKey: ['jobs'] });
//     },
//   });
// }

// // Delete job mutation hook
// export function useDeleteJob() {
//   const queryClient = useQueryClient();
  
//   return useMutation({
//     mutationFn: deleteJob,
//     onSuccess: () => {
//       // Invalidate jobs list
//       queryClient.invalidateQueries({ queryKey: ['jobs'] });
//     },
//   });
// }
// */

// // ============================================================================
// // EXAMPLE 3: Dashboard Data Fetching
// // ============================================================================

// async function fetchDashboardData() {
//   try {
//     // Fetch all dashboard data in parallel
//     const [stats] = await Promise.all([
//       getDashboardStats(),
//     ]);
    
//     console.log('Dashboard stats:', stats);
//   } catch (error) {
//     console.error('Error fetching dashboard data:', error);
//   }
// }

// // ============================================================================
// // EXAMPLE 4: Pricing Calculation
// // ============================================================================

// async function calculateJobPricing() {
//   try {
//     const pricingData = {
//       service_id: 1,
//       agent_id: 2,
//       base_price: 100.0,
//     };
    
//     const pricing = await calculatePricing(pricingData);
//     console.log('Calculated pricing:', pricing.data);
//   } catch (error) {
//     console.error('Error calculating pricing:', error);
//   }
// }

// // ============================================================================
// // EXAMPLE 5: Chat Integration
// // ============================================================================

// async function sendChatQuery() {
//   try {
//     const response = await sendChatMessage('Show me all active jobs');
//     console.log('Chat response:', response.data?.response);
//     console.log('Suggestions:', response.data?.suggestions);
//   } catch (error) {
//     console.error('Error sending chat message:', error);
//   }
// }

// // ============================================================================
// // EXAMPLE 6: Error Handling Pattern
// // ============================================================================

// async function robustDataFetching() {
//   try {
//     // Attempt to fetch data with retry logic
//     const jobs = await getJobs();
//     return jobs;
//   } catch (error) {
//     if (error instanceof Error) {
//       // Handle specific error types
//       if (error.message.includes('401')) {
//         console.error('Authentication required');
//         // Redirect to login
//       } else if (error.message.includes('404')) {
//         console.error('Resource not found');
//         // Show not found message
//       } else if (error.message.includes('500')) {
//         console.error('Server error');
//         // Show server error message
//       } else {
//         console.error('Unexpected error:', error.message);
//         // Show generic error message
//       }
//     }
//     throw error; // Re-throw for component error boundaries
//   }
// }

// // ============================================================================
// // EXAMPLE 7: Form Submission Pattern
// // ============================================================================

// async function handleJobFormSubmission(formData: JobFormData) {
//   try {
//     // Validate form data
//     if (!formData.customer_name || !formData.pickup_location) {
//       throw new Error('Required fields missing');
//     }
    
//     // Create job
//     const response = await createJob(formData);
    
//     if (response.success) {
//       console.log('Job created successfully:', response.data);
//       // Show success message
//       // Redirect to job details
//     } else {
//       console.error('Failed to create job:', response.message);
//       // Show error message
//     }
//   } catch (error) {
//     console.error('Error submitting job form:', error);
//     // Show error message to user
//   }
// }

// // ============================================================================
// // EXPORT EXAMPLES FOR REFERENCE
// // ============================================================================

// export {
//   fetchAllJobs,
//   fetchFilteredJobs,
//   fetchJobDetails,
//   createNewJob,
//   fetchDashboardData,
//   calculateJobPricing,
//   sendChatQuery,
//   robustDataFetching,
//   handleJobFormSubmission,
// }; 