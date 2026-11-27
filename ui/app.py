"""Streamlit interface for the MyList dynamic array in the project notebook."""

import html
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from dynamic_array import MyList


def parse_value(raw_value):
    """Parse numeric text as a number and keep other input as text."""
    value = raw_value.strip()
    if not value:
        raise ValueError("Enter a value.")
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def parse_values(raw_values):
    values = [value.strip() for value in raw_values.split(",")]
    if not raw_values.strip() or any(not value for value in values):
        raise ValueError("Enter comma-separated values, for example: 3, 5, 8.")
    return [parse_value(value) for value in values]


def parse_optional_index(raw_index):
    return None if not raw_index.strip() else int(raw_index)


OPERATION_FAILED = object()


def set_message(message, location):
    st.session_state.operation_outputs[location] = message
    history = st.session_state.operation_history
    history.insert(0, message)
    del history[20:]


def render_operation_output(location):
    message = st.session_state.operation_outputs.get(location)
    if message:
        st.success(message)


def run_operation(operation):
    try:
        result = operation()
    except (ValueError, TypeError, IndexError) as error:
        st.error(str(error))
        return OPERATION_FAILED
    return result


def render_array(array):
    if not len(array):
        st.markdown(
            '<div class="empty-state"><span class="empty-icon">[]</span>'
            "<strong>Your array is ready</strong>"
            "<span>Add a value below to create your first slot.</span></div>",
            unsafe_allow_html=True,
        )
        return

    slots = "".join(
        '<div class="array-slot">'
        f'<span class="slot-index">INDEX {index}</span>'
        f'<span class="slot-value">{html.escape(repr(value))}</span>'
        "</div>"
        for index, value in enumerate(array)
    )
    free_slots = array.size - len(array)
    if free_slots:
        slots += "".join(
            '<div class="array-slot empty-slot">'
            f'<span class="slot-index">INDEX {index}</span>'
            '<span class="slot-value">empty</span></div>'
            for index in range(len(array), array.size)
        )
    st.markdown(f'<div class="array-grid">{slots}</div>', unsafe_allow_html=True)


