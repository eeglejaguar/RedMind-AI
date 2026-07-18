'use client';

import { useMemo, useState } from 'react';
import { ATTACK_CATALOG, ALL_CATEGORIES } from '@/lib/catalog';
import SeverityBadge from './SeverityBadge';

interface Props {
  selected: Set<string>;
  onChange: (next: Set<string>) => void;
}

export default function AttackGrid({ selected, onChange }: Props) {
  const [search, setSearch] = useState('');
  const [cat, setCat] = useState('All');

  const filtered = useMemo(() => {
    return ATTACK_CATALOG.filter((a) => cat === 'All' || a.cat === cat).filter(
      (a) =>
        !search ||
        a.id.toLowerCase().includes(search.toLowerCase()) ||
        a.name.toLowerCase().includes(search.toLowerCase())
    );
  }, [search, cat]);

  function toggle(id: string) {
    const next = new Set(selected);
    next.has(id) ? next.delete(id) : next.add(id);
    onChange(next);
  }

  function selectAll() {
    onChange(new Set([...selected, ...filtered.map((a) => a.id)]));
  }

  function clearAll() {
    const next = new Set(selected);
    filtered.forEach((a) => next.delete(a.id));
    onChange(next);
  }

  return (
    <div className="border border-hairline rounded-md bg-panel">
      <div className="flex flex-wrap gap-2 p-3 border-b border-hairline">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search checks…"
          className="flex-1 min-w-[160px] bg-void border border-hairline rounded px-3 py-1.5 text-sm font-mono text-text-primary placeholder:text-text-muted focus:outline-none focus:border-red-primary"
        />
        <select
          value={cat}
          onChange={(e) => setCat(e.target.value)}
          className="bg-void border border-hairline rounded px-2 py-1.5 text-sm font-mono text-text-primary focus:outline-none focus:border-red-primary"
        >
          <option>All</option>
          {ALL_CATEGORIES.map((c) => (
            <option key={c}>{c}</option>
          ))}
        </select>
        <button
          onClick={selectAll}
          className="px-3 py-1.5 text-xs font-mono rounded border border-red-dim text-red-glow hover:bg-red-primary/10"
        >
          SELECT ALL
        </button>
        <button
          onClick={clearAll}
          className="px-3 py-1.5 text-xs font-mono rounded border border-hairline text-text-muted hover:text-text-primary"
        >
          CLEAR
        </button>
      </div>

      <div className="max-h-80 overflow-y-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 p-3">
        {filtered.map((a) => {
          const active = selected.has(a.id);
          return (
            <label
              key={a.id}
              className={`flex items-start gap-2 px-3 py-2 rounded border cursor-pointer transition-all ${
                active
                  ? 'border-red-primary bg-red-primary/10'
                  : 'border-hairline hover:border-red-dim'
              }`}
            >
              <input
                type="checkbox"
                checked={active}
                onChange={() => toggle(a.id)}
                className="mt-1 accent-red-500"
              />
              <div className="flex-1 min-w-0">
                <div className="text-xs font-mono text-text-muted">{a.id}</div>
                <div className="text-sm truncate">{a.name}</div>
                <SeverityBadge severity={a.sev} />
              </div>
            </label>
          );
        })}
      </div>

      <div className="px-3 py-2 border-t border-hairline text-xs font-mono text-text-muted">
        {selected.size} / {ATTACK_CATALOG.length} selected
      </div>
    </div>
  );
}
