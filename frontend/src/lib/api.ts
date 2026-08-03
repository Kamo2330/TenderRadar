const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000/api";

export type User = {
  id: number;
  username: string;
  email: string;
  is_staff: boolean;
  is_client: boolean;
};

export type Tender = {
  id: number;
  title: string;
  description: string;
  department: string;
  province: string;
  closing_date: string | null;
  url: string;
  download_url: string;
  source: { name: string; slug: string };
};

export type TenderListResponse = {
  count: number;
  results: Tender[];
};

function authHeaders(token: string): HeadersInit {
  return { Authorization: `Token ${token}`, "Content-Type": "application/json" };
}

export async function login(username: string, password: string) {
  const res = await fetch(`${API_URL}/auth/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error("Invalid credentials");
  return res.json() as Promise<{ token: string; user: User }>;
}

export type RegisterPayload = {
  username: string;
  email: string;
  password: string;
  company_name: string;
};

export async function register(payload: RegisterPayload) {
  const res = await fetch(`${API_URL}/auth/register/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    const message =
      typeof data.detail === "string"
        ? data.detail
        : Object.values(data).flat().join(" ") || "Could not create account.";
    throw new Error(message);
  }
  return res.json() as Promise<{ token: string; user: User }>;
}

export async function fetchTenders(token: string, params: Record<string, string> = {}) {
  const query = new URLSearchParams(params).toString();
  const res = await fetch(`${API_URL}/tenders/?${query}`, {
    headers: authHeaders(token),
    cache: "no-store",
  });
  if (!res.ok) throw new Error("Failed to load tenders");
  return res.json() as Promise<TenderListResponse>;
}
