import React from 'react';
import { Box, Chip, Paper, Stack, Typography } from '@mui/material';
import type { AlertSeries } from '../api/types';

export interface SeriesSummaryProps {
  series: AlertSeries[];
}

const SeriesCard: React.FC<{ item: AlertSeries }> = ({ item }) => {
  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Stack spacing={1}>
        <Typography variant="subtitle1" fontWeight={600}>
          {item.name || 'Untitled Alert'}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {item.start_date || '—'} {item.start_date || item.end_date ? '→' : ''} {item.end_date || '—'}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {item.start_time || '—'} {item.start_time || item.end_time ? '→' : ''} {item.end_time || '—'}
        </Typography>
        <Box>
          <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
            {(item.days || []).map((d) => (
              <Chip key={d} size="small" label={d} />
            ))}
            {(item.weeks || []).map((w) => (
              <Chip key={w} size="small" label={`W${w}`} color="default" />
            ))}
          </Stack>
        </Box>
      </Stack>
    </Paper>
  );
};

const SeriesSummary: React.FC<SeriesSummaryProps> = ({ series }) => {
  if (!series || series.length === 0) return null;
  return (
    <Stack spacing={2}>
      {series.map((s, i) => (
        <SeriesCard key={s.name ? `${s.name}-${i}` : i} item={s} />
      ))}
    </Stack>
  );
};

export default SeriesSummary;

