"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import {
  daysUntilClose,
  fetchTenderMeta,
  fetchTenders,
  formatDate,
  tenderTypeLabel,
  type Tender,
  type TenderMeta,
} from "@/lib/api";

export default function HomePage() {
  const [tenders, setTenders] = useState<Tender[]>([]);
  const [meta, setMeta] = useState<TenderMeta | null>(null);
  const [total, setTotal] = useState(0);
  const [q, setQ] = useState("");
  const [province, setProvince] = useState("");
  const [tenderType, setTenderType] = useState("");
  const [source, setSource] = useState("");
  const [sort, setSort] = useState("newest");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const params: Record<string, string> = { date_filter: "open", sort };
      if (q) params.q = q;
      if (province) params.province = province;
      if (tenderType) params.tender_type = tenderType;
      if (source) params.source = source;
      const [list, filterMeta] = await Promise.all([
        fetchTenders(params),
        meta ? Promise.resolve(meta) : fetchTenderMeta(),
      ]);
      setTenders(list.results);
      setTotal(list.count);
      if (!meta) setMeta(filterMeta);
    } catch {
      setError("Could not load tenders. Make sure the Django server is running on port 8000.");
    } finally {
      setLoading(false);
    }
  }, [q, province, tenderType, source, sort, meta]);

  useEffect(() => {
    load();
  }, [load]);

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    load();
  }

  const inputClass =
    "w-full rounded-lg border border-[var(--border)] bg-white px-3 py-2.5 text-sm outline-none focus:border-[var(--navy-light)] focus:ring-2 focus:ring-[var(--navy-light)]/10";

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-50 bg-gradient-to-r from-[var(--navy)] to-[var(--navy-light)] text-white shadow-lg">
        <div className="mx-auto flex max-w-6xl items-center gap-3 px-4 py-4">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-[var(--gold)] text-lg">
            📡
          </span>
          <div>
            <p className="text-lg font-bold leading-tight">TenderRadar</p>
            <p className="text-xs opacity-70">SA Tender Discovery</p>
          </div>
        </div>
      </header>

      <section className="bg-gradient-to-b from-[var(--navy-light)] to-[var(--navy)] px-4 pb-10 pt-8 text-center text-white">
        <h1 className="mx-auto max-w-2xl text-3xl font-bold tracking-tight md:text-4xl">
          Find tenders &amp; RFQs across South Africa
        </h1>
        <p className="mx-auto mt-3 max-w-xl text-sm opacity-85 md:text-base">
          Government, municipalities, SOCs and private-sector opportunities — no account needed.
        </p>
        {!loading && (
          <p className="mt-5 text-2xl font-bold text-[var(--gold)]">{total} open tenders</p>
        )}
      </section>

      <main className="mx-auto max-w-6xl px-4 pb-16 pt-6">
        <form
          onSubmit={handleSearch}
          className="-mt-8 rounded-xl border border-[var(--border)] bg-white p-5 shadow-lg"
        >
          <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">
            Filter &amp; search
          </p>
          <div className="grid gap-3 md:grid-cols-6">
            <input
              className={`md:col-span-2 ${inputClass}`}
              placeholder="Keywords — cleaning, security, IT…"
              value={q}
              onChange={(e) => setQ(e.target.value)}
            />
            <select className={inputClass} value={province} onChange={(e) => setProvince(e.target.value)}>
              <option value="">All provinces</option>
              {meta?.provinces.map((p) => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
            <select className={inputClass} value={tenderType} onChange={(e) => setTenderType(e.target.value)}>
              <option value="">All types</option>
              {meta?.tender_types.map((t) => (
                <option key={t.value} value={t.value}>{t.label}</option>
              ))}
            </select>
            <select className={inputClass} value={source} onChange={(e) => setSource(e.target.value)}>
              <option value="">All sources</option>
              {meta?.sources.map((s) => (
                <option key={s.slug} value={s.slug}>{s.name}</option>
              ))}
            </select>
            <select className={inputClass} value={sort} onChange={(e) => setSort(e.target.value)}>
              <option value="newest">Newest first</option>
              <option value="closing_soon">Closing soon</option>
              <option value="closing_latest">Closing latest</option>
            </select>
          </div>
          <button
            type="submit"
            className="mt-4 rounded-lg bg-[var(--gold)] px-6 py-2.5 text-sm font-semibold text-[var(--navy)] hover:opacity-90"
          >
            Search tenders
          </button>
        </form>

        {loading && <p className="mt-8 text-center text-[var(--muted)]">Loading tenders…</p>}
        {error && <p className="mt-8 text-center text-red-600">{error}</p>}

        {!loading && !error && (
          <div className="mt-6 space-y-3">
            {tenders.length === 0 ? (
              <div className="rounded-xl border-2 border-dashed border-[var(--border)] bg-white py-16 text-center">
                <h3 className="font-semibold text-[var(--navy)]">No tenders found</h3>
                <p className="mt-2 text-sm text-[var(--muted)]">
                  Run <code className="rounded bg-[var(--surface)] px-1.5 py-0.5">python manage.py scrape_tenders</code> to load data.
                </p>
              </div>
            ) : (
              tenders.map((t) => {
                const days = daysUntilClose(t.closing_date);
                const urgent = days !== null && days <= 7 && days >= 0;
                return (
                  <Link
                    key={t.id}
                    href={t.download_url || t.url}
                    target="_blank"
                    className="block rounded-xl border border-[var(--border)] bg-white p-5 transition hover:border-[var(--navy-light)] hover:shadow-md"
                  >
                    <div className="flex flex-col gap-4 md:flex-row md:justify-between">
                      <div className="flex-1">
                        <h2 className="font-semibold text-[var(--navy)] leading-snug">{t.title}</h2>
                        <p className="mt-1 text-sm text-[var(--muted)]">
                          {[t.department, t.province, t.category].filter(Boolean).join(" · ")}
                        </p>
                        {t.description && (
                          <p className="mt-2 line-clamp-2 text-sm text-[var(--muted)]">{t.description}</p>
                        )}
                        <div className="mt-3 flex flex-wrap gap-2">
                          <span className="rounded-full bg-[var(--gold-soft)] px-2.5 py-0.5 text-xs font-semibold text-[#7a5a18]">
                            {tenderTypeLabel(t.tender_type)}
                          </span>
                          <span className="rounded-full bg-[#e8eef5] px-2.5 py-0.5 text-xs font-semibold text-[var(--navy-light)]">
                            {t.source.name}
                          </span>
                        </div>
                      </div>
                      <div className="shrink-0 text-left md:text-right">
                        <p className="text-xs font-semibold uppercase tracking-wide text-[var(--muted)]">Closes</p>
                        <p className={`text-base font-bold ${urgent ? "text-[var(--urgent)]" : "text-[var(--success)]"}`}>
                          {formatDate(t.closing_date)}
                        </p>
                        {days !== null && days >= 0 && (
                          <span className={`mt-1 inline-block rounded-md px-2 py-0.5 text-xs font-semibold ${urgent ? "bg-red-50 text-[var(--urgent)]" : "bg-green-50 text-[var(--success)]"}`}>
                            {days === 0 ? "Closes today" : `${days} day${days === 1 ? "" : "s"} left`}
                          </span>
                        )}
                        <p className="mt-2 text-sm font-semibold text-[var(--gold)]">View tender →</p>
                      </div>
                    </div>
                  </Link>
                );
              })
            )}
          </div>
        )}
      </main>

      <footer className="bg-[var(--navy)] py-6 text-center text-sm text-white/60">
        TenderRadar — public tender data from eTenders, Tenders-SA and other sources.
      </footer>
    </div>
  );
}
