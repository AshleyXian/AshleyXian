"""CSC148 Assignment 1: Tests for checkout classes

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for testing the checkout classes.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from store import RegularLine, ExpressLine, SelfServeLine, Customer, Item


def test_regular_line_attributes() -> None:
    """Test the public attributes of a regular line."""
    r1 = RegularLine(10)
    assert r1.capacity == 10
    assert r1.is_open is True
    assert r1.queue == []


def test_regular_line_start_checkout_no_next_customer() -> None:
    """Test RegularLine.start_checkout when there is no next customer."""
    r1 = RegularLine(10)
    c1 = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
    r1.accept(c1)
    assert r1.start_checkout() == 10


def test_regular_line_start_checkout() -> None:
    """Test RegularLine.start_checkout."""
    r1 = RegularLine(10)
    c1 = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
    r1.accept(c1)
    c2 = Customer('B', [Item('apples', 3)])
    r1.accept(c2)
    assert r1.start_checkout() == 10


def test_start_checkout_no_customer_reg() -> None:
    """Test RegularLine.start_checkout with no customer in line."""
    r1 = RegularLine(10)
    assert r1.start_checkout() == -1


def test_start_checkout_no_customer_exp() -> None:
    """Test ExpressLine.start_checkout with no customer in line."""
    e1 = ExpressLine(2)
    assert e1.start_checkout() == -1


def test_start_checkout_no_customer_self() -> None:
    """Test SelfServeLine.start_checkout with no customer in line."""
    s1 = SelfServeLine(10)
    assert s1.start_checkout() == -1


def test_express_line_attributes() -> None:
    """Test the public attributes of a express line."""
    e2 = ExpressLine(5)
    assert e2.capacity == 5
    assert e2.is_open is True
    assert e2.queue == []


def test_can_accept() -> None:
    """Test ExpressLine.can_accept when num_items < 8."""
    e2 = ExpressLine(2)
    c1 = Customer('A', [Item('bananas', 7)])
    assert e2.can_accept(c1) is True


def test_can_not_accept() -> None:
    """Test ExpressLine.can_accept when num_items >= 8."""
    e2 = ExpressLine(3)
    c1 = Customer('A', [Item('bananas', 7), Item('apples', 5), Item('pop', 3),
                        Item('pen', 2), Item('pickle', 4), Item('plum', 4),
                        Item('cheese', 5), Item('beer', 8)])
    assert e2.can_accept(c1) is False


def test_express_line_start_checkout_no_next_customer() -> None:
    """Test ExpressLine.start_checkout when there is no next customer."""
    e1 = ExpressLine(2)
    c1 = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
    e1.accept(c1)
    assert e1.start_checkout() == 10


def test_express_line_start_checkout() -> None:
    """Test ExpressLine.start_checkout."""
    e1 = ExpressLine(3)
    c1 = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
    e1.accept(c1)
    c2 = Customer('B', [Item('apples', 3)])
    e1.accept(c2)
    assert e1.start_checkout() == 10


def test_self_serve_line_attributes() -> None:
    """Test the public attributes of a self-serve line."""
    s2 = SelfServeLine(10)
    assert s2.capacity == 10
    assert s2.is_open is True
    assert s2.queue == []


def test_self_serve_line_start_checkout_no_next_customer() -> None:
    """Test SelfServeLine.start_checkout when there is no next customer."""
    s1 = SelfServeLine(2)
    c1 = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
    s1.accept(c1)
    assert s1.start_checkout() == 20


def test_self_serve_line_start_checkout() -> None:
    """Test SelfServeLine.start_checkout."""
    s1 = SelfServeLine(3)
    c1 = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
    s1.accept(c1)
    c2 = Customer('B', [Item('apples', 3)])
    s1.accept(c2)
    assert s1.start_checkout() == 20


if __name__ == '__main__':
    import pytest
    pytest.main(['test_checkouts.py'])
