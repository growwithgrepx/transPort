// ============================================================================
// FLEET MANAGEMENT SYSTEM - TYPE DEFINITIONS
// ============================================================================
// This file contains TypeScript interfaces that correspond to the legacy
// Python SQLAlchemy models from the Flask backend.

// ============================================================================
// BASE TYPES
// ============================================================================

export type EntityStatus = 'Active' | 'Inactive' | 'Pending' | 'Completed' | 'Cancelled';
export type PaymentStatus = 'Pending' | 'Paid' | 'Overdue' | 'Cancelled';
export type PaymentMode = 'Cash' | 'Credit Card' | 'Bank Transfer' | 'Online Payment';
export type DiscountType = 'percentage' | 'fixed';
export type Currency = 'SGD' | 'USD' | 'EUR' | 'GBP';

// ============================================================================
// CORE ENTITY INTERFACES
// ============================================================================

export interface User {
  id: number;
  email: string;
  password: string;
  active: boolean;
  fs_uniquifier: string;
  username?: string;
  confirmed_at?: string; // ISO date string
  roles: Role[];
}

export interface Role {
  id: number;
  name: string;
  description?: string;
  permissions?: string;
  users?: User[];
}

export interface Driver {
  id: number;
  name: string;
  phone: string;
  jobs?: Job[];
}

export interface Agent {
  id: number;
  name: string;
  email: string;
  mobile: string;
  type: string;
  status: EntityStatus;
  agent_discount_percent: number;
  jobs?: Job[];
  discounts?: CustomerDiscount[];
}

export interface Vehicle {
  id: number;
  name: string;
  number: string;
  type: string;
  status: EntityStatus;
}

export interface Service {
  id: number;
  name: string;
  description?: string;
  status: EntityStatus;
  base_price: number;
  jobs?: Job[];
  prices?: Price[];
}

export interface Price {
  id: number;
  service_id: number;
  amount: number;
  currency: Currency;
  service?: Service;
}

// ============================================================================
// JOB MANAGEMENT INTERFACES
// ============================================================================

export interface Job {
  id: number;
  
  // Customer Information
  customer_name: string;
  customer_email: string;
  customer_mobile: string;
  customer_reference: string;
  
  // Passenger Information
  passenger_name: string;
  passenger_email: string;
  passenger_mobile: string;
  
  // Service Information
  type_of_service: string;
  service_id: number;
  service?: Service;
  
  // Trip Details
  pickup_date: string;
  pickup_time: string;
  pickup_location: string;
  dropoff_location: string;
  
  // Vehicle Information
  vehicle_type: string;
  vehicle_number: string;
  
  // Driver Information
  driver_contact: string;
  driver_id: number;
  driver?: Driver;
  
  // Agent Information
  agent_id: number;
  agent?: Agent;
  
  // Payment Information
  payment_mode: PaymentMode;
  payment_status: PaymentStatus;
  
  // Status and Tracking
  order_status: string;
  status: EntityStatus;
  reference: string;
  date: string;
  
  // Additional Information
  message?: string;
  remarks?: string;
  has_additional_stop: boolean;
  additional_stops?: string;
  has_request: boolean;
  
  // Billing Information
  base_price: number;
  base_discount_percent: number;
  agent_discount_percent: number;
  additional_discount_percent: number;
  additional_charges: number;
  final_price: number;
  invoice_number?: string;
  
  // Relationships
  billing?: Billing;
}

// ============================================================================
// BILLING AND PRICING INTERFACES
// ============================================================================

export interface Billing {
  id: number;
  job_id: number;
  job?: Job;
  
  // Invoice Information
  invoice_number: string;
  invoice_date: string; // ISO date string
  due_date?: string; // ISO date string
  
  // Pricing Breakdown
  base_price: number;
  base_discount_amount: number;
  agent_discount_amount: number;
  additional_discount_amount: number;
  additional_charges: number;
  subtotal: number;
  tax_amount: number;
  total_amount: number;
  
  // Payment Information
  payment_status: PaymentStatus;
  payment_date?: string; // ISO date string
  payment_method?: PaymentMode;
  
  // Discount Information
  discount_id?: number;
  discount?: Discount;
  
  // Additional Information
  notes?: string;
  terms_conditions?: string;
}

export interface Discount {
  id: number;
  name: string;
  code?: string;
  percent: number;
  amount: number;
  discount_type: DiscountType;
  is_base_discount: boolean;
  is_active: boolean;
  valid_from?: string; // ISO date string
  valid_to?: string; // ISO date string
  
  // Relationships
  billings?: Billing[];
  customer_discounts?: CustomerDiscount[];
}

