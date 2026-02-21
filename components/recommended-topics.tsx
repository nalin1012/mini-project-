import { ArrowRight } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

const topicsData = [
  {
    title: "Equivalent Fractions",
    description:
      "Master the concept of equivalent fractions through interactive examples and practice problems.",
    tag: "Fractions",
  },
  {
    title: "Linear Equations",
    description:
      "Learn to solve single-variable linear equations with step-by-step guided walkthroughs.",
    tag: "Algebra",
  },
  {
    title: "Area & Perimeter",
    description:
      "Explore the formulas for calculating area and perimeter of common geometric shapes.",
    tag: "Geometry",
  },
]

export function RecommendedTopics() {
  return (
    <Card className="border bg-card shadow-sm">
      <CardHeader>
        <CardTitle className="text-lg font-semibold text-foreground">
          Recommended Topics
        </CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        {topicsData.map((topic) => (
          <div
            key={topic.title}
            className="flex flex-col gap-3 rounded-xl border bg-background p-4 sm:flex-row sm:items-center sm:justify-between"
          >
            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-semibold text-foreground">
                  {topic.title}
                </h3>
                <span className="rounded-md bg-primary/10 px-2 py-0.5 text-xs font-medium text-primary">
                  {topic.tag}
                </span>
              </div>
              <p className="text-sm leading-relaxed text-muted-foreground">
                {topic.description}
              </p>
            </div>
            <Button
              size="sm"
              className="w-full gap-1.5 rounded-lg sm:w-auto"
            >
              Start Learning
              <ArrowRight className="size-3.5" />
            </Button>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
