"use client"

import { useEffect, useState } from "react"
import { DashboardNavbar } from "@/components/dashboard-navbar"
import { Button } from "@/components/ui/button"
import { Clock, CheckCircle2, XCircle, Loader } from "lucide-react"
import Link from "next/link"

interface QuizQuestion {
  question: string
  options: string[]
  difficulty: string
}

interface QuizData {
  topic: string
  difficulty: string
  total_questions: number
  questions: QuizQuestion[]
}

interface SubmitResult {
  is_correct: boolean
  explanation: string
  correct_option: number
  selected_option: number
  mastery_update: number
  message: string
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://192.168.0.131:8001"
const TOPICS = ["Fractions", "Algebra", "Loops", "Variables", "Functions", "Motion", "Grammar", "Reasoning"]

export default function QuizPage() {
  const [stage, setStage] = useState<"topic-select" | "difficulty-select" | "quiz" | "results">("topic-select")
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null)
  const [selectedDifficulty, setSelectedDifficulty] = useState<"easy" | "medium" | "hard" | null>(null)
  const [quizData, setQuizData] = useState<QuizData | null>(null)
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const [timeLeft, setTimeLeft] = useState(0)
  const [results, setResults] = useState<SubmitResult[]>([])
  const [mastery, setMastery] = useState(0)
  const [questionStartTime, setQuestionStartTime] = useState(Date.now())

  // Timer effect
  useEffect(() => {
    if (stage !== "quiz" || loading) return
    
    const timer = setInterval(() => {
      setTimeLeft(prev => prev > 0 ? prev - 1 : 0)
    }, 1000)
    
    return () => clearInterval(timer)
  }, [stage, loading])

