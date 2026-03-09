"use client"

import { useState } from "react"
import { Send, Bot, User } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const initialMessages = [
  {
    role: "tutor" as const,
    content:
      "Hi Jane! I noticed you've been working on Fractions. Would you like me to explain equivalent fractions with a step-by-step example?",
  },
  {
    role: "student" as const,
    content: "Yes please! I keep getting confused when comparing fractions.",
  },
  {
    role: "tutor" as const,
    content:
      "No worries! Let's start simple. To compare 1/3 and 2/6, we find a common denominator. Since 6 is a multiple of 3, we can multiply 1/3 by 2/2 to get 2/6. They're equal! Want to try one?",
  },
]

export function TutorChat() {
  const [input, setInput] = useState("")

  return (
    <Card className="flex flex-col border bg-card shadow-sm">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg font-semibold text-foreground">
          <Bot className="size-5 text-primary" />
          TutorVoice Chat
        </CardTitle>
      </CardHeader>
      <CardContent className="flex flex-1 flex-col gap-4">
        <div className="flex flex-1 flex-col gap-3 rounded-xl bg-muted/50 p-4">
          {initialMessages.map((msg, i) => (
            <div
              key={i}
              className={`flex gap-2.5 ${msg.role === "student" ? "flex-row-reverse" : "flex-row"}`}
            >
              <div
                className={`flex size-7 shrink-0 items-center justify-center rounded-full ${
                  msg.role === "tutor"
                    ? "bg-primary text-primary-foreground"
                    : "bg-secondary text-secondary-foreground"
                }`}
              >
                {msg.role === "tutor" ? (
                  <Bot className="size-4" />
                ) : (
                  <User className="size-4" />
                )}
              </div>
              <div
                className={`max-w-[80%] rounded-xl px-3.5 py-2.5 text-sm leading-relaxed ${
                  msg.role === "tutor"
                    ? "bg-card text-card-foreground shadow-sm"
                    : "bg-primary text-primary-foreground"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}
        </div>

        <form
          className="flex gap-2"
          onSubmit={(e) => {
            e.preventDefault()
            setInput("")
          }}
        >
          <Input
            placeholder="Ask your tutor a question..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="h-10 flex-1 rounded-lg"
          />
          <Button type="submit" size="icon" className="size-10 shrink-0 rounded-lg">
            <Send className="size-4" />
            <span className="sr-only">Send message</span>
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
