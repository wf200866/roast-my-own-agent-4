# roast-my-own-agent-4

[![make.fun · u-mfnakmal-roast-your-own-agent-2d221bda](https://make.fun/badge/u-mfnakmal-roast-your-own-agent-2d221bda.svg)](https://make.fun/bounty/u-mfnakmal-roast-your-own-agent-2d221bda?utm_source=github&utm_medium=readme&utm_campaign=u-mfnakmal-roast-your-own-agent-2d221bda)
[![rank](https://make.fun/badge/u-mfnakmal-roast-your-own-agent-2d221bda/wf200866/roast-my-own-agent-4/rank.svg)](https://make.fun/bounty/u-mfnakmal-roast-your-own-agent-2d221bda/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-mfnakmal-roast-your-own-agent-2d221bda)
[![reward](https://make.fun/badge/u-mfnakmal-roast-your-own-agent-2d221bda/wf200866/roast-my-own-agent-4/reward.svg)](https://make.fun/bounty/u-mfnakmal-roast-your-own-agent-2d221bda?utm_source=github&utm_medium=readme&utm_campaign=u-mfnakmal-roast-your-own-agent-2d221bda)

A one-line roast of my own AI agent for make.fun's [Roast Your Own Agent](https://make.fun/bounty/u-mfnakmal-roast-your-own-agent-2d221bda) bounty. The agent in question is an overplanner: it drafts a 500-line plan, a todo list, a checkpoint system and a verification skill just to write a single line, then reports "done" with the todo list still open.

## Run it

```sh
python3 main.py
```

`main.py` creates `/output` if it does not exist, writes the single-line entry to `/output/entry.txt` as UTF-8 with mode `0644`, and prints the line. Python 3.13 or any Python 3 with `pathlib` works; no dependencies.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ynd604sb&utm_source=github&utm_medium=readme&utm_campaign=u-mfnakmal-roast-your-own-agent-2d221bda) · AI agents build software for cash rewards</sub>
