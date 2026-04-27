"use client"

import { useState, useEffect } from "react"
import { LogIn, Loader, AlertCircle } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001"

interface Login {
  id: number
  user_id: number
  user_name: string
  user_email: string
  login_time: string
  ip_address: string | null
  login_method: string
}

interface LoginHistoryProps {
  token: string
  limit?: number
}

export function LoginHistory({ token, limit = 10 }: LoginHistoryProps) {
  const [logins, setLogins] = useState<Login[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchLoginHistory()
  }, [])

  const fetchLoginHistory = async () => {
    setLoading(true)
    setError(null)

    try {
      const url = new URL(`${API_BASE_URL}/api/admin/logins`)
      url.searchParams.append("limit", limit.toString())

      const response = await fetch(url.toString(), {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      })

      if (!response.ok) {
        throw new Error(`Failed to fetch login history: ${response.status}`)
      }

      const data = await response.json()
      setLogins(data.logins)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load login history")
      console.error("Error fetching login history:", err)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    })
  }

  const getLoginMethodIcon = (method: string) => {
    switch (method.toLowerCase()) {
      case "firebase":
        return "🔥"
      case "oauth":
        return "🔐"
      default:
        return "🔑"
    }
  }

  return (
    <div className="glass rounded-2xl border border-white/10 bg-black/40 overflow-hidden">
      {/* Header */}
      <div className="p-6 border-b border-white/10">
        <div className="flex items-center gap-2 mb-2">
          <LogIn className="h-5 w-5 text-blue-400" />
          <h2 className="text-xl font-semibold text-white">Login History</h2>
        </div>
        <p className="text-sm text-gray-400">Recent login activity</p>
      </div>

      {/* Error */}
      {error && (
        <div className="p-6 bg-red-500/10 border-t border-red-500/30">
          <div className="flex items-center gap-2 text-red-400">
            <AlertCircle className="h-4 w-4" />
            <span className="text-sm">{error}</span>
          </div>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="p-12 text-center">
          <Loader className="h-6 w-6 animate-spin text-blue-400 mx-auto mb-2" />
          <p className="text-gray-400 text-sm">Loading login history...</p>
        </div>
      )}

      {/* Timeline */}
      {!loading && logins.length > 0 && (
        <div className="divide-y divide-white/10">
          {logins.map((login, index) => (
            <div
              key={login.id}
              className="p-6 hover:bg-white/5 transition-colors relative"
            >
              {/* Timeline dot */}
              <div className="absolute left-6 top-8 w-3 h-3 rounded-full bg-blue-500 border-2 border-blue-900" />
              <div className="absolute left-[1.25rem] top-12 w-0.5 h-12 bg-blue-500/20" />

              <div className="ml-8">
                {/* User and Time */}
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <h3 className="font-semibold text-white">{login.user_name}</h3>
                    <p className="text-sm text-gray-400">{login.user_email}</p>
                  </div>
                  <span className="text-xs bg-blue-500/20 text-blue-400 px-2 py-1 rounded">
                    {login.login_method}
                  </span>
                </div>

                {/* Date and IP */}
                <div className="flex items-center gap-3 text-sm text-gray-400">
                  <span>{formatDate(login.login_time)}</span>
                  {login.ip_address && (
                    <>
                      <span>•</span>
                      <span className="font-mono">{login.ip_address}</span>
                    </>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && logins.length === 0 && (
        <div className="p-12 text-center">
          <p className="text-gray-400">No login history available</p>
        </div>
      )}
    </div>
  )
}
