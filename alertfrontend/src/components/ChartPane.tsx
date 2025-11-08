import React from 'react';
import { Box, Paper, Typography } from '@mui/material';
import ShowChartIcon from '@mui/icons-material/ShowChart';

export interface ChartPaneProps {
  placeholder?: string;
}

const ChartPane: React.FC<React.PropsWithChildren<ChartPaneProps>> = ({
  children,
  placeholder = 'Chart renders here',
}) => {
  return (
    <Paper
      elevation={3}
      sx={{
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        p: 3,
        background: 'linear-gradient(180deg, #1A1A1A 0%, #0A0A0A 100%)',
        border: '2px solid #404040',
        borderRadius: 2,
        position: 'relative',
        overflow: 'hidden',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: '4px',
          background: 'linear-gradient(90deg, #C0C0C0, #808080, #C0C0C0)',
        },
      }}
    >
      {children ? (
        <Box sx={{ width: '100%', height: '100%' }}>
          {children}
        </Box>
      ) : (
        <Box
          sx={{
            width: '100%',
            height: '100%',
            border: '3px dashed #404040',
            borderRadius: 2,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 2,
            color: 'text.secondary',
            textAlign: 'center',
            p: 4,
          }}
        >
          <ShowChartIcon sx={{ fontSize: 80, color: '#505050', opacity: 0.5 }} />
          <Typography variant="h5" sx={{ color: '#808080', fontWeight: 500 }}>
            {placeholder}
          </Typography>
          <Typography variant="body1" sx={{ color: '#606060', maxWidth: 400 }}>
            Select filters and click "Apply Filters" to visualize your trading alerts
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default ChartPane;

