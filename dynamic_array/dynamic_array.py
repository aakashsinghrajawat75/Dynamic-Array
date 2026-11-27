"""MyList implementation based on the project's dynamic_array.ipynb notebook."""

import ctypes


class MyList:
    """A dynamic array implemented with a resizable ctypes array."""

    def __init__(self):
        self.size = 1
        self.n = 0
        self.A = self.__make_array(self.size)

    def __str__(self):
        return "[" + ",".join(str(self.A[i]) for i in range(self.n)) + "]"

    def __len__(self):
        return self.n

    def __iter__(self):
        for i in range(self.n):
            yield self.A[i]

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self.A[i] for i in range(*index.indices(self.n))]
        if not isinstance(index, int):
            raise TypeError("array indices must be integers or slices")
        if index < 0:
            index += self.n
        if not 0 <= index < self.n:
            raise IndexError("MyList index out of range")
        return self.A[index]

    def append(self, item):
        if self.n == self.size:
            self.__resize(self.size * 2)
        self.A[self.n] = item
        self.n += 1

    def pop(self, index=-1):
        if self.n == 0:
            raise IndexError("pop from empty MyList")
        if not isinstance(index, int):
            raise TypeError("pop index must be an integer")
        if index < 0:
            index += self.n
        if not 0 <= index < self.n:
            raise IndexError("pop index out of range")
        item = self.A[index]
        for i in range(index, self.n - 1):
            self.A[i] = self.A[i + 1]
        self.n -= 1
        return item

    def clear(self):
        self.size = 1
        self.n = 0
        self.A = self.__make_array(self.size)

    def find(self, item):
        for i in range(self.n):
            if self.A[i] == item:
                return i
        return "ValueError - item is not in the list"

    def insert(self, pos, item):
        if not isinstance(pos, int):
            raise TypeError("insert position must be an integer")
        if pos < 0:
            pos = max(0, self.n + pos)
        else:
            pos = min(pos, self.n)
        if self.n == self.size:
            self.__resize(self.size * 2)
        for i in range(self.n, pos, -1):
            self.A[i] = self.A[i - 1]
        self.A[pos] = item
        self.n += 1

    def __delitem__(self, pos):
        if not isinstance(pos, int):
            raise TypeError("array indices must be integers")
        if pos < 0:
            pos += self.n
        if not 0 <= pos < self.n:
            raise IndexError("MyList index out of range")
        for i in range(pos, self.n - 1):
            self.A[i] = self.A[i + 1]
        self.n -= 1

    def remove(self, item):
        pos = self.find(item)
        if isinstance(pos, int):
            self.__delitem__(pos)
        else:
            return pos

    def min(self):
        if self.n == 0:
            raise ValueError("min() arg is an empty MyList")
        result = self.A[0]
        for i in range(1, self.n):
            if self.A[i] < result:
                result = self.A[i]
        return result

    def max(self):
        if self.n == 0:
            raise ValueError("max() arg is an empty MyList")
        result = self.A[0]
        for i in range(1, self.n):
            if self.A[i] > result:
                result = self.A[i]
        return result

    def sum(self):
        result = 0
        for i in range(self.n):
            result += self.A[i]
        return result

    def sort(self):
        for i in range(self.n - 1):
            for j in range(i + 1, self.n):
                if self.A[i] > self.A[j]:
                    self.A[i], self.A[j] = self.A[j], self.A[i]

    def merge(self, list2):
        count = list2.n
        total_elements = self.n + count
        if self.size < total_elements:
            self.__resize(max(total_elements, self.size * 2))
        for i in range(count):
            self.A[self.n] = list2.A[i]
            self.n += 1

    def extend(self, list2):
        self.merge(list2)

    def __resize(self, new_capacity):
        new_array = self.__make_array(new_capacity)
        for i in range(self.n):
            new_array[i] = self.A[i]
        self.A = new_array
        self.size = new_capacity

    def __make_array(self, capacity):
        return (capacity * ctypes.py_object)()
