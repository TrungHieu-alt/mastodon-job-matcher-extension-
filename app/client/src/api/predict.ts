// Misc endpoints: candidate/recruiter profiles, cv, applications, match, health.
// All types local to this file. Flat functions only.

const BASE = (import.meta.env.VITE_API_URL ?? "").replace(/\/$/, "");

/* Types (local) */
export type CandidateProfileRequest = { full_name: string; location?: string | null; experience_years?: number; skills?: string[]; summary?: string | null };
export type CandidateProfileResponse = { user_id: number; full_name: string; location?: string | null; experience_years: number; skills: string[]; summary?: string | null; created_at: string; updated_at: string };

export type RecruiterProfileRequest = { company_name: string; recruiter_title: string; company_logo?: string | null; about_company?: string | null; hiring_fields?: string[] };
export type RecruiterProfileResponse = { user_id: number; company_name: string; recruiter_title: string; company_logo?: string | null; about_company?: string | null; hiring_fields: string[]; created_at: string; updated_at: string };

export type CandidateResumeRequest = { title: string; location?: string | null; experience_years?: number; skills?: string[]; summary?: string | null; full_text?: string | null; pdf_url?: string | null; is_main?: boolean };
export type CandidateResumeResponse = { cv_id: number; user_id: number; title: string; location?: string | null; experience_years: number; skills: string[]; summary?: string | null; full_text?: string | null; pdf_url?: string | null; is_main: boolean; created_at: string; updated_at: string };

export type ApplicationRequest = { job_id: number; cv_id: number };
export type ApplicationUpdateRequest = { status: "pending" | "viewed" | "interviewing" | "rejected" | "hired" };
export type ApplicationResponse = { app_id: number; job_id: number; candidate_id: number; cv_id: number; status: string; created_at: string; updated_at: string };

export type MatchResultResponse = { cv_id: number; job_id: number; score: number; created_at: string; updated_at: string };
export type HealthResponse = { status: string };

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

/* Candidate profile */
export async function getCandidateProfile(userId: number): Promise<CandidateProfileResponse> {
  const res = await fetch(`${BASE}/candidate/profile/${encodeURIComponent(String(userId))}`, { method: "GET", headers: { ...getAuthHeader() } });
  return parseOrThrow(res);
}
export async function updateCandidateProfile(userId: number, payload: CandidateProfileRequest): Promise<CandidateProfileResponse> {
  const res = await fetch(`${BASE}/candidate/profile/${encodeURIComponent(String(userId))}`, { method: "PUT", headers: { "Content-Type": "application/json", ...getAuthHeader() }, body: JSON.stringify(payload) });
  return parseOrThrow(res);
}

/* Recruiter profile */
export async function createRecruiterProfile(userId: number, payload: RecruiterProfileRequest): Promise<RecruiterProfileResponse> {
  const res = await fetch(`${BASE}/recruiter/profile/${encodeURIComponent(String(userId))}`, { method: "POST", headers: { "Content-Type": "application/json", ...getAuthHeader() }, body: JSON.stringify(payload) });
  return parseOrThrow(res);
}
export async function getRecruiterProfile(userId: number): Promise<RecruiterProfileResponse> {
  const res = await fetch(`${BASE}/recruiter/profile/${encodeURIComponent(String(userId))}`, { method: "GET", headers: { ...getAuthHeader() } });
  return parseOrThrow(res);
}
export async function updateRecruiterProfile(userId: number, payload: RecruiterProfileRequest): Promise<RecruiterProfileResponse> {
  const res = await fetch(`${BASE}/recruiter/profile/${encodeURIComponent(String(userId))}`, { method: "PUT", headers: { "Content-Type": "application/json", ...getAuthHeader() }, body: JSON.stringify(payload) });
  return parseOrThrow(res);
}

