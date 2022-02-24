from sudoku_puzzle import SudokuPuzzle
from word_ladder_puzzle import WordLadderPuzzle, EASY, TRIVIAL
from expression_tree import ExprTree, construct_from_list
from expression_tree_puzzle import ExpressionTreePuzzle
from solver import BfsSolver, DfsSolver


# Below is an incomplete set of tests: these tests are mostly the provided
# doctest examples.
#
# We encourage you to write additional test cases and test your own code,
# using the provided test cases as a template!


def test_sudoku_fail_fast_doctest() -> None:
    """Test SudokuPuzzle.fail_fast on the provided doctest."""
    s = SudokuPuzzle(4, [["A", "B", "C", "D"],
                         ["C", "D", " ", " "],
                         [" ", " ", " ", " "],
                         [" ", " ", " ", " "]],
                     {"A", "B", "C", "D"})

    assert s.fail_fast() is False

    s = SudokuPuzzle(4, [["B", "D", "A", "C"],
                         ["C", "A", "B", "D"],
                         ["A", "B", " ", " "],
                         [" ", " ", " ", " "]],
                     {"A", "B", "C", "D"})
    assert s.fail_fast() is True


def test_has_unique_solution_doctest() -> None:
    """Test has_unique_solution on a SudokuPuzzle with a non-unique solution."""
    s = SudokuPuzzle(4, [["D", "C", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["C", " ", "A", " "],
                         ["A", " ", "C", " "]],
                     {"A", "B", "C", "D"})

    assert s.has_unique_solution() is False


def test_dfs_solver_example() -> None:
    """Test DfsSolver.solve on a SudokuPuzzle."""
    # This SudokuPuzzle is a more filled-in version of the one in the
    # example from the handout.
    s = SudokuPuzzle(4, [["C", "D", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["D", " ", "A", " "],
                         ["A", " ", "C", " "]],
                     {"A", "B", "C", "D"})

    solver = DfsSolver()
    actual = solver.solve(s)[-1]

    expected = SudokuPuzzle(4, [["C", "D", "B", "A"],
                                ["B", "A", "D", "C"],
                                ["D", "C", "A", "B"],
                                ["A", "B", "C", "D"]],
                            {"A", "B", "C", "D"})

    assert actual == expected


def test_bfs_solver_example() -> None:
    """Test BfsSolver.solve on a SudokuPuzzle."""
    # This SudokuPuzzle is a more filled-in version of the one in the
    # example from the handout.
    s = SudokuPuzzle(4, [["C", "D", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["D", " ", "A", " "],
                         ["A", " ", "C", " "]],
                     {"A", "B", "C", "D"})

    solver = BfsSolver()
    actual = solver.solve(s)[-1]

    expected = SudokuPuzzle(4, [["C", "D", "B", "A"],
                                ["B", "A", "D", "C"],
                                ["D", "C", "A", "B"],
                                ["A", "B", "C", "D"]],
                            {"A", "B", "C", "D"})

    assert actual == expected


def test_word_ladder_eq_doctest() -> None:
    """Test WordLadder.__eq__ on the provided doctest"""
    wl1 = WordLadderPuzzle("me", "my", {"me", "my", "ma"})
    wl2 = WordLadderPuzzle("me", "my", {"me", "my", "mu"})
    wl3 = WordLadderPuzzle("me", "my", {"ma", "me", "my"})
    assert wl1.__eq__(wl2) is False
    assert wl1.__eq__(wl3) is True


def test_word_ladder_str_doctest() -> None:
    """Test WordLadder.__str__ on the provided doctest"""
    wl1 = WordLadderPuzzle("me", "my", {"me", "my", "ma"})
    wl2 = WordLadderPuzzle("me", "my", {"me", "my", "mu"})
    assert str(wl1) == 'me -> my'
    assert str(wl2) == 'me -> my'


def test_word_ladder_extensions_doctest() -> None:
    """Test WordLadder.__str__ on the provided doctest"""
    wl1 = WordLadderPuzzle("me", "my", {"me", "be", "my"})
    wl2 = WordLadderPuzzle("be", "my", {"me", "be", "my"})
    wl3 = WordLadderPuzzle("my", "my", {"me", "be", "my"})

    msg1 = f"{wl1.extensions()} is missing some valid puzzle states"
    msg2 = f"{wl1.extensions()} contains extra invalid puzzle states"

    assert all([wlp in wl1.extensions() for wlp in [wl2, wl3]]), msg1
    assert all([wlp in [wl2, wl3] for wlp in wl1.extensions()]), msg2


def test_word_ladder_is_solved_doctest() -> None:
    """Test WordLadder.is_solved on the provided doctest"""
    wl1 = WordLadderPuzzle("me", "me", {"me", "my"})
    wl2 = WordLadderPuzzle("me", "my", {"me", "my"})
    assert wl1.is_solved() is True
    assert wl2.is_solved() is False


def test_word_ladder_get_difficulty() -> None:
    """Test WordLadder.get_difficulty on TRIVIAL and EASY puzzles."""
    wl1 = WordLadderPuzzle("done", "done", {"done"})
    wl2 = WordLadderPuzzle("come", "done", {"come", "cone", "done"})
    assert wl1.get_difficulty() == TRIVIAL
    assert wl2.get_difficulty() == EASY


if __name__ == '__main__':
    import pytest
    pytest.main(['test.py'])
