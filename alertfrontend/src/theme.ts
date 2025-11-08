import { createTheme } from '@mui/material/styles';

// Black and Silver theme configuration
export const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#C0C0C0', // Silver
      light: '#E8E8E8', // Light silver
      dark: '#A0A0A0', // Dark silver
      contrastText: '#000000',
    },
    secondary: {
      main: '#808080', // Medium gray
      light: '#B0B0B0',
      dark: '#606060',
      contrastText: '#FFFFFF',
    },
    background: {
      default: '#0A0A0A', // Deep black
      paper: '#1A1A1A', // Slightly lighter black
    },
    text: {
      primary: '#E8E8E8', // Light silver for text
      secondary: '#A0A0A0', // Medium silver for secondary text
    },
    divider: '#404040', // Dark gray for dividers
    error: {
      main: '#FF6B6B',
    },
    warning: {
      main: '#FFD93D',
    },
    info: {
      main: '#6BCF7F',
    },
    success: {
      main: '#51CF66',
    },
  },
  typography: {
    fontFamily: "'Inter', 'Roboto', 'Helvetica', 'Arial', sans-serif",
    h6: {
      fontWeight: 600,
      letterSpacing: '0.5px',
    },
    button: {
      fontWeight: 600,
      textTransform: 'none', // More modern look
      fontSize: '1rem',
    },
  },
  shape: {
    borderRadius: 8, // Slightly more rounded for modern look
  },
  components: {
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#000000',
          borderBottom: '2px solid #C0C0C0',
          boxShadow: '0 4px 12px rgba(192, 192, 192, 0.15)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          padding: '12px 28px',
          fontSize: '1.05rem',
          fontWeight: 600,
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 6px 16px rgba(192, 192, 192, 0.25)',
          },
        },
        contained: {
          background: 'linear-gradient(135deg, #C0C0C0 0%, #A0A0A0 100%)',
          color: '#000000',
          '&:hover': {
            background: 'linear-gradient(135deg, #E8E8E8 0%, #C0C0C0 100%)',
          },
        },
        outlined: {
          borderColor: '#C0C0C0',
          borderWidth: 2,
          color: '#E8E8E8',
          '&:hover': {
            borderColor: '#E8E8E8',
            borderWidth: 2,
            backgroundColor: 'rgba(192, 192, 192, 0.1)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: '#1A1A1A',
          border: '1px solid #404040',
          transition: 'all 0.3s ease',
        },
        elevation2: {
          boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(192, 192, 192, 0.1)',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            backgroundColor: '#121212',
            borderRadius: 8,
            '& fieldset': {
              borderColor: '#505050',
              borderWidth: 2,
            },
            '&:hover fieldset': {
              borderColor: '#808080',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#C0C0C0',
            },
          },
          '& .MuiInputLabel-root': {
            fontSize: '1rem',
            fontWeight: 500,
          },
          '& .MuiInputBase-input': {
            padding: '14px 16px',
            fontSize: '1rem',
          },
        },
      },
    },
    MuiAutocomplete: {
      styleOverrides: {
        paper: {
          backgroundColor: '#1A1A1A',
          border: '1px solid #505050',
        },
        option: {
          '&:hover': {
            backgroundColor: 'rgba(192, 192, 192, 0.15)',
          },
          '&[aria-selected="true"]': {
            backgroundColor: 'rgba(192, 192, 192, 0.25)',
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          backgroundColor: '#2A2A2A',
          borderColor: '#606060',
          color: '#E8E8E8',
          fontWeight: 500,
          '& .MuiChip-deleteIcon': {
            color: '#A0A0A0',
            '&:hover': {
              color: '#C0C0C0',
            },
          },
        },
        outlined: {
          borderWidth: 2,
          borderColor: '#707070',
        },
      },
    },
    MuiDivider: {
      styleOverrides: {
        root: {
          borderColor: '#404040',
          borderWidth: 1,
        },
      },
    },
  },
});
