# Teach Me

A self-directed learning workspace: a small static site of short, self-contained
lessons across several subjects, published to GitHub Pages.

Each subject is a top-level folder containing its own lessons, reference material,
and a record of what's been learned. Lessons are quick to complete and tied to a
concrete personal mission.

## Subjects

- **Chess** — climb ~300 rating points (blitz & rapid).
- **Hungarian History** — general cultural fluency in Magyar történelem.
- **Geography** — a durable, practical mental map of the world.

## Layout

```
teach-me/
├── index.html            # Combined landing page (generated)
├── build_site.py         # Builds the index pages from lesson folders
├── <subject>/
│   ├── index.html        # Per-subject index (generated)
│   ├── MISSION.md        # Why the subject is being learned
│   ├── RESOURCES.md      # Trusted resources to ground lessons
│   ├── NOTES.md          # Teaching preferences / working notes
│   ├── lessons/*.html    # The lessons (self-contained HTML)
│   ├── reference/*.html  # Cheat sheets and quick-reference docs
│   └── learning-records/*.md  # What's been learned, ADR-style
```

A new subject needs no configuration — any top-level folder with a `lessons/`
directory is picked up automatically.

## Building

Regenerate the per-subject indexes and the combined landing page:

```sh
python3 build_site.py
```

## Deployment

Lessons are published to GitHub Pages. When a lesson is added or changed, the site
is rebuilt and the change is committed and pushed automatically:

- A `PostToolUse` hook (`.claude/hooks/deploy-lesson.py`) rebuilds, commits, and
  pushes whenever a `lessons/*.html` file is written.
- The teaching workflow also publishes explicitly as the final step of creating a
  lesson, so deployment is reliable even when working inside a subject subfolder.
