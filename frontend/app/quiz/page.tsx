"use client"

import { useEffect, useMemo, useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Clock, Sparkles } from "lucide-react"
import { DashboardNavbar } from "@/components/dashboard-navbar"
import { Button } from "@/components/ui/button"

export default function QuizPage() {
	const router = useRouter()
	const [selected, setSelected] = useState("")
	const [isSubmitting, setIsSubmitting] = useState(false)
	const [submitted, setSubmitted] = useState(false)
	const [result, setResult] = useState<any>(null)
	const [timeLeft, setTimeLeft] = useState(8 * 60)

	const options = useMemo(() => ["1/4", "1/2", "3/4", "1"], [])
	const currentQuestion = 2
	const totalQuestions = 10

	useEffect(() => {
		if (submitted) return
		const id = window.setInterval(() => {
			setTimeLeft((prev) => (prev > 0 ? prev - 1 : 0))
		}, 1000)
		return () => window.clearInterval(id)
	}, [submitted])

	const minutes = String(Math.floor(timeLeft / 60)).padStart(2, "0")
	const seconds = String(timeLeft % 60).padStart(2, "0")

	const submitQuiz = async () => {
		if (!selected) return
		setIsSubmitting(true)

		const res = await fetch("http://127.0.0.1:8000/api/recommendations/analyze", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				concept: "Fractions",
				correct: selected === "3/4" ? 1 : 0,
				total: 1,
				time_spent: 25,
			}),
		})

		const data = await res.json()
		localStorage.setItem("ml_result", JSON.stringify(data))
		localStorage.setItem("result", JSON.stringify(data))
		setResult(data)
		setSubmitted(true)
		setIsSubmitting(false)
	}

	return (
		<div className="min-h-screen">
			<DashboardNavbar />
			<main className="mx-auto flex w-full max-w-4xl flex-col gap-8 px-4 py-12">
				<section className="glass rounded-3xl p-8">
					<div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
						<div>
							<p className="text-xs font-semibold uppercase tracking-[0.3em] text-primary/80">
								Adaptive Quiz
							</p>
							<h1 className="mt-3 text-2xl font-semibold text-foreground md:text-3xl">
								Fractions Mastery Check
							</h1>
							<p className="mt-2 text-sm text-muted-foreground">
								Question {currentQuestion}/{totalQuestions} • Stay focused and keep your pace.
							</p>
						</div>
						<div className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-foreground">
							<Clock className="size-4 text-primary" />
							{minutes}:{seconds}
						</div>
					</div>

					<div className="mt-6 h-2 w-full overflow-hidden rounded-full bg-white/10">
						<div
							className="h-full rounded-full bg-gradient-to-r from-[#7B61FF] to-[#00D1FF]"
							style={{ width: `${(currentQuestion / totalQuestions) * 100}%` }}
						/>
					</div>

					<div className="mt-8 rounded-2xl border border-white/10 bg-white/5 p-6">
						<p className="text-sm text-muted-foreground">Question</p>
						<h2 className="mt-2 text-xl font-semibold text-foreground md:text-2xl">
							What is 1/2 + 1/4?
						</h2>

						<div className="mt-6 grid gap-3 md:grid-cols-2">
							{options.map((option) => {
								const isActive = selected === option
								return (
									<button
										key={option}
										type="button"
										onClick={() => setSelected(option)}
										className={`flex items-center justify-between rounded-2xl border px-4 py-3 text-left text-sm font-medium transition hover-float ${
											isActive
												? "border-primary/80 bg-primary/15 text-primary neon-ring"
												: "border-white/10 bg-white/5 text-foreground hover:border-primary/40"
										}`}
									>
										{option}
										{isActive && <Sparkles className="size-4" />}
									</button>
								)
							})}
						</div>

						<div className="mt-6 flex flex-wrap items-center gap-3">
							<Button
								onClick={submitQuiz}
								disabled={!selected || isSubmitting}
								className="neon-ring bg-primary text-primary-foreground hover:bg-primary/90"
							>
								{isSubmitting ? "Submitting..." : "Submit Answer"}
							</Button>
							<Link href="/dashboard">
								<Button variant="outline" className="border-white/15 bg-white/5 text-foreground">
									Back to Dashboard
								</Button>
							</Link>
						</div>
					</div>
				</section>

				{submitted && result && (
					<section className="glass hover-float rounded-3xl p-8">
						<div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
							<div>
								<h2 className="text-xl font-semibold text-foreground">Result Summary</h2>
								<p className="text-sm text-muted-foreground">
									Instant feedback to power your next session.
								</p>
							</div>
							<span className="rounded-full border border-emerald-400/30 bg-emerald-400/10 px-3 py-1 text-xs font-semibold text-emerald-300">
								Submitted
							</span>
						</div>

						<div className="mt-6 grid gap-4 md:grid-cols-3">
							<div className="rounded-2xl border border-white/10 bg-white/5 p-4">
								<p className="text-xs uppercase text-muted-foreground">Score</p>
								<p className="mt-2 text-2xl font-semibold text-foreground">
									{typeof result?.mastery_score === "number"
										? `${Math.round(result.mastery_score * 100)}%`
										: result?.mastery_score ?? "--"}
								</p>
							</div>
							<div className="rounded-2xl border border-white/10 bg-white/5 p-4">
								<p className="text-xs uppercase text-muted-foreground">Correct / Incorrect</p>
								<p className="mt-2 text-2xl font-semibold text-foreground">
									{selected === "3/4" ? "1 / 0" : "0 / 1"}
								</p>
							</div>
							<div className="rounded-2xl border border-white/10 bg-white/5 p-4">
								<p className="text-xs uppercase text-muted-foreground">Next Improvement</p>
								<p className="mt-2 text-sm text-foreground">
									{result?.recommendation || "Keep practicing fractions to improve speed."}
								</p>
							</div>
						</div>

						<div className="mt-6 flex flex-wrap gap-3">
							<Button
								onClick={() => router.push("/subjects")}
								className="neon-ring bg-primary text-primary-foreground hover:bg-primary/90"
							>
								Continue Learning
							</Button>
							<Button
								variant="outline"
								className="border-white/15 bg-white/5 text-foreground"
								onClick={() => {
									setSelected("")
									setSubmitted(false)
									setResult(null)
									setTimeLeft(8 * 60)
								}}
							>
								Retry Quiz
							</Button>
						</div>
					</section>
				)}
			</main>
		</div>
	)
}