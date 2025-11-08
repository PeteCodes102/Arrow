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
      <div style={{ 
        width: '100%', 
        height: '100%', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center', 
        color: '#808080',
        fontSize: '1.1rem',
      }}>
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
        paper_bgcolor: '#0A0A0A',
        plot_bgcolor: '#1A1A1A',
        font: {
          color: '#E8E8E8',
          family: 'Inter, Roboto, Arial, sans-serif',
          ...(figure.layout?.font || {}),
        },
        margin: { l: 50, r: 30, t: 50, b: 50, ...(figure.layout?.margin || {}) },
        xaxis: {
          gridcolor: '#303030',
          linecolor: '#505050',
          ...(figure.layout?.xaxis || {}),
        },
        yaxis: {
          gridcolor: '#303030',
          linecolor: '#505050',
          ...(figure.layout?.yaxis || {}),
        },
      }}
      frames={figure.frames}
      config={{ 
        displaylogo: false, 
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['lasso2d', 'select2d'],
        ...(figure.config || {}) 
      }}
      useResizeHandler
      style={{ width: '100%', height: '100%', ...style }}
    />
  );
};

export default PlotlyChart;
