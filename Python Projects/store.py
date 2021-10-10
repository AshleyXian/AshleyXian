"""CSC148 Assignment 1 - Modelling a Grocery Store (Task 1a)

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains all of the classes necessary to model the entities
in a grocery store.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from __future__ import annotations
from typing import List, Optional, TextIO
import json

# Use this constant in your code
EXPRESS_LIMIT = 7


# TODO: Complete the GroceryStore class and methods according to the docstrings
# You may add private attributes and helper methods, but do not change the
# public interface.
# Write docstrings for all methods you write, and document your attributes
# in the class docstring.
class GroceryStore:
    """A grocery store.

    === Attributes ===
    regular_count:
        the number of regular checkout lines
    express_count:
        the number of express checkout lines
    self_serve_count:
        the number of self-serve checkout lines
    line_capacity:
        the maximum number of customers allowed in each line (all lines have
        the same capacity)
    gro_list:
        a dictionary which the keys are types of checkout line, and the values
        are lists of checkout lines
    === Representation invariants ===
    - regular_count >= 0
    - express_count >= 0
    - self_serve_count >= 0
    - line_capacity >= 0
    """
    regular_count: int
    express_count: int
    self_serve_count: int
    line_capacity: int
    gro_list: dict

    def __init__(self, config_file: TextIO) -> None:
        """Initialize a GroceryStore from a configuration file <config_file>.

        >>> filename = 'input_files/config_001_10.json'
        >>> file = open(filename)
        >>> grocery1 = GroceryStore(file)
        >>> file.close()
        >>> grocery1.regular_count
        0
        >>> grocery1.express_count
        0
        >>> grocery1.self_serve_count
        1
        >>> grocery1.line_capacity
        10
        >>> grocery1.gro_list['self'][0].capacity
        10
        """
        data = json.load(config_file)
        self.regular_count = data["regular_count"]
        self.express_count = data["express_count"]
        self.self_serve_count = data["self_serve_count"]
        self.line_capacity = data["line_capacity"]
        self.gro_list = {'reg': {}, 'exp': {}, 'self': {}}
        for i in range(self.regular_count):
            self.gro_list['reg'][i] = RegularLine(self.line_capacity)
        for i in range(self.regular_count, self.express_count
                       + self.regular_count):
            self.gro_list['exp'][i] = ExpressLine(self.line_capacity)
        for i in range(self.express_count + self.regular_count,
                       self.express_count + self.regular_count
                       + self.self_serve_count):
            self.gro_list['self'][i] = SelfServeLine(self.line_capacity)

    def enter_line(self, customer: Customer) -> int:
        """Pick a new line for <customer> to join.

        Return the index of the line that the customer joined.
        Must use the algorithm from the handout.

        Return -1 if there is no line available for the customer to join.
        """
        for line_type in self.gro_list:
            line_lst = self.gro_list[line_type]
            for i in line_lst:
                if line_lst[i].can_accept(customer) and \
                        line_lst[i].accept(customer):
                    return i
        return -1

    def line_is_ready(self, line_number: int) -> bool:
        """Return True iff checkout line <line_number> is ready to start a
        checkout.
        """
        for line_type in self.gro_list:
            line_lst = self.gro_list[line_type]
            if line_number in line_lst:
                return line_lst[line_number].__len__() == 1
        return False

    def start_checkout(self, line_number: int) -> int:
        """Return the time it will take to check out the next customer in
        line <line_number>
        """
        for line_type in self.gro_list:
            line_lst = self.gro_list[line_type]
            if line_number in line_lst:
                return line_lst[line_number].start_checkout()
        return -1

    def complete_checkout(self, line_number: int) -> int:
        """Return the number of customers remaining to be checked out in line
        <line_number>
        """
        for line_type in self.gro_list:
            line_lst = self.gro_list[line_type]
            if line_number in line_lst:
                return line_lst[line_number].__len__()
        return 0

    def close_line(self, line_number: int) -> List[Customer]:
        """Close checkout line <line_number> and return the customers from
        that line who are still waiting to be checked out.
        """
        for line_type in self.gro_list:
            line_lst = self.gro_list[line_type]
            if line_number in line_lst:
                return line_lst[line_number].close()
        return []

    def get_first_in_line(self, line_number: int) -> Optional[Customer]:
        """Return the first customer in line <line_number>, or None if there
        are no customers in line.
        """
        for line_type in self.gro_list:
            line_lst = self.gro_list[line_type]
            if line_number in line_lst:
                queue = line_lst[line_number].queue
                if queue:
                    return queue[0]
        return None


# TODO: Complete the methods in Customer according to their docstrings
# You should use the existing attributes in your solution. However, if you need
# to, you may add private attributes and helper methods, but do not change the
# public interface.
# Write docstrings for all methods you write, and document your attributes
# in the class docstring.
class Customer:
    """A grocery store customer.

    === Attributes ===
    name: A unique identifier for this customer.
    arrival_time: The time this customer joined a line.
    _items: The items this customer has.

    === Representation Invariant ===
    arrival_time >= 0 if this customer has joined a line, and -1 otherwise
    """
    name: str
    arrival_time: int
    _items: List[Item]

    def __init__(self, name: str, items: List[Item]) -> None:
        """Initialize a customer with the given <name>, an initial arrival time
         of -1, and a copy of the list <items>.

        >>> item_list = [Item('bananas', 7)]
        >>> belinda = Customer('Belinda', item_list)
        >>> belinda.name
        'Belinda'
        >>> belinda._items == item_list
        True
        >>> belinda.arrival_time
        -1
        """
        self.name = name
        self.arrival_time = -1
        self._items = []
        for item in items:
            self._items.append(item)

    def num_items(self) -> int:
        """Return the number of items this customer has.

        >>> c = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
        >>> c.num_items()
        2
        """
        return len(self._items)

    def get_item_time(self) -> int:
        """Return the number of seconds it takes to check out this customer.

        >>> c = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
        >>> c.get_item_time()
        10
        """
        count = 0
        for item in self._items:
            count += item.get_time()
        return count


class Item:
    """A class to represent an item to be checked out.

    Do not change this class.

    === Attributes ===
    name: the name of this item
    _time: the amount of time it takes to checkout this item
    """
    name: str
    _time: int

    def __init__(self, name: str, time: int) -> None:
        """Initialize a new time with <name> and <time>.

        >>> item = Item('bananas', 7)
        >>> item.name
        'bananas'
        >>> item._time
        7
        """
        self.name = name
        self._time = time

    def get_time(self) -> int:
        """Return how many seconds it takes to checkout this item.

        >>> item = Item('bananas', 7)
        >>> item.get_time()
        7
        """
        return self._time


# TODO: Complete the CheckoutLine class and methods according to the docstrings
# Do not add any new attributes or methods (public or private) to this class.
class CheckoutLine:
    """A checkout line in a grocery store.

    This is an abstract class; subclasses are responsible for implementing
    start_checkout().

    === Attributes ===
    capacity: The number of customers allowed in this CheckoutLine.
    is_open: True iff the line is open.
    queue: Customers in this line in FIFO order.

    === Representation Invariants ===
    - Each customer in this line has not been checked out yet.
    - The number of customers is less than or equal to capacity.
    """
    capacity: int
    is_open: bool
    queue: List[Customer]

    def __init__(self, capacity: int) -> None:
        """Initialize an open and empty CheckoutLine.

        >>> line = CheckoutLine(1)
        >>> line.capacity
        1
        >>> line.is_open
        True
        >>> line.queue
        []
        """
        self.capacity = capacity
        self.is_open = True
        self.queue = []

    def __len__(self) -> int:
        """Return the size of this CheckoutLine.
        """
        return len(self.queue)

    def can_accept(self, customer: Customer) -> bool:
        """Return True iff this CheckoutLine can accept <customer>.
        """
        return self.is_open

    def accept(self, customer: Customer) -> bool:
        """Accept <customer> at the end of this CheckoutLine.
        Return True iff the customer is accepted.

        >>> line = CheckoutLine(1)
        >>> c1 = Customer('Belinda', [Item('cheese', 3)])
        >>> c2 = Customer('Hamman', [Item('chips', 4), Item('gum', 1)])
        >>> line.accept(c1)
        True
        >>> line.accept(c2)
        False
        >>> line.queue == [c1]
        True
        """
        if self.__len__() < self.capacity:
            self.queue.append(customer)
            return True
        else:
            return False

    def start_checkout(self) -> int:
        """Checkout the next customer in this CheckoutLine.

        Return the time it will take to checkout the next customer.
        """
        raise NotImplementedError('Implemented in a subclass')

    def complete_checkout(self) -> bool:
        """Finish the checkout for this CheckoutLine.

        Return whether there are any remaining customers in the line.
        """
        return self.__len__() == 0

    def close(self) -> List[Customer]:
        """Close this line.

        Return a list of all customers that need to be moved to another line.
        """
        self.is_open = False
        return self.queue[1:]


# TODO: implement the following subclasses of CheckoutLine
# Only implement those methods that cannot be used exactly as inherited
# from the superclass.
# You may add private attributes and helper methods, but do not change the
# public interface of the subclasses.
# Write docstrings for all methods you write, and document your attributes
# in the class docstring.

class RegularLine(CheckoutLine):
    """A regular CheckoutLine."""
    capacity: int
    is_open: bool
    queue: List[Customer]

    def __init__(self, capacity: int) -> None:
        """Initialize an open and empty RegularLine.

        >>> line = RegularLine(1)
        >>> line.capacity
        1
        >>> line.is_open
        True
        >>> line.queue
        []
        """
        CheckoutLine.__init__(self, capacity)

    def start_checkout(self) -> int:
        """Checkout the next customer in this RegularLine.

        Return the time it will take to checkout the next customer.
        """
        if self.queue:
            self.queue.pop(0)
        if self.queue:
            customer = self.queue[0]
            return customer.get_item_time()
        else:
            return -1


class ExpressLine(CheckoutLine):
    """An express CheckoutLine.
    """
    capacity: int
    is_open: bool
    queue: List[Customer]

    def __init__(self, capacity: int) -> None:
        """Initialize an open and empty RegularLine.

        >>> line = ExpressLine(1)
        >>> line.capacity
        1
        >>> line.is_open
        True
        >>> line.queue
        []
        """
        CheckoutLine.__init__(self, capacity)

    def can_accept(self, customer: Customer) -> bool:
        """Return True iff this ExpressLine can accept <customer>.
        """
        return self.is_open and (customer.num_items() < 8)

    def start_checkout(self) -> int:
        """Checkout the next customer in this ExpressLine.

        Return the time it will take to checkout the next customer.
        """
        self.queue.pop(0)
        if self.queue:
            customer = self.queue[0]
            return customer.get_item_time()
        else:
            return -1


class SelfServeLine(CheckoutLine):
    """A self-serve CheckoutLine.
    """
    capacity: int
    is_open: bool
    queue: List[Customer]

    def __init__(self, capacity: int) -> None:
        """Initialize an open and empty RegularLine.

        >>> line = SelfServeLine(1)
        >>> line.capacity
        1
        >>> line.is_open
        True
        >>> line.queue
        []
        """
        CheckoutLine.__init__(self, capacity)

    def start_checkout(self) -> int:
        """Checkout the next customer in this SelfServeLine.

        Return the time it will take to checkout the next customer.
        If there is no next customer in the line, return -1
        """
        self.queue.pop(0)
        if self.queue:
            customer = self.queue[0]
            return 2 * customer.get_item_time()
        else:
            return -1


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['__future__', 'typing', 'json',
                                   'python_ta', 'doctest'],
        'disable': ['W0613']})
