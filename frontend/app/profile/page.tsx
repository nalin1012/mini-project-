"use client"

import Link from "next/link"
import { Award, BookOpen, Mail, Shield } from "lucide-react"
import { DashboardNavbar } from "@/components/dashboard-navbar"
import { Button } from "@/components/ui/button"

export default function ProfilePage() {
  return (
    <div className="min-h-screen">
      <DashboardNavbar />
      <main className="mx-auto flex w-full max-w-5xl flex-col gap-8 px-4 py-10 lg:px-8">
        <section className="glass rounded-3xl p-8">
          <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.3em] text-primary/80">
                Learner Profile
              </p>
              <h1 className="mt-3 text-3xl font-semibold text-foreground">Jane Smith</h1>
              <p className="mt-2 text-sm text-muted-foreground">
                AI-powered progress tracking and personalized goals.
              </p>
            </div>
            <Link href="/dashboard">
              <Button className="neon-ring bg-primary text-primary-foreground hover:bg-primary/90">
                View Dashboard
              </Button>
            </Link>
          </div>
        </section>

        <section className="grid gap-6 md:grid-cols-2">
          <div className="glass hover-float rounded-2xl p-6">
            <div className="flex items-center gap-3">
              <div className="flex size-10 items-center justify-center rounded-xl bg-primary/15 text-primary">
                <Mail className="size-5" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Email</p>
                <p className="text-base font-semibold text-foreground">jane.smith@email.com</p>
              </div>
            </div>
          </div>
          <div className="glass hover-float rounded-2xl p-6">
            <div className="flex items-center gap-3">
              <div className="flex size-10 items-center justify-center rounded-xl bg-primary/15 text-primary">
                <Shield className="size-5" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Plan</p>
                <p className="text-base font-semibold text-foreground">Premium Scholar</p>
              </div>
            </div>
          </div>
        </section>

        <section className="grid gap-6 md:grid-cols-2">
          <div className="glass hover-float rounded-2xl p-6">
            <div className="flex items-center gap-3">
              <div className="flex size-10 items-center justify-center rounded-xl bg-primary/15 text-primary">
                <Award className="size-5" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Achievements</p>
                <p className="text-base font-semibold text-foreground">12 badges unlocked</p>
              </div>
            </div>
          </div>
          <div className="glass hover-float rounded-2xl p-6">
            <div className="flex items-center gap-3">
              <div className="flex size-10 items-center justify-center rounded-xl bg-primary/15 text-primary">
                <BookOpen className="size-5" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Learning Focus</p>
                <p className="text-base font-semibold text-foreground">Math + Programming</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}
