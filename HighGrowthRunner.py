import logging
import sys
from pathlib import Path
from typing import Any

from MightyLogic.Heroes.Collection import Collection
from MightyLogic.HighGrowth import Discount
from MightyLogic.HighGrowth.Calculator import HighGrowthCalculation
from MightyLogic.HighGrowth.Strategies.MinimizeGold import MinimizeGold

logging.basicConfig(stream=sys.stdout, format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()


def pretty_format(thing: Any, indent: int = 0):
    def do_indent(s, i=indent):
        return ("  " * i) + s + "\n"

    formatted = ""
    if isinstance(thing, dict):
        formatted += do_indent("{")
        for k, v in thing.items():
            formatted += do_indent(f"{k}: {pretty_format(v, indent + 1).strip()}", indent + 1)
        formatted += do_indent("}")
    elif isinstance(thing, list) or isinstance(thing, set) or isinstance(thing, frozenset):
        formatted += do_indent("[")
        for v in thing:
            formatted += pretty_format(v, indent + 1)
        formatted += do_indent("]")
    else:
        formatted += do_indent(str(thing))
    return formatted


collection = Collection.from_squad_export_file(Path("tests/HighGrowth/2021-07-25-1342_Bobo_squad_export.txt"))

logger.info(f"Your heroes (before): {pretty_format(collection.oh_dir.values())}")
logger.info(f"Summary: {pretty_format(collection.oh_dir.summarize())}")

logger.info("-" * 120)

calc = HighGrowthCalculation.from_strategy(
    high_growth_strategy=MinimizeGold(collection.oh_dir, Discount.GUILD_5.value),
    gold_cap=188_000
)

logger.info(calc)

logger.info("-" * 120)

logger.info(f"Your heroes (after): {pretty_format(collection.oh_dir.values())}")
logger.info(f"Summary: {pretty_format(collection.oh_dir.summarize())}")
