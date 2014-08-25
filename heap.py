import enum
import math
import operator
import unittest


HeapType = enum.Enum('HeapType', ('MIN', 'MAX'))


class Heap:

    """Binary heap based on Wikipedia descriptions:

    - https://en.wikipedia.org/wiki/Heap_(data_structure)
    - https://en.wikipedia.org/wiki/Binary_heap

    """

    def __init__(self, items=(), heap_type=HeapType.MIN, comparator=None):
        self._items = []
        if comparator:
            self.comparator = comparator
        elif heap_type is HeapType.MIN:
            self.comparator = operator.le
        elif heap_type is HeapType.MAX:
            self.comparator = operator.ge
        if items:
            self._items.extend(items)
            self.heapify(self._items)

    def heapify(self, items):
        """Heapify ``items`` in place."""
        num_items = len(items)
        if num_items in (0, 1):
            return items
        # Start from the end of the second level from the bottom.
        last_level = math.floor(math.log(num_items, 2))
        item_index = 2 ** last_level - 1
        while item_index >= 0:
            self._push_down(items, item_index)
            item_index -= 1

    def pop(self):
        if self.is_empty:
            raise TypeError('Can\'t pop from empty heap')
        items = self._items
        item = items[0]
        last_item = items.pop()
        if self.size > 0:
            items[0] = last_item
            self._push_down(items, 0)
        return item

    def peek(self):
        if self.is_empty:
            raise TypeError('Can\'t peek at empty heap')
        return self._items[0]

    def insert(self, item):
        items = self._items
        items.append(item)
        item_index = self.size - 1
        parent_index = (item_index - 1) // 2
        comparator = self.comparator
        while parent_index >= 0:
            parent = items[parent_index]
            if comparator(parent, item):
                break
            items[item_index] = parent
            items[parent_index] = item
            item_index = parent_index
            parent_index = (item_index - 1) // 2

    @property
    def is_empty(self):
        return len(self._items) == 0

    @property
    def size(self):
        return len(self._items)

    def _push_down(self, items, i):
        """Push the item at ``i`` down.

        This pushes the item at ``i`` downward (i.e., swaps it with one
        of its children) until the heap property is restored for the
        item (relative to its children).

        """
        item = items[i]
        size = len(items)
        comparator = self.comparator
        while i < size:
            child = None
            left_i = 2 * i + 1
            if left_i < size:
                child_i = left_i
                child = items[left_i]
                right_i = left_i + 1
                if right_i < size and comparator(items[right_i], child):
                    child_i = right_i
                    child = items[right_i]
            if child is None:
                break
            if comparator(child, item):
                items[i] = child
                items[child_i] = item
                i = child_i
            else:
                break

    def __repr__(self):
        return str(self._items)

    def __str__(self):
        items = self._items
        rows = []
        d = 0
        i = 0
        while i < self.size:
            i = 2 ** d - 1
            j = 2 ** (d + 1) - 1
            d += 1
            template = '{{:<{}}}'.format((j - i) * 2 - 1)
            row = items[i:j]
            row = ' '.join(str(item) for item in row)
            row = template.format(row)
            rows.append(row)
        return '\n'.join('{:^80}'.format(r) for r in rows)


class TestMinHeap(unittest.TestCase):

    def setUp(self):
        self.heap = Heap([6, 1, 3, 2, 7, 4, 5])

    def test_heapify_empty_list(self):
        empty_list = []
        self.heap.heapify(empty_list)
        self.assertEqual(empty_list, [])

    def test_heapify_single_item_list(self):
        single_item_list = [1]
        self.heap.heapify(single_item_list)
        self.assertEqual(single_item_list, [1])

    def test_heapify_two_item_list(self):
        two_item_list = [1, 0]
        self.heap.heapify(two_item_list)
        self.assertEqual(two_item_list, [0, 1])

    def test_heapify_three_item_list(self):
        three_item_list = [2, 1, 0]
        self.heap.heapify(three_item_list)
        self.assertEqual(three_item_list[0], 0)
        self.assertIn(1, three_item_list[1:])
        self.assertIn(2, three_item_list[1:])

    def test_size(self):
        self.assertEqual(self.heap.size, 7)

    def test_is_empty(self):
        self.assertFalse(self.heap.is_empty)

    def test_peek(self):
        self.assertEqual(self.heap.peek(), 1)

    def test_insert_min(self):
        self.heap.insert(0)
        self.assertEqual(self.heap.peek(), 0)

    def test_insert_dup(self):
        self.heap.insert(2)
        self.assertEqual(self.heap.peek(), 1)
        self.assertEqual(self.heap._items.count(2), 2)

    def test_pop(self):
        smallest = self.heap.pop()
        self.assertEqual(smallest, 1)
        self.assertEqual(self.heap.peek(), 2)

    def test_pop_till_empty(self):
        items = []
        self.heap.insert(0)
        self.heap.insert(2)
        self.heap.insert(2)
        while not self.heap.is_empty:
            items.append(self.heap.pop())
        self.assertTrue(self.heap.is_empty)
        self.assertEqual(items, [0, 1, 2, 2, 2, 3, 4, 5, 6, 7])


class TestMaxHeap(unittest.TestCase):

    def setUp(self):
        self.heap = Heap([6, 1, 3, 2, 7, 4, 5], heap_type=HeapType.MAX)

    def test_heapify_empty_list(self):
        empty_list = []
        self.heap.heapify(empty_list)
        self.assertEqual(empty_list, [])

    def test_heapify_single_item_list(self):
        single_item_list = [1]
        self.heap.heapify(single_item_list)
        self.assertEqual(single_item_list, [1])

    def test_heapify_two_item_list(self):
        two_item_list = [0, 1]
        self.heap.heapify(two_item_list)
        self.assertEqual(two_item_list, [1, 0])

    def test_heapify_three_item_list(self):
        three_item_list = [0, 1, 2]
        self.heap.heapify(three_item_list)
        self.assertEqual(three_item_list[0], 2)
        self.assertIn(1, three_item_list[1:])
        self.assertIn(0, three_item_list[1:])

    def test_size(self):
        self.assertEqual(self.heap.size, 7)

    def test_is_empty(self):
        self.assertFalse(self.heap.is_empty)

    def test_peek(self):
        self.assertEqual(self.heap.peek(), 7)

    def test_insert_max(self):
        self.heap.insert(8)
        self.assertEqual(self.heap.peek(), 8)

    def test_insert_dup(self):
        self.heap.insert(2)
        self.assertEqual(self.heap.peek(), 7)
        self.assertEqual(self.heap._items.count(2), 2)

    def test_pop(self):
        largest = self.heap.pop()
        self.assertEqual(largest, 7)
        self.assertEqual(self.heap.peek(), 6)

    def test_pop_till_empty(self):
        items = []
        self.heap.insert(0)
        self.heap.insert(2)
        self.heap.insert(2)
        while not self.heap.is_empty:
            items.append(self.heap.pop())
        self.assertTrue(self.heap.is_empty)
        self.assertEqual(items, [7, 6, 5, 4, 3, 2, 2, 2, 1, 0])
