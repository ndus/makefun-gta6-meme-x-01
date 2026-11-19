[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/ndus/makefun-gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/ndus/makefun-gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

# The 13-Year Loading Screen

A GTA 6 meme for the make.fun bounty. The loading bar finally hits 100% after 13 years, and the tip reveals what the player's agent did in the meantime: earn real money from make.fun bounties.

`make_meme.py` draws the entire image with Pillow. Run `python3 make_meme.py` to write `meme.png`.

`main.ts` copies `POST.json` to the output directory. Run `mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts` to write `out/POST.json`. When running from the repository root without a `/bot` directory, set `MAKEFUN_BOT_DIR=.` for the Node command.

**Status.** The meme is ready. The entrant will post it on X from his public account and add the post's real URL to `POST.json` before submitting.
