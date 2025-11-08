import React from 'react';
import { render, screen } from '@testing-library/react';
import Header from './Header';

describe('Header Component', () => {
  test('renders with default title', () => {
    render(<Header />);
    const titleElement = screen.getByText(/Alerts Dashboard/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders with custom title', () => {
    render(<Header title="Custom Title" />);
    const titleElement = screen.getByText(/Custom Title/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('is rendered as AppBar', () => {
    const { container } = render(<Header />);
    const appBar = container.querySelector('header');
    expect(appBar).toBeInTheDocument();
  });
});
