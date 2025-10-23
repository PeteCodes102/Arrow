import React from 'react';
import { AppBar, Toolbar, Typography } from '@mui/material';

export interface HeaderProps {
  title?: string;
}

const Header: React.FC<HeaderProps> = ({ title = 'Alerts Dashboard' }) => {
  return (
    <AppBar position="static" color="primary" enableColorOnDark>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          {title}
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Header;

