'use client'

import * as React from 'react'
import { X, Lightbulb } from 'lucide-react'

const TUTOR_TIPS = [
  "💡 Tip: Use the Pomodoro technique - study for 25 minutes, then take a 5-minute break.",
  "🧠 Memory hack: Try the method of loci - associate information with familiar locations.",
  "📝 Note-taking: Use the Cornell method for better organization and review.",
  "🎯 Focus areas: Review your weak areas regularly to improve faster.",
  "⚡ Quick wins: Start with easier questions to build confidence.",
  "🔄 Spaced repetition: Review material at increasing intervals for better retention.",
  "✍️ Practice writing: Explain concepts in your own words to deepen understanding.",
  "🎮 Gamification: Complete quizzes daily to maintain your study streak!",
  "📚 Active learning: Test yourself before reading the notes.",
  "🤝 Group study: Teaching others helps reinforce your own understanding.",
]

export function TutorTip() {
  const [isVisible, setIsVisible] = React.useState(true)
  const [currentTip, setCurrentTip] = React.useState(0)

  const nextTip = () => {
    setCurrentTip((prev) => (prev + 1) % TUTOR_TIPS.length)
  }

  if (!isVisible) {
    return (
      <button
        onClick={() => setIsVisible(true)}
        className="fixed bottom-4 right-4 z-40 p-3 rounded-full bg-blue-500 hover:bg-blue-600 text-white shadow-lg hover:shadow-xl transition-all"
        aria-label="Show tutor tip"
        title="Show tutor tip"
      >
        <Lightbulb className="h-5 w-5" />
      </button>
    )
  }

  return (
    <div className="fixed bottom-4 right-4 z-40 max-w-xs">
      <div className="glass rounded-lg p-4 bg-blue-500/10 border border-blue-400/30 shadow-lg backdrop-blur-sm">
        <div className="flex items-start justify-between gap-3 mb-2">
          <div className="flex items-start gap-2 flex-1">
            <Lightbulb className="h-5 w-5 text-blue-400 mt-0.5 flex-shrink-0" />
            <p className="text-sm text-white leading-relaxed">{TUTOR_TIPS[currentTip]}</p>
          </div>
          <button
            onClick={() => setIsVisible(false)}
            className="text-blue-300 hover:text-blue-200 transition-colors flex-shrink-0"
            aria-label="Close tip"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
        <button
          onClick={nextTip}
          className="text-xs text-blue-300 hover:text-blue-200 transition-colors mt-2"
        >
          Next tip →
        </button>
      </div>
    </div>
  )
}
