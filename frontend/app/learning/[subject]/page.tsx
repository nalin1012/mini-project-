'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { 
  Brain, 
  Zap, 
  BarChart3, 
  ArrowLeft, 
  AlertCircle, 
  Loader,
  BookOpen,
  Target,
  ChevronLeft,
  ChevronRight,
  Lightbulb,
  AlertTriangle
} from 'lucide-react'
import { DashboardNavbar } from '@/components/dashboard-navbar'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'

interface StructuredTopic {
  title: string
  explanation: string
  keyPoints: string[]
  formulas?: string[]
  realLifeExample: string
}

interface StructuredFlashcard {
  front: string
  back: string
}

interface RevisionGuide {
  importantTopics: string[]
  commonMistakes: string[]
  quickTips: string[]
}

interface Progress {
  topic: string
  mastery_score: number
  sessions_completed: number
  total_questions: number
  correct_answers: number
  status: string
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://192.168.0.131:8001'

export default function LearningPage() {
  const router = useRouter()
  const params = useParams()
  const subject = params?.subject as string

  const [topics, setTopics] = useState<StructuredTopic[]>([])
  const [flashcards, setFlashcards] = useState<StructuredFlashcard[]>([])
  const [revisionGuide, setRevisionGuide] = useState<RevisionGuide | null>(null)
  const [progress, setProgress] = useState<Progress | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'notes' | 'flashcards' | 'revision'>('notes')
  const [currentFlashcardIndex, setCurrentFlashcardIndex] = useState(0)
  const [isFlipped, setIsFlipped] = useState(false)

  // Convert URL format to display format
  const displaySubject = subject?.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) || ''

