"""Assignment 1 - Scheduling algorithms (Task 4)

CSC148, Winter 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

===== Module Description =====

This module contains the abstract Scheduler class, as well as the two
subclasses RandomScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.
"""
from typing import List, Callable, Dict, Union
from random import shuffle, choice
from container import PriorityQueue
from domain import Parcel, Truck


class Scheduler:
    """A scheduler, capable of deciding what parcels go onto which trucks, and
    what route each truck will take.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks>, that is, decide
        which parcels will go on which trucks, as well as the route each truck
        will take.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what route they will
        take.  Do *not* mutate the list <parcels>, or any of the parcel objects
        in that list.

        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        raise NotImplementedError


class RandomScheduler(Scheduler):
    """A random scheduler, randomly decides what parcels go onto which trucks,
    and what route each truck will take. For each parcel, it will schedule it
    onto a randomly chosen truck (from among those trucks that have capacity to
    add that parcel).
    """
    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Randomly schedule the given <parcels> onto the given <trucks>, that
        is, decide which parcels will go on which trucks, as well as the route
        each truck will take.
        """
        parcels2 = parcels
        shuffle(parcels2)
        unscheduled = []
        for parcel in parcels2:
            available_trucks = []
            for truck in trucks:
                if truck.left_capacity >= parcel.volume:
                    available_trucks.append(truck)
            if available_trucks:
                t = choice(available_trucks)
                t.pack(parcel)
            else:
                unscheduled.append(parcel)
        return unscheduled


class GreedyScheduler(Scheduler):
    """A strategic scheduler, it processes parcels one at a time, picking a
    truck for each, but it tries to pick the “best” truck it can for each
    parcel.

    === Private Attributes ===
    _priority_q: A queue of Parcels that operates in FIFO-priority order.
    _truck_priority: A function that compares two Trucks by their priority.
    """
    _priority_q: PriorityQueue
    _truck_priority: Callable[[Truck, Truck], bool]

    def __init__(self, config: Dict[str, Union[str, bool]]) -> None:
        """Initialize the GreedyScheduler with the four different parcel
        priority and the two truck priority. (See the priority functions below)
        """
        if config['parcel_priority'] == 'volume':
            if config['parcel_order'] == 'non-decreasing' and \
                    config['truck_order'] == 'non-decreasing':
                self._priority_q = PriorityQueue(_smaller_v)
                self._truck_priority = _smaller_space
            if config['parcel_order'] == 'non-decreasing' and \
                    config['truck_order'] == 'non-increasing':
                self._priority_q = PriorityQueue(_smaller_v)
                self._truck_priority = _larger_space
            if config['parcel_order'] == 'non-increasing' and \
                    config['truck_order'] == 'non-increasing':
                self._priority_q = PriorityQueue(_larger_v)
                self._truck_priority = _larger_space
            if config['parcel_order'] == 'non-increasing' and \
                    config['truck_order'] == 'non-decreasing':
                self._priority_q = PriorityQueue(_larger_v)
                self._truck_priority = _smaller_space

        elif config['parcel_priority'] == 'destination':
            if config['parcel_order'] == 'non-decreasing' and \
                    config['truck_order'] == 'non-decreasing':
                self._priority_q = PriorityQueue(_smaller_d)
                self._truck_priority = _smaller_space
            if config['parcel_order'] == 'non-decreasing' and \
                    config['truck_order'] == 'non-increasing':
                self._priority_q = PriorityQueue(_smaller_d)
                self._truck_priority = _larger_space
            if config['parcel_order'] == 'non-increasing' and \
                    config['truck_order'] == 'non-increasing':
                self._priority_q = PriorityQueue(_larger_d)
                self._truck_priority = _larger_space
            if config['parcel_order'] == 'non-increasing' and \
                    config['truck_order'] == 'non-decreasing':
                self._priority_q = PriorityQueue(_larger_d)
                self._truck_priority = _smaller_space

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Strategically schedule the given <parcels> onto the given <trucks>,
        that is, decide which parcels will go on which trucks, as well as the
        route each truck will take.

        # >>> gs = GreedyScheduler(_larger_v, _larger_space)
        # >>> t1 = Truck(1423, 10, 'Toronto')
        # >>> t = [t1]
        # >>> p1 = Parcel(1, 4, 'Toronto', 'Montreal')
        # >>> p2 = Parcel(2, 5, 'Toronto', 'York')
        # >>> p3 = Parcel(3, 1, 'Toronto', 'York')
        # >>> p4 = Parcel(4, 5, 'Toronto', 'London')
        # >>> p = [p1,p2,p3,p4]
        # >>> gs.schedule(p,t) == [p1, p3]
        # True
        """
        unscheduled = []
        for parcel in parcels:
            self._priority_q.add(parcel)
        while not self._priority_q.is_empty():
            p = self._priority_q.remove()
            available_trucks = []
            for truck in trucks:
                if truck.left_capacity >= p.volume:
                    available_trucks.append(truck)
            if not available_trucks:
                unscheduled.append(p)
            else:
                self._schedule_helper(p, available_trucks)
        return unscheduled

    def _schedule_helper(self, p: Parcel, available_trucks: [Truck]) -> None:
        """Strategically schedule the given <parcels> onto the given <trucks>,
        that is, decide which parcels will go on which trucks, as well as the
        route each truck will take.
        """
        trucks_by_dest = []
        for truck in available_trucks:
            if truck.route[-2] == p.destination:
                trucks_by_dest.append(truck)
        truck_queue = PriorityQueue(self._truck_priority)
        if not trucks_by_dest:
            for t in available_trucks:
                truck_queue.add(t)
        else:
            for t in trucks_by_dest:
                truck_queue.add(t)
        t = truck_queue.remove()
        t.pack(p)


# Functions for the four kinds of parcel priority, and two truck priority.
# By parcel volume:
def _larger_v(a: Parcel, b: Parcel) -> bool:
    """
    Return True if Parcel <a> has larger volume than Parcel <b>.
    """
    return a.volume > b.volume


def _smaller_v(a: Parcel, b: Parcel) -> bool:
    """
    Return True if Parcel <a> has smaller volume than Parcel <b>.
    """
    return a.volume < b.volume


# By parcel destination:
def _larger_d(a: Parcel, b: Parcel) -> bool:
    """
    Return True if Parcel <a> has larger destination than Parcel <b>. Since
    destinations are strings, larger and smaller is determined by comparing
    strings (city names) alphabetically.
    """
    return a.destination > b.destination


def _smaller_d(a: Parcel, b: Parcel) -> bool:
    """
    Return True if Parcel <a> has smaller destination than Parcel <b>. Since
    destinations are strings, larger and smaller is determined by comparing
    strings (city names) alphabetically.
    """
    return a.destination < b.destination


# By the available space of trucks:
def _larger_space(a: Truck, b: Truck) -> bool:
    """
    Return True if Truck <a> has larger available space than Parcel <b>.
    """
    return a.left_capacity > b.left_capacity


def _smaller_space(a: Truck, b: Truck) -> bool:
    """
    Return True if Truck <a> has smaller available space than Parcel <b>.
    """
    return a.left_capacity < b.left_capacity


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['compare_algorithms'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', 'container', 'domain'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
