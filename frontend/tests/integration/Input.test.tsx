import { render, screen, fireEvent } from '@testing-library/react';
import { Input } from '@/components/atoms/Input';

describe('Input', () => {
  describe('Rendering', () => {
    it('renders the input with correct placeholder', () => {
      render(<Input placeholder="Enter text" />);
      expect(screen.getByPlaceholderText('Enter text')).toBeInTheDocument();
    });

    it('renders with default value', () => {
      render(<Input defaultValue="Initial value" />);
      expect(screen.getByDisplayValue('Initial value')).toBeInTheDocument();
    });

    it('renders with controlled value', () => {
      render(<Input value="Controlled value" onChange={() => {}} />);
      expect(screen.getByDisplayValue('Controlled value')).toBeInTheDocument();
    });

    it('renders with label when provided', () => {
      render(<Input label="Email Address" />);
      expect(screen.getByLabelText('Email Address')).toBeInTheDocument();
    });
  });

  describe('Input Handling', () => {
    it('calls the onChange handler when value changes', () => {
      const handleChange = jest.fn();
      render(<Input onChange={handleChange} />);
      
      const input = screen.getByRole('textbox');
      fireEvent.change(input, { target: { value: 'new value' } });
      
      expect(handleChange).toHaveBeenCalledTimes(1);
      expect(handleChange).toHaveBeenCalledWith(
        expect.objectContaining({
          target: expect.objectContaining({ value: 'new value' }),
        })
      );
    });

    it('calls the onFocus handler when focused', () => {
      const handleFocus = jest.fn();
      render(<Input onFocus={handleFocus} />);
      
      const input = screen.getByRole('textbox');
      fireEvent.focus(input);
      
      expect(handleFocus).toHaveBeenCalledTimes(1);
    });

    it('calls the onBlur handler when blurred', () => {
      const handleBlur = jest.fn();
      render(<Input onBlur={handleBlur} />);
      
      const input = screen.getByRole('textbox');
      fireEvent.blur(input);
      
      expect(handleBlur).toHaveBeenCalledTimes(1);
    });

    it('does not update value when disabled', () => {
      const handleChange = jest.fn();
      render(<Input onChange={handleChange} disabled value="initial" />);
      
      const input = screen.getByRole('textbox');
      fireEvent.change(input, { target: { value: 'new value' } });
      
      // The value should remain unchanged
      expect(input).toHaveValue('initial');
    });
  });

  describe('Input Attributes', () => {
    it('passes disabled attribute correctly', () => {
      render(<Input disabled />);
      expect(screen.getByRole('textbox')).toBeDisabled();
    });

    it('passes type attribute correctly', () => {
      render(<Input type="email" />);
      expect(screen.getByRole('textbox')).toHaveAttribute('type', 'email');
    });

    it('passes name attribute correctly', () => {
      render(<Input name="email" />);
      expect(screen.getByRole('textbox')).toHaveAttribute('name', 'email');
    });

    it('passes id attribute correctly', () => {
      render(<Input id="email-input" />);
      expect(screen.getByRole('textbox')).toHaveAttribute('id', 'email-input');
    });

    it('passes placeholder attribute correctly', () => {
      render(<Input placeholder="Enter your email" />);
      expect(screen.getByRole('textbox')).toHaveAttribute('placeholder', 'Enter your email');
    });

    it('passes required attribute correctly', () => {
      render(<Input required />);
      expect(screen.getByRole('textbox')).toBeRequired();
    });

    it('passes aria-label attribute correctly', () => {
      render(<Input aria-label="Email input" />);
      expect(screen.getByRole('textbox')).toHaveAttribute('aria-label', 'Email input');
    });

    it('passes data-testid attribute correctly', () => {
      render(<Input data-testid="email-input" />);
      expect(screen.getByTestId('email-input')).toBeInTheDocument();
    });

    it('passes className attribute correctly', () => {
      render(<Input className="custom-input" />);
      expect(screen.getByRole('textbox')).toHaveClass('custom-input');
    });

    it('passes multiple attributes correctly', () => {
      render(
        <Input
          disabled
          type="email"
          name="email"
          id="email-id"
          placeholder="Enter email"
          required
          className="multi-class"
          data-testid="multi-test"
        />
      );
      
      const input = screen.getByRole('textbox');
      expect(input).toBeDisabled();
      expect(input).toHaveAttribute('type', 'email');
      expect(input).toHaveAttribute('name', 'email');
      expect(input).toHaveAttribute('id', 'email-id');
      expect(input).toHaveAttribute('placeholder', 'Enter email');
      expect(input).toBeRequired();
      expect(input).toHaveClass('multi-class');
      expect(input).toHaveAttribute('data-testid', 'multi-test');
    });
  });

  describe('Label Integration', () => {
    it('associates label with input using htmlFor', () => {
      render(<Input label="Email" id="email" />);
      
      const label = screen.getByText('Email');
      const input = screen.getByRole('textbox');
      
      expect(label).toHaveAttribute('for', 'email');
      expect(input).toHaveAttribute('id', 'email');
    });

    it('renders label with correct styling class', () => {
      render(<Input label="Email" />);
      
      const label = screen.getByText('Email');
      expect(label).toHaveClass('form-label');
    });

    it('does not render label when not provided', () => {
      render(<Input placeholder="Enter text" />);
      
      expect(screen.queryByText('Email')).not.toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('has correct role', () => {
      render(<Input />);
      expect(screen.getByRole('textbox')).toBeInTheDocument();
    });

    it('can be focused when not disabled', () => {
      render(<Input />);
      
      const input = screen.getByRole('textbox');
      input.focus();
      
      expect(input).toHaveFocus();
    });

    it('cannot be focused when disabled', () => {
      render(<Input disabled />);
      
      const input = screen.getByRole('textbox');
      input.focus();
      
      expect(input).not.toHaveFocus();
    });

    it('supports keyboard navigation', () => {
      render(<Input />);
      
      const input = screen.getByRole('textbox');
      fireEvent.keyDown(input, { key: 'Tab' });
      
      // Should not throw any errors
      expect(input).toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    it('handles undefined onChange gracefully', () => {
      render(<Input />);
      
      const input = screen.getByRole('textbox');
      expect(() => fireEvent.change(input, { target: { value: 'test' } })).not.toThrow();
    });

    it('handles undefined onFocus gracefully', () => {
      render(<Input />);
      
      const input = screen.getByRole('textbox');
      expect(() => fireEvent.focus(input)).not.toThrow();
    });

    it('handles undefined onBlur gracefully', () => {
      render(<Input />);
      
      const input = screen.getByRole('textbox');
      expect(() => fireEvent.blur(input)).not.toThrow();
    });

    it('handles empty string value', () => {
      render(<Input value="" onChange={() => {}} />);
      
      const input = screen.getByRole('textbox');
      expect(input).toHaveValue('');
    });

    it('handles null value', () => {
      render(<Input value={null as any} onChange={() => {}} />);
      
      const input = screen.getByRole('textbox');
      expect(input).toHaveValue('');
    });
  });
}); 