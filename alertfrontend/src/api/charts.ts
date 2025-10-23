import { post } from './client';
import type { AlertSeries } from './types';

// Plotly JSON returned by Python's plotly.graph_objs.Figure.to_json()
// Backend may return a JSON string or a parsed object; normalize both.
export interface PlotlyFigure {
  data: any[];
  layout?: Record<string, any>;
  frames?: any[];
  config?: Record<string, any>;
}

export type PlotlyPayload = string | PlotlyFigure;

export const normalizePlotly = (payload: PlotlyPayload): PlotlyFigure => {
  let obj: any = payload;
  if (typeof payload === 'string') {
    try {
      obj = JSON.parse(payload);
    } catch (e) {
      throw new Error('Invalid Plotly JSON string from server');
    }
  }
  if (!obj || !Array.isArray(obj.data)) {
    throw new Error('Malformed Plotly payload: missing data array');
  }
  return {
    data: obj.data,
    layout: obj.layout,
    frames: obj.frames,
    config: obj.config,
  };
};

// Minimal FilterParams shape matching the FastAPI model
export interface FilterParams {
  name? : string;
  start_time?: string;
  end_time?: string;
  days?: Array<string | number>;
  weeks?: number[];
  start_date?: string; // YYYY-MM-DD
  end_date?: string;   // YYYY-MM-DD
}

export interface ChartDataResponse {
  chart_json: PlotlyPayload;
}

export const toFilterParams = (s: AlertSeries): FilterParams => ({
  name: s.name,
  start_time: s.start_time,
  end_time: s.end_time,
  days: s.days,
  weeks: s.weeks,
  start_date: s.start_date,
  end_date: s.end_date,
});

// Posts filters to your Python backend and returns a normalized Plotly figure
// Default path targets localhost:8000 as per your request. You can override.
export const fetchPlotlyChartFromFilters = async (
  series: AlertSeries,
  path: string = 'http://localhost:8000/data/chart/filters'
): Promise<PlotlyFigure> => {
  const resp = await post<ChartDataResponse>(path, toFilterParams(series));
  return normalizePlotly(resp.chart_json);
};
