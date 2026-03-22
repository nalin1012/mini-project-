"use client"

import { useEffect, useMemo, useState } from "react"
import Link from "next/link"
import {
	BookOpen,
	Brain,
	Calculator,
	Code2,
	FlaskConical,
	Languages,
	Target,
	Trophy,
} from "lucide-react"
import { DashboardNavbar } from "@/components/dashboard-navbar"
import { Button } from "@/components/ui/button"

export default function DashboardPage() {
	const [mlData, setMlData] = useState<any>(null)
	const [user, setUser] = useState("")

	useEffect(() => {
		const stored = localStorage.getItem("ml_result")
		const username = localStorage.getItem("user")

		if (stored) {
			setMlData(JSON.parse(stored))
		}

		if (username) {
			setUser(username)
		}
	}, [])

	const stats = useMemo(
		() => [
			{ label: "Total Subjects", value: "5", icon: BookOpen },
			{ label: "Quizzes Completed", value: "18", icon: Trophy },
			{
				label: "Accuracy",
				value:
					typeof mlData?.mastery_score === "number"
						? `${Math.round(mlData.mastery_score * 100)}%`
						: "86%",
				icon: Target,
			},
			{ label: "Study Streak", value: "7 days", icon: Brain },
		],
		[mlData]
	)

	const subjects = [
		{
			title: "Math",
			description: "Build strong foundations in algebra and reasoning.",
			icon: Calculator,
		},
		{
			title: "Science",
			description: "Explore physics, chemistry, and biology with AI labs.",
			icon: FlaskConical,
		},
		{
			title: "Programming",
			description: "Learn modern coding skills with guided projects.",
			icon: Code2,
		},
		{
			title: "English",
			description: "Boost comprehension, writing, and vocabulary.",
			icon: Languages,
		},
		{
			title: "Aptitude",
			description: "Sharpen logic, speed, and competitive readiness.",
			icon: Brain,
		},
	]

	return (
		<div className="min-h-screen">
			<DashboardNavbar />
			<main className="mx-auto flex w-full max-w-6xl flex-col gap-10 px-4 py-10 lg:px-8">
				<section className="glass hover-float rounded-3xl p-8">
					<div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
						<div>
							<p className="text-sm font-semibold uppercase tracking-[0.2em] text-primary/80">
								AI + Education Fusion
							</p>
							<h1 className="mt-3 text-3xl font-semibold text-foreground md:text-4xl">
								Welcome back,
								<span className="gradient-text"> {user || "Learner"}</span>
							</h1>
							<p className="mt-3 max-w-xl text-sm text-muted-foreground md:text-base">
								Your learning journey is powered by real-time insights and adaptive guidance.
								Keep the streak alive and unlock your next milestone.
							</p>
						</div>
						<div className="flex flex-wrap gap-3">
							<Link href="/quiz">
								<Button className="neon-ring bg-primary text-primary-foreground hover:bg-primary/90">
									Start a Quiz
								</Button>
							</Link>
							<Link href="/subjects">
								<Button variant="outline" className="border-white/15 bg-white/5 text-foreground">
									Explore Subjects
								</Button>
							</Link>
						</div>
					</div>
				</section>

				<section className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
					{stats.map((stat) => {
						const Icon = stat.icon
						return (
							<div key={stat.label} className="glass hover-float rounded-2xl p-6">
								<div className="flex items-center justify-between">
									<span className="text-sm text-muted-foreground">{stat.label}</span>
									<div className="flex size-10 items-center justify-center rounded-xl bg-primary/15 text-primary">
										<Icon className="size-5" />
									</div>
								</div>
								<p className="mt-4 text-2xl font-semibold text-foreground">{stat.value}</p>
							</div>
						)
					})}
				</section>

				{mlData && (
					<section className="glass hover-float rounded-2xl p-6">
						<div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
							<div>
								<h2 className="text-lg font-semibold text-foreground">AI Insight Snapshot</h2>
								<p className="text-sm text-muted-foreground">
									Personalized diagnostics based on your latest quiz.
								</p>
							</div>
							<span className="rounded-full border border-primary/30 bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">
								Updated just now
							</span>
						</div>
						<div className="mt-6 grid gap-4 md:grid-cols-3">
							<div className="rounded-2xl border border-white/10 bg-white/5 p-4">
								<p className="text-xs uppercase text-muted-foreground">Mastery Score</p>
								<p className="mt-2 text-xl font-semibold text-foreground">
									{mlData.mastery_score}
								</p>
							</div>
							<div className="rounded-2xl border border-white/10 bg-white/5 p-4">
								<p className="text-xs uppercase text-muted-foreground">Knowledge Gap</p>
								<p className="mt-2 text-xl font-semibold text-foreground">
									{mlData.knowledge_gap}
								</p>
							</div>
							<div className="rounded-2xl border border-white/10 bg-white/5 p-4">
								<p className="text-xs uppercase text-muted-foreground">Recommendation</p>
								<p className="mt-2 text-sm text-foreground">{mlData.recommendation}</p>
							</div>
						</div>
					</section>
				)}

				<section id="subjects" className="flex flex-col gap-6">
					<div className="flex flex-col gap-2">
						<h2 className="text-2xl font-semibold text-foreground">Subjects</h2>
						<p className="text-sm text-muted-foreground">
							Curated learning paths designed to keep you motivated and on track.
						</p>
					</div>
					<div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
						{subjects.map((subject) => {
							const Icon = subject.icon
							return (
								<div key={subject.title} className="glass hover-float rounded-2xl p-6">
									<div className="flex items-center gap-3">
										<div className="flex size-12 items-center justify-center rounded-2xl bg-primary/15 text-primary">
											<Icon className="size-5" />
										</div>
										<div>
											<h3 className="text-lg font-semibold text-foreground">{subject.title}</h3>
											<p className="text-xs text-muted-foreground">AI-assisted learning</p>
										</div>
									</div>
									<p className="mt-4 text-sm text-muted-foreground">{subject.description}</p>
									<div className="mt-6 flex items-center justify-between">
										<span className="text-xs text-primary/80">New modules weekly</span>
										<Button className="neon-ring bg-primary/15 text-primary hover:bg-primary/25">
											Start Learning
										</Button>
									</div>
								</div>
							)
						})}
					</div>
				</section>
			</main>
		</div>
	)
}
