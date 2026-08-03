"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { login } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    try {
      const { token } = await login(username, password);
      localStorage.setItem("tenderradar_token", token);
      router.push("/dashboard");
    } catch {
      setError("Invalid username or password.");
    }
  }

  const inputClass =
    "w-full rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2 outline-none focus:border-[var(--accent)]";

  return (
    <main className="flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-md rounded-2xl border border-[var(--border)] bg-[var(--card)] p-8">
        <h1 className="text-2xl font-bold">Sign in</h1>
        <p className="mt-2 text-sm text-[var(--muted)]">Welcome back to TenderRadar.</p>

        <form onSubmit={handleSubmit} className="mt-6">
          <input
            className={inputClass}
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            className={`mt-3 ${inputClass}`}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <p className="mt-2 text-sm text-red-400">{error}</p>}
          <button
            type="submit"
            className="mt-4 w-full rounded-lg bg-[var(--accent)] py-2.5 font-medium text-slate-900"
          >
            Sign in
          </button>
        </form>

        <div className="my-6 border-t border-[var(--border)]" />

        <p className="mb-3 text-center text-sm text-[var(--muted)]">New here?</p>
        <Link
          href="/signup"
          className="block w-full rounded-lg border border-[var(--accent)] py-2.5 text-center font-medium text-[var(--accent)] hover:bg-[var(--accent)] hover:text-slate-900"
        >
          Create account
        </Link>
      </div>
    </main>
  );
}
