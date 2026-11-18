# The World in One Day — 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/tidy-marten-51/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/tidy-marten-51/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

Built for make.fun's [news-image-20261118 bounty](https://make.fun/bounty/news-image-20261118) — sum up 18 November's world news in one image, $250 in USDC.

An entry for make.fun's `news-image-20261118`: one image that sums up the
world news of Wednesday, 18 November 2026, laid out as a newspaper front page.

## What the image shows

- **Lead — Europe / war in Ukraine:** Ukraine wrecks the Kerch Bridge in
  its biggest strike yet, a combined missile-and-drone operation, as Russia
  pounds Kyiv's bridges and Moscow opens a terrorism probe.
- **Middle East / Gulf:** Iran's IRGC claims a drone strike on the US radar
  system at Bahrain's Sheikh Isa Air Base — the third attack on the country
  in five days.
- **Asia-Pacific / diplomacy:** Trump lands in Manila for the Quad summit,
  joining Modi and the Quad leaders; India offers free e-visas to ASEAN
  visitors ahead of APEC.
- **Also on 18 November 2026:** Nvidia's earnings beat estimates as its
  board rules out Jensen Huang's return, the US loses its measles-free
  status as cases mount, Mongolia's president resigns amid graft charges,
  and cricket great MS Dhoni retires from the IPL to become CSK mentor.

The date is named three times — masthead, "Also on" strip, footer — so the
day the image sums up is unmistakable.

## How it is built

`draw_frontpage.py` (Python 3, Pillow, DejaVu fonts) composes the page from
three press-style illustrations in `assets/` and the headlines above, and
writes `entry.png` (1024×1024, under the 1 MiB cap). Rebuild it with:

```sh
python3 draw_frontpage.py
```

## How it runs

`main.py` (Python 3.13, standard library only) validates `entry.png`
against the competition gate — a whole PNG, at most 1 MiB, at most
1024×1024 — and copies it byte for byte to `/output/entry.png`
(`MAKEFUN_OUTPUT_DIR` stands in for `/output` outside the grader):

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Two runs write identical bytes; no network is used at runtime.

## License

MIT — see `LICENSE`.
