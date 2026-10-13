// Single HTTP client. Mock mode is controlled by VITE_USE_MOCK (see .env.example).
export const USE_MOCK = import.meta.env.VITE_USE_MOCK !== "false";
const BASE = import.meta.env.VITE_API_BASE_URL || "/api/v1";
let token = null;
export const setToken = (t) => { token = t; };

export async function request(path) {
  const res = await fetch(BASE + path, { headers: token ? { Authorization: `Bearer ${token}` } : {} });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}
