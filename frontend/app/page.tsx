import { LoginForm } from "@/components/login-form"

export default function LoginPage() {
  return (
    <main className="flex min-h-svh items-center justify-center bg-login-bg px-4 py-12">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-1/3 left-1/2 h-[820px] w-[820px] -translate-x-1/2 rounded-full bg-primary/15 blur-3xl" />
        <div className="absolute bottom-0 left-0 h-[420px] w-[420px] rounded-full bg-[#7B61FF]/15 blur-3xl" />
        <div className="absolute right-0 top-1/3 h-[320px] w-[320px] rounded-full bg-emerald-400/10 blur-3xl" />
      </div>
      <LoginForm />
    </main>
  )
}
