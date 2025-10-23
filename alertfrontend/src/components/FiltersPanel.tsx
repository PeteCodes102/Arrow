import React from 'react';
import { Box, Divider, Stack, Typography, TextField, Button, Autocomplete, Chip, CircularProgress } from '@mui/material';
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
  width = 360,
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
    <Box
      component="aside"
      sx={{
        width: { xs: 320, sm: 340, md: width },
        borderLeft: 1,
        borderColor: 'divider',
        p: 2,
        overflow: 'auto',
        flexShrink: 0,
      }}
    >
      <Typography variant="h6" sx={{ mb: 1 }}>
        Filters & Options
      </Typography>
      <Divider sx={{ mb: 2 }} />
      <Stack spacing={2}>
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
                    {loadingStrategies ? <CircularProgress color="inherit" size={16} /> : null}
                    {params.InputProps.endAdornment}
                  </>
                ),
              }}
            />
          )}
        />

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

        <Autocomplete
          multiple
          options={["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}
          value={state.days || []}
          onChange={(_, v) => setState((s) => ({ ...s, days: v }))}
          renderTags={(value: readonly string[], getTagProps) =>
            value.map((option: string, index: number) => (
              <Chip variant="outlined" label={option} {...getTagProps({ index })} key={option} />
            ))
          }
          renderInput={(params) => <TextField {...params} label="Days" placeholder="Select days" />}
        />

        <Autocomplete
          multiple
          options={[1, 2, 3, 4, 5]}
          value={state.weeks || []}
          onChange={(_, v) => setState((s) => ({ ...s, weeks: v }))}
          renderTags={(value: readonly number[], getTagProps) =>
            value.map((option: number, index: number) => (
              <Chip variant="outlined" label={`Week ${option}`} {...getTagProps({ index })} key={option} />
            ))
          }
          renderInput={(params) => <TextField {...params} label="Weeks" placeholder="Select weeks" />}
        />

        <Stack direction="row" spacing={1}>
          <Button variant="contained" onClick={handleApply}>
            Apply
          </Button>
          <Button variant="outlined" color="inherit" onClick={handleReset}>
            Reset
          </Button>
        </Stack>
      </Stack>
    </Box>
  );
};

export default FiltersPanel;
