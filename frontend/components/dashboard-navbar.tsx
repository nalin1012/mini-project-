import Link from "next/link"
import { BookOpen, LogOut } from "lucide-react"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"

export function DashboardNavbar() {
  return (
    <header className="sticky top-0 z-50 border-b bg-card">
      <nav className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 lg:px-8">
        <Link href="/dashboard" className="flex items-center gap-2.5">
          <div className="flex size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <BookOpen className="size-4" />
          </div>
          <span className="text-lg font-bold tracking-tight text-foreground">
            AI Personalized Learning
          </span>
        </Link>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2.5">
            <Avatar className="size-9 border">
              <AvatarFallback className="bg-primary/10 text-sm font-semibold text-primary">
                JS
              </AvatarFallback>
            </Avatar>
            <span className="hidden text-sm font-medium text-foreground sm:inline">
              Jane Smith
            </span>
          </div>
          <Link href="/">
            <Button variant="ghost" size="sm" className="gap-1.5 text-muted-foreground">
              <LogOut className="size-4" />
              <span className="hidden sm:inline">Logout</span>
            </Button>
          </Link>
        </div>
      </nav>
    </header>
  )
}
