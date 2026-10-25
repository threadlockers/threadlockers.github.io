## Blogroll

`blogroll/index.md` and `blogroll/index.html` are kept in sync by the
`Sync blogroll` GitHub Action on every push to `main`:

- Add or remove a URL in `index.md` (one per line, optionally
  `[Custom title](URL)`): the action fetches the title and favicon,
  updates `index.html`, and pushes.
- Edit only `index.html`: the action rewrites `index.md` to match.
- Mark featured links with `data-featured` on the `<li>` in `index.html`.

Run it locally with `python3 scripts/sync_blogroll.py --from md` (or `--from html`).
