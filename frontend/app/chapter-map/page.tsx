"use client"

import { useEffect, useMemo, useState } from "react"
import Link from "next/link"
import { DashboardNavbar } from "@/components/dashboard-navbar"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Loader2, AlertCircle } from "lucide-react"

type ChapterNode = {
  id: string
  type: "subject" | "chapter" | "subtopic" | "micro"
  title: string
  subjectId: string
  percentComplete: number
  status: "locked" | "in_progress" | "done"
  children: ChapterNode[]
}

type Summary = {
  keyPoints: string[]
  formulas: string[]
  example: string
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://mini-project-xpie.onrender.com"

function StatusBadge({ status }: { status: ChapterNode["status"] }) {
  if (status === "done") return <Badge className="bg-green-500/15 text-green-300 border border-green-500/30">Done</Badge>
  if (status === "in_progress") return <Badge className="bg-blue-500/15 text-blue-300 border border-blue-500/30">In Progress</Badge>
  return <Badge variant="outline" className="border-white/15 text-muted-foreground">Locked</Badge>
}

function NodeCard({ node, onOpen }: { node: ChapterNode; onOpen: (n: ChapterNode) => void }) {
  return (
    <Card
      className="glass border-white/10 bg-white/5 p-4 transition hover:bg-white/7"
      role="button"
      tabIndex={0}
      onClick={() => onOpen(node)}
      onKeyDown={(e) => {
        if (e.key === "Enter") onOpen(node)
      }}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-sm font-semibold text-white">{node.title}</div>
          <div className="mt-2">
            <Progress value={node.percentComplete} />
          </div>
          <div className="mt-2 text-xs text-muted-foreground">{node.percentComplete}% complete</div>
        </div>
        <StatusBadge status={node.status} />
      </div>
    </Card>
  )
}

export default function ChapterMapPage() {
  const [subjects, setSubjects] = useState<string[]>([])
  const [selectedSubject, setSelectedSubject] = useState<string>("Math")
  const [tree, setTree] = useState<ChapterNode | null>(null)
  const [loadingTree, setLoadingTree] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [drawerOpen, setDrawerOpen] = useState(false)
  const [activeNode, setActiveNode] = useState<ChapterNode | null>(null)
  const [summary, setSummary] = useState<Summary | null>(null)
  const [loadingSummary, setLoadingSummary] = useState(false)
  const [saveStatus, setSaveStatus] = useState<ChapterNode["status"]>("locked")
  const [savePercent, setSavePercent] = useState<number>(0)
  const [saving, setSaving] = useState(false)
  const [saveError, setSaveError] = useState<string | null>(null)

  useEffect(() => {
    const token = localStorage.getItem("access_token")
    if (!token) {
      window.location.href = "/login"
      return
    }

    const loadSubjects = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/api/subjects`)
        if (res.ok) {
          const data = await res.json()
          const names = (data.subjects || []).map((s: any) => s.name).filter(Boolean)
          setSubjects(names)
          if (names.length && !names.includes(selectedSubject)) setSelectedSubject(names[0])
        }
      } catch {
        setSubjects(["Math", "Science", "Programming", "English", "Aptitude"])
      }
    }

    void loadSubjects()
  }, [selectedSubject])

  const fetchTree = async (subject: string) => {
    try {
      setLoadingTree(true)
      setError(null)
      const token = localStorage.getItem("access_token")
      const res = await fetch(`${API_BASE_URL}/api/chapters?subject=${encodeURIComponent(subject)}`, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      })
      if (res.status === 401) {
        localStorage.removeItem("access_token")
        window.location.href = "/login"
        return
      }
      if (!res.ok) {
        const txt = await res.text()
        throw new Error(txt || "Failed to load chapter map")
      }
      const data = await res.json()
      setTree(data.tree)
    } catch (e: any) {
      setError(e?.message || "Failed to load chapter map")
      setTree(null)
    } finally {
      setLoadingTree(false)
    }
  }

  useEffect(() => {
    void fetchTree(selectedSubject)
  }, [selectedSubject])

  const subjectList = useMemo(() => (subjects.length ? subjects : ["Math", "Science", "Programming", "English", "Aptitude"]), [subjects])

  const openNode = async (node: ChapterNode) => {
    setActiveNode(node)
    setDrawerOpen(true)
    setSummary(null)
    setLoadingSummary(true)
    setSaveError(null)
    setSaveStatus(node.status)
    setSavePercent(node.percentComplete)

    try {
      const token = localStorage.getItem("access_token")
      const res = await fetch(`${API_BASE_URL}/api/chapters/summary`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          subjectId: node.subjectId,
          chapterId: node.id,
          title: node.title,
          path: [node.subjectId, node.title],
        }),
      })
      if (!res.ok) {
        const txt = await res.text()
        throw new Error(txt || "Failed to load summary")
      }
      const data = await res.json()
      setSummary(data)
    } catch (e: any) {
      setSummary({ keyPoints: [], formulas: [], example: "" })
      setSaveError(e?.message || "Failed to load summary")
    } finally {
      setLoadingSummary(false)
    }
  }

  const saveProgress = async () => {
    if (!activeNode) return
    try {
      setSaving(true)
      setSaveError(null)
      const token = localStorage.getItem("access_token")
      const res = await fetch(`${API_BASE_URL}/api/chapters/progress`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          subjectId: activeNode.subjectId,
          chapterId: activeNode.id,
          status: saveStatus,
          percent: savePercent,
        }),
      })
      if (!res.ok) {
        const txt = await res.text()
        throw new Error(txt || "Failed to save progress")
      }
      await fetchTree(selectedSubject)
    } catch (e: any) {
      setSaveError(e?.message || "Failed to save progress")
    } finally {
      setSaving(false)
    }
  }

  const renderChildren = (nodes: ChapterNode[], depth: number) => {
    if (!nodes.length) return null

    return (
      <Accordion type="multiple" className="w-full">
        {nodes.map((n) => (
          <AccordionItem key={n.id} value={n.id} className="border-white/10">
            <AccordionTrigger className="py-3">
              <div className="w-full" style={{ paddingLeft: depth * 12 }}>
                <NodeCard node={n} onOpen={openNode} />
              </div>
            </AccordionTrigger>
            <AccordionContent className="pb-4">
              <div className="mt-3 space-y-3">{renderChildren(n.children || [], depth + 1)}</div>
            </AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    )
  }

  return (
    <div className="min-h-screen bg-[#0B0F1A]">
      <DashboardNavbar />
      <main className="mx-auto w-full max-w-6xl px-4 py-10 lg:px-8">
        <div className="mb-6">
          <h1 className="text-2xl font-semibold text-white">Chapter Map</h1>
          <p className="mt-2 text-sm text-muted-foreground">Pick a subject and explore the roadmap. Tap any node for AI smart summaries.</p>
        </div>

        {error && (
          <Alert className="mb-6 border-red-500/30 bg-red-500/10">
            <AlertCircle className="h-4 w-4 text-red-400" />
            <AlertDescription className="text-red-200">{error}</AlertDescription>
          </Alert>
        )}

        <div className="flex flex-col gap-6 lg:flex-row">
          <aside className="glass rounded-2xl border border-white/10 bg-white/5 p-4 lg:w-72">
            <div className="text-sm font-semibold text-white">Subjects</div>
            <div className="mt-4 space-y-2">
              {subjectList.map((s) => (
                <button
                  key={s}
                  type="button"
                  onClick={() => setSelectedSubject(s)}
                  className={
                    "w-full rounded-xl px-4 py-3 text-left text-sm font-medium transition " +
                    (selectedSubject === s ? "bg-primary/15 text-primary neon-ring" : "bg-white/5 text-foreground hover:bg-primary/10")
                  }
                >
                  {s}
                </button>
              ))}
            </div>
          </aside>

          <section className="flex-1">
            <div className="glass rounded-2xl border border-white/10 bg-white/5 p-4">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <div className="text-sm font-semibold text-white">{selectedSubject} Roadmap</div>
                  <div className="mt-1 text-xs text-muted-foreground">Expand nodes to drill down into subtopics and micro-concepts.</div>
                </div>
                {loadingTree && (
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Loading…
                  </div>
                )}
              </div>

              <div className="mt-5 space-y-3">
                {!loadingTree && tree && renderChildren(tree.children || [], 0)}
                {!loadingTree && !tree && !error && (
                  <div className="rounded-xl border border-white/10 bg-white/5 p-6 text-sm text-muted-foreground">
                    No roadmap found.
                  </div>
                )}
              </div>
            </div>
          </section>
        </div>

        <Sheet open={drawerOpen} onOpenChange={setDrawerOpen}>
          <SheetContent side="right" className="glass w-full border-white/10 sm:max-w-[520px]">
            <SheetHeader>
              <SheetTitle className="text-white">{activeNode?.title || "Details"}</SheetTitle>
            </SheetHeader>

            {saveError && (
              <Alert className="mt-4 border-red-500/30 bg-red-500/10">
                <AlertCircle className="h-4 w-4 text-red-400" />
                <AlertDescription className="text-red-200">{saveError}</AlertDescription>
              </Alert>
            )}

            <div className="mt-4 space-y-6">
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="text-sm font-semibold text-white">Smart Summary</div>
                {loadingSummary ? (
                  <div className="mt-3 flex items-center gap-2 text-sm text-muted-foreground">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Generating summary…
                  </div>
                ) : (
                  <div className="mt-3 space-y-4">
                    <div>
                      <div className="text-xs font-semibold text-muted-foreground">Key Points</div>
                      <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-foreground">
                        {(summary?.keyPoints || []).length ? (
                          (summary?.keyPoints || []).map((p, idx) => <li key={idx}>{p}</li>)
                        ) : (
                          <li className="text-muted-foreground">No key points generated.</li>
                        )}
                      </ul>
                    </div>

                    <div>
                      <div className="text-xs font-semibold text-muted-foreground">Important Formulas</div>
                      <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-foreground">
                        {(summary?.formulas || []).length ? (
                          (summary?.formulas || []).map((f, idx) => <li key={idx}>{f}</li>)
                        ) : (
                          <li className="text-muted-foreground">None for this topic.</li>
                        )}
                      </ul>
                    </div>

                    <div>
                      <div className="text-xs font-semibold text-muted-foreground">Worked Example</div>
                      <div className="mt-2 whitespace-pre-wrap rounded-xl bg-white/5 p-3 text-sm text-foreground">
                        {summary?.example || "No example generated."}
                      </div>
                    </div>

                    <div className="flex flex-wrap gap-2">
                      <Link href={`/quiz/smart?topic=${encodeURIComponent(activeNode?.title || "")}`}>
                        <Button className="bg-blue-600 text-white hover:bg-blue-700 border-0">Start Quiz on This Topic</Button>
                      </Link>
                    </div>
                  </div>
                )}
              </div>

              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="text-sm font-semibold text-white">Progress</div>
                <div className="mt-3 grid grid-cols-1 gap-3">
                  <label className="text-xs text-muted-foreground">
                    Status
                    <select
                      value={saveStatus}
                      onChange={(e) => setSaveStatus(e.target.value as any)}
                      className="mt-1 h-10 w-full rounded-md border border-white/10 bg-background px-3 text-sm"
                    >
                      <option value="locked">Locked</option>
                      <option value="in_progress">In Progress</option>
                      <option value="done">Done</option>
                    </select>
                  </label>

                  <label className="text-xs text-muted-foreground">
                    Percent
                    <input
                      type="range"
                      min={0}
                      max={100}
                      value={savePercent}
                      onChange={(e) => setSavePercent(Number(e.target.value))}
                      className="mt-2 w-full"
                    />
                    <div className="mt-1 text-sm text-foreground">{savePercent}%</div>
                  </label>

                  <Button onClick={() => void saveProgress()} disabled={saving} className="bg-blue-600 text-white hover:bg-blue-700 border-0">
                    {saving ? (
                      <span className="flex items-center gap-2">
                        <Loader2 className="h-4 w-4 animate-spin" />
                        Saving…
                      </span>
                    ) : (
                      "Save Progress"
                    )}
                  </Button>
                </div>
              </div>
            </div>
          </SheetContent>
        </Sheet>
      </main>
    </div>
  )
}
