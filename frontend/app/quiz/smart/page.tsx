"use client"

import { useEffect } from "react"
import { useSearchParams } from "next/navigation"

export default function SmartQuizRedirectPage() {
  const params = useSearchParams()

  useEffect(() => {
    const topic = params.get("topic")
    if (topic) {
      localStorage.setItem("selected_topic", topic)
    }

    const noteId = params.get("noteId")
    if (noteId) {
      localStorage.setItem("selected_note_id", noteId)
    }

    window.location.href = "/quiz"
  }, [params])

  return (
    <div className="min-h-screen bg-[#0B0F1A] flex items-center justify-center px-4">
      <div className="rounded-2xl border border-white/10 bg-white/5 p-6 text-sm text-muted-foreground">
        Preparing your smart quiz…
      </div>
    </div>
  )
}
