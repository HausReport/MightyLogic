from __future__ import annotations

import logging
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Any, List, Callable, Dict, Set

logger = logging.getLogger("MightyLogic.Heroes")


def create_secondary_index(data: Iterable[Any], for_accessor: Callable[[Any], Any]) -> Dict[Any, Any]:
    return create_secondary_indices(data, [for_accessor])[0]


def create_secondary_indices(data: Iterable[Any], for_accessors: List[Callable[[Any], Any]]) -> List[Dict[Any, Any]]:
    secondary_indices = [dict() for _accessor in for_accessors]
    for datum in data:
        for i, accessor in enumerate(for_accessors):
            index = secondary_indices[i]
            key = accessor(datum)
            if key in index.keys():
                raise KeyError(f"Data for key \"{key}\" already exists in {index}")
            index[key] = datum
    return secondary_indices


def deserialize_lines(path_to_file: Path, deserializer: Callable[[str], Any]) -> List[Any]:
    _list = []
    with path_to_file.open() as file:
        for line in file:
            line = line.strip()
            try:
                deserialized = deserializer(line)
                logger.debug(f"Deserialized {deserialized} (created from \"{line}\")")
                _list.append(deserialized)
            except Exception as e:
                raise RuntimeError(f"Failed to deserialize: \"{line}\"") from e
    return _list


def group_by(values: Iterable[Any], grouper: Callable[[Any], Any], include_all: bool) -> Dict[Any, Set[Any]]:
    grouped = defaultdict(set)
    for value in values:
        if include_all:
            grouped["all"].add(value)
        grouped[grouper(value)].add(value)
    return grouped


def per_group(grouped: Dict[Any, Set[Any]], do: Callable[[Set[Any]], Any]) -> Dict[Any, Any]:
    return dict((name, do(group)) for name, group in grouped.items())


def stats_for(values: Iterable[Any]) -> Dict[str, float]:
    return {
        "min": min(values) if values else None,
        #"mean": mean(values) if values else None,
        #"median": median(values) if values else None,
        #"mode": mode(values) if values else None,
        "max": max(values) if values else None,
        #"variance": pvariance(values) if values else None,
        #"stdev": stdev(values) if values else None,
        # TODO: "quantiles": quantiles(values, n=4, method="inclusive")
    }
