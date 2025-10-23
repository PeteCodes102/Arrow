import axios, { AxiosError, AxiosInstance } from 'axios';
import { maybeApiBaseUrl } from '../config/env';
import type { ApiErrorShape } from './types';

export class ApiError extends Error {
  status: number;
  body: unknown;

  constructor(message: string, status: number, body?: unknown) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.body = body;
  }
}

export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

export interface RequestOptions {
  method?: HttpMethod;
  headers?: Record<string, string>;
  query?: Record<string, string | number | boolean | null | undefined>;
  body?: unknown; // will be JSON-encoded by default
  signal?: AbortSignal;
  timeoutMs?: number; // axios request timeout in ms
}

// Create a single Axios instance; baseURL is optional at import-time
const api: AxiosInstance = axios.create({
  baseURL: maybeApiBaseUrl(),
});

// Optional: response normalization or auth can go here via interceptors.
// api.interceptors.request.use((config) => config);
// api.interceptors.response.use((res) => res);

export async function request<T = unknown>(path: string, opts: RequestOptions = {}): Promise<T> {
  try {
    // Guard: if baseURL is missing and the path is relative, provide a clear runtime error
    const isAbsolute = /^https?:\/\//i.test(path);
    if (!api.defaults.baseURL && !isAbsolute) {
      throw new ApiError(
        'Missing REACT_APP_API_BASE_URL. Define it in .env.local or set a full absolute URL in the request path.',
        0
      );
    }
    const res = await api.request<T>({
      url: path,
      method: opts.method ?? 'GET',
      headers: opts.headers,
      params: opts.query ?? undefined,
      data: opts.body ?? undefined,
      signal: opts.signal,
      timeout: opts.timeoutMs,
    });
    return res.data as T;
  } catch (err) {
    // AxiosError handling
    if (axios.isAxiosError(err)) {
      const axErr = err as AxiosError<ApiErrorShape | unknown>;
      const status = axErr.response?.status ?? 0;
      const body = axErr.response?.data;
      const message = (typeof body === 'object' && body && (body as ApiErrorShape).message)
        ? (body as ApiErrorShape).message!
        : axErr.message || `HTTP ${status}`;
      throw new ApiError(message, status, body);
    }
    throw new ApiError('Network error', 0, err);
  }
}

export const get = <T = unknown>(path: string, opts?: Omit<RequestOptions, 'method' | 'body'>) =>
  request<T>(path, { ...opts, method: 'GET' });

export const post = <T = unknown>(path: string, body?: unknown, opts?: Omit<RequestOptions, 'method' | 'body'>) =>
  request<T>(path, { ...opts, method: 'POST', body });

export const put = <T = unknown>(path: string, body?: unknown, opts?: Omit<RequestOptions, 'method' | 'body'>) =>
  request<T>(path, { ...opts, method: 'PUT', body });

export const patch = <T = unknown>(path: string, body?: unknown, opts?: Omit<RequestOptions, 'method' | 'body'>) =>
  request<T>(path, { ...opts, method: 'PATCH', body });

export const del = <T = unknown>(path: string, opts?: Omit<RequestOptions, 'method' | 'body'>) =>
  request<T>(path, { ...opts, method: 'DELETE' });

// Export axios instance if consumers need to add interceptors
export { api };
