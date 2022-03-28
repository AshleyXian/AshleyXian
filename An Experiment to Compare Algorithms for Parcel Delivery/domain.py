"""Assignment 1 - Domain classes (Task 2)

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

This module contains the classes required to represent the entities
in the simulation: Parcel, Truck and Fleet.
"""
from typing import List, Dict
from distance_map import DistanceMap


class Parcel:
    """The information of a single parcel.

    === Public Attributes ===
    parcel_id: The unique ID of a parcel.
    volume: The volume of the parcel, measured in units of cubic centimetres
    (cc).
    source: The name of the city the parcel came from.
    destination: the name of the city where it must be delivered.

    === Representation Invariants ===
    - No two parcel can have the same ID.
    - The volume is a positive integer.
    """
    parcel_id: int
    volume: int
    source: str
    destination: str

    def __init__(self, unique_id: int, volume: int, source: str,
                 destination: str) -> None:
        """Initialize the parcel with its <unique_id>, <volume>, <source> and
        <destination>.

        >>> p = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> p.destination
        'Montreal'
        >>> p.volume
        4
        """
        self.parcel_id = unique_id
        self.volume = volume
        self.source = source
        self.destination = destination


class Truck:
    """The information of a single truck.

    === Public Attributes ===
    truck_id: The unique ID of a truck.
    total_capacity: The total volume capacity of the truck, measured in units
    of cubic centimetres (cc).
    left_capacity: The empty capacity left for the truck or how many more
    volumes of parcels can be added onto the truck.
    route: An ordered list of city names that it is scheduled to travel through.
    parcels_id: The IDs of the parcels that have been packed onto this truck.

    === Representation Invariants ===
    - No two trucks can have the same ID.
    - The sum of the volumes of the parcels on a track cannot exceed its volume
    capacity. (The range of the current capacity would be zero to the total
    capacity.
    - The volume capacity is a positive integer.

    """
    truck_id: int
    total_capacity: int
    left_capacity: int
    route: List[str]
    parcels_id: List[int]

    def __init__(self, unique_id: int, total: int, depot: str) -> None:
        """Initialize an empty truck with its <unique_id>, <total> capacity and
        <depot>. The depot is a special city that all parcels and trucks must
        start from, and all trucks return to at the end of their route.

        >>> t = Truck(1423, 1000, 'Toronto')
        >>> t.left_capacity
        1000
        >>> t.route
        ['Toronto', 'Toronto']
        """
        self.truck_id = unique_id
        self.total_capacity = total
        self.left_capacity = total
        self.route = [depot, depot]
        self.parcels_id = []

    def pack(self, parcel: Parcel) -> bool:
        """Pack the <parcel> onto the truck. Return True if the truck still have
        enough volume left for the parcel and False if there's not enough volume
        left for the parcel.

        >>> t = Truck(1423, 10, 'Toronto')
        >>> p = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t.pack(p)
        True
        >>> t.route
        ['Toronto', 'Montreal', 'Toronto']
        >>> p2 = Parcel(5, 50, 'Toronto', 'Montreal')
        >>> t.pack(p2)
        False
        """
        result = False
        if parcel.volume <= self.left_capacity:
            self.left_capacity = self.left_capacity - parcel.volume
            self.parcels_id.append(parcel.parcel_id)
            result = True
            if parcel.destination != self.route[-2]:
                self.route.insert(-1, parcel.destination)
        return result

    def fullness(self) -> float:
        """Return the percentage fullness of the track which will be the
        volume used divided by the total volume.

        >>> t = Truck(1423, 10, 'Toronto')
        >>> p = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t.pack(p)
        True
        >>> t.fullness()
        40.0
        >>> t2 = Truck(1425, 10, 'Toronto')
        >>> t2.fullness()
        0.0
        """
        used = self.total_capacity - self.left_capacity
        return (used / self.total_capacity) * 100


