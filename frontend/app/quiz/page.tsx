"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"

export default function QuizPage(){

const router = useRouter()

const [answer,setAnswer] = useState("")

const submitQuiz = async () => {

const res = await fetch("http://127.0.0.1:8000/api/recommendations/analyze",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body: JSON.stringify({
concept:"Fractions",
correct:2,
total:5,
time_spent:25
})

})

const data = await res.json()

localStorage.setItem("ml_result",JSON.stringify(data))

router.push("/dashboard")

}

return(

<div style={{padding:"40px"}}>

<h1>Quiz</h1>

<p>What is 1/2 + 1/4 ?</p>

<input
value={answer}
onChange={(e)=>setAnswer(e.target.value)}
placeholder="Enter answer"
/>

<br/><br/>

<button onClick={submitQuiz}>
Submit Quiz
</button>

</div>

)

}