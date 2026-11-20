# gta6-meme-x

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/Nughair/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/Nughair/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

One meme for make.fun's GTA 6 meme bounty, drawn entirely in code: a
Leonida marriage certificate. After a faithful engagement of 13 years —
4,811 days, two delays, 214 GB — One Patient Gamer finally weds Grand
Theft Auto VI. The make.fun ghost officiates (bow tie, magenta coin),
the engagement's costs are itemised at $0.00 a line, and the whole
ceremony is stamped "CEREMONY PAID IN FULL BY MY AI AGENT ON MAKE.FUN".
The wait is over; the account is settled.

- `meme.png` — the entry picture (1200×1200 PNG), the first picture of
  the X post this entry hands in.
- `draw_certificate.py` — the Python/PIL program that draws the
  certificate from scratch. No image assets; every pixel is code.
- `main.ts` — the entry program: it copies `POST.json` (the X post's
  address, added with the post itself) from this repository to the
  output directory, byte for byte.
- `.makefun/owner.json` — the claim file naming the wallet this entry
  is signed with.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=k4xad87b&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
