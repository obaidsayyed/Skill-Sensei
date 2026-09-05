import type { ReactNode } from 'react'
export default function SectionHeader({ eyebrow, title, action }: { eyebrow?: string; title: string; action?: ReactNode }) {
  return <div className="section-header">{eyebrow && <span className="eyebrow">{eyebrow}</span>}<div className="section-header-row"><h2>{title}</h2>{action}</div></div>
}
