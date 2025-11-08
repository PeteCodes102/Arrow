import React from 'react';
import { render, screen } from '@testing-library/react';
import ChartPane from './ChartPane';

describe('ChartPane Component', () => {
  test('renders default placeholder text when no children', () => {
    render(<ChartPane />);
    const placeholder = screen.getByText(/Chart renders here/i);
    expect(placeholder).toBeInTheDocument();
  });

  test('renders custom placeholder text', () => {
    render(<ChartPane placeholder="Custom placeholder" />);
    const placeholder = screen.getByText(/Custom placeholder/i);
    expect(placeholder).toBeInTheDocument();
  });

  test('renders children when provided', () => {
    render(
      <ChartPane>
        <div>Test Chart Content</div>
      </ChartPane>
    );
    const content = screen.getByText(/Test Chart Content/i);
    expect(content).toBeInTheDocument();
  });

  test('does not show placeholder when children provided', () => {
    render(
      <ChartPane>
        <div>Test Chart Content</div>
      </ChartPane>
    );
    const placeholder = screen.queryByText(/Chart renders here/i);
    expect(placeholder).not.toBeInTheDocument();
  });
});
