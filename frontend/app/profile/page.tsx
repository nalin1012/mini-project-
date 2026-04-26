"use client"

import Link from "next/link"
import { useEffect, useState } from "react"
import { Award, BookOpen, Mail, Shield, Loader, Settings, LogOut, Edit2, TrendingUp, Zap } from "lucide-react"
import { DashboardNavbar } from "@/components/dashboard-navbar"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://192.168.0.131:8001"

interface UserProfile {
  id: number
  email: string
  name: string
  role: string
  created_at: string
}

interface UserStats {
  total_quizzes_completed: number
  overall_accuracy: number
  total_questions_attempted: number
  correct_answers: number
  weak_areas: Array<{
    topic: string
    mastery_score: number
  }>
}

export default function ProfilePage() {
  const [user, setUser] = useState<UserProfile | null>(null)
  const [stats, setStats] = useState<UserStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [editMode, setEditMode] = useState(false)

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem("access_token")
        if (!token) {
          window.location.href = "/login"
          return
        }

        // Fetch user profile
        const userRes = await fetch(`${API_BASE_URL}/api/auth/me`, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        })

        if (!userRes.ok) throw new Error("Failed to fetch user data")
        const userData = await userRes.json()
        setUser(userData)

        // Fetch user stats
        const statsRes = await fetch(`${API_BASE_URL}/api/knowledge-gap/dashboard-summary`, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        })

        if (statsRes.ok) {
          const statsData = await statsRes.json()
          setStats(statsData)
        }

        setError(null)
      } catch (err) {
        console.error("Error fetching profile:", err)
        setError(err instanceof Error ? err.message : "Failed to load profile")
      } finally {
        setLoading(false)
      }
    }

    fetchUserData()
  }, [])

  const handleLogout = () => {
    localStorage.removeItem("access_token")
    localStorage.removeItem("user_data")
    window.location.href = "/"
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0B0F1A]">
        <DashboardNavbar />
        <main className="flex items-center justify-center py-40">
          <div className="text-center">
            <Loader className="h-8 w-8 animate-spin text-blue-400 mx-auto mb-4" />
            <p className="text-white">Loading your profile...</p>
          </div>
        </main>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#0B0F1A]">
      <DashboardNavbar />
      <main className="mx-auto flex w-full max-w-5xl flex-col gap-8 px-4 py-10 lg:px-8">
        {error && (
          <Alert className="bg-red-500/10 border-red-500/30">
            <AlertDescription className="text-red-300">{error}</AlertDescription>
          </Alert>
        )}

        {/* Profile Header */}
        <section className="glass rounded-3xl p-8 bg-gradient-to-br from-blue-500/10 to-purple-500/10 border border-white/10">
          <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.3em] text-blue-400/80">
                Learner Profile
              </p>
              <h1 className="mt-3 text-3xl font-semibold text-white md:text-4xl">
                {user?.name || "Loading..."}
              </h1>
              <p className="mt-2 text-sm text-gray-400">
                Role: <span className="text-blue-400 font-semibold capitalize">{user?.role}</span>
              </p>
              <p className="mt-1 text-sm text-gray-500">
                Member since {user?.created_at ? new Date(user.created_at).toLocaleDateString() : "N/A"}
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <Button
                onClick={() => setEditMode(!editMode)}
                className="gap-2 bg-blue-600 text-white hover:bg-blue-700 border-0"
              >
                <Edit2 className="size-4" />
                Edit Profile
              </Button>
              <Link href="/dashboard">
                <Button className="gap-2 bg-purple-600 text-white hover:bg-purple-700 border-0">
                  <TrendingUp className="size-4" />
                  View Dashboard
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* Account Information */}
        <section className="grid gap-6 md:grid-cols-2">
          <div className="glass hover-float rounded-2xl p-6 bg-white/5 border border-white/10">
            <div className="flex items-center gap-3">
              <div className="flex size-10 items-center justify-center rounded-xl bg-blue-500/20 text-blue-400">
                <Mail className="size-5" />
              </div>
              <div>
                <p className="text-sm text-gray-400">Email Address</p>
                <p className="text-base font-semibold text-white">{user?.email || "N/A"}</p>
              </div>
            </div>
          </div>
          <div className="glass hover-float rounded-2xl p-6 bg-white/5 border border-white/10">
            <div className="flex items-center gap-3">
              <div className="flex size-10 items-center justify-center rounded-xl bg-purple-500/20 text-purple-400">
                <Shield className="size-5" />
              </div>
              <div>
                <p className="text-sm text-gray-400">Account Status</p>
                <p className="text-base font-semibold text-green-400">✓ Active</p>
              </div>
            </div>
          </div>
        </section>

        {/* Learning Statistics */}
        {stats && (
          <section className="glass rounded-2xl p-6 bg-gradient-to-r from-green-500/10 to-emerald-500/10 border border-green-500/20">
            <h2 className="text-xl font-semibold text-white mb-6">📊 Learning Statistics</h2>
            <div className="grid gap-4 md:grid-cols-4">
              <div className="rounded-lg bg-black/30 p-4 border border-green-500/20">
                <p className="text-sm text-gray-400 mb-2">Quizzes Completed</p>
                <p className="text-3xl font-bold text-green-400">{stats.total_quizzes_completed}</p>
              </div>
              <div className="rounded-lg bg-black/30 p-4 border border-green-500/20">
                <p className="text-sm text-gray-400 mb-2">Questions Attempted</p>
                <p className="text-3xl font-bold text-blue-400">{stats.total_questions_attempted}</p>
              </div>
              <div className="rounded-lg bg-black/30 p-4 border border-green-500/20">
                <p className="text-sm text-gray-400 mb-2">Correct Answers</p>
                <p className="text-3xl font-bold text-purple-400">{stats.correct_answers}</p>
              </div>
              <div className="rounded-lg bg-black/30 p-4 border border-green-500/20">
                <p className="text-sm text-gray-400 mb-2">Overall Accuracy</p>
                <p className="text-3xl font-bold text-yellow-400">{Math.round(stats.overall_accuracy)}%</p>
              </div>
            </div>
          </section>
        )}

        {/* Achievements & Focus Areas */}
        <section className="grid gap-6 md:grid-cols-2">
          <div className="glass hover-float rounded-2xl p-6 bg-white/5 border border-white/10">
            <div className="flex items-center gap-3 mb-4">
              <div className="flex size-10 items-center justify-center rounded-xl bg-yellow-500/20 text-yellow-400">
                <Award className="size-5" />
              </div>
              <div>
                <p className="text-sm text-gray-400">Achievements</p>
                <p className="text-base font-semibold text-yellow-300">
                  {stats ? Math.min(stats.total_quizzes_completed + 5, 12) : 0} badges unlocked
                </p>
              </div>
            </div>
            <p className="text-xs text-gray-500">Keep taking quizzes to unlock more badges!</p>
          </div>
          <div className="glass hover-float rounded-2xl p-6 bg-white/5 border border-white/10">
            <div className="flex items-center gap-3 mb-4">
              <div className="flex size-10 items-center justify-center rounded-xl bg-cyan-500/20 text-cyan-400">
                <BookOpen className="size-5" />
              </div>
              <div>
                <p className="text-sm text-gray-400">Learning Focus</p>
                <p className="text-base font-semibold text-cyan-300">
                  {stats?.weak_areas.length ? `${stats.weak_areas.length} areas to improve` : "On track!"}
                </p>
              </div>
            </div>
            <p className="text-xs text-gray-500">Focus on weak areas to improve your mastery</p>
          </div>
        </section>

        {/* Weak Areas */}
        {stats && stats.weak_areas.length > 0 && (
          <section className="glass rounded-2xl p-6 bg-gradient-to-r from-orange-500/10 to-red-500/10 border border-orange-500/20">
            <h2 className="text-lg font-semibold text-white mb-4">🎯 Areas for Improvement</h2>
            <div className="grid gap-3 md:grid-cols-2">
              {stats.weak_areas.map((area) => (
                <div key={area.topic} className="rounded-lg bg-black/30 p-4 border border-orange-500/20">
                  <div className="flex items-center justify-between mb-2">
                    <p className="font-semibold text-orange-300">{area.topic}</p>
                    <span className="text-xs bg-orange-500/20 text-orange-300 px-2 py-1 rounded">
                      {Math.round(area.mastery_score * 100)}% mastery
                    </span>
                  </div>
                  <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-orange-500 to-red-500"
                      style={{ width: `${area.mastery_score * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Settings & Actions */}
        <section className="glass rounded-2xl p-6 bg-white/5 border border-white/10">
          <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Settings className="size-5" />
            Account Settings
          </h2>
          <div className="space-y-3">
            <Button variant="outline" className="w-full border-white/15 bg-white/5 text-white hover:bg-white/10 justify-start gap-2">
              <Zap className="size-4" />
              Change Password
            </Button>
            <Button variant="outline" className="w-full border-white/15 bg-white/5 text-white hover:bg-white/10 justify-start gap-2">
              <Shield className="size-4" />
              Privacy Settings
            </Button>
            <Button
              onClick={handleLogout}
              className="w-full bg-red-600 text-white hover:bg-red-700 justify-start gap-2"
            >
              <LogOut className="size-4" />
              Logout
            </Button>
          </div>
        </section>
      </main>
    </div>
  )
}

