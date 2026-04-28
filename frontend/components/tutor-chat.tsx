"use client"

import { useState, useEffect, useRef } from "react"
import { Send, Bot, User, Loader, Sparkles } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

interface Message {
  role: "tutor" | "student"
  content: string
  isLoading?: boolean
}

// ✅ ONLY ONE DEFINITION (SAFE)
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://192.168.0.131:8001"

// Suggested questions for quick learning
const SUGGESTED_QUESTIONS = [
  "What are fractions?",
  "How do I solve algebra?",
  "Explain geometry",
  "What is physics?",
  "Tell me about biology",
]

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
  const [showSuggestions, setShowSuggestions] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSuggestedQuestion = (question: string) => {
    setInput(question)
    setShowSuggestions(false)
  }

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = {
      role: "student",
      content: input,
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setShowSuggestions(false)
    setLoading(true)

    try {
      const token = localStorage.getItem("access_token")

      let context = undefined
      const topics = ["fractions", "algebra", "loops", "variables", "functions", "geometry", "physics", "biology"]

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
        const errorData = await response.json().catch(() => ({}))
        console.error("API Error:", response.status, errorData)
        throw new Error(errorData.detail || `API Error: ${response.status}`)
      }

      const data = await response.json()

      const tutorMessage: Message = {
        role: "tutor",
        content: data.response,
      }

      // ✅ Single update to avoid async issues
      let newMessages: Message[] = [tutorMessage]

      if (data.explanation) {
        newMessages.push({
          role: "tutor",
          content: `💡 ${data.explanation}`,
        })
      }

      if (data.examples && data.examples.length > 0) {
        newMessages.push({
          role: "tutor",
          content: `📚 Examples:\n${data.examples
            .map((ex: string, idx: number) => `${idx + 1}. ${ex}`)
            .join("\n")}`,
        })
      }

      setMessages((prev) => [...prev, ...newMessages])
      setShowSuggestions(true)
    } catch (err) {
      console.error("Error:", err)

      setMessages((prev) => [
        ...prev,
        {
          role: "tutor",
          content:
            "I'm having trouble connecting to my knowledge base right now. Try asking about: Fractions, Algebra, Geometry, Physics, Biology, or Chemistry.",
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="flex flex-col h-[600px] border border-white/10 bg-gradient-to-br from-slate-900/50 to-slate-800/50 shadow-lg">
      <CardHeader className="border-b border-white/10 bg-gradient-to-r from-blue-600/20 to-purple-600/20">
        <CardTitle className="flex items-center gap-2 text-lg font-semibold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
          <div className="flex size-8 items-center justify-center rounded-full bg-gradient-to-br from-blue-400 to-purple-400">
            <Sparkles className="size-5 text-white" />
          </div>
          TutorVoice - Interactive Learning
        </CardTitle>
      </CardHeader>

      <CardContent className="flex-1 flex flex-col gap-4 overflow-hidden py-4">
        <div className="flex-1 overflow-y-auto flex flex-col gap-4 pr-2">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex gap-3 animate-fadeIn ${
                msg.role === "student" ? "flex-row-reverse" : "flex-row"
              }`}
            >
              <div
                className={`flex size-8 items-center justify-center rounded-full flex-shrink-0 ${
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
                className={`max-w-[70%] rounded-lg px-4 py-3 text-sm leading-relaxed ${
                  msg.role === "tutor"
                    ? "bg-white/10 text-gray-100 border border-white/10 hover:bg-white/15 transition-colors"
                    : "bg-blue-600 text-white shadow-md"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex gap-3 animate-fadeIn">
              <div className="flex size-8 items-center justify-center rounded-full bg-gradient-to-br from-blue-400 to-purple-400 flex-shrink-0">
                <Bot className="size-5 text-white" />
              </div>
              <div className="flex items-center gap-2 rounded-lg bg-white/10 px-4 py-3 border border-white/10">
                <Loader className="size-4 animate-spin text-blue-400" />
                <span className="text-sm text-gray-300">
                  Thinking<span className="animate-pulse">...</span>
                </span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {showSuggestions && !loading && (
          <div className="border-t border-white/10 pt-3">
            <p className="text-xs text-gray-400 mb-2">💡 Try asking:</p>
            <div className="flex flex-wrap gap-2">
              {SUGGESTED_QUESTIONS.map((q) => (
                <button
                  key={q}
                  onClick={() => {
                    handleSuggestedQuestion(q)
                    setTimeout(
                      () =>
                        document
                          .querySelector("form")
                          ?.dispatchEvent(
                            new Event("submit", { bubbles: true })
                          ),
                      100
                    )
                  }}
                  className="text-xs px-3 py-1 rounded-full bg-blue-500/20 hover:bg-blue-500/40 text-blue-300 border border-blue-500/30 transition-colors cursor-pointer hover:scale-105 transform"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        <form
          className="flex gap-2 pt-4 border-t border-white/10"
          onSubmit={handleSendMessage}
        >
          <Input
            placeholder="Ask anything about your learning..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
            className="h-10 flex-1 rounded-lg bg-white/10 border-white/20 text-white placeholder-gray-400 focus:bg-white/20 transition-colors"
          />
          <Button
            type="submit"
            disabled={loading || !input.trim()}
            size="icon"
            className="size-10 rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:opacity-50"
          >
            <Send className="size-4" />
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
