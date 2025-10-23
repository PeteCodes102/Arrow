import React from 'react';
import { Box, Paper, Typography } from '@mui/material';

export interface ChartPaneProps {
  placeholder?: string;
}

const ChartPane: React.FC<React.PropsWithChildren<ChartPaneProps>> = ({
  children,
  placeholder = 'Chart renders here',
}) => {
  return (
    <Paper
      elevation={2}
      sx={{
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        p: 2,
      }}
    >
      {children ? (
        children
      ) : (
        <Box
          sx={{
            width: '100%',
            height: '100%',
            border: '2px dashed',
            borderColor: 'divider',
            borderRadius: 1,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'text.secondary',
            textAlign: 'center',
            p: 2,
          }}
        >
          <Typography variant="h5">{placeholder}</Typography>
        </Box>
      )}
    </Paper>
  );
};

export default ChartPane;

