import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-4 text-center">
      <h1 className="text-4xl font-bold">TenderRadar</h1>
      <p className="mt-3 max-w-md text-[var(--muted)]">
        Discover South African tenders and RFQs in one place.
      </p>
      <div className="mt-8 flex w-full max-w-xs flex-col gap-3">
        <Link
          href="/signup"
          className="rounded-lg bg-[var(--accent)] py-3 font-medium text-slate-900"
        >
          Create account
        </Link>
        <Link
          href="/login"
          className="rounded-lg border border-[var(--border)] py-3 font-medium hover:border-[var(--accent)]"
        >
          Sign in
        </Link>
      </div>
    </main>
  );
}
