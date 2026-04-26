"use client"

import { useState, useEffect, useRef } from "react"
import { Send, Bot, User, Loader } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

interface Message {
	role: "tutor" | "student"
	content: string
	isLoading?: boolean
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://192.168.0.131:8001"

export function TutorChat() {
	const [messages, setMessages] = useState<Message[]>([
		{
			role: "tutor",
			content:
				"Hi there! 👋 I'm TutorVoice, your AI learning companion. I'm here to help you understand any topic - from Fractions to Functions. What would you like to learn about today?",
		},
	])
	const [input, setInput] = useState("")
	const [loading, setLoading] = useState(false)
	const messagesEndRef = useRef<HTMLDivElement>(null)

	const scrollToBottom = () => {
		messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
	}

	useEffect(() => {
		scrollToBottom()
	}, [messages])

	const handleSendMessage = async (e: React.FormEvent) => {
		e.preventDefault()
		if (!input.trim()) return

		// Add student message
		const userMessage: Message = {
			role: "student",
			content: input,
		}
		setMessages((prev) => [...prev, userMessage])
		setInput("")
		setLoading(true)

		try {
			const token = localStorage.getItem("access_token")

			// Extract context from user message
			let context = undefined
			const topics = ["fractions", "algebra", "loops", "variables", "functions"]
			for (const topic of topics) {
				if (input.toLowerCase().includes(topic)) {
					context = topic
					break
				}
			}

			const response = await fetch(`${API_BASE_URL}/api/tutor/ask`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					...(token && { Authorization: `Bearer ${token}` }),
				},
				body: JSON.stringify({
					message: input,
					context: context,
				}),
			})

			if (!response.ok) {
				throw new Error("Failed to get response")
			}

			const data = await response.json()

			// Add tutor response
			const tutorMessage: Message = {
				role: "tutor",
				content: data.response,
			}

			// Add explanation as separate message if available
			if (data.explanation) {
				setMessages((prev) => [
					...prev,
					tutorMessage,
					{
						role: "tutor",
						content: `💡 ${data.explanation}`,
					},
				])
			} else {
				setMessages((prev) => [...prev, tutorMessage])
			}

			// Add examples if available
			if (data.examples && data.examples.length > 0) {
				const examplesText = `Here are some examples:\n${data.examples
					.map((ex: string, idx: number) => `${idx + 1}. ${ex}`)
					.join("\n")}`

				setMessages((prev) => [
					...prev,
					{
						role: "tutor",
						content: examplesText,
					},
				])
			}
		} catch (err) {
			console.error("Error:", err)
			// Fallback response
			const fallbackMessage: Message = {
				role: "tutor",
				content:
					"I'm having trouble connecting to my knowledge base right now. Try asking about: Fractions, Algebra, Loops, Variables, or Functions.",
			}
			setMessages((prev) => [...prev, fallbackMessage])
		} finally {
			setLoading(false)
		}
	}

	return (
		<Card className="flex flex-col h-[600px] border border-white/10 bg-white/5 shadow-sm">
			<CardHeader className="border-b border-white/10">
				<CardTitle className="flex items-center gap-2 text-lg font-semibold text-white">
					<div className="flex size-8 items-center justify-center rounded-full bg-gradient-to-br from-blue-400 to-purple-400">
						<Bot className="size-5 text-white" />
					</div>
					TutorVoice - AI Learning Assistant
				</CardTitle>
			</CardHeader>

			<CardContent className="flex-1 flex flex-col gap-4 overflow-hidden py-4">
				{/* Messages Container */}
				<div className="flex-1 overflow-y-auto flex flex-col gap-4 pr-2">
					{messages.map((msg, i) => (
						<div
							key={i}
							className={`flex gap-3 ${msg.role === "student" ? "flex-row-reverse" : "flex-row"}`}
						>
							<div
								className={`flex size-8 shrink-0 items-center justify-center rounded-full flex-shrink-0 ${
									msg.role === "tutor"
										? "bg-gradient-to-br from-blue-400 to-purple-400"
										: "bg-gradient-to-br from-green-400 to-cyan-400"
								}`}
							>
								{msg.role === "tutor" ? (
									<Bot className="size-5 text-white" />
								) : (
									<User className="size-5 text-white" />
								)}
							</div>

							<div
								className={`max-w-[70%] rounded-lg px-4 py-3 text-sm leading-relaxed break-words whitespace-pre-wrap ${
									msg.role === "tutor"
										? "bg-white/10 text-gray-100 border border-white/10"
										: "bg-blue-600 text-white"
								}`}
							>
								{msg.content}
								{msg.isLoading && (
									<span className="inline-block ml-2">
										<Loader className="size-4 animate-spin" />
									</span>
								)}
							</div>
						</div>
					))}

					{loading && (
						<div className="flex gap-3">
							<div className="flex size-8 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-blue-400 to-purple-400">
								<Bot className="size-5 text-white" />
							</div>
							<div className="flex items-center gap-2 rounded-lg bg-white/10 px-4 py-3 border border-white/10">
								<Loader className="size-4 animate-spin text-blue-400" />
								<span className="text-sm text-gray-300">Thinking...</span>
							</div>
						</div>
					)}

					<div ref={messagesEndRef} />
				</div>

				{/* Input Form */}
				<form className="flex gap-2 pt-4 border-t border-white/10" onSubmit={handleSendMessage}>
					<Input
						placeholder="Ask about Fractions, Algebra, Loops, Variables, Functions..."
						value={input}
						onChange={(e) => setInput(e.target.value)}
						disabled={loading}
						className="h-10 flex-1 rounded-lg bg-white/10 border-white/20 text-white placeholder-gray-500 focus:border-blue-400"
					/>
					<Button
						type="submit"
						disabled={loading || !input.trim()}
						size="icon"
						className="size-10 shrink-0 rounded-lg bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
					>
						<Send className="size-4" />
						<span className="sr-only">Send message</span>
					</Button>
				</form>
			</CardContent>
		</Card>
	)
}