  const startQuiz = async () => {
    if (!selectedTopic || !selectedDifficulty) return

    setLoading(true)
    try {
      const token = localStorage.getItem("access_token")
      if (!token) {
        window.location.href = "/login"
        return
      }

      const response = await fetch(
        `${API_BASE_URL}/api/quiz/generate/${selectedTopic}?count=5&difficulty=${selectedDifficulty}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      )

      if (!response.ok) throw new Error("Failed to load quiz")

      const data = await response.json()
      setQuizData(data)
      setCurrentQuestion(0)
      setResults([])
      setSelectedAnswer(null)
      setTimeLeft(5 * 60)
      setQuestionStartTime(Date.now())
      setStage("quiz")
    } catch (err) {
      console.error("Error loading quiz:", err)
      alert("Failed to load quiz. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  const handleAnswerSubmit = async () => {
    if (selectedAnswer === null || !quizData) return

    setLoading(true)
    try {
      const token = localStorage.getItem("access_token")
      const timeTaken = Math.floor((Date.now() - questionStartTime) / 1000)

      const response = await fetch(`${API_BASE_URL}/api/quiz/submit-answer`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          topic: selectedTopic,
          question_index: currentQuestion,
          selected_option: selectedAnswer,
          time_taken: timeTaken,
        }),
      })

      if (!response.ok) throw new Error("Failed to submit answer")

      const result: SubmitResult = await response.json()
      const newResults = [...results, result]
      setResults(newResults)
      setMastery(result.mastery_update)

      if (currentQuestion < quizData.total_questions - 1) {
        setCurrentQuestion(currentQuestion + 1)
        setSelectedAnswer(null)
        setQuestionStartTime(Date.now())
      } else {
        setStage("results")
      }
    } catch (err) {
      console.error("Error submitting answer:", err)
      alert("Failed to submit answer. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  const minutes = String(Math.floor(timeLeft / 60)).padStart(2, "0")
  const seconds = String(timeLeft % 60).padStart(2, "0")
  const progress = ((currentQuestion + 1) / (quizData?.total_questions || 1)) * 100
  const correctAnswers = results.filter(r => r.is_correct).length

  return (
    <div className="min-h-screen bg-[#0B0F1A]">
      <DashboardNavbar />
      <main className="mx-auto max-w-4xl px-4 py-10 lg:px-8">
        {/* TOPIC SELECTION */}
        {stage === "topic-select" && (
          <>
            <div className="mb-12 text-center">
              <h1 className="text-4xl font-bold text-white">Choose a Topic</h1>
              <p className="mt-3 text-gray-400">Select what you'd like to practice today</p>
            </div>

            <div className="grid gap-4 md:grid-cols-4 sm:grid-cols-2">
              {TOPICS.map((topic) => (
                <button
                  key={topic}
                  onClick={() => {
                    setSelectedTopic(topic)
                    setStage("difficulty-select")
                  }}
                  className="glass rounded-lg p-6 text-center transition-all border border-white/10 bg-white/5 hover:bg-white/10"
                >
                  <p className="font-semibold text-white">{topic}</p>
                  <p className="mt-2 text-xs text-gray-400">Click to select</p>
                </button>
              ))}
            </div>
          </>
        )}

        {/* DIFFICULTY SELECTION */}
        {stage === "difficulty-select" && (
          <>
            <div className="mb-12 text-center">
              <h1 className="text-4xl font-bold text-white">Select Difficulty</h1>
              <p className="mt-3 text-gray-400">
                Topic: <span className="text-blue-400 font-semibold">{selectedTopic}</span>
              </p>
            </div>

            <div className="grid gap-6 md:grid-cols-3 mb-8">
              {[
                { level: "easy" as const, label: "Easy", description: "Build your foundation", icon: "🌱" },
                { level: "medium" as const, label: "Medium", description: "Challenge yourself", icon: "⚡" },
                { level: "hard" as const, label: "Hard", description: "Master the concept", icon: "🔥" },
              ].map(({ level, label, description, icon }) => (
                <button
                  key={level}
                  onClick={() => {
                    setSelectedDifficulty(level)
                    startQuiz()
                  }}
                  disabled={loading}
                  className="glass rounded-lg p-8 text-center transition-all border-2 border-white/10 bg-white/5 hover:bg-white/10 disabled:opacity-50"
                >
                  <div className="text-4xl mb-3">{icon}</div>
                  <p className="text-xl font-semibold text-white">{label}</p>
                  <p className="mt-2 text-sm text-gray-400">{description}</p>
                </button>
              ))}
            </div>

            <div className="flex gap-4">
              <Button
                onClick={() => {
                  setSelectedTopic(null)
                  setStage("topic-select")
                }}
                variant="outline"
                className="flex-1"
              >
                ← Back
              </Button>
            </div>
          </>
        )}

        {/* QUIZ */}
        {stage === "quiz" && quizData && quizData.questions[currentQuestion] && (
          <>
            <div className="mb-8">
              <div className="flex justify-between items-center mb-4">
                <div>
                  <p className="text-sm text-gray-400">Question {currentQuestion + 1}/{quizData.total_questions}</p>
                  <h2 className="text-2xl font-bold text-white mt-1">{selectedTopic}</h2>
                </div>
                <div className="flex items-center gap-2 rounded-lg border border-white/10 bg-white/5 px-4 py-2">
                  <Clock className="h-4 w-4 text-blue-400" />
                  <span className="text-white">{minutes}:{seconds}</span>
                </div>
              </div>
              <div className="h-2 w-full rounded-full bg-white/10 overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>

            <div className="glass rounded-lg p-8 bg-white/5 border border-white/10 mb-8">
              <p className="text-lg text-white mb-6">{quizData.questions[currentQuestion].question}</p>

              <div className="space-y-3">
                {quizData.questions[currentQuestion].options.map((option, idx) => (
                  <button
                    key={idx}
                    onClick={() => setSelectedAnswer(idx)}
                    className={`w-full p-4 rounded-lg border-2 transition-all text-left ${
                      selectedAnswer === idx
                        ? "border-blue-500 bg-blue-500/20 text-white"
                        : "border-white/10 bg-white/5 text-gray-300 hover:bg-white/10"
                    }`}
                  >
                    <span className="font-semibold">{String.fromCharCode(65 + idx)}.</span> {option}
                  </button>
                ))}
              </div>
            </div>

            <Button
              onClick={handleAnswerSubmit}
              disabled={selectedAnswer === null || loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3"
            >
              {loading ? <Loader className="h-4 w-4 mr-2 animate-spin" /> : null}
              {currentQuestion === quizData.total_questions - 1 ? "Finish" : "Next"} →
            </Button>
          </>
        )}

        {/* RESULTS */}
        {stage === "results" && quizData && (
          <>
            <div className="text-center mb-12">
              <div className="text-6xl mb-4">{correctAnswers === quizData.total_questions ? "🎉" : "✨"}</div>
              <h1 className="text-4xl font-bold text-white">Quiz Complete!</h1>
              <p className="mt-4 text-gray-400">
                Your mastery score: <span className="text-blue-400 text-2xl font-bold">{Math.round(mastery)}%</span>
              </p>
            </div>

            <div className="grid gap-6 md:grid-cols-3 mb-8">
              <div className="glass rounded-lg p-6 bg-white/5 border border-white/10 text-center">
                <p className="text-gray-400 text-sm">Correct Answers</p>
                <p className="text-3xl font-bold text-green-400 mt-2">{correctAnswers}/{quizData.total_questions}</p>
              </div>
              <div className="glass rounded-lg p-6 bg-white/5 border border-white/10 text-center">
                <p className="text-gray-400 text-sm">Accuracy</p>
                <p className="text-3xl font-bold text-blue-400 mt-2">{Math.round((correctAnswers / quizData.total_questions) * 100)}%</p>
              </div>
              <div className="glass rounded-lg p-6 bg-white/5 border border-white/10 text-center">
                <p className="text-gray-400 text-sm">Difficulty</p>
                <p className="text-3xl font-bold text-purple-400 mt-2 capitalize">{quizData.difficulty}</p>
              </div>
            </div>

            <div className="space-y-4">
              {results.map((result, idx) => (
                <div key={idx} className={`glass rounded-lg p-6 border-2 ${
                  result.is_correct ? "border-green-500/30 bg-green-500/5" : "border-red-500/30 bg-red-500/5"
                }`}>
                  <div className="flex items-start gap-4">
                    {result.is_correct ? (
                      <CheckCircle2 className="h-6 w-6 text-green-400 flex-shrink-0 mt-1" />
                    ) : (
                      <XCircle className="h-6 w-6 text-red-400 flex-shrink-0 mt-1" />
                    )}
                    <div className="flex-1">
                      <p className="text-white font-semibold">Question {idx + 1}</p>
                      <p className={`mt-2 ${result.is_correct ? "text-green-300" : "text-red-300"}`}>
                        {result.message}
                      </p>
                      <p className="text-sm text-gray-400 mt-2">{result.explanation}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex gap-4 mt-8">
              <Link href="/dashboard" className="flex-1">
                <Button variant="outline" className="w-full">
                  Back to Dashboard
                </Button>
              </Link>
              <Button
                onClick={() => {
                  setStage("topic-select")
                  setSelectedTopic(null)
                  setSelectedDifficulty(null)
                  setResults([])
                }}
                className="flex-1 bg-blue-600 hover:bg-blue-700"
              >
                Try Another Quiz
              </Button>
            </div>
          </>
        )}
      </main>
    </div>
  )
}