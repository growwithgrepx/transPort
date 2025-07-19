import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '@/components/atoms/Button';

describe('Button', () => {
  describe('Rendering', () => {
    it('renders the button with correct children', () => {
      render(<Button>Click Me</Button>);
      expect(screen.getByRole('button', { name: /Click Me/i })).toBeInTheDocument();
    });

    it('renders with empty children', () => {
      render(<Button></Button>);
      expect(screen.getByRole('button')).toBeInTheDocument();
    });

    it('renders with complex children', () => {
      render(
        <Button>
          <span>Icon</span>
          <span>Text</span>
        </Button>
      );
      expect(screen.getByRole('button')).toBeInTheDocument();
      expect(screen.getByText('Icon')).toBeInTheDocument();
      expect(screen.getByText('Text')).toBeInTheDocument();
    });
  });

  describe('Click Handling', () => {
    it('calls the onClick handler when clicked', () => {
      const handleClick = jest.fn();
      render(<Button onClick={handleClick}>Click Me</Button>);
      
      fireEvent.click(screen.getByRole('button'));
      
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('does not call onClick when disabled', () => {
      const handleClick = jest.fn();
      render(
        <Button onClick={handleClick} disabled>
          Click Me
        </Button>
      );
      
      fireEvent.click(screen.getByRole('button'));
      
      expect(handleClick).not.toHaveBeenCalled();
    });

    it('calls onClick with correct event object', () => {
      const handleClick = jest.fn();
      render(<Button onClick={handleClick}>Click Me</Button>);
      
      const button = screen.getByRole('button');
      fireEvent.click(button);
      
      expect(handleClick).toHaveBeenCalledWith(
        expect.objectContaining({
          type: 'click',
          target: button,
        })
      );
    });
  });

  describe('Button Attributes', () => {
    it('passes disabled attribute correctly', () => {
      render(<Button disabled>Disabled Button</Button>);
      
      const button = screen.getByRole('button');
      expect(button).toBeDisabled();
    });

    it('passes type attribute correctly', () => {
      render(<Button type="submit">Submit Button</Button>);
      
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('type', 'submit');
    });

    it('passes name attribute correctly', () => {
      render(<Button name="test-button">Named Button</Button>);
      
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('name', 'test-button');
    });

    it('passes id attribute correctly', () => {
      render(<Button id="unique-button">ID Button</Button>);
      
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('id', 'unique-button');
    });

    it('passes aria-label attribute correctly', () => {
      render(<Button aria-label="Accessible button">Button</Button>);
      
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('aria-label', 'Accessible button');
    });

    it('passes data-testid attribute correctly', () => {
      render(<Button data-testid="test-button">Test Button</Button>);
      
      const button = screen.getByTestId('test-button');
      expect(button).toBeInTheDocument();
    });

    it('passes className attribute correctly', () => {
      render(<Button className="custom-class">Styled Button</Button>);
      
      const button = screen.getByRole('button');
      expect(button).toHaveClass('custom-class');
    });

    it('passes multiple attributes correctly', () => {
      render(
        <Button
          disabled
          type="button"
          name="multi-button"
          id="multi-id"
          className="multi-class"
          data-testid="multi-test"
        >
          Multi Button
        </Button>
      );
      
      const button = screen.getByRole('button');
      expect(button).toBeDisabled();
      expect(button).toHaveAttribute('type', 'button');
      expect(button).toHaveAttribute('name', 'multi-button');
      expect(button).toHaveAttribute('id', 'multi-id');
      expect(button).toHaveClass('multi-class');
      expect(button).toHaveAttribute('data-testid', 'multi-test');
    });
  });

  describe('Accessibility', () => {
    it('has correct role', () => {
      render(<Button>Accessible Button</Button>);
      
      const button = screen.getByRole('button');
      expect(button).toBeInTheDocument();
    });

    it('can be focused when not disabled', () => {
      render(<Button>Focusable Button</Button>);
      
      const button = screen.getByRole('button');
      button.focus();
      
      expect(button).toHaveFocus();
    });

    it('cannot be focused when disabled', () => {
      render(<Button disabled>Disabled Button</Button>);
      
      const button = screen.getByRole('button');
      button.focus();
      
      expect(button).not.toHaveFocus();
    });

    it('can be activated with keyboard (Enter key)', () => {
      const handleClick = jest.fn();
      render(<Button onClick={handleClick}>Keyboard Button</Button>);
      
      const button = screen.getByRole('button');
      fireEvent.keyDown(button, { key: 'Enter', code: 'Enter' });
      
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('can be activated with keyboard (Space key)', () => {
      const handleClick = jest.fn();
      render(<Button onClick={handleClick}>Keyboard Button</Button>);
      
      const button = screen.getByRole('button');
      fireEvent.keyDown(button, { key: ' ', code: 'Space' });
      
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('does not activate with other keys', () => {
      const handleClick = jest.fn();
      render(<Button onClick={handleClick}>Keyboard Button</Button>);
      
      const button = screen.getByRole('button');
      fireEvent.keyDown(button, { key: 'Tab', code: 'Tab' });
      
      expect(handleClick).not.toHaveBeenCalled();
    });
  });

  describe('Edge Cases', () => {
    it('handles undefined onClick gracefully', () => {
      render(<Button>No Click Handler</Button>);
      
      const button = screen.getByRole('button');
      expect(() => fireEvent.click(button)).not.toThrow();
    });

    it('handles null children gracefully', () => {
      render(<Button>{null}</Button>);
      
      const button = screen.getByRole('button');
      expect(button).toBeInTheDocument();
    });

    it('handles undefined children gracefully', () => {
      render(<Button>{undefined}</Button>);
      
      const button = screen.getByRole('button');
      expect(button).toBeInTheDocument();
    });

    it('handles boolean children gracefully', () => {
      render(<Button>{true}</Button>);
      
      const button = screen.getByRole('button');
      expect(button).toBeInTheDocument();
    });

    it('handles number children gracefully', () => {
      render(<Button>{42}</Button>);
      
      const button = screen.getByRole('button');
      expect(button).toHaveTextContent('42');
    });
  });
}); 