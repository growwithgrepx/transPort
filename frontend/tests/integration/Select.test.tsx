import { render, screen, fireEvent } from '@testing-library/react';
import { Select } from '@/components/atoms/Select';

describe('Select', () => {
  const mockOptions = [
    { value: 'option1', label: 'Option 1' },
    { value: 'option2', label: 'Option 2' },
    { value: 'option3', label: 'Option 3' },
  ];

  describe('Rendering', () => {
    it('renders the select with options', () => {
      render(<Select options={mockOptions} />);
      
      expect(screen.getByRole('combobox')).toBeInTheDocument();
      expect(screen.getByText('Option 1')).toBeInTheDocument();
      expect(screen.getByText('Option 2')).toBeInTheDocument();
      expect(screen.getByText('Option 3')).toBeInTheDocument();
    });

    it('renders with placeholder when provided', () => {
      render(<Select options={mockOptions} placeholder="Select an option" />);
      
      expect(screen.getByText('Select an option')).toBeInTheDocument();
    });

    it('renders with default value', () => {
      render(<Select options={mockOptions} defaultValue="option2" />);
      
      const select = screen.getByRole('combobox');
      expect(select).toHaveValue('option2');
    });

    it('renders with controlled value', () => {
      render(<Select options={mockOptions} value="option3" onChange={() => {}} />);
      
      const select = screen.getByRole('combobox');
      expect(select).toHaveValue('option3');
    });

    it('renders with label when provided', () => {
      render(<Select options={mockOptions} label="Choose Option" />);
      
      expect(screen.getByLabelText('Choose Option')).toBeInTheDocument();
    });
  });

  describe('Selection Handling', () => {
    it('calls the onChange handler when selection changes', () => {
      const handleChange = jest.fn();
      render(<Select options={mockOptions} onChange={handleChange} />);
      
      const select = screen.getByRole('combobox');
      fireEvent.change(select, { target: { value: 'option2' } });
      
      expect(handleChange).toHaveBeenCalledTimes(1);
      expect(handleChange).toHaveBeenCalledWith(
        expect.objectContaining({
          target: expect.objectContaining({ value: 'option2' }),
        })
      );
    });

    it('calls the onFocus handler when focused', () => {
      const handleFocus = jest.fn();
      render(<Select options={mockOptions} onFocus={handleFocus} />);
      
      const select = screen.getByRole('combobox');
      fireEvent.focus(select);
      
      expect(handleFocus).toHaveBeenCalledTimes(1);
    });

    it('calls the onBlur handler when blurred', () => {
      const handleBlur = jest.fn();
      render(<Select options={mockOptions} onBlur={handleBlur} />);
      
      const select = screen.getByRole('combobox');
      fireEvent.blur(select);
      
      expect(handleBlur).toHaveBeenCalledTimes(1);
    });

    it('does not update value when disabled', () => {
      const handleChange = jest.fn();
      render(<Select options={mockOptions} onChange={handleChange} disabled value="option1" />);
      
      const select = screen.getByRole('combobox');
      fireEvent.change(select, { target: { value: 'option2' } });
      
      // The value should remain unchanged
      expect(select).toHaveValue('option1');
    });
  });

  describe('Select Attributes', () => {
    it('passes disabled attribute correctly', () => {
      render(<Select options={mockOptions} disabled />);
      expect(screen.getByRole('combobox')).toBeDisabled();
    });

    it('passes name attribute correctly', () => {
      render(<Select options={mockOptions} name="category" />);
      expect(screen.getByRole('combobox')).toHaveAttribute('name', 'category');
    });

    it('passes id attribute correctly', () => {
      render(<Select options={mockOptions} id="category-select" />);
      expect(screen.getByRole('combobox')).toHaveAttribute('id', 'category-select');
    });

    it('passes required attribute correctly', () => {
      render(<Select options={mockOptions} required />);
      expect(screen.getByRole('combobox')).toBeRequired();
    });

    it('passes aria-label attribute correctly', () => {
      render(<Select options={mockOptions} aria-label="Category selection" />);
      expect(screen.getByRole('combobox')).toHaveAttribute('aria-label', 'Category selection');
    });

    it('passes data-testid attribute correctly', () => {
      render(<Select options={mockOptions} data-testid="category-select" />);
      expect(screen.getByTestId('category-select')).toBeInTheDocument();
    });

    it('passes className attribute correctly', () => {
      render(<Select options={mockOptions} className="custom-select" />);
      expect(screen.getByRole('combobox')).toHaveClass('custom-select');
    });

    it('passes multiple attributes correctly', () => {
      render(
        <Select
          options={mockOptions}
          disabled
          name="category"
          id="category-id"
          required
          className="multi-class"
          data-testid="multi-test"
        />
      );
      
      const select = screen.getByRole('combobox');
      expect(select).toBeDisabled();
      expect(select).toHaveAttribute('name', 'category');
      expect(select).toHaveAttribute('id', 'category-id');
      expect(select).toBeRequired();
      expect(select).toHaveClass('multi-class');
      expect(select).toHaveAttribute('data-testid', 'multi-test');
    });
  });

  describe('Label Integration', () => {
    it('associates label with select using htmlFor', () => {
      render(<Select options={mockOptions} label="Category" id="category" />);
      
      const label = screen.getByText('Category');
      const select = screen.getByRole('combobox');
      
      expect(label).toHaveAttribute('for', 'category');
      expect(select).toHaveAttribute('id', 'category');
    });

    it('renders label with correct styling class', () => {
      render(<Select options={mockOptions} label="Category" />);
      
      const label = screen.getByText('Category');
      expect(label).toHaveClass('form-label');
    });

    it('does not render label when not provided', () => {
      render(<Select options={mockOptions} />);
      
      expect(screen.queryByText('Category')).not.toBeInTheDocument();
    });
  });

  describe('Options Handling', () => {
    it('renders empty select when no options provided', () => {
      render(<Select options={[]} />);
      
      const select = screen.getByRole('combobox');
      expect(select).toBeInTheDocument();
      expect(select.children.length).toBe(0);
    });

    it('renders options with correct values and labels', () => {
      render(<Select options={mockOptions} />);
      
      const select = screen.getByRole('combobox');
      const options = select.querySelectorAll('option');
      
      expect(options[0]).toHaveValue('option1');
      expect(options[0]).toHaveTextContent('Option 1');
      expect(options[1]).toHaveValue('option2');
      expect(options[1]).toHaveTextContent('Option 2');
      expect(options[2]).toHaveValue('option3');
      expect(options[2]).toHaveTextContent('Option 3');
    });

    it('handles options with same value and label', () => {
      const simpleOptions = [
        { value: 'option1', label: 'option1' },
        { value: 'option2', label: 'option2' },
      ];
      
      render(<Select options={simpleOptions} />);
      
      expect(screen.getByText('option1')).toBeInTheDocument();
      expect(screen.getByText('option2')).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('has correct role', () => {
      render(<Select options={mockOptions} />);
      expect(screen.getByRole('combobox')).toBeInTheDocument();
    });

    it('can be focused when not disabled', () => {
      render(<Select options={mockOptions} />);
      
      const select = screen.getByRole('combobox');
      select.focus();
      
      expect(select).toHaveFocus();
    });

    it('cannot be focused when disabled', () => {
      render(<Select options={mockOptions} disabled />);
      
      const select = screen.getByRole('combobox');
      select.focus();
      
      expect(select).not.toHaveFocus();
    });

    it('supports keyboard navigation', () => {
      render(<Select options={mockOptions} />);
      
      const select = screen.getByRole('combobox');
      fireEvent.keyDown(select, { key: 'ArrowDown' });
      
      // Should not throw any errors
      expect(select).toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    it('handles undefined onChange gracefully', () => {
      render(<Select options={mockOptions} />);
      
      const select = screen.getByRole('combobox');
      expect(() => fireEvent.change(select, { target: { value: 'option2' } })).not.toThrow();
    });

    it('handles undefined onFocus gracefully', () => {
      render(<Select options={mockOptions} />);
      
      const select = screen.getByRole('combobox');
      expect(() => fireEvent.focus(select)).not.toThrow();
    });

    it('handles undefined onBlur gracefully', () => {
      render(<Select options={mockOptions} />);
      
      const select = screen.getByRole('combobox');
      expect(() => fireEvent.blur(select)).not.toThrow();
    });

    it('handles empty string value', () => {
      render(<Select options={mockOptions} value="" onChange={() => {}} />);
      
      const select = screen.getByRole('combobox');
      // When value is empty string, it should default to first option
      expect(select).toHaveValue('option1');
    });

    it('handles null value', () => {
      render(<Select options={mockOptions} value={null as any} onChange={() => {}} />);
      
      const select = screen.getByRole('combobox');
      // When value is null, it should default to first option
      expect(select).toHaveValue('option1');
    });

    it('handles options with null or undefined values', () => {
      const problematicOptions = [
        { value: null, label: 'Null Option' },
        { value: undefined, label: 'Undefined Option' },
        { value: 'valid', label: 'Valid Option' },
      ];
      
      render(<Select options={problematicOptions as any} />);
      
      expect(screen.getByText('Null Option')).toBeInTheDocument();
      expect(screen.getByText('Undefined Option')).toBeInTheDocument();
      expect(screen.getByText('Valid Option')).toBeInTheDocument();
    });
  });
}); 