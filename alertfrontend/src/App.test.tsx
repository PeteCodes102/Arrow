import React from 'react';
import { render, screen } from '@testing-library/react';
import { ThemeProvider } from '@mui/material';
import { theme } from './theme';
import App from './App';

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider theme={theme}>
      {component}
    </ThemeProvider>
  );
};

test('renders Alerts Dashboard header', () => {
  renderWithTheme(<App />);
  // The app should render "Alerts Dashboard" in the header
  const headerElement = screen.getByText(/Alerts Dashboard/i);
  expect(headerElement).toBeInTheDocument();
});

test('renders filters panel with Apply button', () => {
  renderWithTheme(<App />);
  // Check for "Apply Filters" button which is part of the filters panel
  const applyButton = screen.getByRole('button', { name: /apply filters/i });
  expect(applyButton).toBeInTheDocument();
});

test('renders chart placeholder initially', () => {
  renderWithTheme(<App />);
  // The app should show chart placeholder text
  const placeholderText = screen.getByText(/Select filters to view chart/i);
  expect(placeholderText).toBeInTheDocument();
});
