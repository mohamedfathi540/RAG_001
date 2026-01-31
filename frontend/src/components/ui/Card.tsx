import { cn } from "../../utils/helpers";
import type { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
  title?: string;
  subtitle?: string;
  actions?: ReactNode;
}

export function Card({
  children,
  className,
  title,
  subtitle,
  actions,
}: CardProps) {
  return (
    <div
      className={cn(
        "bg-bg-secondary border border-border rounded-xl overflow-hidden",
        className,
      )}
    >
      {(title || subtitle || actions) && (
        <div className="px-6 py-4 border-b border-border flex items-center justify-between">
          <div>
            {title && (
              <h3 className="text-lg font-semibold text-text-primary">
                {title}
              </h3>
            )}
            {subtitle && (
              <p className="text-sm text-text-secondary mt-1">{subtitle}</p>
            )}
          </div>
          {actions && <div className="flex items-center gap-2">{actions}</div>}
        </div>
      )}
      <div className="p-6">{children}</div>
    </div>
  );
}
