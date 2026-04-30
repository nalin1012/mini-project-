"use client"

import React, { ReactNode } from "react"
import { AlertCircle, Home, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

interface ErrorBoundaryProps {
  children: ReactNode
  fallback?: ReactNode
}

interface ErrorBoundaryState {
  hasError: boolean
  error?: Error
}

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("Error caught by boundary:", error, errorInfo)
  }

  resetError = () => {
    this.setState({ hasError: false, error: undefined })
  }

  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800 p-4">
            <Card className="w-full max-w-md bg-slate-800 border-red-500/20">
              <CardHeader className="text-center">
                <div className="flex justify-center mb-4">
                  <AlertCircle className="h-12 w-12 text-red-400" />
                </div>
                <CardTitle className="text-white">Oops! Something went wrong</CardTitle>
                <CardDescription className="text-gray-400">
                  The application encountered an unexpected error.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="bg-slate-900/50 border border-red-500/20 rounded p-3">
                  <p className="text-sm text-gray-300">
                    {this.state.error?.message || "Unknown error"}
                  </p>
                </div>
                <div className="flex gap-2">
                  <Button
                    onClick={this.resetError}
                    className="flex-1 bg-blue-600 hover:bg-blue-700"
                  >
                    <RefreshCw className="w-4 h-4 mr-2" />
                    Try Again
                  </Button>
                  <Button
                    onClick={() => (window.location.href = "/")}
                    variant="outline"
                    className="flex-1 border-gray-600 text-gray-300 hover:bg-slate-700"
                  >
                    <Home className="w-4 h-4 mr-2" />
                    Home
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )
      )
    }

    return this.props.children
  }
}

// Functional component version for easier use
export function ErrorBoundaryWrapper({ children }: { children: ReactNode }) {
  return <ErrorBoundary>{children}</ErrorBoundary>
}
