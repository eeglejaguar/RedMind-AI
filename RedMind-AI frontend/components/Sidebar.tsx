"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Crosshair,
  ScrollText,
  History,
  FileWarning,
  Settings,
  Skull,
  Bot,
} from "lucide-react";

const NAV = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  {
    href: "/assistant",
    label: "AI Assistant",
    icon: Bot,
  },

  { href: "/scan", label: "New Scan", icon: Crosshair },
  { href: "/history", label: "History", icon: History },
  { href: "/reports", label: "Reports", icon: FileWarning },
  { href: "/settings", label: "Settings", icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-60 shrink-0 h-screen bg-panel border-r border-hairline flex flex-col sticky top-0">
      <div className="px-5 py-6 flex items-center gap-2 border-b border-hairline">
        <Skull
          size={22}
          className="text-red-primary animate-pulseglow rounded"
        />
        <span className="font-display font-bold text-xl tracking-widest">
          RED<span className="text-red-primary text-glow">MIND</span>
        </span>
      </div>

      <nav className="flex-1 flex flex-col gap-1 px-2 py-4">
        {NAV.map(({ href, label, icon: Icon }) => {
          const active = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              className={`group flex items-center gap-3 px-4 py-3 rounded-md font-mono text-sm tracking-wide transition-all
                ${
                  active
                    ? "bg-panel-raised text-red-glow border-l-2 border-red-primary shadow-[0_0_14px_rgba(255,26,26,0.35)]"
                    : "text-text-muted border-l-2 border-transparent hover:text-text-primary hover:bg-panel-raised/60"
                }`}
            >
              <Icon size={18} className={active ? "text-red-primary" : ""} />
              {label.toUpperCase()}
            </Link>
          );
        })}
      </nav>

      <div className="px-5 py-4 border-t border-hairline text-[10px] text-text-muted font-mono">
        RedMind-AI VAPT ENGINE
        <br />
        <span className="text-red-dim">v2.0 // NEXT.JS</span>
      </div>
    </aside>
  );
}
