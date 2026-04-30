"use client"

import { useRouter } from "next/navigation"
import { BookOpen, Loader } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { useState } from "react"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://mini-project-xpie.onrender.com"

export function LoginForm() {
	const router = useRouter()
	const [email, setEmail] = useState("")
	const [password, setPassword] = useState("")
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState("")

	async function handleSubmit(e: React.FormEvent) {
		e.preventDefault()
		setError("")
		setLoading(true)

		try {
			const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					email,
					password,
				}),
			})

			if (!response.ok) {
				const data = await response.json()
				
				// Better error messages
				let errorMessage = "Login failed. Please check your credentials."
				if (data.detail) {
					if (typeof data.detail === "string") {
						if (data.detail.includes("Invalid")) {
							errorMessage = "Invalid email or password. If you forgot your password, use the 'Forgot password' link."
						} else if (data.detail.includes("deactivated")) {
							errorMessage = "Your account has been deactivated"
						} else {
							errorMessage = data.detail
						}
					}
				}
				setError(errorMessage)
				return
			}

			const data = await response.json()
			localStorage.setItem("access_token", data.access_token)
			localStorage.setItem("user", JSON.stringify(data.user))
			router.push("/dashboard")
		} catch (err) {
			console.error("Login error:", err)
			
			// Handle network errors specifically
			if (err instanceof TypeError && err.message.includes("fetch")) {
				setError("Unable to connect to server. Make sure the backend is running at " + API_BASE_URL)
			} else {
				setError(err instanceof Error ? err.message : "Failed to connect to server. Please try again.")
			}
		} finally {
			setLoading(false)
		}
	}

	const demoLogin = () => {
		localStorage.setItem("access_token", "demo-token-12345")
		localStorage.setItem("user", "Demo Learner")
		router.push("/dashboard")
	}

	return (
		<Card className="glass relative z-10 w-full max-w-md border border-white/10 bg-black/40 shadow-2xl">
			<CardHeader className="items-center text-center">
				<div className="flex size-12 items-center justify-center rounded-xl bg-blue-500/20 text-blue-400 border border-blue-400/30">
					<BookOpen className="size-6" />
				</div>
				<CardTitle className="mt-2 text-2xl font-semibold tracking-tight text-white">
					<span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
						AI Personalized Learning
					</span>
				</CardTitle>
				<CardDescription className="text-gray-400">
					Sign in to access your personalized dashboard
				</CardDescription>
			</CardHeader>
			<CardContent className="flex flex-col gap-5">
				{error && (
					<div className="rounded-lg bg-red-500/20 border border-red-500/30 p-3 text-sm text-red-300">
						{error}
					</div>
				)}

				<form onSubmit={handleSubmit} className="flex flex-col gap-4">
					<div className="flex flex-col gap-2">
						<Label htmlFor="email" className="text-white">
							Email
						</Label>
						<Input
							id="email"
							type="email"
							placeholder="student@university.edu"
							value={email}
							onChange={(e) => setEmail(e.target.value)}
							disabled={loading}
							className="h-11 rounded-xl border-white/10 bg-white/5 text-white placeholder-gray-500 focus:border-blue-400"
							required
						/>
					</div>
					<div className="flex flex-col gap-2">
						<Label htmlFor="password" className="text-white">
							Password
						</Label>
						<Input
							id="password"
							type="password"
							placeholder="Enter your password"
							value={password}
							onChange={(e) => setPassword(e.target.value)}
							disabled={loading}
							className="h-11 rounded-xl border-white/10 bg-white/5 text-white placeholder-gray-500 focus:border-blue-400"
							required
						/>
					</div>
					<Button
						type="submit"
						disabled={loading}
						className="h-11 w-full rounded-xl text-sm font-semibold bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
						size="lg"
					>
						{loading ? (
							<>
								<Loader className="mr-2 size-4 animate-spin" />
								Signing in...
							</>
						) : (
							"Sign In"
						)}
					</Button>
				</form>

				<div className="flex items-center gap-3">
					<Separator className="flex-1 bg-white/10" />
					<span className="text-xs text-gray-500">or try demo</span>
					<Separator className="flex-1 bg-white/10" />
				</div>

				<Button
					type="button"
					onClick={demoLogin}
					className="h-11 w-full rounded-xl border border-white/10 bg-white/5 text-sm font-medium text-white hover:bg-white/10"
					size="lg"
				>
					Continue as Demo User
				</Button>

				<div className="text-center text-sm text-gray-400">
					Don't have an account?{" "}
					<a href="/register" className="text-blue-400 hover:text-blue-300">
						Sign up here
					</a>
				</div>
			</CardContent>
		</Card>
	)
}
