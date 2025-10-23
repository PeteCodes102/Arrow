import { get } from './client';
import type { AlertSeries } from './types';

// Example endpoint mapping; adjust path/params to match your backend.
export const fetchAlertSeries = (params: AlertSeries) =>
  get<AlertSeries[]>('/alerts/series', {
    query: {
      name: params.name,
      start_time: params.start_time,
      end_time: params.end_time,
      start_date: params.start_date,
      end_date: params.end_date,
      days: params.days?.join(',') || undefined,
      weeks: params.weeks?.join(',') || undefined,
    },
  });

export const fetchStrategyNamesFromDB = () => {
  // Use absolute URL to avoid requiring REACT_APP_API_BASE_URL for this call
  return get<string[]>('http://localhost:8000/data/strategy-names/all');
}