/* CV */
export async function createCv(userId: number, payload: CandidateResumeRequest): Promise<CandidateResumeResponse> {
  const res = await fetch(`${BASE}/cv/create/${encodeURIComponent(String(userId))}`, { method: "POST", headers: { "Content-Type": "application/json", ...getAuthHeader() }, body: JSON.stringify(payload) });
  return parseOrThrow(res);
}
export async function uploadCv(userId: number, file: File, meta?: { title?: string }): Promise<any> {
  const fd = new FormData();
  fd.append("file", file);
  if (meta?.title) fd.append("title", meta.title);
  const res = await fetch(`${BASE}/cv/upload/${encodeURIComponent(String(userId))}`, { method: "POST", headers: { ...getAuthHeader() }, body: fd });
  return parseOrThrow(res);
}
export async function getCv(cvId: number): Promise<CandidateResumeResponse> {
  const res = await fetch(`${BASE}/cv/${encodeURIComponent(String(cvId))}`, { method: "GET", headers: { ...getAuthHeader() } });
  return parseOrThrow(res);
}
export async function getUserCvs(userId: number): Promise<CandidateResumeResponse[]> {
  const res = await fetch(`${BASE}/cv/user/${encodeURIComponent(String(userId))}`, { method: "GET", headers: { ...getAuthHeader() } });
  return parseOrThrow(res);
}
export async function getMainCv(userId: number): Promise<CandidateResumeResponse> {
  const res = await fetch(`${BASE}/cv/main/user/${encodeURIComponent(String(userId))}`, { method: "GET", headers: { ...getAuthHeader() } });
  return parseOrThrow(res);
}
export async function updateCv(cvId: number, payload: CandidateResumeRequest): Promise<CandidateResumeResponse> {
  const res = await fetch(`${BASE}/cv/${encodeURIComponent(String(cvId))}`, { method: "PUT", headers: { "Content-Type": "application/json", ...getAuthHeader() }, body: JSON.stringify(payload) });
  return parseOrThrow(res);
}
export async function deleteCv(cvId: number): Promise<{ message: string }> {
  const res = await fetch(`${BASE}/cv/${encodeURIComponent(String(cvId))}`, { method: "DELETE", headers: { ...getAuthHeader() } });
  return parseOrThrow(res);
}

/* Applications */
export async function createApplication(userId: number, payload: ApplicationRequest): Promise<ApplicationResponse> {
  const qs = `?user_id=${encodeURIComponent(String(userId))}`;
  const res = await fetch(`${BASE}/applications${qs}`, { method: "POST", headers: { "Content-Type": "application/json", ...getAuthHeader() }, body: JSON.stringify(payload) });
  return parseOrThrow(res);
}
export async function getApplicationsByJob(jobId: number): Promise<ApplicationResponse[]> {
  const res = await fetch(`${BASE}/applications/job/${encodeURIComponent(String(jobId))}`, { method: "GET", headers: { ...getAuthHeader() } });
  return parseOrThrow(res);
}
export async function getApplicationsByCandidate(userId: number): Promise<ApplicationResponse[]> {
  const res = await fetch(`${BASE}/applications/candidate/${encodeURIComponent(String(userId))}`, { method: "GET", headers: { ...getAuthHeader() } });
  return parseOrThrow(res);
}
export async function updateApplication(appId: number, payload: ApplicationUpdateRequest): Promise<ApplicationResponse> {
  const res = await fetch(`${BASE}/applications/${encodeURIComponent(String(appId))}`, { method: "PUT", headers: { "Content-Type": "application/json", ...getAuthHeader() }, body: JSON.stringify(payload) });
  return parseOrThrow(res);
}
export async function deleteApplication(appId: number): Promise<{ message: string }> {
  const res = await fetch(`${BASE}/applications/${encodeURIComponent(String(appId))}`, { method: "DELETE", headers: { ...getAuthHeader() } });
  return parseOrThrow(res);
}

/* Match (stubs) */
export async function getMatchesForCv(cvId: number): Promise<MatchResultResponse[]> {
  const res = await fetch(`${BASE}/match/cv/${encodeURIComponent(String(cvId))}`, { method: "GET", headers: { ...getAuthHeader() } });
  return parseOrThrow(res);
}
export async function getMatchesForJob(jobId: number): Promise<MatchResultResponse[]> {
  const res = await fetch(`${BASE}/match/job/${encodeURIComponent(String(jobId))}`, { method: "GET", headers: { ...getAuthHeader() } });
  return parseOrThrow(res);
}
export async function recomputeCvMatches(cvId: number): Promise<MatchResultResponse[]> {
  const res = await fetch(`${BASE}/match/recompute/cv/${encodeURIComponent(String(cvId))}`, { method: "POST", headers: { ...getAuthHeader() } });
  return parseOrThrow(res);
}
export async function recomputeJobMatches(jobId: number): Promise<MatchResultResponse[]> {
  const res = await fetch(`${BASE}/match/recompute/job/${encodeURIComponent(String(jobId))}`, { method: "POST", headers: { ...getAuthHeader() } });
  return parseOrThrow(res);
}

/* System */
export async function health(): Promise<HealthResponse> {
  const res = await fetch(`${BASE}/health`, { method: "GET" });
  return parseOrThrow(res);
}