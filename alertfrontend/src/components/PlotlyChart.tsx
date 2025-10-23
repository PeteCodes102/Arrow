import React from 'react';
import Plot from 'react-plotly.js';
import type { PlotlyFigure } from '../api/charts';

export interface PlotlyChartProps {
  figure: PlotlyFigure;
  style?: React.CSSProperties;
}

const PlotlyChart: React.FC<PlotlyChartProps> = ({ figure, style }) => {
  // Add fallback if data is empty
  if (!figure || !Array.isArray(figure.data) || figure.data.length === 0) {
    return (
      <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#888' }}>
        No chart data available for selected filters.
      </div>
    );
  }

  return (
    <Plot
      data={figure.data}
      layout={{
        ...figure.layout,
        autosize: true,
        margin: { l: 40, r: 20, t: 30, b: 40, ...(figure.layout?.margin || {}) },
      }}
      frames={figure.frames}
      config={{ displaylogo: false, responsive: true, ...(figure.config || {}) }}
      useResizeHandler
      style={{ width: '100%', height: '100%', ...style }}
    />
  );
};

export default PlotlyChart;
