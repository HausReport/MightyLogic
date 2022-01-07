import pytest

from MightyLogic.HighGrowth.IndexedMinHeap import IndexedMinHeap

# index based on even vs odd length-ed strings
# prioritize by length of the string
heap = IndexedMinHeap(
    index_fn=lambda s: len(s) % 2,
    prioritization_fn=lambda s: len(s))


def test_e2e():
    heap.push("abc")

    assert len(heap) == 1
    assert heap.peek() == "abc"
    assert len(heap) == 1
    assert heap.pop() == "abc"
    assert len(heap) == 0
    assert heap.peek() is None
    assert heap.pop() is None

    heap.push("a")
    heap.push("ab")
    heap.push("abc")
    heap.push("abcd")

    assert len(heap) == 4

    assert heap.peek() == "a"
    assert heap.peek(1) == "a"
    assert heap.peek(0) == "ab"

    assert len(heap) == 4

    assert heap.pop(0) == "ab"
    assert len(heap) == 3
    assert heap.pop() == "a"
    assert len(heap) == 2
    assert heap.pop(1) == "abc"
    assert len(heap) == 1
    assert heap.pop() == "abcd"
    assert len(heap) == 0
