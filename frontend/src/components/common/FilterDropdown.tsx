/**
 * 필터 드롭다운 컴포넌트
 */
interface Option {
  id: number;
  name: string;
}

interface FilterDropdownProps {
  label: string;
  options: Option[];
  value: number | null;
  onChange: (value: number | null) => void;
  placeholder?: string;
}

export function FilterDropdown({
  label,
  options,
  value,
  onChange,
  placeholder = '전체',
}: FilterDropdownProps) {
  return (
    <div className="flex flex-col gap-2">
      <label className="text-sm font-medium text-neutral-muted">
        {label}
      </label>
      <select
        value={value ?? ''}
        onChange={(e) => onChange(e.target.value ? parseInt(e.target.value) : null)}
        className="
          px-4 py-3
          bg-white border-2 border-neutral-border
          rounded-xl
          text-neutral-text
          focus:outline-none focus:border-primary
          transition-colors
          cursor-pointer
        "
        aria-label={label}
      >
        <option value="">{placeholder}</option>
        {options.map((option) => (
          <option key={option.id} value={option.id}>
            {option.name}
          </option>
        ))}
      </select>
    </div>
  );
}
