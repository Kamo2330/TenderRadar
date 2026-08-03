"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { fetchTenders, type Tender } from "@/lib/api";

export default function DashboardPage() {
  const router = useRouter();
  const [tenders, setTenders] = useState<Tender[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("tenderradar_token");
    if (!token) {
      router.replace("/login");
      return;
    }
    fetchTenders(token, { date_filter: "open" })
      .then((data) => setTenders(data.results))
      .catch(() => setError("Could not load tenders. Is the Django API running on port 8000?"));
  }, [router]);

  return (
    <div className="min-h-screen p-8">
      <h1 className="text-2xl font-bold">TenderRadar Dashboard</h1>
      {error && <p className="mt-4 text-red-400">{error}</p>}
      <div className="mt-6 space-y-3">
        {tenders.map((t) => (
          <article key={t.id} className="rounded-xl border border-[var(--border)] bg-[var(--card)] p-4">
            <h2 className="font-semibold">{t.title}</h2>
            <p className="text-sm text-[var(--muted)]">{t.department} · {t.province}</p>
            <Link href={t.download_url || t.url} target="_blank" className="text-sm text-[var(--accent)]">
              View tender
            </Link>
          </article>
        ))}
      </div>
    </div>
  );
}
