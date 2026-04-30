"use client"

import { useState, useEffect } from "react"
import { Search, ChevronLeft, ChevronRight, Loader, AlertCircle } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://mini-project-xpie.onrender.com"

interface User {
  id: number
  name: string
  email: string
  created_at: string
  last_login: string | null
  role: string
  is_active: boolean
}

interface AdminUserTableProps {
  token: string
}

export function AdminUserTable({ token }: AdminUserTableProps) {
  const [users, setUsers] = useState<User[]>([])
  const [search, setSearch] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [currentPage, setCurrentPage] = useState(1)
  const [total, setTotal] = useState(0)
  const itemsPerPage = 10

  useEffect(() => {
    fetchUsers()
  }, [search, currentPage])

  const fetchUsers = async () => {
    setLoading(true)
    setError(null)

    try {
      const skip = (currentPage - 1) * itemsPerPage
      const url = new URL(`${API_BASE_URL}/api/admin/users`)
      url.searchParams.append("skip", skip.toString())
      url.searchParams.append("limit", itemsPerPage.toString())
      if (search) {
        url.searchParams.append("search", search)
      }

      const response = await fetch(url.toString(), {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      })

      if (!response.ok) {
        throw new Error(`Failed to fetch users: ${response.status}`)
      }

      const data = await response.json()
      setUsers(data.users)
      setTotal(data.total)
      setCurrentPage(1) // Reset to first page on search
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load users")
      console.error("Error fetching users:", err)
    } finally {
      setLoading(false)
    }
  }

  const totalPages = Math.ceil(total / itemsPerPage)

  const formatDate = (dateString: string | null) => {
    if (!dateString) return "Never"
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  return (
    <div className="glass rounded-2xl border border-white/10 bg-black/40 overflow-hidden">
      {/* Header */}
      <div className="p-6 border-b border-white/10">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-white">Users</h2>
          <span className="text-sm text-gray-400">{total} total users</span>
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
          <Input
            placeholder="Search by name or email..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-10 h-10 rounded-lg border-white/10 bg-white/5 text-white placeholder-gray-500 focus:border-blue-400"
          />
        </div>
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
          <p className="text-gray-400 text-sm">Loading users...</p>
        </div>
      )}

      {/* Table */}
      {!loading && users.length > 0 && (
        <>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-white/10">
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Name</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Email</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Created</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Last Login</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Status</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr
                    key={user.id}
                    className="border-b border-white/5 hover:bg-white/5 transition-colors"
                  >
                    <td className="px-6 py-4 text-sm text-gray-300">{user.id}</td>
                    <td className="px-6 py-4 text-sm font-medium text-white">{user.name}</td>
                    <td className="px-6 py-4 text-sm text-gray-400">{user.email}</td>
                    <td className="px-6 py-4 text-sm text-gray-400">
                      {formatDate(user.created_at)}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-400">
                      {formatDate(user.last_login)}
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-medium ${
                          user.is_active
                            ? "bg-green-500/20 text-green-400"
                            : "bg-red-500/20 text-red-400"
                        }`}
                      >
                        {user.is_active ? "Active" : "Inactive"}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="px-6 py-4 border-t border-white/10 flex items-center justify-between">
            <span className="text-sm text-gray-400">
              Page {currentPage} of {totalPages}
            </span>
            <div className="flex gap-2">
              <Button
                onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                disabled={currentPage === 1 || loading}
                className="h-8 gap-1 px-3 bg-white/10 hover:bg-white/20 text-white border border-white/10 disabled:opacity-50"
              >
                <ChevronLeft className="h-4 w-4" />
                Previous
              </Button>
              <Button
                onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                disabled={currentPage === totalPages || loading}
                className="h-8 gap-1 px-3 bg-white/10 hover:bg-white/20 text-white border border-white/10 disabled:opacity-50"
              >
                Next
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </>
      )}

      {/* Empty State */}
      {!loading && users.length === 0 && (
        <div className="p-12 text-center">
          <p className="text-gray-400">No users found</p>
        </div>
      )}
    </div>
  )
}
