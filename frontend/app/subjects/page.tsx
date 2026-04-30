"use client"

import { useRouter } from "next/navigation"
import Link from "next/link"
import { BookOpen, Brain, Calculator, Code2, FlaskConical, Languages } from "lucide-react"
import { DashboardNavbar } from "@/components/dashboard-navbar"
import { Button } from "@/components/ui/button"

const subjects = [
  {
    title: "Math",
    description: "Adaptive drills, smart hints, and mastery checkpoints.",
    icon: Calculator,
    level: "Intermediate",
  },
  {
    title: "Science",
    description: "Interactive experiments with AI-guided discovery.",
    icon: FlaskConical,
    level: "Beginner",
  },
  {
    title: "Programming",
    description: "Project-based learning with real-world challenges.",
    icon: Code2,
    level: "Advanced",
  },
  {
    title: "English",
    description: "Comprehension, writing, and confidence training.",
    icon: Languages,
    level: "Intermediate",
  },
  {
    title: "Aptitude",
    description: "Speed, logic, and pattern recognition boosters.",
    icon: Brain,
    level: "Intermediate",
  },
  {
    title: "Study Skills",
    description: "Memory systems, focus routines, and study hacks.",
    icon: BookOpen,
    level: "Beginner",
  },
]

export default function SubjectsPage() {
  const router = useRouter()

  const handleStartLearning = (subject: string) => {
    router.push(`/learning/${subject.toLowerCase().replace(/\s+/g, '-')}`)
  }

  return (
    <div className="min-h-screen">
      <DashboardNavbar />
      <main className="mx-auto flex w-full max-w-6xl flex-col gap-10 px-4 py-10 lg:px-8">
        <section className="glass rounded-3xl p-8">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.3em] text-primary/80">
                Subjects Studio
              </p>
              <h1 className="mt-3 text-3xl font-semibold text-foreground">Choose your next focus</h1>
              <p className="mt-2 text-sm text-muted-foreground">
                Each subject blends AI tutoring, quizzes, and project missions.
              </p>
            </div>
            <Link href="/quiz">
              <Button className="neon-ring bg-primary text-primary-foreground hover:bg-primary/90">
                Start a Smart Quiz
              </Button>
            </Link>
          </div>
        </section>

        <section className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {subjects.map((subject) => {
            const Icon = subject.icon
            return (
              <div key={subject.title} className="glass hover-float rounded-2xl p-6">
                <div className="flex items-center justify-between">
                  <div className="flex size-12 items-center justify-center rounded-2xl bg-primary/15 text-primary">
                    <Icon className="size-5" />
                  </div>
                  <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-muted-foreground">
                    {subject.level}
                  </span>
                </div>
                <h2 className="mt-4 text-lg font-semibold text-foreground">{subject.title}</h2>
                <p className="mt-2 text-sm text-muted-foreground">{subject.description}</p>
                <div className="mt-6 flex items-center justify-between">
                  <span className="text-xs text-primary/80">AI Curated Path</span>
                  <Button 
                    onClick={() => handleStartLearning(subject.title)}
                    className="neon-ring bg-primary/15 text-primary hover:bg-primary/25"
                  >
                    Start Learning
                  </Button>
                </div>
              </div>
            )
          })}
        </section>
      </main>
    </div>
  )
}
