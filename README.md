# Dynamic Array Python

A Python dynamic-array project based on the `MyList` implementation in
`dynamic_array.ipynb`. The package, example, tests, and Streamlit dashboard use
that same `ctypes`-backed implementation and its notebook operations.

## Author

[Aakash Rajawat on LinkedIn](https://www.linkedin.com/in/aakashrajawat75/)

## Project layout

- `dynamic_array/` — reusable `MyList` implementation based on the project notebook
- `tests/` — unit tests
- `examples/` — runnable basic-operations example
- `dynamic_array.ipynb` — project notebook containing the `MyList` implementation
- `notebooks/` — additional Jupyter demo
- `ui/` — Streamlit dashboard for the notebook's `MyList` operations
- `screenshots/` — location for captured UI screenshots

## Setup

Use Python 3.10 or newer. From the project root, install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run

Run the example:

```bash
python -m examples.basic_operations
```

Launch the dashboard:

```bash
streamlit run ui/app.py
```

The dashboard shows array values in indexed memory slots, current length and
capacity metrics, and recent activity. Use the tabs to append values, inspect
indexes and slices, edit the array, merge or extend values, and run searches or
statistics.

Run the tests:

```bash
pytest
```

`MyList` supports append, length, indexing, slicing (including negative
indexes), pop, clear, find, insert, delete, remove, sort, min, max, sum, merge,
and extend. The dashboard exposes these operations interactively.
