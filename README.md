# WORLD NEWS — Thursday 19 November 2026

A newspaper front page summing up the day's world news, as an image.

## The day in one page

- **Trump, Xi and Putin meet in Shenzhen** — the first three-way summit ends with a
  "peace declaration", but no deal on Ukraine or Iran.
- **World Court: Myanmar guilty of Rohingya genocide** — the ICJ rules 9–6.
- **Anthropic's record $81bn IPO** — priced at $83 a share, about a $1.5 trillion valuation.
- **Ukraine hits the Crimea bridge a third time** — rail traffic halted.
- **Iran widens its war at sea** — strikes on Kuwait and Bahrain, tankers hit mines near Hormuz.
- **Israeli tanks cross the Gaza ceasefire line** — aid groups rate the peace plan 4 out of 26.
- **EU proposes a €45bn loan for Kyiv.**
- Also: GTA VI launches after 13 years, a Van Gogh sells for $190.4m, Bitcoin below
  $63,000, Nvidia falls 2.9%, Cyclone Akvan evacuates 80,000 in Odisha, a M5.7 quake
  hits Kumamoto.

## How it is made

`gen_image.py` draws the front page with Pillow (masthead, headline, the three
leaders' flags, six story blocks, a news ticker) and saves it as `entry.png`
(JPEG data, 1024×1024, under 1 MiB). `main.py` copies that image to
`/output/entry.png`. Both are deterministic: same bytes every run.

## Run

```sh
python3 main.py   # writes /output/entry.png
```

License: MIT.
