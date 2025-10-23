import type { ChartPoint, ChartSeries } from './types';

export const ensureSorted = (series: ChartSeries): ChartSeries => {
  const sorted = [...series.series].sort((a, b) => Number(a.t) - Number(b.t));
  return { ...series, series: sorted };
};

export const movingAverage = (points: ChartPoint[], windowSize = 5): ChartPoint[] => {
  if (windowSize <= 1) return points;
  const out: ChartPoint[] = [];
  let sum = 0;
  for (let i = 0; i < points.length; i++) {
    sum += points[i].y;
    if (i >= windowSize) sum -= points[i - windowSize].y;
    const avg = i >= windowSize - 1 ? sum / windowSize : points[i].y;
    out.push({ t: points[i].t, y: avg });
  }
  return out;
};

export const normalizeSeries = (series: ChartSeries, opts?: { smooth?: number }) => {
  const sorted = ensureSorted(series);
  const smoothed = opts?.smooth && opts.smooth > 1
    ? movingAverage(sorted.series, opts.smooth)
    : sorted.series;
  return { ...sorted, series: smoothed };
};

