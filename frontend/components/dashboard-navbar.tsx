"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { BookOpen, LogOut, Menu } from "lucide-react"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"
import { useEffect, useState } from "react"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://mini-project-xpie.onrender.com"

interface UserData {
  id: number
  email: string
  name: string
  role: string
}

export function DashboardNavbar() {
  const pathname = usePathname()
  const [userData, setUserData] = useState<UserData | null>(null)
  const [userName, setUserName] = useState("User")
  const [isAdmin, setIsAdmin] = useState(false)
  
  const links = [
    { label: "Dashboard", href: "/dashboard" },
    { label: "Subjects", href: "/subjects" },
    { label: "Quiz", href: "/quiz" },
    { label: "Progress", href: "/result" },
    { label: "Profile", href: "/profile" },
  ]
  
  const adminLinks = isAdmin ? [{ label: "Admin", href: "/admin" }] : []
  const allLinks = [...links, ...adminLinks]

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem("access_token")
        if (!token) return

        const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        })

        if (response.ok) {
          const data = await response.json()
          setUserData(data)
          setUserName(data.name || "User")
          setIsAdmin(data.role === "admin")
        }
      } catch (err) {
        console.error("Error fetching user data:", err)
        setUserName("User")
      }
    }

    fetchUserData()
  }, [])

  const handleLogout = () => {
    localStorage.removeItem("access_token")
    localStorage.removeItem("user_data")
    window.location.href = "/"
  }

  const userInitials = userName
    .split(" ")
    .map(n => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2)

  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-card/40 backdrop-blur-xl">
      <nav className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 lg:px-8">
        <Link href="/dashboard" className="flex items-center gap-2.5">
          <div className="flex size-9 items-center justify-center rounded-lg bg-primary/20 text-primary neon-ring">
            <BookOpen className="size-4" />
          </div>
          <span className="text-lg font-semibold tracking-tight text-foreground">
            <span className="gradient-text">AI Learning</span> Hub
          </span>
        </Link>

        <div className="hidden items-center gap-6 lg:flex">
          {links.map((link) => {
            const isActive = pathname === link.href
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`text-sm font-medium transition ${
                  isActive
                    ? "text-primary after:mt-1 after:block after:h-0.5 after:w-full after:rounded-full after:bg-primary after:shadow-[0_0_12px_rgba(0,209,255,0.8)]"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                {link.label}
              </Link>
            )
          })}
        </div>

        <div className="flex items-center gap-3">
          <Sheet>
            <SheetTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                className="neon-ring bg-white/5 text-foreground lg:hidden"
              >
                <Menu className="size-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="glass border-white/10">
              <SheetHeader>
                <SheetTitle className="text-lg">
                  <span className="gradient-text">AI Learning</span> Hub
                </SheetTitle>
                <SheetDescription>
                  Jump back into your personalized study journey.
                </SheetDescription>
              </SheetHeader>
              <div className="flex flex-col gap-2 px-4">
                {links.map((link) => {
                  const isActive = pathname === link.href
                  return (
                    <Link
                      key={link.href}
                      href={link.href}
                      className={`rounded-xl px-4 py-3 text-sm font-medium transition ${
                        isActive
                          ? "bg-primary/15 text-primary neon-ring"
                          : "bg-white/5 text-foreground hover:bg-primary/10"
                      }`}
                    >
                      {link.label}
                    </Link>
                  )
                })}
              </div>
            </SheetContent>
          </Sheet>
          <div className="flex items-center gap-2.5">
            <Avatar className="size-9 border border-white/10 bg-card/60">
              <AvatarFallback className="bg-primary/10 text-sm font-semibold text-primary">
                {userInitials}
              </AvatarFallback>
            </Avatar>
            <span className="hidden text-sm font-medium text-foreground sm:inline">
              {userName}
            </span>
          </div>
          <Button
            onClick={handleLogout}
            variant="ghost"
            size="sm"
            className="gap-1.5 text-muted-foreground hover:text-foreground"
          >
            <LogOut className="size-4" />
            <span className="hidden sm:inline">Logout</span>
          </Button>
        </div>
      </nav>
    </header>
  )
}