st.set_page_config(page_title="Dynamic Array", page_icon="📦")
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(ellipse at 5% 0%, rgba(20, 184, 166, .13), transparent 34%),
            #0b1120;
    }
    [data-testid="stHeader"] { background: rgba(11, 17, 32, .75); }
    .block-container { max-width: 1180px; padding-top: 2rem; }
    .hero {
        padding: 1.7rem 2rem;
        margin: .4rem 0 1.4rem;
        border: 1px solid rgba(148, 163, 184, .16);
        border-radius: 22px;
        background: linear-gradient(120deg, rgba(15, 23, 42, .97), rgba(15, 45, 54, .88));
        box-shadow: 0 18px 55px rgba(0, 0, 0, .22);
    }
    .hero-kicker {
        color: #5eead4;
        font-size: .73rem;
        font-weight: 800;
        letter-spacing: .18em;
        text-transform: uppercase;
    }
    .hero h1 {
        margin: .35rem 0 .45rem;
        color: #f8fafc;
        font-size: clamp(2rem, 5vw, 3rem);
        letter-spacing: -.055em;
    }
    .hero p { margin: 0; color: #a8b7c9; font-size: 1rem; }
    [data-testid="stMetric"] {
        padding: 1rem 1.15rem;
        border: 1px solid rgba(148, 163, 184, .14);
        border-radius: 16px;
        background: rgba(15, 23, 42, .78);
    }
    [data-testid="stMetricLabel"] p {
        color: #94a3b8;
        font-size: .8rem;
        font-weight: 650;
    }
    [data-testid="stMetricValue"] { color: #f8fafc; }
    [data-testid="stTabs"] [role="tablist"] {
        gap: .45rem;
        border-bottom: 1px solid rgba(148, 163, 184, .16);
    }
    [data-testid="stTabs"] button[role="tab"] {
        border-radius: 10px 10px 0 0;
        color: #a8b7c9;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #5eead4;
        background: rgba(20, 184, 166, .09);
    }
    .array-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(112px, 1fr));
        gap: .7rem;
        margin: .5rem 0 1rem;
    }
    .array-slot {
        min-height: 82px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        gap: .6rem;
        padding: .8rem .9rem;
        border: 1px solid rgba(45, 212, 191, .28);
        border-radius: 14px;
        background: linear-gradient(145deg, rgba(15, 46, 54, .93), rgba(15, 23, 42, .95));
        box-shadow: inset 0 1px rgba(255,255,255,.035);
    }
    .slot-index {
        color: #5eead4;
        font-size: .63rem;
        font-weight: 800;
        letter-spacing: .1em;
    }
    .slot-value {
        overflow-wrap: anywhere;
        color: #f8fafc;
        font-size: 1.08rem;
        font-weight: 700;
    }
    .empty-slot {
        border-style: dashed;
        border-color: rgba(148, 163, 184, .24);
        background: rgba(15, 23, 42, .45);
    }
    .empty-slot .slot-index, .empty-slot .slot-value { color: #64748b; }
    .empty-state {
        min-height: 165px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: .45rem;
        border: 1px dashed rgba(148, 163, 184, .25);
        border-radius: 18px;
        background: rgba(15, 23, 42, .5);
        color: #94a3b8;
    }
    .empty-state strong { color: #e2e8f0; font-size: 1.05rem; }
    .empty-icon { color: #5eead4; font: 800 1.8rem ui-monospace, monospace; }
    .section-label {
        margin: 1.2rem 0 .35rem;
        color: #e2e8f0;
        font-size: 1.1rem;
        font-weight: 750;
    }
    .section-hint { margin: 0 0 .8rem; color: #94a3b8; font-size: .86rem; }
    [data-testid="stForm"] {
        padding: 1rem;
        border: 1px solid rgba(148, 163, 184, .14);
        border-radius: 15px;
        background: rgba(15, 23, 42, .52);
    }
    [data-testid="stButton"] button[kind="primary"],
    [data-testid="stFormSubmitButton"] button[kind="primary"] {
        border: 1px solid rgba(45, 212, 191, .55);
        background: linear-gradient(100deg, #0f766e, #0d9488);
        color: white;
    }
    .history-item {
        margin: .35rem 0;
        padding: .55rem .75rem;
        border-left: 2px solid #14b8a6;
        border-radius: 0 8px 8px 0;
        background: rgba(15, 23, 42, .55);
        color: #cbd5e1;
        font-size: .85rem;
    }
    @media (max-width: 640px) {
        .hero { padding: 1.25rem; }
        .block-container { padding: 1rem .8rem 2rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    '<section class="hero"><div class="hero-kicker">Data structures · interactive lab</div>'
    "<h1>Dynamic Array</h1>"
    "<p>Explore how your notebook's <code>MyList</code> stores, shifts, and grows values.</p>"
    "</section>",
    unsafe_allow_html=True,
)

if "my_list" not in st.session_state:
    st.session_state.my_list = MyList()
if "operation_history" not in st.session_state:
    st.session_state.operation_history = []
if "operation_outputs" not in st.session_state:
    st.session_state.operation_outputs = {}

array = st.session_state.my_list
length_col, capacity_col, free_col, type_col = st.columns(4)
length_col.metric("Length", len(array))
capacity_col.metric("Capacity", array.size)
free_col.metric("Free slots", array.size - len(array))
type_col.metric("Storage", "ctypes")
st.progress(len(array) / array.size, text="Capacity used")

st.markdown('<div class="section-label">Array memory view</div>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-hint">Each tile shows a stored value and its index. Empty tiles '
    "show available capacity.</p>",
    unsafe_allow_html=True,
)
render_array(array)

with st.expander("Recent activity", expanded=bool(st.session_state.operation_history)):
    if st.session_state.operation_history:
        for message in st.session_state.operation_history:
            st.markdown(
                f'<div class="history-item">{html.escape(message)}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.caption("Successful operations will appear here.")

build_tab, access_tab, edit_tab, combine_tab, stats_tab = st.tabs(
    ["Build", "Index & Slice", "Edit", "Merge & Extend", "Find & Statistics"]
)

with build_tab:
    st.markdown("Append one value or multiple comma-separated values.")
    with st.form("append_form"):
        append_input = st.text_input("Values", placeholder="10, 20, 30")
        append_submitted = st.form_submit_button("Append")
    if append_submitted:
        values = run_operation(lambda: parse_values(append_input))
        if values is not OPERATION_FAILED:
            for value in values:
                array.append(value)
            set_message(f"Appended {len(values)} value(s).", "append")
            st.rerun()
    render_operation_output("append")

with access_tab:
    st.markdown("Read values by index, including negative indexes, or slice the array.")
    with st.form("index_form"):
        index_input = st.text_input("Index", placeholder="-1")
        index_submitted = st.form_submit_button("Get item")
    if index_submitted:
        result = run_operation(lambda: array[int(index_input)])
        if result is not OPERATION_FAILED:
            set_message(f"Read index {index_input}: {result!r}", "index")
            st.rerun()
    render_operation_output("index")

    with st.form("slice_form"):
        slice_col1, slice_col2, slice_col3 = st.columns(3)
        slice_start = slice_col1.text_input("Start (optional)", placeholder="0 or -3")
        slice_stop = slice_col2.text_input("Stop (optional)", placeholder="end")
        slice_step = slice_col3.text_input("Step (optional)", placeholder="1")
        slice_submitted = st.form_submit_button("Get slice")
    if slice_submitted:
        slice_parts = run_operation(
            lambda: (
                parse_optional_index(slice_start),
                parse_optional_index(slice_stop),
                parse_optional_index(slice_step),
            )
        )
        if slice_parts is not OPERATION_FAILED:
            result = run_operation(lambda: array[slice(*slice_parts)])
            if result is not OPERATION_FAILED:
                set_message(f"Slice result: {result!r}", "slice")
                st.rerun()
    render_operation_output("slice")

with edit_tab:
    st.markdown("Insert, pop, delete, remove, sort, or clear values.")
    with st.form("insert_form"):
        insert_col1, insert_col2 = st.columns(2)
        insert_index = insert_col1.text_input("Insert position", placeholder="0 or -1")
        insert_value = insert_col2.text_input("Value to insert")
        insert_submitted = st.form_submit_button("Insert")
    if insert_submitted:
        parsed = run_operation(lambda: (int(insert_index), parse_value(insert_value)))
        if parsed is not OPERATION_FAILED:
            array.insert(*parsed)
            set_message(
                f"Inserted {parsed[1]!r} at position {parsed[0]}.", "insert"
            )
            st.rerun()
    render_operation_output("insert")

    with st.form("pop_form"):
        pop_index = st.text_input("Pop index (blank means last item)", placeholder="-1")
        pop_submitted = st.form_submit_button("Pop")
    if pop_submitted:
        parsed_index = run_operation(lambda: parse_optional_index(pop_index))
        if parsed_index is not OPERATION_FAILED:
            result = run_operation(lambda: array.pop() if parsed_index is None else array.pop(parsed_index))
            if result is not OPERATION_FAILED:
                set_message(f"Popped {result!r}.", "pop")
                st.rerun()
    render_operation_output("pop")

    with st.form("delete_form"):
        delete_index = st.text_input("Delete index", placeholder="0 or -1")
        delete_submitted = st.form_submit_button("Delete item")
    if delete_submitted:
        result = run_operation(lambda: array.__delitem__(int(delete_index)))
        if result is not OPERATION_FAILED:
            set_message(f"Deleted the item at index {delete_index}.", "delete")
            st.rerun()
    render_operation_output("delete")

    with st.form("remove_form"):
        remove_value = st.text_input("Value to remove")
        remove_submitted = st.form_submit_button("Remove first match")
    if remove_submitted:
        value = run_operation(lambda: parse_value(remove_value))
        if value is not OPERATION_FAILED:
            result = run_operation(lambda: array.remove(value))
            if result is not OPERATION_FAILED:
                message = (
                    result if isinstance(result, str) else f"Removed {value!r}."
                )
                set_message(message, "remove")
                st.rerun()
    render_operation_output("remove")

    sort_col, clear_col = st.columns(2)
    if sort_col.button("Sort", use_container_width=True):
        if run_operation(array.sort) is not OPERATION_FAILED:
            set_message("Sorted the array.", "sort")
            st.rerun()
    with sort_col:
        render_operation_output("sort")
    if clear_col.button("Clear array", use_container_width=True):
        array.clear()
        set_message("Cleared the array.", "clear")
        st.rerun()
    with clear_col:
        render_operation_output("clear")

with combine_tab:
    st.markdown("Enter a second array as comma-separated values.")
    with st.form("combine_form"):
        second_values_input = st.text_input(
            "Values to merge or extend", placeholder="40, 50, 60"
        )
        combine_col1, combine_col2 = st.columns(2)
        merge_submitted = combine_col1.form_submit_button("Merge")
        extend_submitted = combine_col2.form_submit_button("Extend")
    if merge_submitted or extend_submitted:
        values = run_operation(lambda: parse_values(second_values_input))
        if values is not OPERATION_FAILED:
            other_array = MyList()
            for value in values:
                other_array.append(value)
            operation = array.merge if merge_submitted else array.extend
            run_result = run_operation(lambda: operation(other_array))
            if run_result is not OPERATION_FAILED:
                action = "Merged" if merge_submitted else "Extended"
                set_message(f"{action} with {len(values)} value(s).", "combine")
                st.rerun()
    render_operation_output("combine")

with stats_tab:
    st.markdown("Find a value or calculate min, max, and sum.")
    with st.form("find_form"):
        find_input = st.text_input("Value to find")
        find_submitted = st.form_submit_button("Find")
    if find_submitted:
        value = run_operation(lambda: parse_value(find_input))
        if value is not OPERATION_FAILED:
            result = array.find(value)
            message = (
                f"Found at index {result}."
                if isinstance(result, int)
                else result
            )
            set_message(message, "find")
            st.rerun()
    render_operation_output("find")

    stat_col1, stat_col2, stat_col3 = st.columns(3)
    if stat_col1.button("Minimum", use_container_width=True):
        result = run_operation(array.min)
        if result is not OPERATION_FAILED:
            set_message(f"Minimum: {result!r}", "minimum")
            st.rerun()
    with stat_col1:
        render_operation_output("minimum")
    if stat_col2.button("Maximum", use_container_width=True):
        result = run_operation(array.max)
        if result is not OPERATION_FAILED:
            set_message(f"Maximum: {result!r}", "maximum")
            st.rerun()
    with stat_col2:
        render_operation_output("maximum")
    if stat_col3.button("Sum", use_container_width=True):
        result = run_operation(array.sum)
        if result is not OPERATION_FAILED:
            set_message(f"Sum: {result!r}", "sum")
            st.rerun()
    with stat_col3:
        render_operation_output("sum")
