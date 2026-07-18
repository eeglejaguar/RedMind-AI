# RedMind-AI Frontend (Next.js)

Replacement for the single-file `dashboard.html`. Same backend contract, new stack.

## Setup

```bash
npm install
npm run dev
```

Runs on `http://localhost:3000`. Requires the existing FastAPI backend (`main.py`) running on
`http://127.0.0.1:8000` (or whatever you set in `.env.local` → `NEXT_PUBLIC_API_URL`).

CORS in `main.py` is already `allow_origins=["*"]`, so no backend change is needed to accept
requests from `localhost:3000`.

## What's real vs. simulated (read this before demoing)

- **Progress bar**: reflects actual completed `/run` calls from this browser tab — it is a
  faithful indicator of "how far the sequential fetch loop has gotten," not of true backend
  execution state. Closing this tab stops the scan, same as the original dashboard. This was a
  deliberate choice to ship fast against the current synchronous `POST /run` endpoint rather than
  rewrite the backend for SSE/WebSocket streaming.
- **State**: Zustand in memory + `localStorage` (`rm_scan_history`, `rm_last_results`) — no
  backend persistence, matching the original architecture. Clearing browser storage clears
  history.
- **Scan profiles / catalog**: ported directly from the original `dashboard.html`
  (`ATTACK_CATALOG`, `MODULES_QUICK/WEB/NETWORK/FULL`) into `lib/catalog.ts`. The underlying
  module logic in the Python backend is unchanged — see `RedMind-AI_PROJECT_REFERENCE.md` for the
  caveat that most "named" checks share one of 8 generic payload templates.

## Structure

```
app/
  layout.tsx          Sidebar shell, global theme
  page.tsx            Dashboard / overview
  scan/page.tsx        Launch + monitor a scan
  results/page.tsx     Redirects to latest scan
  results/[id]/page.tsx  Scan detail + findings
  history/page.tsx     Past scans
  reports/page.tsx     Summary report view
  settings/page.tsx    Backend URL (read-only, env-driven)
components/
  Sidebar.tsx
  ProgressBar.tsx       Segmented threat-meter, driven by scanStore
  ScanConsole.tsx       Terminal-style live log
  AttackGrid.tsx        Custom check selector
  ResultsTable.tsx       Expandable per-check findings
  SeverityBadge.tsx
store/
  scanStore.ts          Zustand — owns the sequential /run loop
lib/
  api.ts                fetch wrapper for POST /run
  catalog.ts             Static check catalog (ported from dashboard.html)
  types.ts               Shared TS types
```

## Migrating to real (server-pushed) progress later

When you're ready to stop simulating progress client-side, the only file that needs a rewrite is
`store/scanStore.ts`'s `startScan` function — swap the `for` loop + sequential `fetch` calls for
an `EventSource` subscription against a new `POST /scan/start` + `GET /scan/{id}/stream` backend
pair. Every component (`ProgressBar`, `ScanConsole`, `ResultsTable`) reads from the store's
`current` state and does not need to change.

## Theme

Aggressive red-on-black. Tokens live in `tailwind.config.ts` (`red.primary`, `red.glow`,
`red.dim`, `critical/high/medium/low/info`, `panel`, `void`). Fonts: Chakra Petch (display),
JetBrains Mono (body/mono) — loaded via Google Fonts in `app/globals.css`.
