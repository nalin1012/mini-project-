"use client"

import { useEffect,useState } from "react"

export default function ResultsPage(){

const [result,setResult] = useState<any>(null)

useEffect(()=>{

const stored = localStorage.getItem("result")

if(stored){
setResult(JSON.parse(stored))
}

},[])

if(!result) return <p>Loading...</p>

return(

<div>

<h1>Quiz Results</h1>

<p>Mastery Score: {result.mastery_score}</p>

<p>Knowledge Gap: {result.knowledge_gap}</p>

<p>Recommendation: {result.recommendation}</p>

</div>

)

}