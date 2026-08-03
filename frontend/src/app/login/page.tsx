"use client";

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

  return (
    <main className="flex min-h-screen items-center justify-center px-4">
      <form onSubmit={handleSubmit} className="w-full max-w-md rounded-2xl border border-[var(--border)] bg-[var(--card)] p-8">
        <h1 className="text-2xl font-bold">TenderRadar</h1>
        <p className="mt-2 text-sm text-[var(--muted)]">Sign in to browse tenders.</p>
        <input
          className="mt-6 w-full rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          className="mt-3 w-full rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <p className="mt-2 text-sm text-red-400">{error}</p>}
        <button type="submit" className="mt-4 w-full rounded-lg bg-[var(--accent)] py-2 font-medium text-slate-900">
          Sign in
        </button>
      </form>
    </main>
  );
}
