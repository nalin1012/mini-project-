import { Award, AlertTriangle, Lightbulb } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"

const summaryData = [
  {
    title: "Mastery Score",
    value: "72%",
    description: "Overall learning progress",
    icon: Award,
    iconBg: "bg-primary/10",
    iconColor: "text-primary",
  },
  {
    title: "Weak Concepts",
    value: "3 Concepts",
    description: "Areas needing improvement",
    icon: AlertTriangle,
    iconBg: "bg-destructive/10",
    iconColor: "text-destructive",
  },
  {
    title: "Next Recommendation",
    value: "Revise Fractions",
    description: "AI-suggested next step",
    icon: Lightbulb,
    iconBg: "bg-chart-4/10",
    iconColor: "text-chart-4",
  },
]

export function SummaryCards() {
  return (
    <section aria-label="Summary statistics">
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {summaryData.map((item) => (
          <Card key={item.title} className="border bg-card shadow-sm">
            <CardContent className="flex items-center gap-4 pt-6">
              <div
                className={`flex size-12 shrink-0 items-center justify-center rounded-xl ${item.iconBg}`}
              >
                <item.icon className={`size-6 ${item.iconColor}`} />
              </div>
              <div className="flex flex-col gap-0.5">
                <p className="text-sm text-muted-foreground">{item.title}</p>
                <p className="text-xl font-bold text-foreground">{item.value}</p>
                <p className="text-xs text-muted-foreground">{item.description}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  )
}
