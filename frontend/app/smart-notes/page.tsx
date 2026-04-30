"use client"

import { useEffect, useMemo, useRef, useState } from "react"
import Link from "next/link"
import { DashboardNavbar } from "@/components/dashboard-navbar"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Loader2, AlertCircle, Trash2, UploadCloud } from "lucide-react"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://mini-project-xpie.onrender.com"

type NoteListItem = {
  id: number
  title: string
  subject?: string
  sourceType: string
  createdAt?: string | null
}

type Flashcard = { q: string; a: string }

type BulletGroup = { topic: string; points: string[] }

type QuizQuestion = {
  question: string
  options: string[]
  correct_option: number
  explanation: string
}

type NoteDetail = {
  id?: number
  title: string
  subject?: string
  sourceType: string
  rawContent: string
  bulletNotes: BulletGroup[]
  flashcards: Flashcard[]
  revisionSheet: string
  quiz: QuizQuestion[]
  revisionNotes?: {
    revisionNotes?: Array<{ topic: string; summary: string }>
    keyPoints?: string[]
    commonMistakes?: string[]
  }
  createdAt?: string | null
}

function formatDate(iso?: string | null) {
  if (!iso) return ""
  const d = new Date(iso)
  return d.toLocaleDateString()
}

function FlashcardView({ cards }: { cards: Flashcard[] }) {
  const [flipped, setFlipped] = useState<Record<number, boolean>>({})

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
      {cards.map((c, idx) => {
        const isFlip = !!flipped[idx]
        return (
          <button
            key={idx}
            type="button"
            onClick={() => setFlipped((p) => ({ ...p, [idx]: !p[idx] }))}
            className="rounded-2xl border border-white/10 bg-white/5 p-4 text-left transition hover:bg-white/7"
            style={{ perspective: 900 }}
          >
            <div
              className="relative min-h-[120px] transition-transform duration-500"
              style={{ transformStyle: "preserve-3d", transform: isFlip ? "rotateY(180deg)" : "rotateY(0deg)" }}
            >
              <div className="absolute inset-0" style={{ backfaceVisibility: "hidden" }}>
                <div className="text-xs font-semibold text-muted-foreground">Question</div>
                <div className="mt-2 text-sm text-white">{c.q}</div>
                <div className="mt-4 text-xs text-muted-foreground">Tap to flip</div>
              </div>
              <div className="absolute inset-0" style={{ backfaceVisibility: "hidden", transform: "rotateY(180deg)" }}>
                <div className="text-xs font-semibold text-muted-foreground">Answer</div>
                <div className="mt-2 whitespace-pre-wrap text-sm text-white">{c.a}</div>
                <div className="mt-4 text-xs text-muted-foreground">Tap to flip back</div>
              </div>
            </div>
          </button>
        )
      })}
    </div>
  )
}

