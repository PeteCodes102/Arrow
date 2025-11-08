import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import FiltersPanel from './FiltersPanel';

// Mock the API call
jest.mock('../api/alerts', () => ({
  fetchStrategyNamesFromDB: jest.fn(() => Promise.resolve(['Strategy 1', 'Strategy 2'])),
}));

describe('FiltersPanel Component', () => {
  test('renders Apply button', () => {
    render(<FiltersPanel />);
    const applyButton = screen.getByRole('button', { name: /apply/i });
    expect(applyButton).toBeInTheDocument();
  });

  test('renders Reset button', () => {
    render(<FiltersPanel />);
    const resetButton = screen.getByRole('button', { name: /reset/i });
    expect(resetButton).toBeInTheDocument();
  });

  test('calls onApply when Apply button is clicked', async () => {
    const mockOnApply = jest.fn();
    render(<FiltersPanel onApply={mockOnApply} />);
    
    const applyButton = screen.getByRole('button', { name: /apply/i });
    await userEvent.click(applyButton);
    
    expect(mockOnApply).toHaveBeenCalledTimes(1);
  });

  test('calls onReset when Reset button is clicked', async () => {
    const mockOnReset = jest.fn();
    render(<FiltersPanel onReset={mockOnReset} />);
    
    const resetButton = screen.getByRole('button', { name: /reset/i });
    await userEvent.click(resetButton);
    
    expect(mockOnReset).toHaveBeenCalledTimes(1);
  });

  test('renders with default width', () => {
    const { container } = render(<FiltersPanel />);
    const panel = container.firstChild as HTMLElement;
    expect(panel).toBeInTheDocument();
  });
});
