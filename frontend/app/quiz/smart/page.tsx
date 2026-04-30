"use client"

export const dynamic = 'force-dynamic'

import { useEffect } from "react"

export default function SmartQuizRedirectPage() {
  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const topic = params.get("topic")
    if (topic) {
      localStorage.setItem("selected_topic", topic)
    }

    const noteId = params.get("noteId")
    if (noteId) {
      localStorage.setItem("selected_note_id", noteId)
    }

    window.location.href = "/quiz"
  }, [])

  return (
    <div className="min-h-screen bg-[#0B0F1A] flex items-center justify-center px-4">
      <div className="rounded-2xl border border-white/10 bg-white/5 p-6 text-sm text-muted-foreground">
        Preparing your smart quiz…
      </div>
    </div>
  )
}
