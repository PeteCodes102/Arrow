import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';

export interface HeaderProps {
  title?: string;
}

const Header: React.FC<HeaderProps> = ({ title = 'Alerts Dashboard' }) => {
  return (
    <AppBar 
      position="static" 
      elevation={0}
      sx={{
        background: 'linear-gradient(135deg, #000000 0%, #1A1A1A 100%)',
        borderBottom: '3px solid',
        borderImage: 'linear-gradient(90deg, #C0C0C0, #808080, #C0C0C0) 1',
      }}
    >
      <Toolbar sx={{ py: 1.5 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexGrow: 1 }}>
          <TrendingUpIcon 
            sx={{ 
              fontSize: 40, 
              color: '#C0C0C0',
              filter: 'drop-shadow(0 0 8px rgba(192, 192, 192, 0.5))'
            }} 
          />
          <Typography 
            variant="h4" 
            component="div" 
            sx={{ 
              fontWeight: 700,
              background: 'linear-gradient(135deg, #E8E8E8 0%, #C0C0C0 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              letterSpacing: '1px',
            }}
          >
            {title}
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;

