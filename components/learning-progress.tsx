import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

const progressData = [
  { concept: "Fractions", progress: 40 },
  { concept: "Algebra", progress: 75 },
  { concept: "Geometry", progress: 60 },
  { concept: "Statistics", progress: 85 },
]

export function LearningProgress() {
  return (
    <Card className="border bg-card shadow-sm">
      <CardHeader>
        <CardTitle className="text-lg font-semibold text-foreground">
          Learning Progress
        </CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-5">
        {progressData.map((item) => (
          <div key={item.concept} className="flex flex-col gap-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-foreground">
                {item.concept}
              </span>
              <span className="text-sm font-semibold text-primary">
                {item.progress}%
              </span>
            </div>
            <Progress value={item.progress} className="h-2.5 rounded-full bg-muted" />
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
