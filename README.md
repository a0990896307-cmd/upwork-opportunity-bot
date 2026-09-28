# Signal-to-Trade Bot (Phase 1: Paper Trading)

Pipeline: **Discord (official Bot Account) → LLM parsing (JSON schema) → rule set → Alpaca paper trades**

## ToS compliance
Access to the Discord channel uses an **official Bot Account** via the Discord API
(`discord.py`, Gateway + Intents). This is the platform-sanctioned method.
A self-bot (user token) is **not** used — it violates Discord ToS and risks a ban.

## Modules
| Module | Purpose |
|---|---|
| `src/discord_listener.py` | Reads signal messages from a channel (bot account) |
| `src/llm_parser.py` | LLM extracts signal → validated `Signal` (pydantic), no hallucinated fields |
| `src/rules.py` | Client's rule set (YAML): allowlist, confidence, position caps, daily loss limit |
| `src/bot.py` | Orchestrator: listener → parser → rules → paper broker |

## Phase 1 = paper only
Every decision is logged (`ACCEPTED (paper)` / `REJECTED`), **nothing is sent to the market yet**.
Phase 2 (live) is a separate milestone after the logic is validated.

## Run
```
pip install -r requirements.txt
cp .env.example .env   # fill real values
python -m src.bot
```

## Safety rails (built-in)
- Kill switch: paper mode until explicitly enabled
- Max position / max open positions / daily loss limit — enforced in rules.yaml
- Strict JSON schema + guardrails: bad signal ⇒ no trade
- Docker deployment with healthcheck + auto-restart (24/7)