export interface CustomerDiscount {
  id: number;
  customer_id: number;
  discount_id: number;
  valid_from?: string; // ISO date string
  valid_to?: string; // ISO date string
  
  // Relationships
  customer?: Agent;
  discount?: Discount;
}

// ============================================================================
// ASSOCIATION TABLES
// ============================================================================

export interface UserRole {
  user_id: number;
  role_id: number;
}

// ============================================================================
// API RESPONSE INTERFACES
// ============================================================================

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}

// ============================================================================
// FORM INTERFACES
// ============================================================================

export interface JobFormData {
  customer_name: string;
  customer_email: string;
  customer_mobile: string;
  customer_reference: string;
  passenger_name: string;
  passenger_email: string;
  passenger_mobile: string;
  type_of_service: string;
  service_id: number;
  pickup_date: string;
  pickup_time: string;
  pickup_location: string;
  dropoff_location: string;
  vehicle_type: string;
  vehicle_number: string;
  driver_contact: string;
  payment_mode: PaymentMode;
  message?: string;
  remarks?: string;
  has_additional_stop: boolean;
  additional_stops?: string;
  has_request: boolean;
  driver_id?: number;
  agent_id?: number;
}

export interface DriverFormData {
  name: string;
  phone: string;
}

export interface AgentFormData {
  name: string;
  email: string;
  mobile: string;
  type: string;
  status: EntityStatus;
  agent_discount_percent: number;
}

export interface VehicleFormData {
  name: string;
  number: string;
  type: string;
  status: EntityStatus;
}

export interface ServiceFormData {
  name: string;
  description?: string;
  status: EntityStatus;
  base_price: number;
}

export interface BillingFormData {
  job_id: number;
  invoice_number: string;
  due_date?: string;
  base_price: number;
  base_discount_amount: number;
  agent_discount_amount: number;
  additional_discount_amount: number;
  additional_charges: number;
  tax_amount: number;
  payment_status: PaymentStatus;
  payment_method?: PaymentMode;
  discount_id?: number;
  notes?: string;
  terms_conditions?: string;
}

export interface DiscountFormData {
  name: string;
  code?: string;
  percent: number;
  amount: number;
  discount_type: DiscountType;
  is_base_discount: boolean;
  is_active: boolean;
  valid_from?: string;
  valid_to?: string;
}

// ============================================================================
// DASHBOARD AND REPORTING INTERFACES
// ============================================================================

export interface DashboardStats {
  total_jobs: number;
  active_jobs: number;
  completed_jobs: number;
  total_revenue: number;
  pending_payments: number;
  total_drivers: number;
  total_vehicles: number;
  total_agents: number;
}

export interface JobStats {
  total: number;
  active: number;
  completed: number;
  cancelled: number;
  pending: number;
}

export interface RevenueStats {
  total_revenue: number;
  monthly_revenue: number;
  pending_revenue: number;
  paid_revenue: number;
}

export interface ChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    backgroundColor?: string[];
    borderColor?: string[];
    borderWidth?: number;
  }[];
}

// ============================================================================
// SEARCH AND FILTER INTERFACES
// ============================================================================

// JobFilters: all possible filter/search parameters for jobs
export type JobFilters = {
  search?: string;
  customer_name?: string;
  customer_email?: string;
  customer_mobile?: string;
  customer_reference?: string;
  passenger_name?: string;
  passenger_email?: string;
  passenger_mobile?: string;
  type_of_service?: string;
  service_id?: number | string;
  pickup_date?: string;
  pickup_time?: string;
  pickup_location?: string;
  dropoff_location?: string;
  vehicle_type?: string;
  vehicle_number?: string;
  driver_contact?: string;
  payment_mode?: string;
  payment_status?: string;
  order_status?: string;
  status?: string;
  reference?: string;
  date?: string;
  driver_id?: number | string;
  agent_id?: number | string;
  invoice_number?: string;
  has_additional_stop?: boolean | string;
  has_request?: boolean | string;
  base_price_min?: number | string;
  base_price_max?: number | string;
  final_price_min?: number | string;
  final_price_max?: number | string;
  // Add more as needed for all column filters
};

export interface SearchParams {
  query?: string;
  page?: number;
  per_page?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface JobSearchParams extends SearchParams, JobFilters {}

// ============================================================================
// NOTIFICATION AND MESSAGING INTERFACES
// ============================================================================

export interface Notification {
  id: number;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  timestamp: string;
  read: boolean;
}

export interface ChatMessage {
  id: number;
  user_id: number;
  message: string;
  timestamp: string;
  type: 'user' | 'system';
} 