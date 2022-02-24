from __future__ import annotations
from typing import Optional, Set, List
from puzzle import Puzzle
from solver import BfsSolver, DfsSolver


# difficulty constants
IMPOSSIBLE = 'impossible'
TRIVIAL = 'trivial'
EASY, MEDIUM, HARD = 'easy', 'medium', 'hard'

# constant for the set of letters used
LETTERS = "abcdefghijklmnopqrstuvwxyz"


# helper function to load a default set of words
def load_words() -> set[str]:
    """
    Return the set of words stored in the file called words.txt.
    """
    with open("words", "r") as words:
        return set(words.read().split())


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle.

    === Public Attributes ===
    from_word: the initial word the puzzle begins with
    to_word: the goal word the puzzle wants to change to
    word_set: the set of all words that are possible valid words to change into

    === Private Attributes ===
    _chars: a string of all possible characters that a word may consist of

    Representation Invariants:
    len(from_word) == len(to_word)
    from_word in word_set
    to_word in word_set
    all words in word_set are lowercase
    """
    from_word: str
    to_word: str
    word_set: Set[str]
    _chars: str

    def __init__(self, from_word: str, to_word: str,
                 word_set: Optional[Set[str]] = None) -> None:
        """
        Create a new word-ladder puzzle with the aim of stepping
        from <from_word> to <to_word> using words in <word_set>, changing one
        character at each step.

        If <word_set> is None, the words are loaded using load_words.

        Precondition:
        len(from_word) == len(to_word)
        from_word and to_word are both in word_set
        all words in word_set are lowercase
        """
        Puzzle.__init__(self)
        if word_set is None:
            word_set = load_words()

        (self.from_word, self.to_word, self.word_set) = (from_word,
                                                         to_word, word_set)
        # set of characters to use for 1-character changes
        self._chars = LETTERS

    # TODO (Task 3): override __eq__
    def __eq__(self, other: WordLadderPuzzle) -> bool:
        """
        Return whether WordLadderPuzzle self is equivalent to other.

        Two WordLadderPuzzles are equal if they have equal
        from_word, to_word, and word_set attributes.

        >>> wl1 = WordLadderPuzzle("me", "my", {"me", "my", "ma"})
        >>> wl2 = WordLadderPuzzle("me", "my", {"me", "my", "mu"})
        >>> wl3 = WordLadderPuzzle("me", "my", {"ma", "me", "my"})
        >>> wl1 == wl2
        False
        >>> wl1 == wl3
        True
        """
        return (self.from_word == other.from_word and
                self.to_word == other.to_word and
                self.word_set == other.word_set)

    # TODO (Task 3): override __str__
    def __str__(self) -> str:
        """
        Return a human-friendly string representing this WordLadderPuzzle's
        state, with the format:

        from_word -> to_word

        >>> wl1 = WordLadderPuzzle("me", "my", {"me", "my", "ma"})
        >>> wl2 = WordLadderPuzzle("me", "my", {"me", "my", "mu"})
        >>> print(wl1)
        me -> my
        >>> print(wl2)
        me -> my
        """
        return self.from_word + ' -> ' + self.to_word

    # TODO (Task 3): override is_solved
    # Note: A WordLadderPuzzle is solved when from_word is the same as its
    # to_word
    def is_solved(self) -> bool:
        """
        Return whether this WordLadderPuzzle is solved.

        >>> wl1 = WordLadderPuzzle("me", "me", {"me", "my"})
        >>> wl2 = WordLadderPuzzle("me", "my", {"me", "my"})
        >>> wl1.is_solved()
        True
        >>> wl2.is_solved()
        False
        """
        return self.from_word == self.to_word

    # TODO (Task 3): override extensions
    # legal extensions are valid WordLadderPuzzles that have a from_word that
    # differs from this WordLadderPuzzle's from_word by exactly one character
    def extensions(self) -> List[WordLadderPuzzle]:
        """
        Return a list of WordLadderPuzzles that are one step
        away from this WordLadderPuzzle.

        >>> wl1 = WordLadderPuzzle("me", "my", {"me", "be", "my"})
        >>> wl2 = WordLadderPuzzle("be", "my", {"me", "be", "my"})
        >>> wl3 = WordLadderPuzzle("my", "my", {"me", "be", "my"})

        # ensure wl1.extensions() contains both wl2 and wl3
        >>> wl1_extensions = wl1.extensions()
        >>> wl2 in wl1_extensions and wl3 in wl1_extensions
        True

        # ensure wl1.extensions() contains no other WordLadderPuzzles
        >>> len(wl1_extensions) == 2
        True
        """
        from_lst = list(self.from_word)
        extend = []
        to_words = []
        for word in self.word_set:
            if len(self.from_word) == len(word):
                to_words.append(word)

        for to_word in to_words:
            to_lst = list(to_word)
            diff = 0
            for i in range(len(from_lst)):
                if from_lst[i] != to_lst[i]:
                    diff += 1
                if diff > 1:
                    break
            if diff == 1:
                puzzle = WordLadderPuzzle(to_word, self.to_word, self.word_set)
                extend.append(puzzle)
        return extend

    # TODO (Task 3): implement get_difficulty
    # Note: implementing this requires you to have completed Task 2
    # Hint: Think about which of BfsSolver and DfsSolver is the right
    #       solver for the task at hand. (You may add any required
    #       imports at the top of the file.)
    def get_difficulty(self) -> str:
        """
        Return the "difficulty" of this puzzle.

        The difficulty is defined as follows:

        TRIVIAL - a solution can be reached in zero moves or just one move

        EASY - the shortest path to a solution is exactly 2 moves.
            e.g. The puzzle 'cost' -> 'moss' is solved in 2 moves:
                    'cost' -> 'most' and then 'most' -> 'moss'
                (So the result of calling a solver's solve method is a
                list of length 3)

        MEDIUM - the shortest path to a solution is less than 5 moves.

        HARD - a solution exists and it takes at least 5 moves to reach.

        IMPOSSIBLE - a solution does not exist
        """
        solver = BfsSolver()
        if self.is_solved():
            return TRIVIAL
        solution = solver.solve(self)
        if not solution:
            return IMPOSSIBLE
        num_step = len(solution) - 1
        if num_step == 1:
            return TRIVIAL
        if num_step == 2:
            return EASY
        if num_step < 5:
            return MEDIUM
        if num_step >= 5:
            return HARD


if __name__ == '__main__':
    # any code you want to write to test WordLadderPuzzle.
    import python_ta

    python_ta.check_all(config={'pyta-reporter': 'ColorReporter',
                                'allowed-io': ['load_words'],
                                'allowed-import-modules': ['doctest',
                                                           'python_ta',
                                                           'typing',
                                                           '__future__',
                                                           'puzzle',
                                                           'solver'],
                                'disable': ['E1136'],
                                'max-attributes': 15}
                        )