class Fleet:
    """ A fleet of trucks for making deliveries.

    ===== Public Attributes =====
    trucks:
      List of all Truck objects in this fleet.
    """
    trucks: List[Truck]

    def __init__(self) -> None:
        """Create a Fleet with no trucks.

        >>> f = Fleet()
        >>> f.num_trucks()
        0
        """
        self.trucks = []

    def add_truck(self, truck: Truck) -> None:
        """Add <truck> to this fleet.

        Precondition: No truck with the same ID as <truck> has already been
        added to this Fleet.

        >>> f = Fleet()
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> f.add_truck(t)
        >>> f.num_trucks()
        1
        """
        self.trucks.append(truck)

    # We will not test the format of the string that you return -- it is up
    # to you.
    def __str__(self) -> str:
        """Produce a string representation of this fleet

        >>> f = Fleet()
        >>> t = Truck(1428, 1000, 'Toronto')
        >>> f.add_truck(t)
        >>> str(f)
        'This fleet has 1 truck(s) in total, and 0 of them is/are nonempty.'
        """
        return f'This fleet has {self.num_trucks()} truck(s) in total, and ' \
               f'{self.num_nonempty_trucks()} of them is/are nonempty.'

    def num_trucks(self) -> int:
        """Return the number of trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> f.num_trucks()
        1
        """
        return len(self.trucks)

    def num_nonempty_trucks(self) -> int:
        """Return the number of non-empty trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        True
        >>> t1.fullness()
        90.0
        >>> t2 = Truck(5912, 20, 'Toronto')
        >>> f.add_truck(t2)
        >>> p3 = Parcel(3, 2, 'New York', 'Windsor')
        >>> t2.pack(p3)
        True
        >>> t2.fullness()
        10.0
        >>> t3 = Truck(1111, 50, 'Toronto')
        >>> f.add_truck(t3)
        >>> f.num_nonempty_trucks()
        2
        """
        n = 0
        for truck in self.trucks:
            if truck.total_capacity > truck.left_capacity:
                n = n + 1
        return n

    def parcel_allocations(self) -> Dict[int, List[int]]:
        """Return a dictionary in which each key is the ID of a truck in this
        fleet and its value is a list of the IDs of the parcels packed onto it,
        in the order in which they were packed.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
        >>> p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.pack(p2)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.parcel_allocations() == {1423: [27, 12], 1333: [28]}
        True
        """
        result = {}
        for truck in self.trucks:
            result[truck.truck_id] = truck.parcels_id
        return result

    def total_unused_space(self) -> int:
        """Return the total unused space, summed over all non-empty trucks in
        the fleet.
        If there are no non-empty trucks in the fleet, return 0.

        >>> f = Fleet()
        >>> f.total_unused_space()
        0
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.total_unused_space()
        995
        """
        result = 0
        for truck in self.trucks:
            if truck.total_capacity > truck.left_capacity:
                result = result + truck.left_capacity
        return result

    def _total_fullness(self) -> float:
        """Return the sum of truck.fullness() for each non-empty truck in the
        fleet. If there are no non-empty trucks, return 0.

        >>> f = Fleet()
        >>> f._total_fullness() == 0.0
        True
        >>> t = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t)
        >>> f._total_fullness() == 0.0
        True
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f._total_fullness()
        50.0
        >>> p1 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t.pack(p1)
        True
        >>> f._total_fullness()
        100.0
        """
        result = 0
        for truck in self.trucks:
            if truck.total_capacity > truck.left_capacity:
                result = result + truck.fullness()
        return result

    def average_fullness(self) -> float:
        """Return the average percent fullness of all non-empty trucks in the
        fleet.

        Precondition: At least one truck is non-empty.

        >>> f = Fleet()
        >>> t = Truck(1423, 10, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.average_fullness()
        50.0
        >>> t2 = Truck(1314, 10, "Toronto")
        >>> p2 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> f.add_truck(t2)
        >>> t2.pack(p2)
        True
        >>> f.average_fullness()
        50.0
        """
        return self._total_fullness() / len(self.trucks)

    def total_distance_travelled(self, dmap: DistanceMap) -> int:
        """Return the total distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Precondition: <dmap> contains all distances required to compute the
                      average distance travelled.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.total_distance_travelled(m)
        36
        >>> t3 = Truck(1488, 10, 'Toronto')
        >>> f.total_distance_travelled(m)
        36
        """
        total = 0
        for truck in self.trucks:
            if truck.route[0] == truck.route[1]:
                total = total + 0
            else:
                for i in range(0, len(truck.route) - 1):
                    d = dmap.distance(truck.route[i], truck.route[i+1])
                    total = total + d
        return total

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the average distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Include in the average only trucks that have actually travelled some
        non-zero distance.

        Preconditions:
        - <dmap> contains all distances required to compute the average
          distance travelled.
        - At least one truck has travelled a non-zero distance.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.average_distance_travelled(m)
        18.0
        """
        n = 0
        for truck in self.trucks:
            if truck.route[0] != truck.route[1]:
                n = n + 1
        total = self.total_distance_travelled(dmap)
        return total / n


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
