"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { register } from "@/lib/api";

export default function SignUpPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");

    if (password !== passwordConfirm) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);
    try {
      const { token } = await register({
        username,
        email,
        password,
        company_name: companyName,
      });
      localStorage.setItem("tenderradar_token", token);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not create account.");
    } finally {
      setLoading(false);
    }
  }

  const inputClass =
    "w-full rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2 outline-none focus:border-[var(--accent)]";

  return (
    <main className="flex min-h-screen items-center justify-center px-4">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md rounded-2xl border border-[var(--border)] bg-[var(--card)] p-8"
      >
        <h1 className="text-2xl font-bold">Create account</h1>
        <p className="mt-2 text-sm text-[var(--muted)]">
          Sign up to browse tenders and set alert preferences.
        </p>

        <label className="mt-6 block text-sm text-[var(--muted)]" htmlFor="username">
          Username
        </label>
        <input
          id="username"
          className={`mt-1 ${inputClass}`}
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <label className="mt-3 block text-sm text-[var(--muted)]" htmlFor="email">
          Email
        </label>
        <input
          id="email"
          type="email"
          className={`mt-1 ${inputClass}`}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <label className="mt-3 block text-sm text-[var(--muted)]" htmlFor="company">
          Company name
        </label>
        <input
          id="company"
          className={`mt-1 ${inputClass}`}
          value={companyName}
          onChange={(e) => setCompanyName(e.target.value)}
          required
        />

        <label className="mt-3 block text-sm text-[var(--muted)]" htmlFor="password">
          Password
        </label>
        <input
          id="password"
          type="password"
          className={`mt-1 ${inputClass}`}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          minLength={8}
          required
        />

        <label className="mt-3 block text-sm text-[var(--muted)]" htmlFor="password2">
          Confirm password
        </label>
        <input
          id="password2"
          type="password"
          className={`mt-1 ${inputClass}`}
          value={passwordConfirm}
          onChange={(e) => setPasswordConfirm(e.target.value)}
          minLength={8}
          required
        />

        {error && <p className="mt-3 text-sm text-red-400">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="mt-4 w-full rounded-lg bg-[var(--accent)] py-2.5 font-medium text-slate-900 disabled:opacity-50"
        >
          {loading ? "Creating account…" : "Create account"}
        </button>

        <p className="mt-4 text-center text-sm text-[var(--muted)]">
          Already have an account?{" "}
          <Link href="/login" className="text-[var(--accent)] hover:underline">
            Sign in
          </Link>
        </p>
      </form>
    </main>
  );
}
