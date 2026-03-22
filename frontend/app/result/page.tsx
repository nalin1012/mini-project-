"use client"

import { useEffect, useState } from "react"
import { DashboardNavbar } from "@/components/dashboard-navbar"

export default function ResultsPage() {
	const [result, setResult] = useState<any>(null)

	useEffect(() => {
		const stored = localStorage.getItem("result") || localStorage.getItem("ml_result")

		if (stored) {
			setResult(JSON.parse(stored))
		}
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

					{!result ? (
						<div className="mt-6 rounded-2xl border border-white/10 bg-white/5 p-6 text-sm text-muted-foreground">
							Loading your results...
						</div>
					) : (
						<div className="mt-6 grid gap-4 md:grid-cols-3">
							<div className="rounded-2xl border border-white/10 bg-white/5 p-4">
								<p className="text-xs uppercase text-muted-foreground">Mastery Score</p>
								<p className="mt-2 text-xl font-semibold text-foreground">
									{result.mastery_score}
								</p>
							</div>
							<div className="rounded-2xl border border-white/10 bg-white/5 p-4">
								<p className="text-xs uppercase text-muted-foreground">Knowledge Gap</p>
								<p className="mt-2 text-xl font-semibold text-foreground">
									{result.knowledge_gap}
								</p>
							</div>
							<div className="rounded-2xl border border-white/10 bg-white/5 p-4">
								<p className="text-xs uppercase text-muted-foreground">Recommendation</p>
								<p className="mt-2 text-sm text-foreground">{result.recommendation}</p>
							</div>
						</div>
					)}
				</section>
			</main>
		</div>
	)
}