  useEffect(() => {
    if (!subject) return

    const fetchData = async () => {
      setLoading(true)
      setError(null)

      try {
        const token = localStorage.getItem('access_token')
        if (!token) {
          window.location.href = '/login'
          return
        }

        // Fetch structured notes
        try {
          const notesRes = await fetch(
            `${API_BASE_URL}/api/notes/structured/${encodeURIComponent(displaySubject)}`,
            {
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
              },
            }
          )

          if (notesRes.ok) {
            const notesData = await notesRes.json()
            setTopics(notesData.topics || [])
          }
        } catch (notesErr) {
          console.error('Failed to fetch notes:', notesErr)
        }

        // Fetch flashcards
        try {
          const flashcardsRes = await fetch(
            `${API_BASE_URL}/api/notes/flashcards/${encodeURIComponent(displaySubject)}`,
            {
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
              },
            }
          )

          if (flashcardsRes.ok) {
            const flashcardsData = await flashcardsRes.json()
            setFlashcards(flashcardsData.flashcards || [])
            setCurrentFlashcardIndex(0)
            setIsFlipped(false)
          }
        } catch (flashcardsErr) {
          console.error('Failed to fetch flashcards:', flashcardsErr)
        }

        // Fetch revision guide
        try {
          const revisionRes = await fetch(
            `${API_BASE_URL}/api/notes/revision/${encodeURIComponent(displaySubject)}`,
            {
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
              },
            }
          )

          if (revisionRes.ok) {
            const revisionData = await revisionRes.json()
            setRevisionGuide(revisionData)
          }
        } catch (revisionErr) {
          console.error('Failed to fetch revision guide:', revisionErr)
        }

        // Fetch progress
        try {
          const progressRes = await fetch(
            `${API_BASE_URL}/api/knowledge-gap/progress/${encodeURIComponent(displaySubject)}`,
            {
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
              },
            }
          )

          if (progressRes.ok) {
            const progressData = await progressRes.json()
            setProgress(progressData)
          }
        } catch (progressErr) {
          console.error('Failed to fetch progress:', progressErr)
        }
      } catch (err) {
        console.error('Error in LearningPage:', err)
        setError(`Failed to load learning content. Make sure the backend is running at ${API_BASE_URL}`)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [subject, displaySubject])

  const masteryPercentage = progress ? Math.round(progress.mastery_score * 100) : 0
  const progressBarColor = masteryPercentage >= 80 ? 'bg-green-500' : masteryPercentage >= 60 ? 'bg-yellow-500' : 'bg-red-500'

  const handleNextFlashcard = () => {
    if (currentFlashcardIndex < flashcards.length - 1) {
      setCurrentFlashcardIndex(currentFlashcardIndex + 1)
      setIsFlipped(false)
    }
  }

  const handlePrevFlashcard = () => {
    if (currentFlashcardIndex > 0) {
      setCurrentFlashcardIndex(currentFlashcardIndex - 1)
      setIsFlipped(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <DashboardNavbar />
        <main className="mx-auto flex w-full max-w-6xl flex-col gap-10 px-4 py-10 lg:px-8">
          <div className="flex items-center justify-center h-96">
            <div className="flex flex-col items-center gap-4">
              <Loader className="size-8 animate-spin text-primary" />
              <p className="text-muted-foreground">Loading {displaySubject}...</p>
            </div>
          </div>
        </main>
      </div>
    )
  }

  const currentFlashcard = flashcards[currentFlashcardIndex]

  return (
    <div className="min-h-screen bg-background">
      <DashboardNavbar />
      <main className="mx-auto flex w-full max-w-6xl flex-col gap-8 px-4 py-10 lg:px-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => router.back()}
              className="hover:bg-muted"
            >
              <ArrowLeft className="size-4 mr-2" />
              Back
            </Button>
            <div>
              <h1 className="text-3xl font-bold text-foreground">{displaySubject}</h1>
              <p className="text-sm text-muted-foreground mt-1">
                Master {displaySubject} with AI-guided learning
              </p>
            </div>
          </div>
        </div>

        {error && (
          <Alert variant="destructive">
            <AlertCircle className="size-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Progress Overview */}
        {progress && (
          <Card className="glass border-white/10 bg-gradient-to-r from-blue-500/10 to-purple-500/10">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="size-5 text-primary" />
                  Your Progress
                </CardTitle>
                <span className="text-2xl font-bold text-primary">{masteryPercentage}%</span>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="w-full bg-muted rounded-full h-3">
                <div 
                  className={`h-full rounded-full transition-all duration-300 ${progressBarColor}`}
                  style={{ width: `${masteryPercentage}%` }}
                />
              </div>
              <div className="grid grid-cols-3 gap-4 text-sm">
                <div>
                  <p className="text-muted-foreground">Sessions</p>
                  <p className="text-lg font-semibold">{progress.sessions_completed || 0}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Questions</p>
                  <p className="text-lg font-semibold">{progress.total_questions || 0}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Accuracy</p>
                  <p className="text-lg font-semibold">
                    {progress.total_questions > 0 
                      ? Math.round((progress.correct_answers / progress.total_questions) * 100)
                      : 0}%
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Tab Navigation */}
        <div className="flex gap-2 border-b border-white/10 overflow-x-auto">
          <button
            onClick={() => {
              setActiveTab('notes')
              setIsFlipped(false)
            }}
            className={`px-4 py-2 font-medium transition-colors whitespace-nowrap ${
              activeTab === 'notes'
                ? 'text-blue-400 border-b-2 border-blue-400'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            <div className="flex items-center gap-2">
              <BookOpen className="size-4" />
              Study Notes
            </div>
          </button>
          <button
            onClick={() => {
              setActiveTab('flashcards')
              setIsFlipped(false)
            }}
            className={`px-4 py-2 font-medium transition-colors whitespace-nowrap ${
              activeTab === 'flashcards'
                ? 'text-green-400 border-b-2 border-green-400'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            <div className="flex items-center gap-2">
              <Zap className="size-4" />
              Flashcards ({flashcards.length})
            </div>
          </button>
          <button
            onClick={() => {
              setActiveTab('revision')
              setIsFlipped(false)
            }}
            className={`px-4 py-2 font-medium transition-colors whitespace-nowrap ${
              activeTab === 'revision'
                ? 'text-red-400 border-b-2 border-red-400'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            <div className="flex items-center gap-2">
              <Target className="size-4" />
              Revision Guide
            </div>
          </button>
        </div>

        {/* Tab Content */}
        <div>
          {/* Study Notes Tab */}
          {activeTab === 'notes' && (
            <div className="space-y-6">
              {topics.length > 0 ? (
                topics.map((topic, idx) => (
                  <Card key={idx} className="glass border-blue-500/20 bg-gradient-to-r from-blue-500/5 to-transparent overflow-hidden">
                    <CardHeader className="bg-blue-500/10 pb-3">
                      <CardTitle className="text-lg text-blue-400">{topic.title}</CardTitle>
                    </CardHeader>
                    <CardContent className="pt-6 space-y-4">
                      <div>
                        <p className="text-sm font-semibold text-blue-300 mb-2">📚 Explanation</p>
                        <p className="text-sm text-muted-foreground leading-relaxed">{topic.explanation}</p>
                      </div>

                      {topic.keyPoints.length > 0 && (
                        <div>
                          <p className="text-sm font-semibold text-blue-300 mb-2">🔑 Key Points</p>
                          <ul className="space-y-1">
                            {topic.keyPoints.map((point, pidx) => (
                              <li key={pidx} className="flex gap-2 text-sm text-muted-foreground">
                                <span className="text-blue-400">•</span>
                                <span>{point}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {topic.formulas && topic.formulas.length > 0 && (
                        <div>
                          <p className="text-sm font-semibold text-blue-300 mb-2">📐 Formulas</p>
                          <div className="space-y-2 bg-black/30 p-3 rounded-lg">
                            {topic.formulas.map((formula, fidx) => (
                              <code key={fidx} className="text-xs text-blue-200 block font-mono">{formula}</code>
                            ))}
                          </div>
                        </div>
                      )}

                      <div>
                        <p className="text-sm font-semibold text-blue-300 mb-2">💡 Real-Life Example</p>
                        <p className="text-sm text-muted-foreground italic">{topic.realLifeExample}</p>
                      </div>
                    </CardContent>
                  </Card>
                ))
              ) : (
                <Card className="glass border-white/10">
                  <CardContent className="py-12 text-center">
                    <BookOpen className="size-8 mx-auto text-muted-foreground mb-3 opacity-50" />
                    <p className="text-muted-foreground">No study notes available yet. Generate notes to get started!</p>
                  </CardContent>
                </Card>
              )}
            </div>
          )}

          {/* Flashcards Tab */}
          {activeTab === 'flashcards' && (
            <div className="space-y-6">
              {currentFlashcard ? (
                <>
                  {/* Main Flashcard with 3D Flip */}
                  <div className="flex justify-center">
                    <div 
                      className="w-full max-w-2xl h-64 cursor-pointer perspective transition-transform duration-500 ease-in-out"
                      onClick={() => setIsFlipped(!isFlipped)}
                      style={{
                        transformStyle: 'preserve-3d',
                        transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
                      }}
                    >
                      <Card 
                        className="glass border-green-500/40 h-full flex items-center justify-center relative bg-gradient-to-br from-green-500/20 to-emerald-500/20"
                        style={{
                          backfaceVisibility: 'hidden',
                        }}
                      >
                        <CardContent className="text-center py-8">
                          <p className="text-sm text-muted-foreground mb-2">Question</p>
                          <p className="text-2xl font-semibold text-green-300">{currentFlashcard.front}</p>
                          <p className="text-xs text-muted-foreground mt-6 opacity-50">Click to reveal answer</p>
                        </CardContent>
                      </Card>

                      <Card 
                        className="glass border-green-500/40 h-full flex items-center justify-center absolute inset-0 bg-gradient-to-br from-emerald-500/20 to-green-500/20"
                        style={{
                          backfaceVisibility: 'hidden',
                          transform: 'rotateY(180deg)',
                        }}
                      >
                        <CardContent className="text-center py-8">
                          <p className="text-sm text-muted-foreground mb-2">Answer</p>
                          <p className="text-lg font-semibold text-green-300">{currentFlashcard.back}</p>
                          <p className="text-xs text-muted-foreground mt-6 opacity-50">Click to show question</p>
                        </CardContent>
                      </Card>
                    </div>
                  </div>

                  {/* Progress Bar */}
                  <div className="space-y-2">
                    <div className="flex justify-between items-center text-xs text-muted-foreground">
                      <span>Card {currentFlashcardIndex + 1} of {flashcards.length}</span>
                      <span>{Math.round(((currentFlashcardIndex + 1) / flashcards.length) * 100)}%</span>
                    </div>
                    <div className="w-full bg-muted rounded-full h-2">
                      <div 
                        className="h-full rounded-full bg-green-500 transition-all duration-300"
                        style={{ width: `${((currentFlashcardIndex + 1) / flashcards.length) * 100}%` }}
                      />
                    </div>
                  </div>

                  {/* Navigation */}
                  <div className="flex gap-4 justify-center">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handlePrevFlashcard}
                      disabled={currentFlashcardIndex === 0}
                      className="border-white/10"
                    >
                      <ChevronLeft className="size-4 mr-2" />
                      Previous
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handleNextFlashcard}
                      disabled={currentFlashcardIndex === flashcards.length - 1}
                      className="border-white/10"
                    >
                      Next
                      <ChevronRight className="size-4 ml-2" />
                    </Button>
                  </div>

                  {/* All Flashcards Grid */}
                  <div className="mt-8">
                    <h3 className="text-sm font-semibold text-green-300 mb-4">All Flashcards</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {flashcards.map((card, idx) => (
                        <button
                          key={idx}
                          onClick={() => {
                            setCurrentFlashcardIndex(idx)
                            setIsFlipped(false)
                          }}
                          className={`p-3 rounded-lg text-left text-sm transition-all ${
                            idx === currentFlashcardIndex
                              ? 'bg-green-500/30 border border-green-500/50 ring-2 ring-green-500/50'
                              : 'bg-muted border border-white/10 hover:border-green-500/30'
                          }`}
                        >
                          <p className="font-semibold text-green-300 mb-1 line-clamp-1">{card.front}</p>
                          <p className="text-muted-foreground text-xs line-clamp-2">{card.back}</p>
                        </button>
                      ))}
                    </div>
                  </div>
                </>
              ) : (
                <Card className="glass border-white/10">
                  <CardContent className="py-12 text-center">
                    <Zap className="size-8 mx-auto text-muted-foreground mb-3 opacity-50" />
                    <p className="text-muted-foreground">No flashcards available yet.</p>
                  </CardContent>
                </Card>
              )}
            </div>
          )}
          {activeTab === 'revision' && revisionGuide && (
            <div className="space-y-6">
              {/* Important Topics */}
              <Card className="glass border-yellow-500/20 bg-gradient-to-r from-yellow-500/5 to-transparent">
                <CardHeader className="bg-yellow-500/10 pb-3">
                  <CardTitle className="flex items-center gap-2 text-yellow-400">
                    <Lightbulb className="size-5" />
                    Important Topics to Master
                  </CardTitle>
                </CardHeader>
                <CardContent className="pt-6">
                  <ul className="space-y-2">
                    {revisionGuide.importantTopics.map((topic, idx) => (
                      <li key={idx} className="flex gap-3 text-sm">
                        <span className="text-yellow-400 font-bold">★</span>
                        <span className="text-muted-foreground">{topic}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              {/* Common Mistakes */}
              <Card className="glass border-red-500/20 bg-gradient-to-r from-red-500/5 to-transparent">
                <CardHeader className="bg-red-500/10 pb-3">
                  <CardTitle className="flex items-center gap-2 text-red-400">
                    <AlertTriangle className="size-5" />
                    Common Mistakes to Avoid
                  </CardTitle>
                </CardHeader>
                <CardContent className="pt-6">
                  <ul className="space-y-2">
                    {revisionGuide.commonMistakes.map((mistake, idx) => (
                      <li key={idx} className="flex gap-3 text-sm">
                        <span className="text-red-400 font-bold">⚠️</span>
                        <span className="text-muted-foreground">{mistake}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              {/* Quick Tips */}
              <Card className="glass border-purple-500/20 bg-gradient-to-r from-purple-500/5 to-transparent">
                <CardHeader className="bg-purple-500/10 pb-3">
                  <CardTitle className="flex items-center gap-2 text-purple-400">
                    <Brain className="size-5" />
                    Quick Study Tips
                  </CardTitle>
                </CardHeader>
                <CardContent className="pt-6">
                  <ul className="space-y-2">
                    {revisionGuide.quickTips.map((tip, idx) => (
                      <li key={idx} className="flex gap-3 text-sm">
                        <span className="text-purple-400 font-bold">💡</span>
                        <span className="text-muted-foreground">{tip}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </div>
          )}

          {activeTab === 'revision' && !revisionGuide && (
            <Card className="glass border-white/10">
              <CardContent className="py-12 text-center">
                <Target className="size-8 mx-auto text-muted-foreground mb-3 opacity-50" />
                <p className="text-muted-foreground">No revision guide available yet.</p>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Quick Action Button */}
        <div className="flex justify-center gap-4">
          <Button 
            onClick={() => router.push(`/quiz?subject=${encodeURIComponent(displaySubject)}`)}
            className="neon-ring bg-primary text-primary-foreground hover:bg-primary/90"
          >
            <Zap className="size-4 mr-2" />
            Take a Quiz
          </Button>
          <Button 
            variant="outline"
            className="border-white/10 hover:bg-muted"
            onClick={() => router.push('/smart-notes')}
          >
            <BookOpen className="size-4 mr-2" />
            Generate Custom Notes
          </Button>
        </div>
      </main>
    </div>
  )
}
