const BASE = (import.meta.env.VITE_API_URL ?? "").replace(/\/$/, "");

/*
  Types (frontend = camelCase). Backend uses snake_case; we map on receive/send.
  Strict: do not add fields.
*/
export type Cv = {
  id: number;
  userId: number;
  title: string;
  location?: string | null;
  experienceYears?: number;
  skills: string[];
  summary?: string | null;
  fullText?: string | null;
  createdAt: string;
};

export type CvCreatePayload = {
  title: string;
  location?: string | null;
  experienceYears?: number;
  skills?: string[];
  summary?: string | null;
  fullText?: string | null;
};

export type CvUpdatePayload = Partial<CvCreatePayload>;

export type StatusResponse = { status: string };

export type ApiError = { status: number; message: string; details?: unknown };

function getAuthHeader(): Record<string, string> {
  try {
    const t = typeof localStorage !== "undefined" ? localStorage.getItem("token") : null;
    return t ? { Authorization: `Bearer ${t}` } : {};
  } catch {
    return {};
  }
}

/* Backend (snake_case) types used for internal assertions/mapping */
type BackendCv = {
  id: number;
  user_id: number;
  title: string;
  location?: string | null;
  experience_years?: number;
  skills: string[];
  summary?: string | null;
  full_text?: string | null;
  created_at: string;
};

function mapBackendCv(b: BackendCv): Cv {
  return {
    id: b.id,
    userId: b.user_id,
    title: b.title,
    location: b.location ?? null,
    experienceYears: b.experience_years,
    skills: Array.isArray(b.skills) ? b.skills : [],
    summary: b.summary ?? null,
    fullText: b.full_text ?? null,
    createdAt: b.created_at,
  };
}

function buildSnakePayload(payload: CvUpdatePayload | CvCreatePayload): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  if ("title" in payload && payload.title !== undefined) out.title = payload.title;
  if ("location" in payload && payload.location !== undefined) out.location = payload.location;
  if ("experienceYears" in payload && payload.experienceYears !== undefined) out.experience_years = payload.experienceYears;
  if ("skills" in payload && payload.skills !== undefined) out.skills = payload.skills;
  if ("summary" in payload && payload.summary !== undefined) out.summary = payload.summary;
  if ("fullText" in payload && payload.fullText !== undefined) out.full_text = payload.fullText;
  return out;
}

/**
 * POST /cvs/upload
 * Request: file
 * Response: CV object (snake_case) -> mapped to camelCase Cv
 */
export async function uploadCv(file: File): Promise<Cv> {
  try {
    const fd = new FormData();
    fd.append("file", file);
    const res = await fetch(`${BASE}/cvs/upload`, {
      method: "POST",
      headers: { ...getAuthHeader() }, // DO NOT set Content-Type for FormData
      body: fd,
    });
    const json = await res.json();
    if (!res.ok) {
      throw { status: res.status, message: json?.detail ?? res.statusText, details: json } as ApiError;
    }
    return mapBackendCv(json as BackendCv);
  } catch (err) {
    if ((err as ApiError)?.status !== undefined) throw err;
    throw { status: 0, message: "Network or parsing error", details: err } as ApiError;
  }
}

/**
 * GET /cvs/{id}
 * Response: CV object
 */
export async function getCv(id: number): Promise<Cv> {
  try {
    const res = await fetch(`${BASE}/cvs/${encodeURIComponent(String(id))}`, {
      method: "GET",
      headers: { ...getAuthHeader() },
    });
    const json = await res.json();
    if (!res.ok) {
      throw { status: res.status, message: json?.detail ?? res.statusText, details: json } as ApiError;
    }
    return mapBackendCv(json as BackendCv);
  } catch (err) {
    if ((err as ApiError)?.status !== undefined) throw err;
    throw { status: 0, message: "Network or parsing error", details: err } as ApiError;
  }
}

/**
 * PUT /cvs/{id}
 * Request: any subset of CV fields (we convert to snake_case)
 * Response: updated CV object
 */
export async function updateCv(id: number, payload: CvUpdatePayload): Promise<Cv> {
  try {
    const body = buildSnakePayload(payload);
    const res = await fetch(`${BASE}/cvs/${encodeURIComponent(String(id))}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json", ...getAuthHeader() },
      body: JSON.stringify(body),
    });
    const json = await res.json();
    if (!res.ok) {
      throw { status: res.status, message: json?.detail ?? res.statusText, details: json } as ApiError;
    }
    return mapBackendCv(json as BackendCv);
  } catch (err) {
    if ((err as ApiError)?.status !== undefined) throw err;
    throw { status: 0, message: "Network or parsing error", details: err } as ApiError;
  }
}

/**
 * DELETE /cvs/{id}
 * Response: { status: string }
 */
export async function deleteCv(id: number): Promise<StatusResponse> {
  try {
    const res = await fetch(`${BASE}/cvs/${encodeURIComponent(String(id))}`, {
      method: "DELETE",
      headers: { ...getAuthHeader() },
    });
    const json = await res.json();
    if (!res.ok) {
      throw { status: res.status, message: json?.detail ?? res.statusText, details: json } as ApiError;
    }
    // strict schema: return { status: string }s
    return { status: String((json as { status?: unknown }).status ?? "") };
  } catch (err) {
    if ((err as ApiError)?.status !== undefined) throw err;
    throw { status: 0, message: "Network or parsing error", details: err } as ApiError;
  }
}