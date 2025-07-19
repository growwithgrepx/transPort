import { render, screen } from '@testing-library/react';
import { Label } from '@/components/atoms/Label';

describe('Label', () => {
  describe('Rendering', () => {
    it('renders the label with correct children', () => {
      render(<Label>Email Address</Label>);
      expect(screen.getByText('Email Address')).toBeInTheDocument();
    });

    it('renders with empty children', () => {
      const { container } = render(<Label></Label>);
      const label = container.querySelector('.form-label');
      expect(label).toBeInTheDocument();
    });

    it('renders with complex children', () => {
      render(
        <Label>
          <span>Required</span>
          <span>Email</span>
        </Label>
      );
      expect(screen.getByText('Required')).toBeInTheDocument();
      expect(screen.getByText('Email')).toBeInTheDocument();
    });

    it('renders with number children', () => {
      render(<Label>42</Label>);
      expect(screen.getByText('42')).toBeInTheDocument();
    });
  });

  describe('Label Attributes', () => {
    it('passes htmlFor attribute correctly', () => {
      render(<Label htmlFor="email-input">Email</Label>);
      expect(screen.getByText('Email')).toHaveAttribute('for', 'email-input');
    });

    it('passes id attribute correctly', () => {
      render(<Label id="email-label">Email</Label>);
      expect(screen.getByText('Email')).toHaveAttribute('id', 'email-label');
    });

    it('passes data-testid attribute correctly', () => {
      render(<Label data-testid="email-label">Email</Label>);
      expect(screen.getByTestId('email-label')).toBeInTheDocument();
    });

    it('passes className attribute correctly', () => {
      render(<Label className="custom-label">Custom</Label>);
      expect(screen.getByText('Custom')).toHaveClass('custom-label');
    });

    it('passes aria-label attribute correctly', () => {
      render(<Label aria-label="Email field label">Email</Label>);
      expect(screen.getByText('Email')).toHaveAttribute('aria-label', 'Email field label');
    });

    it('passes multiple attributes correctly', () => {
      render(
        <Label
          htmlFor="email-input"
          id="email-label"
          className="multi-class"
          data-testid="multi-test"
          aria-label="Multi label"
        >
          Multi
        </Label>
      );
      
      const label = screen.getByText('Multi');
      expect(label).toHaveAttribute('for', 'email-input');
      expect(label).toHaveAttribute('id', 'email-label');
      expect(label).toHaveClass('multi-class');
      expect(label).toHaveAttribute('data-testid', 'multi-test');
      expect(label).toHaveAttribute('aria-label', 'Multi label');
    });
  });

  describe('Required Indicator', () => {
    it('renders required indicator when required is true', () => {
      render(<Label required>Email</Label>);
      
      const label = screen.getByText('Email');
      expect(label).toBeInTheDocument();
      expect(screen.getByText('*')).toBeInTheDocument();
    });

    it('does not render required indicator when required is false', () => {
      render(<Label required={false}>Email</Label>);
      
      const label = screen.getByText('Email');
      expect(label).toBeInTheDocument();
      expect(screen.queryByText('*')).not.toBeInTheDocument();
    });

    it('does not render required indicator when required is not specified', () => {
      render(<Label>Email</Label>);
      
      const label = screen.getByText('Email');
      expect(label).toBeInTheDocument();
      expect(screen.queryByText('*')).not.toBeInTheDocument();
    });

    it('renders required indicator with custom text', () => {
      render(<Label required requiredText="(required)">Email</Label>);
      
      const label = screen.getByText('Email');
      expect(label).toBeInTheDocument();
      expect(screen.getByText('(required)')).toBeInTheDocument();
    });
  });

  describe('Label Sizes', () => {
    it('renders with small size', () => {
      render(<Label size="small">Small</Label>);
      
      const label = screen.getByText('Small');
      expect(label).toHaveClass('form-label', 'text-xs');
    });

    it('renders with medium size', () => {
      render(<Label size="medium">Medium</Label>);
      
      const label = screen.getByText('Medium');
      expect(label).toHaveClass('form-label', 'text-sm');
    });

    it('renders with large size', () => {
      render(<Label size="large">Large</Label>);
      
      const label = screen.getByText('Large');
      expect(label).toHaveClass('form-label', 'text-base');
    });

    it('renders with default size when none specified', () => {
      render(<Label>Default</Label>);
      
      const label = screen.getByText('Default');
      expect(label).toHaveClass('form-label', 'text-sm');
    });
  });

  describe('Label Variants', () => {
    it('renders with error variant', () => {
      render(<Label variant="error">Error Label</Label>);
      
      const label = screen.getByText('Error Label');
      expect(label).toHaveClass('form-label', 'text-red-600');
    });

    it('renders with success variant', () => {
      render(<Label variant="success">Success Label</Label>);
      
      const label = screen.getByText('Success Label');
      expect(label).toHaveClass('form-label', 'text-green-600');
    });

    it('renders with warning variant', () => {
      render(<Label variant="warning">Warning Label</Label>);
      
      const label = screen.getByText('Warning Label');
      expect(label).toHaveClass('form-label', 'text-yellow-600');
    });

    it('renders with default variant when none specified', () => {
      render(<Label>Default</Label>);
      
      const label = screen.getByText('Default');
      expect(label).toHaveClass('form-label');
      expect(label).not.toHaveClass('text-red-600', 'text-green-600', 'text-yellow-600');
    });
  });

  describe('Accessibility', () => {
    it('has correct semantic structure', () => {
      render(<Label>Accessible Label</Label>);
      
      const label = screen.getByText('Accessible Label');
      expect(label.tagName).toBe('LABEL');
    });

    it('supports screen readers with aria-label', () => {
      render(<Label aria-label="Email field description">Email</Label>);
      
      const label = screen.getByLabelText('Email field description');
      expect(label).toBeInTheDocument();
    });

    it('associates with form elements using htmlFor', () => {
      render(
        <div>
          <Label htmlFor="email-input">Email</Label>
          <input id="email-input" type="email" />
        </div>
      );
      
      const label = screen.getByText('Email');
      const input = screen.getByRole('textbox');
      
      expect(label).toHaveAttribute('for', 'email-input');
      expect(input).toHaveAttribute('id', 'email-input');
    });
  });

  describe('Edge Cases', () => {
    it('handles null children gracefully', () => {
      const { container } = render(<Label>{null}</Label>);
      
      const label = container.querySelector('.form-label');
      expect(label).toBeInTheDocument();
    });

    it('handles undefined children gracefully', () => {
      const { container } = render(<Label>{undefined}</Label>);
      
      const label = container.querySelector('.form-label');
      expect(label).toBeInTheDocument();
    });

    it('handles boolean children gracefully', () => {
      const { container } = render(<Label>{true}</Label>);
      
      const label = container.querySelector('.form-label');
      expect(label).toBeInTheDocument();
    });

    it('handles zero as children', () => {
      render(<Label>{0}</Label>);
      
      const label = screen.getByText('0');
      expect(label).toBeInTheDocument();
    });

    it('handles empty string children', () => {
      const { container } = render(<Label>{''}</Label>);
      
      const label = container.querySelector('.form-label');
      expect(label).toBeInTheDocument();
    });

    it('handles invalid variant gracefully', () => {
      render(<Label variant="invalid">Invalid</Label>);
      
      const label = screen.getByText('Invalid');
      expect(label).toBeInTheDocument();
      expect(label).toHaveClass('form-label');
    });

    it('handles invalid size gracefully', () => {
      render(<Label size="invalid">Invalid</Label>);
      
      const label = screen.getByText('Invalid');
      expect(label).toBeInTheDocument();
      expect(label).toHaveClass('form-label', 'text-sm');
    });
  });

  describe('Combined Props', () => {
    it('combines variant, size, required, and custom className', () => {
      render(
        <Label variant="error" size="large" required className="custom-class">
          Combined
        </Label>
      );
      
      const label = screen.getByText('Combined');
      expect(label).toHaveClass('form-label', 'text-red-600', 'text-base', 'custom-class');
      expect(screen.getByText('*')).toBeInTheDocument();
    });

    it('combines htmlFor, required, and custom required text', () => {
      render(
        <Label htmlFor="test-input" required requiredText="(mandatory)">
          Test Label
        </Label>
      );
      
      const label = screen.getByText('Test Label');
      expect(label).toHaveAttribute('for', 'test-input');
      expect(screen.getByText('(mandatory)')).toBeInTheDocument();
    });
  });
}); 