export default function SmartNotesPage() {
  const [notes, setNotes] = useState<NoteListItem[]>([])
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [detail, setDetail] = useState<NoteDetail>({
    title: "Untitled Note",
    subject: undefined,
    sourceType: "text",
    rawContent: "",
    bulletNotes: [],
    flashcards: [],
    revisionSheet: "",
    quiz: [],
    revisionNotes: undefined,
  })

  const [rawText, setRawText] = useState("")
  const [file, setFile] = useState<File | null>(null)
  const fileInputRef = useRef<HTMLInputElement | null>(null)

  const [loadingList, setLoadingList] = useState(false)
  const [loadingNote, setLoadingNote] = useState(false)
  const [generating, setGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [activeTab, setActiveTab] = useState<"short" | "flash" | "sheet" | "revision">("short")
  const [selectedSubject, setSelectedSubject] = useState<string | undefined>(undefined)

  const subjects = ["Math", "Science", "Programming", "English", "Aptitude", "Study Skills"]

  const token = useMemo(() => (typeof window !== "undefined" ? localStorage.getItem("access_token") : null), [])

  useEffect(() => {
    if (!token) {
      window.location.href = "/login"
      return
    }
    void refreshList()
  }, [token])

  const refreshList = async () => {
    try {
      setLoadingList(true)
      setError(null)
      const res = await fetch(`${API_BASE_URL}/api/notes`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
      })
      if (res.status === 401) {
        localStorage.removeItem("access_token")
        window.location.href = "/login"
        return
      }
      if (!res.ok) throw new Error(await res.text())
      const data = await res.json()
      setNotes(data.notes || [])
    } catch (e: any) {
      setError(e?.message || "Failed to load notes")
    } finally {
      setLoadingList(false)
    }
  }

  const loadNote = async (id: number) => {
    try {
      setLoadingNote(true)
      setError(null)
      const res = await fetch(`${API_BASE_URL}/api/notes/${id}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
      })
      if (!res.ok) throw new Error(await res.text())
      const data = await res.json()
      setSelectedId(id)
      setDetail({
        id: data.id,
        title: data.title,
        subject: data.subject,
        sourceType: data.sourceType,
        rawContent: data.rawContent,
        bulletNotes: data.bulletNotes || [],
        flashcards: data.flashcards || [],
        revisionSheet: data.revisionSheet || "",
        quiz: data.quiz || [],
        revisionNotes: data.revisionNotes,
        createdAt: data.createdAt,
      })
      setSelectedSubject(data.subject)
      setRawText(data.rawContent || "")
      setFile(null)
    } catch (e: any) {
      setError(e?.message || "Failed to load note")
    } finally {
      setLoadingNote(false)
    }
  }

  const onDrop = (ev: React.DragEvent) => {
    ev.preventDefault()
    const f = ev.dataTransfer.files?.[0]
    if (!f) return
    setFile(f)
    setError(null)
  }

  const generate = async (opts?: { save?: boolean; explainSimply?: boolean }) => {
    try {
      setGenerating(true)
      setError(null)

      // Validation
      const hasContent = file || (rawText && rawText.trim().length > 10)
      if (!hasContent) {
        setError("Please upload a PDF/TXT file or paste at least 10 characters of text")
        setGenerating(false)
        return
      }

      const form = new FormData()
      if (file) {
        form.append("file", file)
      } else {
        form.append("text", rawText)
      }
      form.append("title", detail.title || "Untitled Note")
      form.append("subject", selectedSubject || "")
      form.append("save", String(!!opts?.save))
      if (selectedId) form.append("noteId", String(selectedId))
      form.append("explainSimply", String(!!opts?.explainSimply))

      const res = await fetch(`${API_BASE_URL}/api/notes/generate`, {
        method: "POST",
        headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
        body: form,
      })

      if (!res.ok) {
        let errorMsg = "Failed to generate notes"
        try {
          const errorData = await res.json()
          errorMsg = errorData.detail || errorMsg
        } catch {
          const txt = await res.text()
          errorMsg = txt || errorMsg
        }
        throw new Error(errorMsg)
      }

      const data = await res.json()
      const newId = data.noteId ?? null

      setDetail((prev) => ({
        ...prev,
        id: newId ?? prev.id,
        title: data.title || prev.title,
        subject: data.subject || prev.subject,
        sourceType: data.sourceType || prev.sourceType,
        rawContent: file ? prev.rawContent : rawText,
        bulletNotes: data.bulletNotes || prev.bulletNotes,
        flashcards: data.flashcards || prev.flashcards,
        revisionSheet: data.revisionSheet || prev.revisionSheet,
        quiz: data.quiz || prev.quiz,
      }))

      if (newId) {
        setSelectedId(newId)
        await refreshList()
      }
    } catch (e: any) {
      setError(e?.message || "Failed to generate notes. Please try again.")
    } finally {
      setGenerating(false)
    }
  }

  const deleteSelected = async () => {
    if (!selectedId) return
    try {
      setError(null)
      const res = await fetch(`${API_BASE_URL}/api/notes/${selectedId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
      })
      if (!res.ok) throw new Error(await res.text())
      setSelectedId(null)
      setSelectedSubject(undefined)
      setDetail({
        title: "Untitled Note",
        subject: undefined,
        sourceType: "text",
        rawContent: "",
        bulletNotes: [],
        flashcards: [],
        revisionSheet: "",
        quiz: [],
        revisionNotes: undefined,
      })
      setRawText("")
      setFile(null)
      await refreshList()
    } catch (e: any) {
      setError(e?.message || "Failed to delete")
    }
  }

  const downloadPdf = () => {
    if (!detail.bulletNotes?.length && !detail.flashcards?.length && !detail.revisionSheet) {
      setError("Please generate notes first to download")
      return
    }

    const title = detail.title || "Smart Notes"
    let content = `
      <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        h1 { color: #2563eb; margin-top: 30px; border-bottom: 2px solid #2563eb; padding-bottom: 10px; }
        h2 { color: #1e40af; margin-top: 20px; }
        h3 { color: #3b82f6; }
        .section { margin: 20px 0; page-break-inside: avoid; }
        ul { margin-left: 20px; }
        li { margin: 8px 0; }
        .flashcard { border: 1px solid #ddd; margin: 10px 0; padding: 12px; background: #f9fafb; }
        .question { font-weight: bold; color: #1e40af; }
        .answer { margin-top: 8px; color: #333; }
        .revision-item { border-left: 3px solid #2563eb; margin: 10px 0; padding: 10px; background: #eff6ff; }
      </style>
    `

    // Add title page
    content += `<h1>${title}</h1>`
    if (detail.subject) {
      content += `<p><strong>Subject:</strong> ${detail.subject}</p>`
    }
    content += `<p><strong>Generated:</strong> ${new Date().toLocaleString()}</p><hr />`

    // Short Notes
    if (detail.bulletNotes?.length) {
      content += `<h2>📝 Notes</h2><div class="section">`
      detail.bulletNotes.forEach((g) => {
        content += `<div class="section"><h3>${g.topic}</h3><ul>${(g.points || []).map((p) => `<li>${p}</li>`).join("")}</ul></div>`
      })
      content += `</div>`
    }

    // Flashcards
    if (detail.flashcards?.length) {
      content += `<h2>🎯 Flashcards</h2><div class="section">`
      detail.flashcards.forEach((c) => {
        content += `<div class="flashcard"><div class="question">Q: ${c.q}</div><div class="answer">A: ${c.a}</div></div>`
      })
      content += `</div>`
    }

    // Revision Notes
    if (detail.revisionNotes) {
      content += `<h2>🔄 Revision</h2><div class="section">`
      
      if (detail.revisionNotes.revisionNotes?.length) {
        content += `<h3>Key Topics</h3>`
        detail.revisionNotes.revisionNotes.forEach((r) => {
          content += `<div class="revision-item"><strong>${r.topic}:</strong> ${r.summary}</div>`
        })
      }

      if (detail.revisionNotes.keyPoints?.length) {
        content += `<h3>Critical Points</h3><ul>`
        detail.revisionNotes.keyPoints.forEach((p) => {
          content += `<li>${p}</li>`
        })
        content += `</ul>`
      }

      if (detail.revisionNotes.commonMistakes?.length) {
        content += `<h3>⚠️ Common Mistakes</h3><ul>`
        detail.revisionNotes.commonMistakes.forEach((m) => {
          content += `<li>${m}</li>`
        })
        content += `</ul>`
      }

      content += `</div>`
    }

    // Revision Sheet
    if (detail.revisionSheet) {
      content += `<h2>📋 Revision Sheet</h2><div class="section"><pre style="white-space:pre-wrap; font-family:monospace;">${detail.revisionSheet.replaceAll("<", "&lt;").replaceAll(">", "&gt;")}</pre></div>`
    }

    const win = window.open("", "_blank")
    if (!win) {
      setError("Could not open print window. Please check your popup blocker.")
      return
    }
    
    win.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>${title}</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
      </head>
      <body>
        ${content}
      </body>
      </html>
    `)
    win.document.close()
    win.focus()
    
    // Print dialog
    setTimeout(() => {
      win.print()
    }, 250)
  }

  return (
    <div className="min-h-screen bg-[#0B0F1A]">
      <DashboardNavbar />
      <main className="mx-auto w-full max-w-6xl px-4 py-10 lg:px-8">
        <div className="mb-6">
          <h1 className="text-2xl font-semibold text-white">Smart Notes</h1>
          <p className="mt-2 text-sm text-muted-foreground">Upload a PDF/text or paste raw text, then generate structured notes, flashcards, and a revision sheet.</p>
        </div>

        {error && (
          <Alert className="mb-6 border-red-500/30 bg-red-500/10">
            <AlertCircle className="h-4 w-4 text-red-400" />
            <AlertDescription className="text-red-200">{error}</AlertDescription>
          </Alert>
        )}

        <div className="flex flex-col gap-6 lg:flex-row">
          <aside className="glass rounded-2xl border border-white/10 bg-white/5 p-4 lg:w-80">
            <div className="flex items-center justify-between">
              <div className="text-sm font-semibold text-white">Your Notes</div>
              <Button variant="outline" className="border-white/15 bg-white/5 text-white hover:bg-white/10" onClick={() => void refreshList()} disabled={loadingList}>
                {loadingList ? <Loader2 className="h-4 w-4 animate-spin" /> : "Refresh"}
              </Button>
            </div>
            <div className="mt-4 space-y-2">
              {notes.length === 0 && <div className="rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-muted-foreground">No notes yet.</div>}
              {notes.map((n) => (
                <button
                  key={n.id}
                  type="button"
                  onClick={() => void loadNote(n.id)}
                  className={
                    "w-full rounded-xl border border-white/10 bg-white/5 p-4 text-left transition hover:bg-white/7 " +
                    (selectedId === n.id ? "neon-ring" : "")
                  }
                >
                  <div className="text-sm font-semibold text-white">{n.title}</div>
                  <div className="mt-1 text-xs text-muted-foreground">
                    {formatDate(n.createdAt)} • {n.sourceType}
                    {n.subject && <span className="ml-2 inline-block px-2 py-1 rounded bg-blue-500/20 text-blue-300">{n.subject}</span>}
                  </div>
                </button>
              ))}
            </div>
          </aside>

          <section className="flex-1">
            <Card className="glass border-white/10 bg-white/5 p-4">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <div className="text-sm font-semibold text-white">Note Workspace</div>
                  {loadingNote && (
                    <div className="mt-2 flex items-center gap-2 text-sm text-muted-foreground">
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Loading note…
                    </div>
                  )}
                </div>
                <div className="flex flex-wrap gap-2">
                  <Button
                    variant="outline"
                    className="border-white/15 bg-white/5 text-white hover:bg-white/10"
                    onClick={() => void generate({ explainSimply: true })}
                    disabled={generating}
                  >
                    Explain Simply
                  </Button>
                  <Button
                    variant="outline"
                    className="border-white/15 bg-white/5 text-white hover:bg-white/10"
                    onClick={() => void generate({ save: true })}
                    disabled={generating}
                  >
                    Save Notes
                  </Button>
                  <Button
                    variant="outline"
                    className="border-white/15 bg-white/5 text-white hover:bg-white/10"
                    onClick={downloadPdf}
                    disabled={generating}
                  >
                    Download PDF
                  </Button>
                  <Button
                    variant="outline"
                    className="border-red-500/30 bg-red-500/10 text-red-200 hover:bg-red-500/15"
                    onClick={() => void deleteSelected()}
                    disabled={!selectedId}
                  >
                    <Trash2 className="mr-2 h-4 w-4" />
                    Delete
                  </Button>
                </div>
              </div>

              <div className="mt-5 grid grid-cols-1 gap-4">
                <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                  <div className="text-sm font-semibold text-white mb-3">Select Subject (Optional)</div>
                  <select
                    value={selectedSubject || ""}
                    onChange={(e) => setSelectedSubject(e.target.value || undefined)}
                    className="w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm text-white focus:border-blue-400 focus:outline-none"
                  >
                    <option value="">-- Choose a subject --</option>
                    {subjects.map((subj) => (
                      <option key={subj} value={subj}>
                        {subj}
                      </option>
                    ))}
                  </select>
                  {selectedSubject && <div className="mt-2 text-xs text-muted-foreground">Subject: <span className="text-blue-300">{selectedSubject}</span></div>}
                </div>

                <div
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={onDrop}
                  className="rounded-2xl border border-dashed border-white/20 bg-white/5 p-5"
                >
                  <div className="flex flex-col items-start gap-3 sm:flex-row sm:items-center sm:justify-between">
                    <div className="flex items-start gap-3">
                      <div className="mt-0.5 rounded-lg bg-primary/15 p-2 text-primary">
                        <UploadCloud className="h-5 w-5" />
                      </div>
                      <div>
                        <div className="text-sm font-semibold text-white">Upload Zone</div>
                        <div className="mt-1 text-xs text-muted-foreground">Drag & drop a .txt or .pdf, or click to upload. Or paste text below.</div>
                        {file && <div className="mt-2 text-xs text-muted-foreground">Selected: {file.name}</div>}
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <input
                        ref={fileInputRef}
                        type="file"
                        accept=".txt,.pdf"
                        className="hidden"
                        onChange={(e) => {
                          const f = e.target.files?.[0] || null
                          setFile(f)
                        }}
                      />
                      <Button
                        variant="outline"
                        className="border-white/15 bg-white/5 text-white hover:bg-white/10"
                        onClick={() => fileInputRef.current?.click()}
                      >
                        Choose File
                      </Button>
                      <Button
                        className="bg-blue-600 text-white hover:bg-blue-700 border-0"
                        onClick={() => void generate({ save: false })}
                        disabled={generating}
                      >
                        {generating ? (
                          <span className="flex items-center gap-2">
                            <Loader2 className="h-4 w-4 animate-spin" />
                            AI is reading your notes...
                          </span>
                        ) : (
                          "Generate Notes"
                        )}
                      </Button>
                    </div>
                  </div>

                  <div className="mt-4">
                    <Textarea
                      value={rawText}
                      onChange={(e) => setRawText(e.target.value)}
                      placeholder="Paste raw text here…"
                      className="min-h-[140px] border-white/10 bg-background"
                    />
                  </div>
                </div>

                <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as any)} className="w-full">
                  <TabsList className="bg-white/5">
                    <TabsTrigger value="short">Short Notes</TabsTrigger>
                    <TabsTrigger value="flash">Flashcards</TabsTrigger>
                    <TabsTrigger value="sheet">Revision Sheet</TabsTrigger>
                    <TabsTrigger value="revision">📌 Revision</TabsTrigger>
                  </TabsList>

                  <TabsContent value="short" className="mt-4">
                    <div className="space-y-4">
                      {(detail.bulletNotes || []).length === 0 && (
                        <div className="rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-muted-foreground">Generate notes to see bullet points.</div>
                      )}
                      {(detail.bulletNotes || []).map((g, idx) => (
                        <div key={idx} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                          <div className="text-sm font-semibold text-white">{g.topic}</div>
                          <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-foreground">
                            {(g.points || []).map((p, i) => (
                              <li key={i}>{p}</li>
                            ))}
                          </ul>
                        </div>
                      ))}
                    </div>
                  </TabsContent>

                  <TabsContent value="flash" className="mt-4">
                    {(detail.flashcards || []).length === 0 ? (
                      <div className="rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-muted-foreground">Generate notes to see flashcards.</div>
                    ) : (
                      <FlashcardView cards={detail.flashcards} />
                    )}
                  </TabsContent>

                  <TabsContent value="sheet" className="mt-4">
                    {detail.revisionSheet ? (
                      <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                        <pre className="whitespace-pre-wrap text-sm text-foreground">{detail.revisionSheet}</pre>
                      </div>
                    ) : (
                      <div className="rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-muted-foreground">Generate notes to see a revision sheet.</div>
                    )}
                  </TabsContent>

                  <TabsContent value="revision" className="mt-4">
                    {detail.revisionNotes && (detail.revisionNotes.revisionNotes?.length || detail.revisionNotes.keyPoints?.length || detail.revisionNotes.commonMistakes?.length) ? (
                      <div className="space-y-4">
                        {detail.revisionNotes.revisionNotes && detail.revisionNotes.revisionNotes.length > 0 && (
                          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                            <div className="text-sm font-semibold text-white mb-3">Key Revision Topics</div>
                            <div className="space-y-3">
                              {detail.revisionNotes.revisionNotes.map((item, idx) => (
                                <div key={idx} className="rounded-lg border border-white/5 bg-white/3 p-3">
                                  <div className="text-sm font-medium text-blue-300">{item.topic}</div>
                                  <div className="mt-1 text-sm text-foreground">{item.summary}</div>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {detail.revisionNotes.keyPoints && detail.revisionNotes.keyPoints.length > 0 && (
                          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                            <div className="text-sm font-semibold text-white mb-3">🎯 Critical Points to Remember</div>
                            <ul className="list-disc space-y-2 pl-5 text-sm text-foreground">
                              {detail.revisionNotes.keyPoints.map((point, idx) => (
                                <li key={idx}>{point}</li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {detail.revisionNotes.commonMistakes && detail.revisionNotes.commonMistakes.length > 0 && (
                          <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-4">
                            <div className="text-sm font-semibold text-red-300 mb-3">⚠️ Common Mistakes to Avoid</div>
                            <ul className="list-disc space-y-2 pl-5 text-sm text-foreground">
                              {detail.revisionNotes.commonMistakes.map((mistake, idx) => (
                                <li key={idx}>{mistake}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    ) : (
                      <div className="rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-muted-foreground">Generate notes to see spaced revision notes.</div>
                    )}
                  </TabsContent>
                </Tabs>

                <div className="flex flex-wrap gap-2">
                  <Button
                    className="bg-blue-600 text-white hover:bg-blue-700 border-0"
                    onClick={() => {
                      if (!detail.quiz || detail.quiz.length === 0) {
                        setError("Please generate notes first to create a quiz")
                        return
                      }
                      // Store quiz data in localStorage
                      localStorage.setItem("smart_quiz_data", JSON.stringify({
                        title: detail.title,
                        subject: detail.subject,
                        questions: detail.quiz,
                        flashcards: detail.flashcards,
                        noteId: detail.id,
                      }))
                      // Navigate to quiz page
                      window.location.href = "/quiz/smart?source=notes"
                    }}
                    disabled={!detail.quiz || detail.quiz.length === 0}
                  >
                    Turn into Quiz
                  </Button>
                </div>
              </div>
            </Card>
          </section>
        </div>
      </main>
    </div>
  )
}
