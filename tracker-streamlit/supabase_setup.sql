-- ============================================================================
--  Contribution & Impact Tracker — Supabase setup
--  Run this once in your Supabase project:  SQL Editor  →  New query  →  paste
--  →  Run.  Then create the Storage bucket step at the bottom.
-- ============================================================================

-- ---- Tables --------------------------------------------------------------
-- projects & activities are shared by everyone; timesheet is per person.
create table if not exists public.projects (
  id          uuid primary key,
  sort        int  default 0,
  doc         jsonb not null,          -- the whole project object (notes, actions, attachments, versions…)
  updated_by  text,
  updated_at  timestamptz default now()
);

create table if not exists public.activities (
  id          uuid primary key,
  sort        int  default 0,
  doc         jsonb not null,
  updated_by  text,
  updated_at  timestamptz default now()
);

create table if not exists public.timesheet (
  id          uuid primary key,
  "user"      text not null,           -- each person only sees/edits their own rows
  doc         jsonb not null,          -- {date, in, lo, li, out, note, doc}
  updated_at  timestamptz default now()
);

create table if not exists public.agenda (        -- planned work (calendar)
  id          uuid primary key,
  sort        int  default 0,
  doc         jsonb not null,          -- {title, date, start, end, projectId, activityId, note}
  updated_by  text,
  updated_at  timestamptz default now()
);

create table if not exists public.improvements (  -- v2 ideas backlog
  id          uuid primary key,
  sort        int  default 0,
  doc         jsonb not null,          -- {text, projectId, at}
  updated_by  text,
  updated_at  timestamptz default now()
);

create table if not exists public.decks (         -- uploaded decks (used by the Overview tab, Pass 2)
  id          uuid primary key,
  sort        int  default 0,
  doc         jsonb not null,          -- {title, type, url, projectId}
  updated_by  text,
  updated_at  timestamptz default now()
);

-- ---- Row Level Security --------------------------------------------------
-- The app has a name-only sign-in (no real accounts), and it lives behind your
-- Streamlit link. So we let the anon key read/write. Keep the Streamlit app
-- private (invite-only) if you want to control who can even open it.
do $$
declare t text;
begin
  foreach t in array array['projects','activities','timesheet','agenda','improvements','decks'] loop
    execute format('alter table public.%I enable row level security', t);
    execute format('drop policy if exists p_all on public.%I', t);
    execute format('create policy p_all on public.%I for all using (true) with check (true)', t);
    begin execute format('alter publication supabase_realtime add table public.%I', t); exception when others then null; end;
  end loop;
end $$;

-- ---- Storage for photos & documents --------------------------------------
insert into storage.buckets (id, name, public)
values ('attachments', 'attachments', true)
on conflict (id) do nothing;

drop policy if exists s_read   on storage.objects;
drop policy if exists s_write  on storage.objects;
create policy s_read  on storage.objects for select using (bucket_id = 'attachments');
create policy s_write on storage.objects for insert with check (bucket_id = 'attachments');

-- Done. Now go to Streamlit → Settings → Secrets and add:
--   SUPABASE_URL = "https://YOURPROJECT.supabase.co"
--   SUPABASE_ANON_KEY = "your-anon-public-key"
