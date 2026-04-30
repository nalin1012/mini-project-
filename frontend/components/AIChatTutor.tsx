'use client'

import * as React from 'react'
import { generateId } from '@/lib/id-generator'

type ChatRole = 'user' | 'assistant'

type ChatMessage = {
  id: string
  role: ChatRole
  content: string
  createdAt: number
}

type TutorChatResponse = {
  reply: string
  sessionId?: string
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://mini-project-xpie.onrender.com'

function nowTimestamp(ts: number) {
  return new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function BrainCapIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}>
      <path d="M9 21h6" />
      <path d="M10 21v-2" />
      <path d="M14 21v-2" />
      <path d="M7.5 14.5c-1.9-.7-3.2-2.5-3.2-4.6C4.3 7.2 6.1 5 8.4 5c.6-1.2 1.9-2 3.4-2 1.4 0 2.6.7 3.2 1.8 2.6 0 4.7 2.1 4.7 4.7 0 2.2-1.5 4.1-3.6 4.7" />
      <path d="M9 17c0-1.7 1.3-3 3-3s3 1.3 3 3" />
      <path d="M8 12c.6-.6 1.4-1 2.3-1" />
      <path d="M16 12c-.6-.6-1.4-1-2.3-1" />
    </svg>
  )
}

function ArrowIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}>
      <path d="M12 19V5" />
      <path d="M5 12l7-7 7 7" />
    </svg>
  )
}

function DotsTyping() {
  return (
    <div className="flex items-center gap-1 px-3 py-2">
      <span className="h-2 w-2 animate-bounce rounded-full bg-muted-foreground [animation-delay:-0.2s]" />
      <span className="h-2 w-2 animate-bounce rounded-full bg-muted-foreground [animation-delay:-0.1s]" />
      <span className="h-2 w-2 animate-bounce rounded-full bg-muted-foreground" />
    </div>
  )
}

function isCodeLike(text: string) {
  const hasFence = text.includes('```')
  const looksLikeFormula = /(^|\n)\s*([A-Za-z]+\s*=|\$.*\$)/.test(text)
  const looksLikeCode = /\b(function|const|let|var|class|def|import|SELECT|FROM|console\.log)\b/.test(text)
  return hasFence || looksLikeFormula || looksLikeCode
}

function splitToLines(text: string) {
  return text.replace(/\r\n/g, '\n').split('\n')
}

