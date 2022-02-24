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
    assert wl1.get_difficulty() == TRIVIAL

    wl2 = WordLadderPuzzle("come", "done", {"come", "cone", "done"})
    assert wl2.get_difficulty() == EASY


def test_expression_tree_eval_doctest() -> None:
    """Test ExprTree.eval on the provided doctest"""
    exp_t = ExprTree('+', [ExprTree(3, []),
                           ExprTree('*', [ExprTree('x', []),
                                          ExprTree('y', [])]),
                           ExprTree('x', [])])
    look_up = {}
    exp_t.populate_lookup(look_up)
    assert exp_t.eval(look_up) == 3

    look_up['x'] = 7
    look_up['y'] = 3
    assert exp_t.eval(look_up) == 31


def test_expression_tree_populate_lookup_doctest() -> None:
    """Test ExprTree.populate_lookup on the provided doctest"""
    expr_t = ExprTree('a', [])
    look_up = {}
    expr_t.populate_lookup(look_up)
    assert look_up['a'] == 0
    assert len(look_up) == 1


def test_expression_tree_construct_from_list_doctest() -> None:
    """Test ExprTree.construct_from_list on the provided doctest"""
    # This test relies on ExprTree.__str__ working correctly.
    example = [[5]]
    exp_t = construct_from_list(example)
    assert str(exp_t) == '5'

    example = [['+'], [3, 'a']]
    exp_t = construct_from_list(example)
    assert str(exp_t) == '(3 + a)'


def test_expression_tree_substitute_doctest() -> None:
    """Test ExprTree.substitute on the provided doctest"""
    # This test relies on ExprTree.__str__ working correctly.
    exp_t = ExprTree('a', [])
    exp_t.substitute({'a': 1})
    assert str(exp_t) == '1'

    exp_t = ExprTree('*', [ExprTree('a', []),
                           ExprTree('*', [ExprTree('a', []),
                                          ExprTree(1, [])])])
    exp_t.substitute({'a': 2, '*': '+'})
    assert str(exp_t) == '(2 + (2 + 1))'


def test_expression_tree_str_doctest() -> None:
    """Test ExprTree.__str__ on the provided doctest"""

    exp_t = ExprTree('+', [ExprTree('a', []),
                           ExprTree('b', []),
                           ExprTree(3, [])])
    assert str(exp_t) == '(a + b + 3)'

    exp_t = ExprTree(None, [])
    assert str(exp_t) == '()'

    exp_t = ExprTree(5, [])
    assert str(exp_t) == '5'

    exp_t = ExprTree('+', [ExprTree('*', [ExprTree(7, []),
                                          ExprTree('+',
                                                   [ExprTree(6, []),
                                                    ExprTree(6, [])])]),
                           ExprTree(5, [])])
    assert str(exp_t) == '((7 * (6 + 6)) + 5)'

    exp_t = ExprTree('+', [ExprTree(3, []),
                           ExprTree('*', [ExprTree('x', []),
                                          ExprTree('y', [])]),
                           ExprTree('x', [])])
    assert str(exp_t) == '(3 + (x * y) + x)'


def test_expression_tree_eq_doctest() -> None:
    """Test ExprTree.__eq__ on the provided doctest"""
    t1 = ExprTree(5, [])
    assert t1.__eq__(ExprTree(5, []))

    t2 = ExprTree('*', [ExprTree(5, []), ExprTree(2, [])])
    assert t2.__eq__(ExprTree('*', [ExprTree(5, []), ExprTree(2, [])]))
    assert t2.__eq__(ExprTree('*', [])) is False


def test_expression_tree_puzzle_is_solved_doctest() -> None:
    """Test ExpressionTreePuzzle.is_solved on the provided doctest"""
    exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
    puz = ExpressionTreePuzzle(exp_t, 7)
    assert puz.is_solved() is False
    puz.variables['a'] = 7
    assert puz.is_solved() is False
    puz.variables['a'] = 5
    puz.variables['b'] = 2
    assert puz.is_solved() is True


def test_expression_tree_puzzle_str_doctest() -> None:
    """Test ExpressionTreePuzzle.__str__ on the provided doctest"""
    exp_t = ExprTree('+', [ExprTree('*',
                                    [ExprTree('a', []),
                                     ExprTree('+', [ExprTree('b', []),
                                                    ExprTree(6, []),
                                                    ExprTree(6, []),
                                                    ])]),
                           ExprTree(5, [])])
    puz = ExpressionTreePuzzle(exp_t, 61)
    assert str(puz) == "{'a': 0, 'b': 0}\n((a * (b + 6 + 6)) + 5) = 61"


def test_expression_tree_puzzle_extensions_doctest() -> None:
    """Test ExpressionTreePuzzle.extensions on the provided doctest"""
    exp_t = ExprTree('a', [])
    puz = ExpressionTreePuzzle(exp_t, 7)
    exts_of_puz = puz.extensions()
    assert len(exts_of_puz) == 9

    exts_of_an_ext = exts_of_puz[0].extensions()
    assert len(exts_of_an_ext) == 0

    exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
    puz = ExpressionTreePuzzle(exp_t, 8)
    exts_of_puz = puz.extensions()
    assert len(exts_of_puz) == 18


def test_expression_tree_puzzle_fail_fast_true() -> None:
    """Test ExpressionTreePuzzle.fail_fast on an unsolvable puzzle."""
    exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
    puz = ExpressionTreePuzzle(exp_t, 7)
    puz.variables['a'] = 9

    assert puz.fail_fast() is True


def test_expression_tree_puzzle_fail_fast_false() -> None:
    """Test ExpressionTreePuzzle.fail_fast on a solvable puzzle."""
    exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
    puz = ExpressionTreePuzzle(exp_t, 7)
    puz.variables['a'] = 2

    assert puz.fail_fast() is False


if __name__ == '__main__':
    import pytest
    pytest.main(['a2_starter_tests.py'])
