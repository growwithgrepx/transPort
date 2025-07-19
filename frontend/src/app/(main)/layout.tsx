"use client";
import React, { useRef } from "react";
import { MainNavigation } from "@/components/organisms/MainNavigation";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

export default function MainLayout({ children }: { children: React.ReactNode }) {
  const queryClientRef = useRef<QueryClient | null>(null);
  if (!queryClientRef.current) {
    queryClientRef.current = new QueryClient();
  }
  return (
    <QueryClientProvider client={queryClientRef.current}>
      <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
        <MainNavigation />
        <main className="flex-1 container mx-auto px-4 py-8">{children}</main>
      </div>
    </QueryClientProvider>
  );
} 