'use client';

import { API_URL } from '@/lib/api';

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <header>
        <h1 className="font-display text-3xl font-bold tracking-wide text-red-glow text-glow">
          SETTINGS
        </h1>
      </header>

      <div className="bg-panel border border-hairline rounded-md p-6 space-y-4">
        <div>
          <label className="text-xs font-mono text-text-muted block mb-1.5">BACKEND API URL</label>
          <input
            value={API_URL}
            disabled
            className="w-full bg-void border border-hairline rounded px-4 py-2.5 font-mono text-sm opacity-60 cursor-not-allowed"
          />
          <p className="text-xs text-text-muted mt-2">
            Configured via <code className="text-red-glow">NEXT_PUBLIC_API_URL</code> in{' '}
            <code className="text-red-glow">.env.local</code>. Change it there and restart the dev
            server — it is intentionally not editable at runtime.
          </p>
        </div>
      </div>
    </div>
  );
}
