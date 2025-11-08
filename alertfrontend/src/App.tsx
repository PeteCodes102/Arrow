import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';
import Header from './components/Header';
import ChartPane from './components/ChartPane';
import FiltersPanel from './components/FiltersPanel';
import PlotlyChart from './components/PlotlyChart';
import { fetchPlotlyChartFromFilters, PlotlyFigure } from './api/charts';
import { type AlertSeries } from './api/types';


function App() {
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [figure, setFigure] = React.useState<PlotlyFigure | null>(null);

  const load = React.useCallback(async (f: AlertSeries) => {
    setLoading(true);
    setError(null);
    try {
      console.log(f);
      const fig = await fetchPlotlyChartFromFilters(f);
      console.log(fig);
      setFigure(fig);
      // Optionally also fetch list/summary if still desired:
      // const list = await fetchAlertSeries(f).catch(() => []);
      // setSeries(list);
    } catch (e: any) {
      setError(e?.message || 'Failed to load data');
      setFigure(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const handleApply = React.useCallback(
    (state: AlertSeries) => {
      load(state);
      // log the response 
    },
    [load]
  );

  // no auto-refresh for this form-based series selection

  return (
    <Box sx={{ 
      height: '100vh', 
      display: 'flex', 
      flexDirection: 'column',
      background: '#0A0A0A',
    }}>
      <Header />

      <Box sx={{ 
        flex: 1, 
        display: 'flex', 
        flexDirection: 'row', 
        gap: 3, 
        p: 3,
        overflow: 'hidden',
      }}>
        <Box sx={{ width: 380, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <FiltersPanel onApply={handleApply} />
        </Box>

        <Box sx={{ flex: 1, minWidth: 0 }}>
          <ChartPane>
            {loading ? (
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
                <CircularProgress size={60} sx={{ color: '#C0C0C0' }} />
                <Typography sx={{ color: '#A0A0A0', fontSize: '1.1rem' }}>
                  Loading chart data...
                </Typography>
              </Box>
            ) : error ? (
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h6" sx={{ color: '#FF6B6B', mb: 1 }}>
                  Error Loading Data
                </Typography>
                <Typography sx={{ color: '#A0A0A0' }}>{error}</Typography>
              </Box>
            ) : figure ? (
              <PlotlyChart figure={figure} />
            ) : (
              <Typography color="textSecondary">Select filters to view chart.</Typography>
            )}
          </ChartPane>
        </Box>
      </Box>
    </Box>
  );
}

export default App;
