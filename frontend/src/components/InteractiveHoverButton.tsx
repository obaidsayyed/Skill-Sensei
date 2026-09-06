import React from 'react'
import { ArrowRight } from 'lucide-react'

export interface InteractiveHoverButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {}

const InteractiveHoverButton = React.forwardRef<HTMLButtonElement, InteractiveHoverButtonProps>(
  ({ className = '', children, type = 'button', ...props }, ref) => {
    return (
      <button
        ref={ref}
        type={type}
        className={`interactive-hover-button ${className}`.trim()}
        {...props}
      >
        <div className="ihb-content">{children}</div>
        <div className="ihb-hover-content" aria-hidden="true">
          <div>{children}</div>
          <ArrowRight className="ihb-arrow" size={16} />
        </div>
        <div className="ihb-fill" aria-hidden="true" />
      </button>
    )
  },
)

InteractiveHoverButton.displayName = 'InteractiveHoverButton'

export { InteractiveHoverButton }
