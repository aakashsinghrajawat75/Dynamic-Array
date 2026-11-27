"""Demonstrate the MyList operations from the project notebook."""

from dynamic_array import MyList


def main() -> None:
    numbers = MyList()
    for number in (10, 20, 30):
        numbers.append(number)

    numbers.insert(1, 15)
    print(f"Values: {numbers}")
    print(f"Length: {len(numbers)}; capacity: {numbers.size}")
    print(f"Removed: {numbers.pop()}")
    print(f"Remaining: {numbers}")


if __name__ == "__main__":
    main()
