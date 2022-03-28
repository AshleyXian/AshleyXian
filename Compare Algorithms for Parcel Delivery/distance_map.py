"""Assignment 1 - Distance map (Task 1)

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

This module contains the class DistanceMap, which is used to store
and look up distances between cities. This class does not read distances
from the map file. (All reading from files is done in module experiment.)
Instead, it provides public methods that can be called to store and look up
distances.
"""
from typing import Dict, Tuple, List


class DistanceMap:
    """A distance map used for storing and looking up the distance between
    any two cities.

    === Private Attributes ===
    _distance_map: A dictionary used to store the distance between two cities.
    Each key is a list of two cities in order of the first city and the second
    city (A and B). The value of each key is the distance from A to B and the
    distance from B to A.

    === Representation Invariants ===
    - The distance is a positive integer.
    - The distance from city B to city A, might be the same or different.
    """
    _distance_map: Dict[Tuple, List]

    def __init__(self) -> None:
        """Initialize a _distance_map with no data in it.

        >>> M = DistanceMap()
        >>> len(M._distance_map)
        0
        """
        self._distance_map = {}

    def add_distance(self, first: str, second: str, dist1: int,
                     dist2: int = None) -> None:
        """Adding an item into the _distance_map dictionary where the keys are
        [first, second] and the values are [dist1, dist2]. Where <first> is the
        city A, and <second> is the city B, dist1 is the distance from city A to
        city B, and dist2 is the distance from city B to city A.

        >>> M = DistanceMap()
        >>> M.add_distance('Toronto', 'Hamilton', 9)
        >>> M._distance_map[('Toronto', 'Hamilton')]
        [9, 9]
        >>> M.add_distance('Toronto', 'Beijing', 10, 11)
        >>> M._distance_map[('Toronto', 'Beijing')]
        [10, 11]
        """
        key = (first, second)
        if key not in self._distance_map:
            if dist2 is None:
                self._distance_map[key] = [dist1, dist1]
            else:
                self._distance_map[key] = [dist1, dist2]

    def distance(self, city1: str, city2: str) -> int:
        """
        Return the distance from the <city1> to the <city2>. Return -1
        if the distance is not stored in the distance map.

        >>> M = DistanceMap()
        >>> M.add_distance('Toronto', 'Hamilton', 9)
        >>> M.distance('Toronto', 'Hamilton')
        9
        >>> M.distance('Hamilton', 'Toronto')
        9
        >>> M.add_distance('Toronto', 'Beijing', 10, 11)
        >>> M.distance('Beijing', 'Toronto')
        11
        """
        cities1 = (city1, city2)
        cities2 = (city2, city1)
        if cities1 in self._distance_map.keys():
            return self._distance_map[cities1][0]
        if cities2 in self._distance_map.keys():
            return self._distance_map[cities2][1]
        return -1


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
