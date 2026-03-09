"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"

export default function RegisterPage() {

const router = useRouter()

const [name,setName] = useState("")
const [email,setEmail] = useState("")
const [password,setPassword] = useState("")

const handleRegister = async (e:any) => {

e.preventDefault()

const res = await fetch("http://127.0.0.1:8000/api/auth/register",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body: JSON.stringify({
name,
email,
password
})
})

if(res.ok){
alert("Account created successfully")
router.push("/login")
}else{
alert("Registration failed")
}

}

return(

<div style={{padding:"40px"}}>

<h1>Register</h1>

<form onSubmit={handleRegister}>

<input
placeholder="Name"
onChange={(e)=>setName(e.target.value)}
/>

<br/><br/>

<input
placeholder="Email"
onChange={(e)=>setEmail(e.target.value)}
/>

<br/><br/>

<input
type="password"
placeholder="Password"
onChange={(e)=>setPassword(e.target.value)}
/>

<br/><br/>

<button type="submit">
Register
</button>

</form>

</div>

)

}