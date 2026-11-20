# THE WORLD — Thursday 19 November 2026 (v2)

A newspaper front page summing up the day's world news, as an image.

## The day in one page

- **Trump, Xi and Putin meet in Shenzhen** — the first three-way summit ends with
  a declaration that nuclear war must never happen, but no arms-control talks
  are agreed.
- **ICJ rules Myanmar committed genocide** — the World Court rules 9–6 in a case
  brought by Gambia over the Rohingya; the state is responsible.
- **COP31 draft drops fossil fuel language** — Antalya negotiators strip the
  phase-out pledge from the draft as finance talks stall.
- **Anthropic's $81.3bn IPO debuts** — shares close at $97.17, up 17% on the
  Nasdaq; the largest IPO on record.
- **Third Crimea bridge strike in a week** — rail traffic halted; the EU plans a
  €45bn loan for 2027.
- **Gaza peace plan scores 4 of 26** — five aid groups rate the truce as
  residents start returning.
- Also: GTA VI launches after 13 years, Cyclone Akvan evacuates 100,000+ in
  Odisha, US–Venezuela restore military ties, a Van Gogh sells for $190.4m.

## How it is made

`gen_image.py` draws the front page with Pillow and saves it as `entry.png`
(JPEG data, 1024×1024, under 1 MiB). v2 changes: a smaller masthead so the lead
wins; the summit shown as one editorial illustration (a round table seen from
above, three flag-coloured chairs, a declaration sheet in the middle) instead
of three flag panels; a 1 + 2 + 3 hierarchy (one lead, two secondary stories,
three short summaries); every headline carries the development, not just the
topic; a two-item ticker. A `fit()` guard refuses to ship any headline or body
longer than two lines. `main.py` copies that image to `/output/entry.png`.
Both are deterministic: same bytes every run.

## Run

```sh
python3 main.py   # writes /output/entry.png
```

License: MIT.
