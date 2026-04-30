"use client"

import Link from "next/link"
import { useState } from "react"
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

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://mini-project-xpie.onrender.com"

export default function RegisterPage() {
	const router = useRouter()

	const [name, setName] = useState("")
	const [email, setEmail] = useState("")
	const [password, setPassword] = useState("")
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState("")
	const [success, setSuccess] = useState(false)

	const validateForm = (): string | null => {
		if (!name.trim()) return "Name is required"
		if (name.trim().length < 2) return "Name must be at least 2 characters"
		if (!email.trim()) return "Email is required"
		if (!password) return "Password is required"
		if (password.length < 6) return "Password must be at least 6 characters"
		return null
	}

	const handleRegister = async (e: React.FormEvent) => {
		e.preventDefault()
		setError("")
		setSuccess(false)

		// Client-side validation
		const validationError = validateForm()
		if (validationError) {
			setError(validationError)
			return
		}

		setLoading(true)

		try {
			const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					name: name.trim(),
					email: email.toLowerCase().trim(),
					password,
				}),
			})

			const data = await response.json()

			if (!response.ok) {
				// Handle specific error messages from backend
				let errorMessage = "Registration failed. Please try again."
				
				if (data.detail) {
					if (typeof data.detail === "string") {
						errorMessage = data.detail
					} else if (Array.isArray(data.detail)) {
						// Pydantic validation errors
						errorMessage = data.detail[0].msg || errorMessage
					}
				}

				// Map common error messages
				if (errorMessage.includes("Email already registered") || errorMessage.includes("already exists")) {
					setError("This email is already registered. Try logging in instead.")
				} else if (errorMessage.includes("Password") || errorMessage.includes("password")) {
					setError("Password must be at least 6 characters")
				} else if (errorMessage.includes("Name") || errorMessage.includes("name")) {
					setError("Please enter a valid name (at least 2 characters)")
				} else if (errorMessage.includes("email") || errorMessage.includes("Email")) {
					setError("Please enter a valid email address")
				} else {
					setError(errorMessage)
				}
				return
			}

			// Success - store token and user info
			setSuccess(true)
			const { access_token, user } = data
			
			localStorage.setItem("access_token", access_token)
			localStorage.setItem("user", JSON.stringify(user))
			
			// Small delay to show success message
			setTimeout(() => {
				router.push("/dashboard")
			}, 500)
		} catch (err) {
			console.error("Registration error:", err)
			
			// Handle network errors
			if (err instanceof TypeError && err.message.includes("fetch")) {
				setError("Unable to connect to server. Please check your internet connection and try again.")
			} else {
				setError(err instanceof Error ? err.message : "An unexpected error occurred. Please try again.")
			}
		} finally {
			setLoading(false)
		}
	}

	return (
		<main className="flex min-h-svh items-center justify-center bg-[#0B0F1A] px-4 py-12">
			<div className="absolute inset-0 overflow-hidden">
				<div className="absolute -top-1/3 left-1/2 h-[820px] w-[820px] -translate-x-1/2 rounded-full bg-blue-500/15 blur-3xl" />
				<div className="absolute bottom-0 left-0 h-[420px] w-[420px] rounded-full bg-purple-600/15 blur-3xl" />
				<div className="absolute right-0 top-1/3 h-[320px] w-[320px] rounded-full bg-emerald-400/10 blur-3xl" />
			</div>

			<Card className="glass relative z-10 w-full max-w-md border border-white/10 bg-black/40 shadow-2xl">
				<CardHeader className="items-center text-center">
					<div className="flex size-12 items-center justify-center rounded-xl bg-blue-500/20 text-blue-400 border border-blue-400/30">
						<BookOpen className="size-6" />
					</div>
					<CardTitle className="mt-2 text-2xl font-semibold tracking-tight text-white">
						<span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
							Create your account
						</span>
					</CardTitle>
					<CardDescription className="text-gray-400">
						Start your AI-powered learning path in minutes.
					</CardDescription>
				</CardHeader>
				<CardContent className="flex flex-col gap-5">
					{error && (
						<div className="rounded-lg bg-red-500/20 border border-red-500/30 p-3 text-sm text-red-300">
							{error}
						</div>
					)}

					{success && (
						<div className="rounded-lg bg-green-500/20 border border-green-500/30 p-3 text-sm text-green-300">
							✓ Account created successfully! Redirecting...
						</div>
					)}

					<form onSubmit={handleRegister} className="flex flex-col gap-4">
						<div className="flex flex-col gap-2">
							<Label htmlFor="name" className="text-white">
								Full Name
							</Label>
							<Input
								id="name"
								placeholder="Jordan Smith"
								value={name}
								onChange={(e) => setName(e.target.value)}
								disabled={loading}
								className="h-11 rounded-xl border-white/10 bg-white/5 text-white placeholder-gray-500 focus:border-blue-400"
								required
							/>
						</div>
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
								placeholder="Min. 6 characters"
								value={password}
								onChange={(e) => setPassword(e.target.value)}
								disabled={loading}
								className="h-11 rounded-xl border-white/10 bg-white/5 text-white placeholder-gray-500 focus:border-blue-400"
								required
								minLength={6}
							/>
						</div>
						<Button
							type="submit"
							disabled={loading || success}
							className="h-11 rounded-xl text-sm font-semibold bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
						>
							{loading ? (
								<>
									<Loader className="mr-2 size-4 animate-spin" />
									Creating Account...
								</>
							) : success ? (
								"✓ Redirecting..."
							) : (
								"Create Account"
							)}
						</Button>
					</form>

					<div className="flex items-center gap-3">
						<Separator className="flex-1 bg-white/10" />
						<span className="text-xs text-gray-500">already a learner?</span>
						<Separator className="flex-1 bg-white/10" />
					</div>

					<Link href="/login" className="w-full">
						<Button className="h-11 w-full rounded-xl border border-white/10 bg-white/5 text-sm font-medium text-white hover:bg-white/10">
							Sign in instead
						</Button>
					</Link>
				</CardContent>
			</Card>
		</main>
	)
}