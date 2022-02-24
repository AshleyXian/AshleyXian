from __future__ import annotations

from typing import List, Optional, Set

# You may remove this import if you don't use it in your code.
from adts import Queue

from puzzle import Puzzle


class Solver:
    """"
    A solver for full-information puzzles. This is an abstract class
    and purely provides the interface for our solve method.
    """

    # You may NOT change the interface to the solve method.
    # Note the optional parameter seen and its type.
    # Your implementations of this method in the two subclasses should use seen
    # to keep track of all puzzle states that you encounter during the
    # solution process.
    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        raise NotImplementedError


# Your solve method MUST be a recursive function (i.e. it must make
# at least one recursive call to itself)
# You may NOT change the interface to the solve method.
class DfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a depth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        if puzzle.fail_fast():
            return []
        rslt = [puzzle]
        solved = puzzle.is_solved()

        if seen is None:
            seen = {str(puzzle)}
        if seen is not None and str(puzzle) not in seen:
            seen.add(str(puzzle))

        i = 0
        while i < len(puzzle.extensions()) and not solved:
            if str(puzzle.extensions()[i]) not in seen:
                child = self.solve(puzzle.extensions()[i], seen)
                if child:
                    rslt.extend(child)
                    solved = True
            i = i + 1

        if not solved:
            return []
        return rslt


# Hint: You may find a Queue useful here.
class BfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a breadth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        if puzzle.fail_fast():
            return []
        if seen is None:
            seen = {str(puzzle)}
        if seen is not None and str(puzzle) not in seen:
            seen.add(str(puzzle))
        q = Queue()
        origin = {}
        for puzzles in puzzle.extensions():
            q.enqueue(puzzles)
            origin[str(puzzles)] = puzzle

        cur = q.dequeue()
        while (cur is not None) and (not cur.is_solved()):
            # if (seen is None) and (not cur.fail_fast()):
            #     for item in cur.extensions():
            #         if str(item) not in seen:
            #             q.enqueue(item)
            #             origin[str(item)] = cur
            if (seen is not None) and (str(cur) not in seen) and \
                    (not cur.fail_fast()):
                lst = _bfs_helper(cur, seen)
                for item in lst:
                    q.enqueue(item)
                    origin[str(item)] = cur
            if seen is None:
                seen = {str(cur)}
            elif str(cur) in seen:
                pass
            else:
                seen.add(str(cur))
            cur = q.dequeue()

        rslt = []
        while str(cur) in origin:
            rslt.insert(0, cur)
            cur = origin[str(cur)]
        rslt.insert(0, puzzle)
        return rslt


def _bfs_helper(cur: Puzzle, seen: List[str]) -> list:
    """

    """
    lst = []
    for item in cur.extensions():
        if str(item) not in seen:
            lst.append(item)
    return lst


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={'pyta-reporter': 'ColorReporter',
                                'allowed-io': [],
                                'allowed-import-modules': ['doctest',
                                                           'python_ta',
                                                           'typing',
                                                           '__future__',
                                                           'puzzle',
                                                           'adts'],
                                'disable': ['E1136'],
                                'max-attributes': 15}
                        )
