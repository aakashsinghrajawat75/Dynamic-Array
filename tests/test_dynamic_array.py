import pytest

from dynamic_array import MyList


def make_list(*values: int) -> MyList:
    result = MyList()
    for value in values:
        result.append(value)
    return result


def test_append_grows_capacity_and_preserves_values() -> None:
    array = MyList()
    for value in (1, 2, 3):
        array.append(value)

    assert list(array) == [1, 2, 3]
    assert len(array) == 3
    assert array.size >= 3


def test_negative_indexing_and_slicing() -> None:
    array = make_list(1, 2, 3, 4)
    assert array[0] == 1
    assert array[-1] == 4
    assert array[-3:-1] == [2, 3]


def test_insert_clamps_index_and_pop_returns_value() -> None:
    array = make_list(2)
    array.insert(100, 3)
    array.insert(-100, 1)

    assert list(array) == [1, 2, 3]
    assert array.pop(1) == 2
    assert array.pop() == 3
    assert list(array) == [1]


def test_find_remove_and_delete() -> None:
    array = make_list(1, 2, 2, 3)
    assert array.find(2) == 1

    array.remove(2)
    assert list(array) == [1, 2, 3]
    del array[-1]
    assert list(array) == [1, 2]
    assert array.find(99) == "ValueError - item is not in the list"


def test_sort_min_max_sum_clear_and_merge_extend() -> None:
    array = make_list(4, 1, 3)
    array.sort()
    assert list(array) == [1, 3, 4]
    assert array.min() == 1
    assert array.max() == 4
    assert array.sum() == 8

    other = make_list(5, 6)
    array.merge(other)
    assert list(array) == [1, 3, 4, 5, 6]
    array.extend(make_list(7))
    assert list(array) == [1, 3, 4, 5, 6, 7]

    array.clear()
    assert len(array) == 0
    assert array.size == 1


def test_invalid_indexes_and_empty_operations_raise() -> None:
    array = MyList()
    with pytest.raises(IndexError):
        _ = array[0]
    with pytest.raises(IndexError):
        array.pop()
    with pytest.raises(IndexError):
        del array[0]
    with pytest.raises(ValueError):
        array.min()
    with pytest.raises(ValueError):
        array.max()
