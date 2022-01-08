from dataclasses import dataclass, field
from heapq import heapify, heappush, heappop
from typing import Any, Optional
from typing import List, Dict, Callable


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


class IndexedMinHeap:
    index_fn: Callable[[Any], Any]
    prioritization_fn: Callable[[Any], Any]
    heap_by_index: Dict[Any, List[PrioritizedItem]]  # actually a min-heap - Python is weird

    def __init__(self, index_fn: Callable[[Any], Any], prioritization_fn: Callable[[Any], Any]):
        self.index_fn = index_fn
        self.prioritization_fn = prioritization_fn
        self.heap_by_index = dict()

    def __len__(self):
        return sum(len(heap) for heap in self.heap_by_index.values())

    def peek(self, index: Optional[Any] = None) -> Any:  # O(i)
        index_to_peek = index if index is not None else self.__min_index()
        if index_to_peek is not None:
            pitem = self.__indexed_peek(index_to_peek)
            if pitem:
                return pitem.item
        return None

    def pop(self, index: Optional[Any] = None) -> Any:  # O(i + log n)
        index_to_pop = index if index is not None else self.__min_index()
        if index_to_pop is not None:
            pitem = self.__indexed_pop(index_to_pop)
            if pitem:
                return pitem.item
        return None

    def push(self, item: Any):  # O(log n)
        index = self.index_fn(item)

        if index not in self.heap_by_index.keys():
            self.heap_by_index[index] = []
            heapify(self.heap_by_index[index])

        heap = self.heap_by_index[index]
        priority = self.prioritization_fn(item)
        heappush(heap, PrioritizedItem(priority, item))

    def __indexed_peek(self, index: Any) -> Optional[PrioritizedItem]:  # O(1)
        heap = self.heap_by_index[index]
        return heap[0] if heap else None  # [0] is always the smallest element

    def __indexed_pop(self, index: Any) -> Optional[PrioritizedItem]:  # O(log n)
        heap = self.heap_by_index[index]
        return heappop(heap) if heap else None

    def __min_index(self) -> Optional[Any]:  # O(i)
        min_index: Optional[Any] = None
        min_pitem: Optional[PrioritizedItem] = None
        for index in self.heap_by_index.keys():
            min_pitem_for_index = self.__indexed_peek(index)
            if min_pitem_for_index is not None and (min_pitem is None or min_pitem_for_index < min_pitem):
                min_pitem = min_pitem_for_index
                min_index = index
        return min_index
