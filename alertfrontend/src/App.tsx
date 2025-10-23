import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';
import Header from './components/Header';
import ChartPane from './components/ChartPane';
import FiltersPanel from './components/FiltersPanel';
import SeriesSummary from './components/SeriesSummary';
import PlotlyChart from './components/PlotlyChart';
import { fetchAlertSeries, fetchStrategyNamesFromDB } from './api/alerts';
import { fetchPlotlyChartFromFilters, PlotlyFigure } from './api/charts';
import { type AlertSeries, blankAlertSeries} from './api/types';


function App() {
  const [series, setSeries] = React.useState<AlertSeries[]>([blankAlertSeries]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [filters, setFilters] = React.useState<AlertSeries | null>(null);
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
      setFilters(state);
      load(state);
      // log the response 
    },
    [load]
  );

  // no auto-refresh for this form-based series selection

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header />

      <Box sx={{ flex: 1, display: 'flex', flexDirection: 'row', gap: 2, p: 2 }}>
        <Box sx={{ width: 320 }}>
          <FiltersPanel onApply={handleApply} />
          <SeriesSummary series={series} />
        </Box>

        <Box sx={{ flex: 1 }}>
          <ChartPane>
            {loading ? (
              <CircularProgress />
            ) : error ? (
              <Typography color="error">{error}</Typography>
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
