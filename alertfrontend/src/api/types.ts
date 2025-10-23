export interface ChartPoint {
  t: string | number; // ISO timestamp or epoch millis
  y: number; // value
}

export interface ChartSeries {
  metric: string;
  series: ChartPoint[];
  unit?: string;
}

export interface ApiErrorShape {
  message?: string;
  code?: string | number;
  details?: unknown;
}


export interface AlertSeries {
  name: string;
  start_time?: string;
  end_time?: string;
  start_date?: string;
  end_date?: string;
  days?: string[]; // e.g. ["Mon", "Tue"]
  weeks?: number[]; // e.g. [1, 2, 3, 4, 5]
}

export const blankAlertSeries: AlertSeries = {
    name: '',
    start_time: undefined,
    end_time: undefined,
    start_date: undefined,
    end_date: undefined,
    days: undefined,
    weeks: undefined,
};
