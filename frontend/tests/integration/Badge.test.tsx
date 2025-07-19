import { render, screen } from '@testing-library/react';
import { Badge } from '@/components/atoms/Badge';

describe('Badge', () => {
  describe('Rendering', () => {
    it('renders the badge with correct children', () => {
      render(<Badge>Success</Badge>);
      expect(screen.getByText('Success')).toBeInTheDocument();
    });

    it('renders with empty children', () => {
      const { container } = render(<Badge></Badge>);
      const badge = container.querySelector('.badge');
      expect(badge).toBeInTheDocument();
    });

    it('renders with complex children', () => {
      render(
        <Badge>
          <span>Icon</span>
          <span>Text</span>
        </Badge>
      );
      expect(screen.getByText('Icon')).toBeInTheDocument();
      expect(screen.getByText('Text')).toBeInTheDocument();
    });

    it('renders with number children', () => {
      render(<Badge>42</Badge>);
      expect(screen.getByText('42')).toBeInTheDocument();
    });
  });

  describe('Badge Variants', () => {
    it('renders with success variant', () => {
      render(<Badge variant="success">Success</Badge>);
      
      const badge = screen.getByText('Success');
      expect(badge).toHaveClass('badge', 'badge-success');
    });

    it('renders with warning variant', () => {
      render(<Badge variant="warning">Warning</Badge>);
      
      const badge = screen.getByText('Warning');
      expect(badge).toHaveClass('badge', 'badge-warning');
    });

    it('renders with danger variant', () => {
      render(<Badge variant="danger">Danger</Badge>);
      
      const badge = screen.getByText('Danger');
      expect(badge).toHaveClass('badge', 'badge-danger');
    });

    it('renders with info variant', () => {
      render(<Badge variant="info">Info</Badge>);
      
      const badge = screen.getByText('Info');
      expect(badge).toHaveClass('badge', 'badge-info');
    });

    it('renders with default variant when none specified', () => {
      render(<Badge>Default</Badge>);
      
      const badge = screen.getByText('Default');
      expect(badge).toHaveClass('badge');
      expect(badge).not.toHaveClass('badge-success', 'badge-warning', 'badge-danger', 'badge-info');
    });

    it('renders with custom variant', () => {
      render(<Badge variant="custom">Custom</Badge>);
      
      const badge = screen.getByText('Custom');
      expect(badge).toHaveClass('badge', 'badge-custom');
    });
  });

  describe('Badge Attributes', () => {
    it('passes id attribute correctly', () => {
      render(<Badge id="status-badge">Status</Badge>);
      expect(screen.getByText('Status')).toHaveAttribute('id', 'status-badge');
    });

    it('passes data-testid attribute correctly', () => {
      render(<Badge data-testid="status-badge">Status</Badge>);
      expect(screen.getByTestId('status-badge')).toBeInTheDocument();
    });

    it('passes className attribute correctly', () => {
      render(<Badge className="custom-badge">Custom</Badge>);
      expect(screen.getByText('Custom')).toHaveClass('custom-badge');
    });

    it('passes aria-label attribute correctly', () => {
      render(<Badge aria-label="Status indicator">Status</Badge>);
      expect(screen.getByText('Status')).toHaveAttribute('aria-label', 'Status indicator');
    });

    it('passes role attribute correctly', () => {
      render(<Badge role="status">Status</Badge>);
      expect(screen.getByText('Status')).toHaveAttribute('role', 'status');
    });

    it('passes multiple attributes correctly', () => {
      render(
        <Badge
          id="multi-badge"
          className="multi-class"
          data-testid="multi-test"
          aria-label="Multi badge"
          role="status"
        >
          Multi
        </Badge>
      );
      
      const badge = screen.getByText('Multi');
      expect(badge).toHaveAttribute('id', 'multi-badge');
      expect(badge).toHaveClass('multi-class');
      expect(badge).toHaveAttribute('data-testid', 'multi-test');
      expect(badge).toHaveAttribute('aria-label', 'Multi badge');
      expect(badge).toHaveAttribute('role', 'status');
    });
  });

  describe('Badge Sizes', () => {
    it('renders with small size', () => {
      render(<Badge size="small">Small</Badge>);
      
      const badge = screen.getByText('Small');
      expect(badge).toHaveClass('badge', 'text-xs');
    });

    it('renders with medium size', () => {
      render(<Badge size="medium">Medium</Badge>);
      
      const badge = screen.getByText('Medium');
      expect(badge).toHaveClass('badge', 'text-sm');
    });

    it('renders with large size', () => {
      render(<Badge size="large">Large</Badge>);
      
      const badge = screen.getByText('Large');
      expect(badge).toHaveClass('badge', 'text-base');
    });

    it('renders with default size when none specified', () => {
      render(<Badge>Default</Badge>);
      
      const badge = screen.getByText('Default');
      expect(badge).toHaveClass('badge', 'text-xs');
    });
  });

  describe('Badge with Icons', () => {
    it('renders with icon on the left', () => {
      render(
        <Badge icon="✓" iconPosition="left">
          Success
        </Badge>
      );
      
      const badge = screen.getByText('Success');
      expect(badge).toBeInTheDocument();
      expect(screen.getByText('✓')).toBeInTheDocument();
    });

    it('renders with icon on the right', () => {
      render(
        <Badge icon="×" iconPosition="right">
          Error
        </Badge>
      );
      
      const badge = screen.getByText('Error');
      expect(badge).toBeInTheDocument();
      expect(screen.getByText('×')).toBeInTheDocument();
    });

    it('renders without icon when not provided', () => {
      render(<Badge>No Icon</Badge>);
      
      const badge = screen.getByText('No Icon');
      expect(badge).toBeInTheDocument();
      expect(screen.queryByText('✓')).not.toBeInTheDocument();
      expect(screen.queryByText('×')).not.toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('has correct semantic structure', () => {
      render(<Badge>Status</Badge>);
      
      const badge = screen.getByText('Status');
      expect(badge).toBeInTheDocument();
    });

    it('supports screen readers with aria-label', () => {
      render(<Badge aria-label="Payment status">Paid</Badge>);
      
      const badge = screen.getByLabelText('Payment status');
      expect(badge).toBeInTheDocument();
    });

    it('supports role attribute for semantic meaning', () => {
      render(<Badge role="status">Active</Badge>);
      
      const badge = screen.getByRole('status');
      expect(badge).toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    it('handles null children gracefully', () => {
      const { container } = render(<Badge>{null}</Badge>);
      
      const badge = container.querySelector('.badge');
      expect(badge).toBeInTheDocument();
    });

    it('handles undefined children gracefully', () => {
      const { container } = render(<Badge>{undefined}</Badge>);
      
      const badge = container.querySelector('.badge');
      expect(badge).toBeInTheDocument();
    });

    it('handles boolean children gracefully', () => {
      const { container } = render(<Badge>{true}</Badge>);
      
      const badge = container.querySelector('.badge');
      expect(badge).toBeInTheDocument();
    });

    it('handles zero as children', () => {
      render(<Badge>{0}</Badge>);
      
      const badge = screen.getByText('0');
      expect(badge).toBeInTheDocument();
    });

    it('handles empty string children', () => {
      const { container } = render(<Badge>{''}</Badge>);
      
      const badge = container.querySelector('.badge');
      expect(badge).toBeInTheDocument();
    });

    it('handles invalid variant gracefully', () => {
      render(<Badge variant="invalid">Invalid</Badge>);
      
      const badge = screen.getByText('Invalid');
      expect(badge).toBeInTheDocument();
      expect(badge).toHaveClass('badge');
    });

    it('handles invalid size gracefully', () => {
      render(<Badge size="invalid">Invalid</Badge>);
      
      const badge = screen.getByText('Invalid');
      expect(badge).toBeInTheDocument();
      expect(badge).toHaveClass('badge', 'text-xs');
    });
  });

  describe('Combined Props', () => {
    it('combines variant, size, and custom className', () => {
      render(
        <Badge variant="success" size="large" className="custom-class">
          Combined
        </Badge>
      );
      
      const badge = screen.getByText('Combined');
      expect(badge).toHaveClass('badge', 'badge-success', 'text-base', 'custom-class');
    });

    it('combines icon, variant, and size', () => {
      render(
        <Badge variant="warning" size="medium" icon="⚠" iconPosition="left">
          Warning
        </Badge>
      );
      
      const badge = screen.getByText('Warning');
      expect(badge).toHaveClass('badge', 'badge-warning', 'text-sm');
      expect(screen.getByText('⚠')).toBeInTheDocument();
    });
  });
}); 