export function AIChatTutor() {
  const [isOpen, setIsOpen] = React.useState(false)
  const [isMinimized, setIsMinimized] = React.useState(false)
  const [hasPulsed, setHasPulsed] = React.useState(false)
  const [sessionId, setSessionId] = React.useState<string | null>(null)
  const [messages, setMessages] = React.useState<ChatMessage[]>(() => [
    {
      id: 'welcome',
      role: 'assistant',
      content: "Hi! I'm your AI Tutor. Ask me anything about your studies.",
      createdAt: Date.now(),
    },
  ])
  const [input, setInput] = React.useState('')
  const [isSending, setIsSending] = React.useState(false)
  const listRef = React.useRef<HTMLDivElement | null>(null)
  const [isMobile, setIsMobile] = React.useState(false)

  React.useEffect(() => {
    setIsMobile(window.matchMedia?.('(max-width: 640px)').matches ?? false)
  }, [])

  React.useEffect(() => {
    if (!hasPulsed) {
      const t = window.setTimeout(() => setHasPulsed(true), 3500)
      return () => window.clearTimeout(t)
    }
  }, [hasPulsed])

  React.useEffect(() => {
    if (!isOpen || isMinimized) return
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' })
  }, [isOpen, isMinimized, messages.length, isSending])

  async function sendMessage() {
    const trimmed = input.trim()
    if (!trimmed || isSending) return

    const userMsg: ChatMessage = {
      id: generateId(),
      role: 'user',
      content: trimmed,
      createdAt: Date.now(),
    }

    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setIsSending(true)

    try {
      const recent = [...messages, userMsg].slice(-10).map((m) => ({ role: m.role, content: m.content }))
      const token = localStorage.getItem('access_token')

      const res = await fetch(`${API_BASE_URL}/api/tutor/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ messages: recent, sessionId }),
      })

      if (!res.ok) {
        const text = await res.text()
        throw new Error(text || `Request failed: ${res.status}`)
      }

      const data = (await res.json()) as TutorChatResponse
      if (data.sessionId) setSessionId(data.sessionId)

      const assistantMsg: ChatMessage = {
        id: generateId(),
        role: 'assistant',
        content: data.reply || 'Sorry — I could not generate a reply.',
        createdAt: Date.now(),
      }

      setMessages((prev) => [...prev, assistantMsg])
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: generateId(),
          role: 'assistant',
          content: `I hit an error responding. ${err?.message ? String(err.message) : ''}`.trim(),
          createdAt: Date.now(),
        },
      ])
    } finally {
      setIsSending(false)
    }
  }

  const shouldFullscreen = isMobile && isOpen && !isMinimized

  return (
    <div className="fixed bottom-4 right-4 z-[9999]">
      {!isOpen && (
        <div className="group relative">
          <button
            type="button"
            aria-label="Open AI Tutor"
            onClick={() => {
              setIsOpen(true)
              setIsMinimized(false)
            }}
            className={
              "flex h-14 w-14 items-center justify-center rounded-full bg-primary text-primary-foreground shadow transition hover:opacity-95 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 " +
              (!hasPulsed ? 'animate-pulse' : '')
            }
          >
            <BrainCapIcon className="h-6 w-6" />
          </button>
          <div className="pointer-events-none absolute bottom-16 right-0 hidden w-max rounded-md bg-popover px-3 py-2 text-sm text-popover-foreground shadow group-hover:block">
            Ask your AI Tutor
          </div>
        </div>
      )}

      {isOpen && (
        <div
          className={
            "origin-bottom-right transition-all duration-300 ease-out " +
            (shouldFullscreen ? 'fixed inset-0 bottom-0 right-0' : isMinimized ? 'w-72 translate-y-2 opacity-95' : 'w-[360px]')
          }
        >
          <div
            className={
              'flex flex-col overflow-hidden rounded-xl border bg-background shadow-lg ' +
              (shouldFullscreen ? 'h-[100vh] w-[100vw] rounded-none' : isMinimized ? 'h-14' : 'h-[480px]')
            }
          >
            <div className="flex items-center justify-between border-b px-3 py-2">
              <div className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-full bg-muted" />
                <div className="leading-tight">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold">AI Tutor</span>
                    <span className="flex items-center gap-1 text-xs text-muted-foreground">
                      <span className="h-2 w-2 rounded-full bg-green-500" />
                      Online
                    </span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-1">
                <button
                  type="button"
                  aria-label="Minimize"
                  onClick={() => setIsMinimized((v) => !v)}
                  className="rounded-md px-2 py-1 text-sm text-muted-foreground hover:bg-muted"
                >
                  —
                </button>
                <button
                  type="button"
                  aria-label="Close"
                  onClick={() => {
                    setIsOpen(false)
                    setIsMinimized(false)
                  }}
                  className="rounded-md px-2 py-1 text-sm text-muted-foreground hover:bg-muted"
                >
                  ×
                </button>
              </div>
            </div>

            {!isMinimized && (
              <>
                <div ref={listRef} className="flex-1 space-y-2 overflow-y-auto px-3 py-3">
                  {messages.map((m) => {
                    const align = m.role === 'user' ? 'items-end' : 'items-start'
                    const bubble = m.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-muted text-foreground'

                    return (
                      <div key={m.id} className={`flex flex-col ${align} gap-1`}>
                        <div className={`max-w-[85%] rounded-2xl px-3 py-2 text-sm ${bubble}`}>
                          {isCodeLike(m.content) ? (
                            <pre className="whitespace-pre-wrap rounded-md bg-black/5 p-2 text-xs">
                              <code>{splitToLines(m.content).join('\n')}</code>
                            </pre>
                          ) : (
                            <div className="whitespace-pre-wrap">{m.content}</div>
                          )}
                        </div>
                        <div className="text-[11px] text-muted-foreground">{nowTimestamp(m.createdAt)}</div>
                      </div>
                    )
                  })}

                  {isSending && (
                    <div className="flex flex-col items-start gap-1">
                      <div className="max-w-[85%] rounded-2xl bg-muted text-foreground">
                        <DotsTyping />
                      </div>
                      <div className="text-[11px] text-muted-foreground">{nowTimestamp(Date.now())}</div>
                    </div>
                  )}
                </div>

                <div className="border-t p-2">
                  <div className="flex items-center gap-2">
                    <input
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                          e.preventDefault()
                          void sendMessage()
                        }
                      }}
                      placeholder="Type your question..."
                      className="h-10 flex-1 rounded-md border bg-background px-3 text-sm outline-none focus:ring-2 focus:ring-ring"
                    />
                    <button
                      type="button"
                      onClick={() => void sendMessage()}
                      disabled={isSending || !input.trim()}
                      className="flex h-10 w-10 items-center justify-center rounded-md bg-primary text-primary-foreground disabled:opacity-50"
                      aria-label="Send"
                    >
                      <ArrowIcon className="h-5 w-5 rotate-90" />
                    </button>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
