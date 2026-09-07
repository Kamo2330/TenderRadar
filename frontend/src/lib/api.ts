const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000/api";

export type Tender = {
  id: number;
  title: string;
  description: string;
  department: string;
  category: string;
  tender_type: string;
  province: string;
  published_date: string | null;
  closing_date: string | null;
  url: string;
  download_url: string;
  source: { name: string; slug: string };
};

export type TenderListResponse = {
  count: number;
  next: string | null;
  previous: string | null;
  results: Tender[];
};

export type TenderMeta = {
  tender_types: { value: string; label: string }[];
  provinces: string[];
  sources: { slug: string; name: string }[];
};

export async function fetchTenders(params: Record<string, string> = {}) {
  const query = new URLSearchParams(params).toString();
  const res = await fetch(`${API_URL}/tenders/?${query}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load tenders");
  return res.json() as Promise<TenderListResponse>;
}

export async function fetchTenderMeta() {
  const res = await fetch(`${API_URL}/tenders/meta/`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load filters");
  return res.json() as Promise<TenderMeta>;
}

export function daysUntilClose(closingDate: string | null): number | null {
  if (!closingDate) return null;
  const close = new Date(closingDate);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  close.setHours(0, 0, 0, 0);
  return Math.ceil((close.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
}

export function formatDate(value: string | null) {
  if (!value) return "TBC";
  return new Date(value).toLocaleDateString("en-ZA", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

export function tenderTypeLabel(value: string) {
  return value.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}
