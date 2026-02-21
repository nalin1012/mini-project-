import { DashboardNavbar } from "@/components/dashboard-navbar"
import { SummaryCards } from "@/components/summary-cards"
import { LearningProgress } from "@/components/learning-progress"
import { TutorChat } from "@/components/tutor-chat"
import { RecommendedTopics } from "@/components/recommended-topics"

export default function DashboardPage() {
  return (
    <div className="min-h-svh bg-background">
      <DashboardNavbar />
      <main className="mx-auto max-w-7xl px-4 py-8 lg:px-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold tracking-tight text-foreground">
            Welcome back, Jane
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            {"Here's an overview of your learning journey"}
          </p>
        </div>

        <div className="flex flex-col gap-8">
          <SummaryCards />

          <div className="grid gap-8 lg:grid-cols-2">
            <LearningProgress />
            <TutorChat />
          </div>

          <RecommendedTopics />
        </div>
      </main>
    </div>
  )
}
