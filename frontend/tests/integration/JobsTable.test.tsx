import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Mock the getJobs function from the API service
jest.mock('@/services/api', () => ({
  getJobs: jest.fn(),
}));

import { getJobs } from '@/services/api';
import { JobsTable } from '@/components/organisms/JobsTable';

function renderWithQueryClient(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>
  );
}

describe('JobsTable', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('shows a loading state initially', async () => {
    (getJobs as jest.Mock).mockReturnValue(new Promise(() => {}));
    renderWithQueryClient(<JobsTable />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('renders a list of jobs on successful API response', async () => {
    (getJobs as jest.Mock).mockResolvedValue({
      items: [
        {
          id: 1,
          customer_name: 'John Doe',
          pickup_location: 'Airport',
          dropoff_location: 'Hotel',
          status: 'Active',
          payment_status: 'Pending',
          date: '2024-01-01',
        },
        {
          id: 2,
          customer_name: 'Jane Smith',
          pickup_location: 'Mall',
          dropoff_location: 'Office',
          status: 'Completed',
          payment_status: 'Paid',
          date: '2024-01-02',
        },
      ],
      total: 2,
      page: 1,
      per_page: 10,
      pages: 1,
    });
    renderWithQueryClient(<JobsTable />);
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
      expect(screen.getByText('Jane Smith')).toBeInTheDocument();
    });
  });

  it('shows an error message if the API call fails', async () => {
    (getJobs as jest.Mock).mockRejectedValue(new Error('API error'));
    renderWithQueryClient(<JobsTable />);
    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });
}); 