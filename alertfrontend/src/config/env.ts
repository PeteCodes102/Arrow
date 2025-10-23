// Centralized environment access. In CRA, env vars must be prefixed with REACT_APP_.

// Non-throwing accessor for import-time use
export const maybeApiBaseUrl = (): string | undefined => {
  const raw = process.env.REACT_APP_API_BASE_URL;
  const url = raw && raw.trim();
  return url ? url.replace(/\/$/, '') : undefined;
};

// Strict accessor for call sites that explicitly want a hard failure
export const getApiBaseUrl = (): string => {
  const url = maybeApiBaseUrl();
  if (!url) {
    throw new Error(
      'Missing REACT_APP_API_BASE_URL. Define it in .env.local (not committed) or your environment.'
    );
  }
  return url;
};
