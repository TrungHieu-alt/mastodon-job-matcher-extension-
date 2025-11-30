// Job-related endpoints + upload. Types are local to this file.

const BASE = (import.meta.env.VITE_API_URL ?? "").replace(/\/$/, "");

export type JobPostRequest = {
  title: string;
  role: string;
  location: string;
  job_type: string;
  experience_level: string;
  skills?: string[];
  salary_min?: number | null;
  salary_max?: number | null;
  full_text?: string | null;
  pdf_url?: string | null;
};
export type JobPostResponse = {
  job_id: number;
  recruiter_id: number;
  title: string;
  role: string;
  location: string;
  job_type: string;
  experience_level: string;
  skills: string[];
  salary_min?: number | null;
  salary_max?: number | null;
  full_text?: string | null;
  pdf_url?: string | null;
  created_at: string;
  updated_at: string;
};
export type ApiError = { status: number; message: string; details?: any };

function getAuthHeader(): Record<string, string> {
  const t = typeof localStorage !== "undefined"
    ? localStorage.getItem("token")
    : null;

  return t ? { Authorization: `Bearer ${t}` } : {};
}


async function parseOrThrow(res: Response) {
  const txt = await res.text();
  const body = txt ? JSON.parse(txt) : null;
  if (!res.ok) throw { status: res.status, message: body?.detail ?? res.statusText, details: body } as ApiError;
  return body;
}

export async function createJob(recruiterId: number, payload: JobPostRequest): Promise<JobPostResponse> {
  const res = await fetch(`${BASE}/jobs/create/${encodeURIComponent(String(recruiterId))}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify(payload),
  });
  return parseOrThrow(res);
}

export async function uploadJobPDF(file: File, recruiter_id?: number): Promise<any> {
  const fd = new FormData();
  fd.append("file", file);
  if (recruiter_id != null) fd.append("recruiter_id", String(recruiter_id));
  const res = await fetch(`${BASE}/jobs/upload`, {
    method: "POST",
    headers: { ...getAuthHeader() }, 
    body: fd,
  });
  return parseOrThrow(res);
}

export async function listJobs(): Promise<JobPostResponse[]> {
  const res = await fetch(`${BASE}/jobs`, { method: "GET", headers: { ...getAuthHeader() } });
  return parseOrThrow(res);
}

export async function getJob(jobId: number): Promise<JobPostResponse> {
  const res = await fetch(`${BASE}/jobs/${encodeURIComponent(String(jobId))}`, { method: "GET", headers: { ...getAuthHeader() } });
  return parseOrThrow(res);
}

export async function updateJob(jobId: number, payload: JobPostRequest): Promise<JobPostResponse> {
  const res = await fetch(`${BASE}/jobs/${encodeURIComponent(String(jobId))}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return parseOrThrow(res);
}

export async function deleteJob(jobId: number): Promise<{ message: string }> {
  const res = await fetch(`${BASE}/jobs/${encodeURIComponent(String(jobId))}`, {
    method: "DELETE",
    headers: { ...getAuthHeader() },
  });
  return parseOrThrow(res);
}