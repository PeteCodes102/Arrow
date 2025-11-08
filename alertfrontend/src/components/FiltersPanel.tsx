import React from 'react';
import { Box, Divider, Stack, Typography, TextField, Button, Autocomplete, Chip, CircularProgress, Paper } from '@mui/material';
import FilterListIcon from '@mui/icons-material/FilterList';
import RefreshIcon from '@mui/icons-material/Refresh';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import type { AlertSeries } from '../api/types';
import { fetchStrategyNamesFromDB } from '../api/alerts';

export type FiltersState = AlertSeries;

export interface FiltersPanelProps {
  defaultState?: Partial<FiltersState>;
  width?: number | string;
  onApply?: (state: FiltersState) => void;
  onReset?: () => void;
}

const defaultState: FiltersState = {
  name: '',
  start_time: undefined,
  end_time: undefined,
  start_date: undefined,
  end_date: undefined,
  days: [],
  weeks: [],
};

const FiltersPanel: React.FC<FiltersPanelProps> = ({
  defaultState: overrides,
  width = 380,
  onApply,
  onReset,
}) => {
  const [state, setState] = React.useState<FiltersState>({
    ...defaultState,
    ...overrides,
  });

  const [strategyOptions, setStrategyOptions] = React.useState<string[]>([]);
  const [loadingStrategies, setLoadingStrategies] = React.useState<boolean>(false);

  React.useEffect(() => {
    let mounted = true;
    const load = async () => {
      setLoadingStrategies(true);
      try {
        const names = await fetchStrategyNamesFromDB();
        console.log('Fetched strategy names:', names);
        if (mounted && Array.isArray(names)) {
          setStrategyOptions(names);
        }
      } catch (e) {
        // Silently ignore; field will just have no options
        if (mounted) setStrategyOptions([]);
      } finally {
        if (mounted) setLoadingStrategies(false);
      }
    };
    load();
    return () => {
      mounted = false;
    };
  }, []);

  const handleApply = () => onApply?.(state);
  const handleReset = () => {
    setState({ ...defaultState, ...overrides });
    onReset?.();
  };

  return (
    <Paper
      elevation={3}
      sx={{
        width: { xs: 340, sm: 360, md: width },
        height: '100%',
        p: 3,
        overflow: 'auto',
        flexShrink: 0,
        background: 'linear-gradient(180deg, #1A1A1A 0%, #0A0A0A 100%)',
        border: '2px solid #404040',
        borderRadius: 2,
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 2 }}>
        <FilterListIcon sx={{ fontSize: 32, color: '#C0C0C0' }} />
        <Typography 
          variant="h5" 
          sx={{ 
            fontWeight: 700,
            background: 'linear-gradient(135deg, #E8E8E8 0%, #C0C0C0 100%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          Filters & Options
        </Typography>
      </Box>
      <Divider sx={{ mb: 3, borderColor: '#505050' }} />
      
      <Stack spacing={3}>
        <Autocomplete
          options={strategyOptions}
          loading={loadingStrategies}
          value={state.name || null}
          onChange={(_, v) => setState((s) => ({ ...s, name: v || '' }))}
          renderInput={(params) => (
            <TextField
              {...params}
              label="Alert Name"
              placeholder="Select alert name"
              InputProps={{
                ...params.InputProps,
                endAdornment: (
                  <>
                    {loadingStrategies ? <CircularProgress color="inherit" size={20} /> : null}
                    {params.InputProps.endAdornment}
                  </>
                ),
              }}
            />
          )}
        />

        <Box>
          <Typography variant="subtitle2" sx={{ mb: 1.5, color: '#A0A0A0', fontWeight: 600 }}>
            Time Range
          </Typography>
          <Stack direction="row" spacing={2}>
            <TextField
              label="Start Time"
              type="time"
              value={state.start_time || ''}
              onChange={(e) => setState((s) => ({ ...s, start_time: e.target.value || undefined }))}
              InputLabelProps={{ shrink: true }}
              inputProps={{ step: 60 }}
              fullWidth
            />
            <TextField
              label="End Time"
              type="time"
              value={state.end_time || ''}
              onChange={(e) => setState((s) => ({ ...s, end_time: e.target.value || undefined }))}
              InputLabelProps={{ shrink: true }}
              inputProps={{ step: 60 }}
              fullWidth
            />
          </Stack>
        </Box>

        <Box>
          <Typography variant="subtitle2" sx={{ mb: 1.5, color: '#A0A0A0', fontWeight: 600 }}>
            Date Range
          </Typography>
          <Stack direction="row" spacing={2}>
            <TextField
              label="Start Date"
              type="date"
              value={state.start_date || ''}
              onChange={(e) => setState((s) => ({ ...s, start_date: e.target.value || undefined }))}
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
            <TextField
              label="End Date"
              type="date"
              value={state.end_date || ''}
              onChange={(e) => setState((s) => ({ ...s, end_date: e.target.value || undefined }))}
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
          </Stack>
        </Box>

        <Autocomplete
          multiple
          options={["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}
          value={state.days || []}
          onChange={(_, v) => setState((s) => ({ ...s, days: v }))}
          renderTags={(value: readonly string[], getTagProps) =>
            value.map((option: string, index: number) => {
              const { key, ...tagProps } = getTagProps({ index });
              return (
                <Chip 
                  variant="outlined" 
                  label={option} 
                  {...tagProps}
                  key={key}
                  sx={{ fontWeight: 600 }}
                />
              );
            })
          }
          renderInput={(params) => <TextField {...params} label="Days of Week" placeholder="Select days" />}
        />

        <Autocomplete
          multiple
          options={[1, 2, 3, 4, 5]}
          value={state.weeks || []}
          onChange={(_, v) => setState((s) => ({ ...s, weeks: v }))}
          renderTags={(value: readonly number[], getTagProps) =>
            value.map((option: number, index: number) => {
              const { key, ...tagProps } = getTagProps({ index });
              return (
                <Chip 
                  variant="outlined" 
                  label={`Week ${option}`} 
                  {...tagProps}
                  key={key}
                  sx={{ fontWeight: 600 }}
                />
              );
            })
          }
          renderInput={(params) => <TextField {...params} label="Weeks" placeholder="Select weeks" />}
        />

        <Stack direction="row" spacing={2} sx={{ pt: 2 }}>
          <Button 
            variant="contained" 
            onClick={handleApply}
            fullWidth
            size="large"
            startIcon={<CheckCircleIcon />}
            sx={{ 
              py: 1.5,
              fontSize: '1.1rem',
            }}
          >
            Apply Filters
          </Button>
          <Button 
            variant="outlined" 
            onClick={handleReset}
            size="large"
            startIcon={<RefreshIcon />}
            sx={{ 
              py: 1.5,
              minWidth: 120,
            }}
          >
            Reset
          </Button>
        </Stack>
      </Stack>
    </Paper>
  );
};

export default FiltersPanel;
