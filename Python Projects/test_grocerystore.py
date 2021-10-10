"""CSC148 Assignment 1: Tests for GroceryStore

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for testing the GroceryStore class.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from io import StringIO
from store import GroceryStore, Customer, Item

# Note - your tests should use StringIO to simulate opening a configuration file
# rather than requiring separate files.
# See the Assignment 0 sample test for an example of using StringIO in testing.


INPUT_FILE_CONTENTS = '{' + '\n' + \
  '"regular_count": 0,' + '\n' + \
  '"express_count": 1,' + '\n' + \
  '"self_serve_count": 0,' + '\n' + \
  '"line_capacity": 1' + '\n' + \
  '}'
INPUT_FILE_CONTENTS_2 = '{' + '\n' + \
  '"regular_count": 2,' + '\n' + \
  '"express_count": 1,' + '\n' + \
  '"self_serve_count": 1,' + '\n' + \
  '"line_capacity": 2' + '\n' + \
  '}'
INPUT_FILE_CONTENTS_3 = '{' + '\n' + \
  '"regular_count": 2,' + '\n' + \
  '"express_count": 1,' + '\n' + \
  '"self_serve_count": 1,' + '\n' + \
  '"line_capacity": 10' + '\n' + \
  '}'


def test_grocery_store_attributes() -> None:
    """Test the public attributes of a grocery store."""
    g1 = GroceryStore(StringIO(INPUT_FILE_CONTENTS))
    assert g1.regular_count == 0
    assert g1.express_count == 1
    assert g1.self_serve_count == 0
    assert g1.line_capacity == 1
    assert g1.gro_list['exp'][0].capacity == 1


def test_enter_line() -> None:
    """Test GroceryStore.enter_line."""
    g1 = GroceryStore(StringIO(INPUT_FILE_CONTENTS))
    c1 = Customer('A', [Item('bananas', 7)])
    assert g1.enter_line(c1) == 0


def test_enter_line_not_available() -> None:
    """Test GroceryStore.enter_line if no line is available."""
    g1 = GroceryStore(StringIO(INPUT_FILE_CONTENTS))
    c1 = Customer('A', [Item('bananas', 7)])
    c2 = Customer('B', [Item('apples', 3)])
    g1.enter_line(c1)
    assert g1.enter_line(c2) == -1


def test_line_is_ready() -> None:
    """Test GroceryStore.line_is_ready is True."""
    g1 = GroceryStore(StringIO(INPUT_FILE_CONTENTS))
    c1 = Customer('A', [Item('bananas', 7)])
    g1.enter_line(c1)
    assert g1.line_is_ready(0) is True


def test_line_is_not_ready() -> None:
    """Test GroceryStore.line_is_ready is False."""
    g2 = GroceryStore(StringIO(INPUT_FILE_CONTENTS_2))
    c1 = Customer('A', [Item('bananas', 7)])
    c2 = Customer('B', [Item('apples', 3)])
    g2.enter_line(c1)
    g2.enter_line(c2)
    assert g2.line_is_ready(0) is False


def test_start_checkout_reg() -> None:
    """Test GroceryStore.start_checkout when it is regular line."""
    g2 = GroceryStore(StringIO(INPUT_FILE_CONTENTS_2))
    c1 = Customer('A', [Item('bananas', 7)])
    c2 = Customer('B', [Item('apples', 3)])
    g2.enter_line(c1)
    g2.enter_line(c2)
    assert g2.start_checkout(0) == 7


def test_start_checkout_exp() -> None:
    """Test GroceryStore.start_checkout when it is express line."""
    g2 = GroceryStore(StringIO(INPUT_FILE_CONTENTS_2))
    c1 = Customer('A', [Item('bananas', 7)])
    c2 = Customer('B', [Item('apples', 3)])
    g2.enter_line(c1)
    g2.enter_line(c2)
    c3 = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
    c4 = Customer('C', [Item('pop', 4), Item('cheese', 3)])
    g2.enter_line(c3)
    g2.enter_line(c4)
    c5 = Customer('Co', [Item('pen', 5), Item('tomatoes', 4)])
    c6 = Customer('Di', [Item('pen', 5), Item('potatoes', 3)])
    g2.enter_line(c5)
    g2.enter_line(c6)
    assert g2.start_checkout(2) == 9


def test_start_checkout_self() -> None:
    """Test GroceryStore.start_checkout when it is self-serve line."""
    g2 = GroceryStore(StringIO(INPUT_FILE_CONTENTS_2))
    c1 = Customer('A', [Item('bananas', 7)])
    c2 = Customer('B', [Item('apples', 3)])
    g2.enter_line(c1)
    g2.enter_line(c2)
    c3 = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
    c4 = Customer('C', [Item('pop', 4), Item('cheese', 3)])
    g2.enter_line(c3)
    g2.enter_line(c4)
    c5 = Customer('Co', [Item('pen', 5), Item('tomatoes', 4)])
    c6 = Customer('Di', [Item('pen', 5), Item('potatoes', 3)])
    g2.enter_line(c5)
    g2.enter_line(c6)
    c7 = Customer('E', [Item('pop', 4), Item('tomatoes', 4)])
    c8 = Customer('F', [Item('pen', 5), Item('potatoes', 3)])
    g2.enter_line(c7)
    g2.enter_line(c8)
    assert g2.start_checkout(3) == 16


def test_start_checkout_sing() -> None:
    """Test GroceryStore.start_checkout with only one customer in line."""
    g2 = GroceryStore(StringIO(INPUT_FILE_CONTENTS_2))
    c1 = Customer('A', [Item('bananas', 7)])
    g2.enter_line(c1)
    assert g2.start_checkout(0) == 7


def test_start_checkout_no_customer() -> None:
    """Test GroceryStore.start_checkout with no customer in line."""
    g2 = GroceryStore(StringIO(INPUT_FILE_CONTENTS_2))
    assert g2.start_checkout(0) == -1


def test_complete_checkout() -> None:
    """Test GroceryStore.complete_checkout."""
    g3 = GroceryStore(StringIO(INPUT_FILE_CONTENTS_3))
    c1 = Customer('A', [Item('bananas', 7)])
    c2 = Customer('B', [Item('apples', 3)])
    g3.enter_line(c1)
    g3.enter_line(c2)
    c3 = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
    c4 = Customer('C', [Item('pop', 4), Item('cheese', 3)])
    g3.enter_line(c3)
    g3.enter_line(c4)
    assert g3.complete_checkout(0) == 4


def test_complete_checkout_empty_line() -> None:
    """Test GroceryStore.complete_checkout when no one remaining to be
    checked out."""
    g2 = GroceryStore(StringIO(INPUT_FILE_CONTENTS_2))
    assert g2.complete_checkout(0) == 0


def test_close_line_with_customer() -> None:
    """Test GroceryStore.close_line with customer."""
    g3 = GroceryStore(StringIO(INPUT_FILE_CONTENTS_3))
    c1 = Customer('A', [Item('bananas', 7)])
    c2 = Customer('B', [Item('apples', 3)])
    g3.enter_line(c1)
    g3.enter_line(c2)
    c3 = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
    c4 = Customer('C', [Item('pop', 4), Item('cheese', 3)])
    g3.enter_line(c3)
    g3.enter_line(c4)
    assert g3.close_line(0) == [c2, c3, c4]


def test_close_line_without_customer() -> None:
    """Test GroceryStore.close_line without customer."""
    g3 = GroceryStore(StringIO(INPUT_FILE_CONTENTS_3))
    assert g3.close_line(2) == []


def test_get_first_in_line_reg() -> None:
    """Test GroceryStore.get_first_in_line when it is regular line."""
    g2 = GroceryStore(StringIO(INPUT_FILE_CONTENTS_2))
    c1 = Customer('A', [Item('bananas', 7)])
    c2 = Customer('B', [Item('apples', 3)])
    g2.enter_line(c1)
    g2.enter_line(c2)
    c3 = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
    c4 = Customer('C', [Item('pop', 4), Item('cheese', 3)])
    g2.enter_line(c3)
    g2.enter_line(c4)
    c5 = Customer('Co', [Item('pen', 5), Item('tomatoes', 4)])
    c6 = Customer('Di', [Item('pen', 5), Item('potatoes', 3)])
    g2.enter_line(c5)
    g2.enter_line(c6)
    assert g2.get_first_in_line(0) == c1


def test_get_first_in_line_exp() -> None:
    """Test GroceryStore.get_first_in_line when it is express line."""
    g2 = GroceryStore(StringIO(INPUT_FILE_CONTENTS_2))
    c1 = Customer('A', [Item('bananas', 7)])
    c2 = Customer('B', [Item('apples', 3)])
    g2.enter_line(c1)
    g2.enter_line(c2)
    c3 = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
    c4 = Customer('C', [Item('pop', 4), Item('cheese', 3)])
    g2.enter_line(c3)
    g2.enter_line(c4)
    c5 = Customer('Co', [Item('pen', 5), Item('tomatoes', 4)])
    c6 = Customer('Di', [Item('pen', 5), Item('potatoes', 3)])
    g2.enter_line(c5)
    g2.enter_line(c6)
    assert g2.get_first_in_line(2) == c5


def test_get_first_in_line_no_customers() -> None:
    """Test GroceryStore.get_first_in_line if there are no customers in line."""
    g2 = GroceryStore(StringIO(INPUT_FILE_CONTENTS_2))
    c1 = Customer('A', [Item('bananas', 7)])
    c2 = Customer('B', [Item('apples', 3)])
    g2.enter_line(c1)
    g2.enter_line(c2)
    assert g2.get_first_in_line(2) is None


if __name__ == '__main__':
    import pytest
    pytest.main(['test_grocerystore.py'])
