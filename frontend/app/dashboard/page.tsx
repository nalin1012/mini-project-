"use client"

import { useEffect, useMemo, useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import {
	BookOpen,
	Brain,
	Calculator,
	Code2,
	FlaskConical,
	Languages,
	Target,
	Trophy,
	AlertCircle,
	Loader,
	ArrowRight,
	Zap,
} from "lucide-react"
import { DashboardNavbar } from "@/components/dashboard-navbar"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { TutorChat } from "@/components/tutor-chat"

interface DashboardData {
	user_name: string
	total_quizzes_completed: number
	total_questions_attempted: number
	correct_answers: number
	overall_accuracy: number
	points: number
	streak: number
	weak_areas: Array<{
		topic: string
		mastery_score: number
		recommendation: string
		suggested_resources: string
	}>
	study_topics: string[]
}

interface ProgressItem {
	topic: string
	subject_id: number
	mastery_score: number
	sessions_completed: number
	total_questions: number
	correct_answers: number
	status: string
	last_updated: string
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://192.168.0.131:8001"

// Fallback API URL for local development if primary fails
const FALLBACK_API_URL = "http://localhost:8001"

export default function DashboardPage() {
	const router = useRouter()
	const [dashboardData, setDashboardData] = useState<DashboardData | null>(null)
	const [allProgress, setAllProgress] = useState<ProgressItem[]>([])
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState<string | null>(null)

	useEffect(() => {
		const fetchDashboardData = async () => {
			try {
				const token = localStorage.getItem("access_token")
				if (!token) {
					window.location.href = "/login"
					return
				}

				// Fetch dashboard summary
				const response = await fetch(
					`${API_BASE_URL}/api/knowledge-gap/dashboard-summary`,
					{
						headers: {
							Authorization: `Bearer ${token}`,
							"Content-Type": "application/json",
						},
					}
				)

				if (response.status === 401) {
					localStorage.removeItem("access_token")
					window.location.href = "/login"
					return
				}

				if (!response.ok) {
					const errorData = await response.json().catch(() => ({}))
					throw new Error(errorData.detail || "Failed to fetch dashboard data")
				}

				const data = await response.json()
				setDashboardData(data)
				setError(null)

				// Fetch all progress with timeout
				try {
					const controller = new AbortController()
					const timeoutId = setTimeout(() => controller.abort(), 8000) // 8 second timeout

					const progressRes = await fetch(
						`${API_BASE_URL}/api/knowledge-gap/progress/all`,
						{
							headers: {
								Authorization: `Bearer ${token}`,
								"Content-Type": "application/json",
							},
							signal: controller.signal,
						}
					)

					clearTimeout(timeoutId)

					if (progressRes.ok) {
						const progressData = await progressRes.json()
						if (progressData && Array.isArray(progressData) && progressData.length > 0) {
							setAllProgress(progressData)
						} else {
							// No data yet - show empty progress
							setAllProgress([])
						}
					} else {
						console.error("Failed to fetch progress:", progressRes.status)
						// Continue with empty progress
						setAllProgress([])
					}
				} catch (progressErr: any) {
					if (progressErr.name === 'AbortError') {
						console.error("Progress fetch timeout")
						setError("Some data took too long to load, but your dashboard is ready.")
					} else {
						console.error("Error fetching progress:", progressErr)
					}
					// Don't block the dashboard from loading
					setAllProgress([])
				}
			} catch (err) {
				console.error("Error fetching dashboard:", err)
				const errorMessage = err instanceof Error ? err.message : "Failed to load dashboard data"
				setError(`${errorMessage}. Make sure the backend is running at ${API_BASE_URL}`)
			} finally {
				setLoading(false)
			}
		}

		fetchDashboardData()
	}, [])

	const stats = useMemo(() => {
		if (!dashboardData) {
			return [
				{ label: "Points", value: "0", icon: Trophy },
				{ label: "Study Streak", value: "0 🔥", icon: Brain },
				{ label: "Quizzes Completed", value: "0", icon: Trophy },
				{ label: "Accuracy", value: "0%", icon: Target },
			]
		}

		return [
			{ label: "Points", value: dashboardData.points.toString(), icon: Trophy },
			{
				label: "Study Streak",
				value: `${dashboardData.streak} 🔥`,
				icon: Brain,
			},
			{
				label: "Quizzes Completed",
				value: dashboardData.total_quizzes_completed.toString(),
				icon: Trophy,
			},
			{
				label: "Accuracy",
				value: `${Math.round(dashboardData.overall_accuracy)}%`,
				icon: Target,
			},
		]
	}, [dashboardData])

	const subjects = [
		{
			title: "Math",
			description: "Build strong foundations in algebra and reasoning.",
			icon: Calculator,
			topic: "Math",
		},
		{
			title: "Science",
			description: "Explore physics, chemistry, and biology.",
			icon: FlaskConical,
			topic: "Science",
		},
		{
			title: "Programming",
			description: "Learn modern coding skills with guided projects.",
			icon: Code2,
			topic: "Programming",
		},
		{
			title: "English",
			description: "Boost comprehension, writing, and vocabulary.",
			icon: Languages,
			topic: "English",
		},
		{
			title: "Aptitude",
			description: "Sharpen logic, speed, and competitive readiness.",
			icon: Brain,
			topic: "Aptitude",
		},
	]

	const getSubjectProgress = (subjectName: string) => {
		if (!Array.isArray(allProgress) || allProgress.length === 0) {
			return undefined
		}
		return allProgress.find(
			p => p.topic.toLowerCase().includes(subjectName.toLowerCase()) ||
				 subjectName.toLowerCase().includes(p.topic.toLowerCase())
		)
	}

	const startLearning = (subjectName: string) => {
		const slug = subjectName.toLowerCase().replace(/\s+/g, '-')
		router.push(`/learning/${slug}`)
	}

	return (
		<div className="min-h-screen bg-[#0B0F1A]">
			<DashboardNavbar />
			<main className="mx-auto flex w-full max-w-6xl flex-col gap-10 px-4 py-10 lg:px-8">
				{/* Welcome Section */}
				<section className="glass hover-float rounded-3xl p-8 bg-gradient-to-br from-blue-500/10 to-purple-500/10 border border-white/10">
					<div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
						<div>
							<p className="text-sm font-semibold uppercase tracking-[0.2em] text-blue-400/80">
								AI + Education Fusion
							</p>
							<h1 className="mt-3 text-3xl font-semibold text-white md:text-4xl">
								Welcome back,
								<span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent ml-2">
									{" "}
									{dashboardData?.user_name || "Learner"}
								</span>
							</h1>
							<p className="mt-3 max-w-xl text-sm text-gray-400 md:text-base">
								Your learning journey is powered by real-time insights and adaptive guidance.
								Keep the streak alive and unlock your next milestone.
							</p>
						</div>
						<div className="flex flex-wrap gap-3">
							<Link href="/quiz">
								<Button className="bg-blue-600 text-white hover:bg-blue-700 border-0">
									Start a Quiz
								</Button>
							</Link>
							<Link href="/subjects">
								<Button
									variant="outline"
									className="border-white/15 bg-white/5 text-white hover:bg-white/10"
								>
									Explore Topics
								</Button>
							</Link>
						</div>
					</div>
				</section>

				{/* Error Alert */}
				{error && (
					<Alert className="bg-red-500/10 border-red-500/30">
						<AlertCircle className="h-4 w-4 text-red-400" />
						<AlertDescription className="text-red-300">{error}</AlertDescription>
					</Alert>
				)}

				{/* Loading State */}
				{loading && (
					<div className="flex items-center justify-center py-20">
						<Loader className="h-8 w-8 animate-spin text-blue-400" />
					</div>
				)}

				{/* Stats Cards */}
				{!loading && (
					<>
						<section className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
							{stats.map((stat) => {
								const Icon = stat.icon
								return (
									<div
										key={stat.label}
										className="glass hover-float rounded-2xl p-6 bg-white/5 border border-white/10 hover:border-blue-400/30 transition-all"
									>
										<div className="flex items-center justify-between">
											<span className="text-sm text-gray-400">{stat.label}</span>
											<div className="flex size-10 items-center justify-center rounded-xl bg-blue-500/15 text-blue-400">
												<Icon className="size-5" />
											</div>
										</div>
										<p className="mt-4 text-2xl font-semibold text-white">{stat.value}</p>
									</div>
								)
							})}
						</section>

						{/* Continue Learning Section - Only show if user has progress */}
				{!loading && Array.isArray(allProgress) && allProgress.length > 0 && (
					<section className="glass rounded-2xl p-6 bg-gradient-to-r from-green-500/10 to-emerald-500/10 border border-green-500/20">
						<div className="flex items-center justify-between mb-4">
							<div className="flex items-center gap-2">
								<Zap className="h-5 w-5 text-green-400" />
								<h2 className="text-lg font-semibold text-white">Continue Learning</h2>
							</div>
							<Link href="/subjects">
								<Button variant="outline" className="border-green-500/30 text-green-400 hover:bg-green-500/10">
									View All
								</Button>
							</Link>
						</div>
						<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
							{allProgress.filter(item => item.mastery_score > 0 || item.status === "In Progress").slice(0, 3).map((item) => {
										const itemMasteryPercentage = Math.round(item.mastery_score * 100)
										const progressBarColor = itemMasteryPercentage >= 80 ? 'bg-green-500' : itemMasteryPercentage >= 60 ? 'bg-yellow-500' : 'bg-red-500'
										return (
											<div
												key={item.topic}
												className="rounded-lg bg-black/30 p-4 border border-green-500/20 hover:border-green-400/40 transition-all cursor-pointer"
												onClick={() => startLearning(item.topic)}
											>
												<div className="flex items-center justify-between mb-3">
													<p className="font-semibold text-green-300">{item.topic}</p>
													<span className="text-xs bg-green-500/20 text-green-300 px-2 py-1 rounded">
														{itemMasteryPercentage}%
													</span>
												</div>
												<div className="w-full bg-muted rounded-full h-2 mb-2">
													<div 
														className={`h-full rounded-full transition-all ${progressBarColor}`}
														style={{ width: `${itemMasteryPercentage}%` }}
													/>
												</div>
												<p className="text-xs text-gray-400">{item.sessions_completed} sessions • {item.total_questions} questions</p>
											</div>
										)
									})}
								</div>
							</section>
						)}

						{/* New User Getting Started Section */}
						{!loading && Array.isArray(allProgress) && allProgress.length === 0 && (
							<section className="glass rounded-2xl p-8 bg-gradient-to-r from-blue-500/10 to-cyan-500/10 border border-blue-500/20">
								<div className="flex flex-col gap-4">
									<div className="flex items-center gap-2">
										<BookOpen className="h-6 w-6 text-blue-400" />
										<h2 className="text-lg font-semibold text-white">Welcome to Your Learning Journey!</h2>
									</div>
									<p className="text-gray-300">
										You haven't started any quizzes yet. Start learning today to build your mastery and track your progress!
									</p>
									<div className="flex flex-wrap gap-3">
										<Link href="/quiz">
											<Button className="bg-blue-600 text-white hover:bg-blue-700">
												Take Your First Quiz
											</Button>
										</Link>
										<Link href="/subjects">
											<Button variant="outline" className="border-blue-500/30 text-blue-400 hover:bg-blue-500/10">
												Explore All Subjects
											</Button>
										</Link>
									</div>
								</div>
							</section>
						)}

						{/* Weak Areas Alert */}
						{dashboardData && dashboardData.weak_areas.length > 0 && (
							<section className="glass rounded-2xl p-6 bg-gradient-to-r from-red-500/10 to-orange-500/10 border border-red-500/20">
								<div className="flex flex-col gap-4">
									<div className="flex items-center gap-2">
										<AlertCircle className="h-5 w-5 text-orange-400" />
										<h2 className="text-lg font-semibold text-white">Focus Areas</h2>
									</div>
									<div className="grid gap-3 md:grid-cols-2">
										{dashboardData.weak_areas.map((area) => (
											<div
												key={area.topic}
												className="rounded-lg bg-black/30 p-4 border border-orange-500/20 hover:border-orange-400/40 transition-all cursor-pointer"
												onClick={() => startLearning(area.topic)}
											>
												<div className="flex items-center justify-between mb-2">
													<p className="font-semibold text-orange-300">{area.topic}</p>
													<span className="text-xs bg-orange-500/20 text-orange-300 px-2 py-1 rounded">
														{Math.round(area.mastery_score * 100)}% mastery
													</span>
												</div>
												<p className="text-sm text-gray-400 mb-3">{area.recommendation}</p>
												<Button
													onClick={(e) => {
														e.stopPropagation()
														startLearning(area.topic)
													}}
													className="w-full bg-orange-600 text-white hover:bg-orange-700 text-xs"
												>
													Focus on This Area
												</Button>
											</div>
										))}
									</div>
								</div>
							</section>
						)}

						{/* Subjects Section */}
						<section id="subjects" className="flex flex-col gap-6">
							<div className="flex flex-col gap-2">
								<h2 className="text-2xl font-semibold text-white">All Subjects</h2>
								<p className="text-sm text-gray-400">
									Curated learning paths designed to keep you motivated and on track.
								</p>
							</div>
							<div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
								{subjects.map((subject) => {
									const Icon = subject.icon
									const progress = getSubjectProgress(subject.title)
									const masteryPercentage = progress ? Math.round(progress.mastery_score * 100) : 0
									return (
										<div
											key={subject.title}
											className="glass hover-float rounded-2xl p-6 bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10 hover:border-blue-400/30 transition-all"
										>
											<div className="flex items-center justify-between mb-3">
												<div className="flex items-center gap-3">
													<div className="flex size-12 items-center justify-center rounded-2xl bg-blue-500/15 text-blue-400">
														<Icon className="size-5" />
													</div>
													<div>
														<h3 className="text-lg font-semibold text-white">{subject.title}</h3>
														<p className="text-xs text-gray-500">AI-assisted learning</p>
													</div>
												</div>
												{progress && (
													<span className="text-sm font-bold text-blue-400">{masteryPercentage}%</span>
												)}
											</div>
											<p className="text-sm text-gray-400 mb-4">{subject.description}</p>
											{progress && (
												<div className="mb-4">
													<div className="w-full bg-muted rounded-full h-2">
														<div 
															className={`h-full rounded-full transition-all ${masteryPercentage >= 80 ? 'bg-green-500' : masteryPercentage >= 60 ? 'bg-yellow-500' : 'bg-red-500'}`}
															style={{ width: `${masteryPercentage}%` }}
														/>
													</div>
													<p className="text-xs text-gray-500 mt-2">{progress.sessions_completed} sessions • {progress.total_questions} questions</p>
												</div>
											)}
											<div className="flex items-center justify-between gap-2">
												<span className="text-xs text-blue-400/80">New modules weekly</span>
												<Button
													onClick={() => startLearning(subject.title)}
													className="bg-blue-600 text-white hover:bg-blue-700 text-xs flex items-center gap-1"
												>
													Learn <ArrowRight className="size-3" />
												</Button>
											</div>
										</div>
									)
								})}
							</div>
						</section>

						{/* Progress Stats */}
						{dashboardData && (
							<section className="glass rounded-2xl p-6 bg-white/5 border border-white/10">
								<h2 className="text-lg font-semibold text-white mb-6">Your Progress</h2>
								<div className="grid gap-4 md:grid-cols-3">
									<div className="rounded-lg bg-black/30 p-4 border border-white/10">
										<p className="text-xs uppercase text-gray-500 mb-2">Total Questions</p>
										<p className="text-2xl font-bold text-blue-400">
											{dashboardData.total_questions_attempted}
										</p>
									</div>
									<div className="rounded-lg bg-black/30 p-4 border border-white/10">
										<p className="text-xs uppercase text-gray-500 mb-2">Correct Answers</p>
										<p className="text-2xl font-bold text-green-400">
											{dashboardData.correct_answers}
										</p>
									</div>
									<div className="rounded-lg bg-black/30 p-4 border border-white/10">
										<p className="text-xs uppercase text-gray-500 mb-2">Overall Accuracy</p>
										<p className="text-2xl font-bold text-purple-400">
											{Math.round(dashboardData.overall_accuracy)}%
										</p>
									</div>
								</div>
							</section>
						)}

						{/* AI Tutor Chat */}
						{!loading && (
							<section className="mt-8">
								<div className="mb-6">
									<h2 className="text-2xl font-semibold text-white">Need Help? Ask TutorVoice 🤖</h2>
									<p className="mt-2 text-sm text-gray-400">
										Get instant explanations and examples for any topic
									</p>
								</div>
								<TutorChat />
							</section>
						)}
					</>
				)}
			</main>
		</div>
	)
}
