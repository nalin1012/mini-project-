"use client"

import Link from "next/link"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { BookOpen } from "lucide-react"
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

export default function RegisterPage() {
	const router = useRouter()

	const [name, setName] = useState("")
	const [email, setEmail] = useState("")
	const [password, setPassword] = useState("")

	const handleRegister = async (e: React.FormEvent) => {
		e.preventDefault()

		const res = await fetch("http://127.0.0.1:8000/api/auth/register", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				name,
				email,
				password,
			}),
		})

		if (res.ok) {
			alert("Account created successfully")
			router.push("/login")
		} else {
			alert("Registration failed")
		}
	}

	return (
		<main className="flex min-h-svh items-center justify-center bg-login-bg px-4 py-12">
			<div className="absolute inset-0 overflow-hidden">
				<div className="absolute -top-1/3 left-1/2 h-[820px] w-[820px] -translate-x-1/2 rounded-full bg-primary/15 blur-3xl" />
				<div className="absolute bottom-0 left-0 h-[420px] w-[420px] rounded-full bg-[#7B61FF]/15 blur-3xl" />
				<div className="absolute right-0 top-1/3 h-[320px] w-[320px] rounded-full bg-emerald-400/10 blur-3xl" />
			</div>

			<Card className="glass relative z-10 w-full max-w-md border border-white/10 text-login-card-foreground shadow-2xl">
				<CardHeader className="items-center text-center">
					<div className="flex size-12 items-center justify-center rounded-xl bg-primary/20 text-primary neon-ring">
						<BookOpen className="size-6" />
					</div>
					<CardTitle className="mt-2 text-2xl font-semibold tracking-tight">
						<span className="gradient-text">Create your account</span>
					</CardTitle>
					<CardDescription className="text-muted-foreground">
						Start your AI-powered learning path in minutes.
					</CardDescription>
				</CardHeader>
				<CardContent className="flex flex-col gap-5">
					<form onSubmit={handleRegister} className="flex flex-col gap-4">
						<div className="flex flex-col gap-2">
							<Label htmlFor="name">Full name</Label>
							<Input
								id="name"
								placeholder="Jordan Smith"
								value={name}
								onChange={(e) => setName(e.target.value)}
								className="h-11 rounded-xl border-white/10 bg-white/5"
							/>
						</div>
						<div className="flex flex-col gap-2">
							<Label htmlFor="email">Email</Label>
							<Input
								id="email"
								type="email"
								placeholder="student@university.edu"
								value={email}
								onChange={(e) => setEmail(e.target.value)}
								className="h-11 rounded-xl border-white/10 bg-white/5"
							/>
						</div>
						<div className="flex flex-col gap-2">
							<Label htmlFor="password">Password</Label>
							<Input
								id="password"
								type="password"
								placeholder="Create a secure password"
								value={password}
								onChange={(e) => setPassword(e.target.value)}
								className="h-11 rounded-xl border-white/10 bg-white/5"
							/>
						</div>
						<Button type="submit" className="neon-ring h-11 rounded-xl text-sm font-semibold">
							Create Account
						</Button>
					</form>

					<div className="flex items-center gap-3">
						<Separator className="flex-1" />
						<span className="text-xs text-muted-foreground">already a learner?</span>
						<Separator className="flex-1" />
					</div>

					<Link href="/login" className="w-full">
						<Button
							variant="outline"
							className="h-11 w-full rounded-xl border-white/10 bg-white/5 text-sm font-medium"
						>
							Sign in instead
						</Button>
					</Link>
				</CardContent>
			</Card>
		</main>
	)
}