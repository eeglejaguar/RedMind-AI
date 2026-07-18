# RedMind Frontend — Hero Landing Integration

This is your full project with the hero landing page integrated, verified with
an actual `next build`, not just assumed to work.

## What changed, concretely

1. **Route restructure** — your dashboard, scan, results, history, reports,
   and settings pages all moved under a route group: `app/(app)/`. URLs are
   unchanged (`/dashboard`, `/scan`, etc.) — `(app)` is a Next.js grouping
   folder, it does not appear in the URL. This was necessary because the
   sidebar was previously wired into the root layout, and putting the hero
   at `/` meant the sidebar had to move somewhere that didn't apply to the
   landing page.

2. **`app/layout.tsx`** — stripped down to just `<html><body>{children}</body></html>`.
   No more sidebar here. This is now the root layout that both the hero and
   the `(app)` group inherit from.

3. **`app/(app)/layout.tsx`** — new file. Contains the sidebar shell that
   used to live in root layout. Applies to every route under `(app)`.

4. **`app/page.tsx`** — now renders the hero (`horizon-hero-section.tsx`) as
   the public landing page.

5. **`components/Sidebar.tsx`** — one-line fix: the "Dashboard" nav link was
   `href: '/'`, which would have pointed at the hero instead of the actual
   dashboard once I moved things. Changed to `href: '/dashboard'`.

6. **`components/ui/horizon-hero-section.tsx`** — the hero component, with:
   - Two real bugs fixed (position-snap hack on scroll replaced with
     continuous opacity fade; a dead/overwritten nebula-position assignment
     removed)
   - Recolored to your actual brand tokens pulled from `tailwind.config.ts`
     (`#ff1a1a` primary, `#ff3333` glow, `#0a0505` void) — not approximated
     guesses, the literal hex values your Tailwind config already defines
   - `'use client'` directive added — this was missing and broke the actual
     production build (caught by running `next build`, not just `tsc`)

7. **`package.json`** — added `three`, `gsap`, `@types/three`. Everything
   else you already had is untouched.

## What I verified before sending this

- `npm install` — clean
- `npx tsc --noEmit` — zero errors across the whole project
- `npx next build` — succeeds, all 9 routes present with correct paths:
  `/`, `/dashboard`, `/history`, `/reports`, `/results`, `/results/[id]`,
  `/scan`, `/settings`

I did not run `next lint` — you have no `.eslintrc` in the original project,
and the interactive setup prompt isn't something I can answer on your behalf.
Run `npx next lint` yourself if you want that configured.

## Before you run this

1. **Recreate `.env.local`** — I deleted it before zipping since it's an
   env file with a local URL in it and shouldn't ship in a zip by default:
   ```
   NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
   ```
   (or whatever your backend's actual current address is)

2. Install and run:
   ```bash
   npm install
   npm run dev
   ```

3. Check all of these, not just `/`:
   - `/` → hero landing page
   - `/dashboard` → your original dashboard, sidebar present
   - `/scan`, `/history`, `/reports`, `/results`, `/settings` → sidebar
     still present, confirming the route group didn't break them

## What I have not touched

`components/AttackGrid.tsx`, `ProgressBar.tsx`, `ResultsTable.tsx`,
`ScanConsole.tsx`, `SeverityBadge.tsx`, `lib/*`, `store/scanStore.ts`,
`globals.css` — all identical to what you uploaded. I read them to confirm
no conflicts, but made no changes.
