"use client"

import { useEffect, useState } from "react"
import { DashboardNavbar } from "@/components/dashboard-navbar"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://192.168.0.131:8001"

export default function ResultsPage() {
	const [result, setResult] = useState<any>(null)
	const [loading, setLoading] = useState(true)

	useEffect(() => {
		const fetchResults = async () => {
			try {
				const token = localStorage.getItem("access_token")
				if (!token) {
					window.location.href = "/login"
					return
				}

				// Try to get stored result first
				const stored = localStorage.getItem("result") || localStorage.getItem("ml_result")
				if (stored) {
					setResult(JSON.parse(stored))
					setLoading(false)
					return
				}

				// Fetch from dashboard summary as fallback
				const response = await fetch(
					`${API_BASE_URL}/api/knowledge-gap/dashboard-summary`,
					{
						headers: {
							Authorization: `Bearer ${token}`,
							"Content-Type": "application/json",
						},
					}
				)

				if (response.ok) {
					const data = await response.json()
					setResult({
						mastery_score: data.overall_accuracy,
						knowledge_gap: data.weak_areas.length,
						recommendation: `You've completed ${data.total_quizzes_completed} quizzes with ${data.correct_answers} correct answers`,
						weak_areas: data.weak_areas,
					})
				}
			} catch (err) {
				console.error("Error fetching results:", err)
			} finally {
				setLoading(false)
			}
		}

		fetchResults()
	}, [])

	return (
		<div className="min-h-screen">
			<DashboardNavbar />
			<main className="mx-auto flex w-full max-w-4xl flex-col gap-8 px-4 py-12">
				<section className="glass rounded-3xl p-8">
					<h1 className="text-2xl font-semibold text-foreground md:text-3xl">Quiz Results</h1>
					<p className="mt-2 text-sm text-muted-foreground">
						Review your AI-powered insights and plan the next session.
					</p>

					{loading || !result ? (
						<div className="mt-6 rounded-2xl border border-white/10 bg-white/5 p-6 text-sm text-muted-foreground">
							{loading ? "Loading your results..." : "No results yet. Take a quiz to get started!"}
						</div>
					) : (
						<div className="mt-6 space-y-6">
							<div className="grid gap-4 md:grid-cols-3">
								<div className="rounded-2xl border border-white/10 bg-white/5 p-4">
									<p className="text-xs uppercase text-muted-foreground">Overall Accuracy</p>
									<p className="mt-2 text-xl font-semibold text-foreground">
										{Math.round(result.mastery_score)}%
									</p>
								</div>
								<div className="rounded-2xl border border-white/10 bg-white/5 p-4">
									<p className="text-xs uppercase text-muted-foreground">Weak Areas</p>
									<p className="mt-2 text-xl font-semibold text-foreground">
										{result.knowledge_gap}
									</p>
								</div>
								<div className="rounded-2xl border border-white/10 bg-white/5 p-4">
									<p className="text-xs uppercase text-muted-foreground">Recommendation</p>
									<p className="mt-2 text-sm text-foreground line-clamp-2">{result.recommendation}</p>
								</div>
							</div>

							{result.weak_areas && result.weak_areas.length > 0 && (
								<div className="rounded-2xl border border-orange-500/30 bg-orange-500/10 p-6">
									<h2 className="text-lg font-semibold text-orange-300 mb-4">Focus Areas</h2>
									<div className="grid gap-3">
										{result.weak_areas.map((area: any, idx: number) => (
											<div key={idx} className="rounded-lg bg-black/30 p-4 border border-orange-500/20">
												<p className="font-semibold text-orange-200">{area.topic}</p>
												<p className="text-sm text-orange-100/70 mt-1">{area.recommendation}</p>
											</div>
										))}
									</div>
								</div>
							)}
						</div>
					)}
				</section>
			</main>
		</div>
	)
}