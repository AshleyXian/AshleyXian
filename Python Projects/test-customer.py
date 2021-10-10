"""CSC148 Assignment 1: Tests for Customer

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for testing the Customer class.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from store import Customer, Item


def test_customer_attributes() -> None:
    """Test the public attributes of a customer."""
    c1 = Customer('A', [Item('bananas', 7)])
    assert c1.name == 'A'
    assert c1.arrival_time == -1


def test_num_items() -> None:
    """Test Customer.num_items."""
    c2 = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
    assert c2.num_items() == 2


def test_num_items_0() -> None:
    """Test Customer.num_items when 0 item."""
    c2 = Customer('Bo', [])
    assert c2.num_items() == 0


def test_get_item_time() -> None:
    """Test Customer.get_item_time."""
    c2 = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
    assert c2.get_item_time() == 10


if __name__ == '__main__':
    import pytest
    pytest.main(['test_customer.py'])
