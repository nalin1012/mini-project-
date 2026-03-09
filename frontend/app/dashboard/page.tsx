"use client"

import { useEffect, useState } from "react"
import Link from "next/link"

export default function DashboardPage(){

const [mlData,setMlData] = useState<any>(null)
const [user,setUser] = useState("")

useEffect(()=>{

const stored = localStorage.getItem("ml_result")
const username = localStorage.getItem("user")

if(stored){
setMlData(JSON.parse(stored))
}

if(username){
setUser(username)
}

},[])

return(

<div style={{padding:"40px"}}>

<h1>Dashboard</h1>

<h2>Welcome {user}</h2>

<br/>

<Link href="/quiz">
<button>
Start Quiz
</button>
</Link>

<br/><br/>

{mlData && (

<div>

<h3>AI Analysis</h3>

<p>
Mastery Score: {mlData.mastery_score}
</p>

<p>
Knowledge Gap: {mlData.knowledge_gap}
</p>

<p>
Recommendation: {mlData.recommendation}
</p>

</div>

)}

</div>

)

}
