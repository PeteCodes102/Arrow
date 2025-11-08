import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Alerts Dashboard header', () => {
  render(<App />);
  // The app should render "Alerts Dashboard" in the header
  const headerElement = screen.getByText(/Alerts Dashboard/i);
  expect(headerElement).toBeInTheDocument();
});

test('renders filters panel with Apply button', () => {
  render(<App />);
  // Check for "Apply" button which is part of the filters panel
  const applyButton = screen.getByRole('button', { name: /apply/i });
  expect(applyButton).toBeInTheDocument();
});

test('renders chart placeholder initially', () => {
  render(<App />);
  // The app should show chart placeholder text
  const placeholderText = screen.getByText(/Chart renders here/i);
  expect(placeholderText).toBeInTheDocument();
});
