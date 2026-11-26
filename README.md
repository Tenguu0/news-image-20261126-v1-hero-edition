# The World in One Page — Thursday 26 November 2026

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Tenguu0/news-image-20261126-v1-hero-edition/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Tenguu0/news-image-20261126-v1-hero-edition/reward.svg)](https://make.fun/bounty/news-image-20261126)

An entry for the [news-image-20261126 bounty](https://make.fun/bounty/news-image-20261126): one 1024×1024 newspaper front page that sums up Thursday 26 November 2026 in a single bold image — the **Hero Edition**.

This is the experiment variant of a two-variant test: instead of the usual dense twelve-story grid, this page bets everything on one big full-bleed hero picture of the day's biggest story, with just two more stories below it and as little small text as possible. A reader who missed the day should be able to tell what happened from the image alone, at a glance.

## How to run

You need Python 3 and Pillow. Install the single dependency with:

```sh
pip install pillow
```

Then, from this directory, run:

```sh
python3 main.py
```

The script reads the pictures from `assets/`, draws the complete page with Pillow, and saves the finished image to `/output/entry.png` when that directory exists (as in the make.fun runner), or to `entry.png` next to the script otherwise. To put the output somewhere else, set `OUTPUT_DIR` before running:

```sh
OUTPUT_DIR=/tmp/out python3 main.py
```

When it finishes it prints the path and the size of the file it wrote, for example `wrote /output/entry.png (1024, 1024)`. It needs no network access while it runs — every picture and every word is already in this repository — and it draws its text with the DejaVu and Liberation fonts that ship with most Linux systems.

## Content list

Three stories from Thursday 26 November 2026, each one checked against same-day reporting before it went on the page.

**Hero story — North Korea.** Kim Jong Un inspected nuclear-material production and weapons research facilities and said North Korea should focus on deploying tactical nuclear weapons across multiple domains, state media KCNA reported on Thursday. Kim also said the country's status as a nuclear weapons state was "absolutely inviolable" and that its nuclear material production capacity was being systematically expanded. KCNA did not identify the facilities or their locations.

**Trade — Taiwan holds its 15% U.S. tariff rate.** Taiwan said on Thursday it is confident it will keep its existing 15% tariff rate from the United States, after the Trump administration proposed new tariffs of 20% to 40% on 14 major trading partners. The U.S. Trade Representative's office said it intends to cap new tariffs at the lower levels agreed under trade deals that are completed or still under negotiation, and Taiwan and the U.S. signed an investment cooperation memorandum and an Agreement on Reciprocal Trade earlier this year.

**Energy — Houthis claim a strike on Saudi Arabia's largest refinery.** Yemen's Houthis said they had attacked the Ras Tanura refinery and Riyadh's financial district; the Saudi-led coalition said air defences destroyed four drones over Ras Tanura, with no injuries in an initial assessment. Brent crude settled $3.21 higher at $94.61 a barrel.

## Design & method notes

The layout is deliberately the opposite of the dense format: one hero picture fills more than half the page, edge to edge, with a single huge serif headline laid over a dark gradient at its foot — "KIM ORDERS WIDER NUCLEAR DEPLOYMENT" — plus one short deck line. Below it, two small stories each get one small picture, a red kicker, a bold headline and a single summary line. The masthead and the date, "THURSDAY 26 NOVEMBER 2026", sit at the top in plain sight, and the footer states honestly that the pictures are AI-generated illustrations, not photographs of real events.

All three pictures are AI-generated pictorial illustrations made to match what each story is about: missile launchers and a nuclear facility under a red dawn sky for the hero, a container ship and a microchip for the tariff story, a refinery at dusk with a smoke column for the energy story. Nothing on the page pretends to be a photograph of the real event.

The build is deterministic. The script centre-crops every picture to its frame, draws the text with fixed fonts, and writes the PNG with no timestamps or random elements, so running it three times on the same assets produces byte-identical output (sha256 verified). The headlines and figures on the page are the figures reported that day — the 15% rate, the four drones downed, the $94.61 Brent settlement — with claims attributed to who made them rather than stated as confirmed fact.

## Files

- `main.py` — the entry program. It builds the page end to end and exits 0 on success.
- `assets/` — the three illustrations: `hero-nuclear.png`, `thumb-tariff.png`, `thumb-refinery.png`.
- `LICENSE` — MIT.
