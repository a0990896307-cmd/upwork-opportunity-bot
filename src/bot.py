"""
Orchestrator: wires Discord listener -> LLM parser -> rules -> broker.

Phase 1 runs in PAPER mode: every decision is logged but nothing is sent
to the market. The whole pipeline is exercised end-to-end.
"""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

from src.discord_listener import run_listener
from src.llm_parser import Signal, SignalParser
from src.rules import RuleSet, RulesEngine

log = logging.getLogger(__name__)


class PaperBroker:
    """Phase 1: pretend to trade, log everything, trade nothing."""

    def __init__(self, engine: RulesEngine):
        self.engine = engine
        self.orders: list[dict] = []

    async def execute(self, signal: Signal) -> None:
        allow, reason = self.engine.decide(signal)
        if not allow:
            log.info("REJECTED: %s (%s)", reason, signal.pair or signal.raw_text[:60])
            return
        order = {
            "pair": signal.pair,
            "side": signal.side.value,
            "entry": signal.entry,
            "stop": signal.stop,
            "target": signal.target,
            "confidence": signal.confidence,
            "status": "PAPER_ORDER",
        }
        self.orders.append(order)
        log.info("ACCEPTED (paper): %s", order)


@dataclass
class BotConfig:
    discord_token: str
    channel_id: int
    openai_key: str
    rules_path: str
    model: str = "gpt-4o-mini"


async def run_bot(cfg: BotConfig) -> None:
    rules = RuleSet.from_yaml(cfg.rules_path)
    engine = RulesEngine(rules)
    broker = PaperBroker(engine)
    parser = SignalParser(api_key=cfg.openai_key, model=cfg.model)

    async def on_signal(msg) -> None:
        signal = await parser.parse(msg.content)
        if signal is None:
            log.warning("Unparseable message ignored: %r", msg.content[:120])
            return
        await broker.execute(signal)

    await run_listener(token=cfg.discord_token, channel_id=cfg.channel_id, on_signal=on_signal)


if __name__ == "__main__":
    import os

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    asyncio.run(
        run_bot(
            BotConfig(
                discord_token=os.environ["DISCORD_TOKEN"],
                channel_id=int(os.environ["SIGNAL_CHANNEL_ID"]),
                openai_key=os.environ["OPENAI_API_KEY"],
                rules_path="rules.yaml",
            )
        )
    )