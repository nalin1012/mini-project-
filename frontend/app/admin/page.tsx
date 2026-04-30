"use client"

import { useEffect, useState } from "react"
import { Loader, BarChart3, Users, TrendingUp, LogIn, AlertCircle } from "lucide-react"
import { DashboardNavbar } from "@/components/dashboard-navbar"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://mini-project-xpie.onrender.com"

interface AdminStats {
  total_users: number
  total_quizzes: number
  average_accuracy: number
  total_logins: number
  recent_logins: RecentLogin[]
  users: UserStats[]
  login_stats: LoginStats
}

interface RecentLogin {
  user_id: number
  user_name: string
  user_email: string
  login_time: string
  ip_address: string | null
  login_method: string
}

interface UserStats {
  id: number
  email: string
  name: string
  role: string
  total_quizzes: number
  overall_accuracy: number
  last_login: string | null
}

interface LoginStats {
  total_users: number
  active_today: number
  total_logins: number
  average_logins_per_user: number
}

export default function AdminPage() {
  const [data, setData] = useState<AdminStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        const token = localStorage.getItem("access_token")
        if (!token) {
          window.location.href = "/login"
          return
        }

        const response = await fetch(`${API_BASE_URL}/api/admin/dashboard`, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        })

        if (!response.ok) {
          if (response.status === 403) {
            setError("Access denied. Admin privileges required.")
          } else {
            setError(`Failed to fetch admin data: ${response.status}`)
          }
          return
        }

        const adminData = await response.json()
        setData(adminData)
        setError(null)
      } catch (err) {
        console.error("Error fetching admin data:", err)
        setError(err instanceof Error ? err.message : "Failed to load admin dashboard")
      } finally {
        setLoading(false)
      }
    }

    fetchAdminData()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0B0F1A]">
        <DashboardNavbar />
        <main className="flex items-center justify-center py-40">
          <div className="text-center">
            <Loader className="h-8 w-8 animate-spin text-blue-400 mx-auto mb-4" />
            <p className="text-white">Loading admin dashboard...</p>
          </div>
        </main>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#0B0F1A]">
        <DashboardNavbar />
        <main className="mx-auto max-w-7xl px-4 py-10">
          <Alert className="bg-red-500/10 border-red-500/30">
            <AlertCircle className="h-4 w-4 text-red-500" />
            <AlertDescription className="text-red-300">{error}</AlertDescription>
          </Alert>
        </main>
      </div>
    )
  }

  if (!data) return null

  return (
    <div className="min-h-screen bg-[#0B0F1A]">
      <DashboardNavbar />
      <main className="mx-auto max-w-7xl px-4 py-10 lg:px-8">
        {/* Page Header */}
        <div className="mb-10">
          <h1 className="text-4xl font-bold text-white">Admin Dashboard</h1>
          <p className="mt-2 text-gray-400">Platform analytics and user management</p>
        </div>

        {/* Stats Grid */}
        <div className="grid gap-4 md:grid-cols-4 mb-10">
          <div className="glass rounded-2xl p-6 bg-gradient-to-br from-blue-500/10 to-blue-500/5 border border-blue-500/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400">Total Users</p>
                <p className="text-3xl font-bold text-blue-400 mt-2">{data.total_users}</p>
              </div>
              <Users className="h-8 w-8 text-blue-500/50" />
            </div>
          </div>

          <div className="glass rounded-2xl p-6 bg-gradient-to-br from-purple-500/10 to-purple-500/5 border border-purple-500/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400">Total Quizzes</p>
                <p className="text-3xl font-bold text-purple-400 mt-2">{data.total_quizzes}</p>
              </div>
              <BarChart3 className="h-8 w-8 text-purple-500/50" />
            </div>
          </div>

          <div className="glass rounded-2xl p-6 bg-gradient-to-br from-green-500/10 to-green-500/5 border border-green-500/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400">Avg Accuracy</p>
                <p className="text-3xl font-bold text-green-400 mt-2">{data.average_accuracy}%</p>
              </div>
              <TrendingUp className="h-8 w-8 text-green-500/50" />
            </div>
          </div>

          <div className="glass rounded-2xl p-6 bg-gradient-to-br from-yellow-500/10 to-yellow-500/5 border border-yellow-500/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400">Total Logins</p>
                <p className="text-3xl font-bold text-yellow-400 mt-2">{data.total_logins}</p>
              </div>
              <LogIn className="h-8 w-8 text-yellow-500/50" />
            </div>
          </div>
        </div>

        {/* Login Stats */}
        <div className="glass rounded-2xl p-6 bg-white/5 border border-white/10 mb-10">
          <h2 className="text-xl font-semibold text-white mb-6">📊 Login Statistics</h2>
          <div className="grid gap-4 md:grid-cols-4">
            <div className="rounded-lg bg-black/30 p-4 border border-white/10">
              <p className="text-sm text-gray-400">Registered Users</p>
              <p className="text-2xl font-bold text-blue-400 mt-2">{data.login_stats.total_users}</p>
            </div>
            <div className="rounded-lg bg-black/30 p-4 border border-white/10">
              <p className="text-sm text-gray-400">Active Today</p>
              <p className="text-2xl font-bold text-green-400 mt-2">{data.login_stats.active_today}</p>
            </div>
            <div className="rounded-lg bg-black/30 p-4 border border-white/10">
              <p className="text-sm text-gray-400">Total Logins</p>
              <p className="text-2xl font-bold text-purple-400 mt-2">{data.login_stats.total_logins}</p>
            </div>
            <div className="rounded-lg bg-black/30 p-4 border border-white/10">
              <p className="text-sm text-gray-400">Avg Per User</p>
              <p className="text-2xl font-bold text-yellow-400 mt-2">{data.login_stats.average_logins_per_user}</p>
            </div>
          </div>
        </div>

        {/* Recent Logins */}
        <div className="glass rounded-2xl p-6 bg-white/5 border border-white/10 mb-10">
          <h2 className="text-xl font-semibold text-white mb-6">🔐 Recent Logins</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="border-b border-white/10">
                <tr>
                  <th className="px-4 py-3 text-left text-gray-400 font-semibold">User</th>
                  <th className="px-4 py-3 text-left text-gray-400 font-semibold">Email</th>
                  <th className="px-4 py-3 text-left text-gray-400 font-semibold">Login Time</th>
                  <th className="px-4 py-3 text-left text-gray-400 font-semibold">IP Address</th>
                  <th className="px-4 py-3 text-left text-gray-400 font-semibold">Method</th>
                </tr>
              </thead>
              <tbody>
                {data.recent_logins.map((login) => (
                  <tr key={login.user_id} className="border-b border-white/5 hover:bg-white/5">
                    <td className="px-4 py-3 text-white">{login.user_name}</td>
                    <td className="px-4 py-3 text-gray-400">{login.user_email}</td>
                    <td className="px-4 py-3 text-gray-400">{new Date(login.login_time).toLocaleString()}</td>
                    <td className="px-4 py-3 text-gray-400">{login.ip_address || "N/A"}</td>
                    <td className="px-4 py-3">
                      <span className="px-2 py-1 rounded bg-blue-500/20 text-blue-300 text-xs">
                        {login.login_method}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Users List */}
        <div className="glass rounded-2xl p-6 bg-white/5 border border-white/10">
          <h2 className="text-xl font-semibold text-white mb-6">👥 Users</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="border-b border-white/10">
                <tr>
                  <th className="px-4 py-3 text-left text-gray-400 font-semibold">Name</th>
                  <th className="px-4 py-3 text-left text-gray-400 font-semibold">Email</th>
                  <th className="px-4 py-3 text-left text-gray-400 font-semibold">Role</th>
                  <th className="px-4 py-3 text-left text-gray-400 font-semibold">Quizzes</th>
                  <th className="px-4 py-3 text-left text-gray-400 font-semibold">Accuracy</th>
                  <th className="px-4 py-3 text-left text-gray-400 font-semibold">Last Login</th>
                </tr>
              </thead>
              <tbody>
                {data.users.map((user) => (
                  <tr key={user.id} className="border-b border-white/5 hover:bg-white/5">
                    <td className="px-4 py-3 text-white font-medium">{user.name}</td>
                    <td className="px-4 py-3 text-gray-400">{user.email}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded text-xs font-semibold ${
                        user.role === "admin" ? "bg-red-500/20 text-red-300" :
                        user.role === "teacher" ? "bg-purple-500/20 text-purple-300" :
                        "bg-blue-500/20 text-blue-300"
                      }`}>
                        {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-gray-400">{user.total_quizzes}</td>
                    <td className="px-4 py-3">
                      <span className={`font-semibold ${
                        user.overall_accuracy >= 80 ? "text-green-400" :
                        user.overall_accuracy >= 60 ? "text-yellow-400" :
                        "text-red-400"
                      }`}>
                        {user.overall_accuracy}%
                      </span>
                    </td>
                    <td className="px-4 py-3 text-gray-400">
                      {user.last_login ? new Date(user.last_login).toLocaleDateString() : "Never"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  )
}
