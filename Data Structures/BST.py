from __future__ import annotations
from typing import Any, List, Optional


class BinarySearchTree:
    """Binary Search Tree class.

    This class represents a binary tree satisfying the Binary Search Tree
    property: for every node, its value is >= all items stored in its left
    subtree, and <= all items stored in its right subtree.
    """
    # === Private Attributes ===
    # The item stored at the root of the tree, or None if the tree is empty.
    _root: Optional[Any]
    # The left subtree, or None if the tree is empty.
    _left: Optional[BinarySearchTree]
    # The right subtree, or None if the tree is empty.
    _right: Optional[BinarySearchTree]

    # === Representation Invariants ===
    #  - If self._root is None, then so are self._left and self._right.
    #    This represents an empty BST.
    #  - If self._root is not None, then self._left and self._right
    #    are BinarySearchTrees.
    #  - (BST Property) If self is not empty, then
    #    all items in self._left are <= self._root, and
    #    all items in self._right are >= self._root.

    def __init__(self, root: Optional[Any]) -> None:
        """Initialize a new BST containing only the given root value.

        If <root> is None, initialize an empty tree.
        """
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)

    def is_empty(self) -> bool:
        """Return True if this BST is empty.

        >>> bst = BinarySearchTree(None)
        >>> bst.is_empty()
        True
        >>> bst = BinarySearchTree(10)
        >>> bst.is_empty()
        False
        """
        return self._root is None

    # -------------------------------------------------------------------------
    # Standard Container methods (search, insert)
    # -------------------------------------------------------------------------
    def __contains__(self, item: Any) -> bool:
        """Return whether <item> is in this BST.

        >>> bst = BinarySearchTree(3)
        >>> bst._left = BinarySearchTree(2)
        >>> bst._right = BinarySearchTree(5)
        >>> 3 in bst
        True
        >>> 5 in bst
        True
        >>> 2 in bst
        True
        >>> 4 in bst
        False
        """
        if self.is_empty():
            return False
        elif item == self._root:
            return True
        elif item < self._root:
            return item in self._left   # or, self._left.__contains__(item)
        else:
            return item in self._right  # or, self._right.__contains__(item)

    # -------------------------------------------------------------------------
    # Additional BST methods
    # -------------------------------------------------------------------------
    def __str__(self) -> str:
        """Return a string representation of this BST.

        This string uses indentation to show depth.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this BST.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            answer = depth * '  ' + str(self._root) + '\n'
            answer += self._left._str_indented(depth + 1)
            answer += self._right._str_indented(depth + 1)
            return answer

    # -------------------------------------------------------------------------
    # Prep exercises
    # -------------------------------------------------------------------------
    def maximum(self) -> Optional[int]:
        """Return the maximum number in this BST, or None if this BST is empty.

        Hint: Review the BST property to ensure you aren't making unnecessary
        recursive calls.

        >>> BinarySearchTree(None).maximum() is None   # Empty BST
        True
        >>> BinarySearchTree(10).maximum()
        10
        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(3)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.maximum()
        13
        """
        if self.is_empty():
            return None
        if self._right.is_empty():
            return self._root
        else:
            return self._right.maximum()

    def count(self, item: Any) -> int:
        """Return the number of occurrences of <item> in this BST.

        Hint: carefully review the BST property!

        >>> BinarySearchTree(None).count(148)  # An empty BST
        0
        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(3)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.count(7)
        1
        >>> bst.count(3)
        2
        >>> bst.count(100)
        0
        """
        if self.is_empty():
            return 0
        count = 0
        if self._root == item:
            count = 1
            count += self._left.count(item)
            count += self._right.count(item)
        elif self._root > item:
            count += self._left.count(item)
        else:
            count += self._right.count(item)
        return count

    def items(self) -> List:
        """Return all of the items in the BST in sorted order.

        You should *not* need to sort the list yourself: instead, use the BST
        property and combine self._left.items() and self._right.items()
        in the right order!

        >>> BinarySearchTree(None).items()  # An empty BST
        []
        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.items()
        [2, 3, 5, 7, 9, 11, 13]
        """
        if self.is_empty():
            return []
        lst = self._left.items() + [self._root] + self._right.items()
        return lst

    def smaller(self, item: Any) -> List:
        """Return all of the items in this BST strictly smaller than <item>

        The items are returned in sorted order.

        Precondition: all items in this BST can be compared with <item>.

        As with BinarySearchTree.items, you should *not* need to sort the list
        yourself!

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.smaller(6)
        [2, 3, 5]
        >>> bst.smaller(13)
        [2, 3, 5, 7, 9, 11]
        """
        if self.is_empty():
            return []
        lst = []
        if item == self._root:
            lst.extend(self._left.smaller(item))
        if item > self._root:

            lst.extend(self._left.smaller(item))
            lst.append(self._root)
            lst.extend(self._right.smaller(item))
        if item < self._root:
            lst.extend(self._left.smaller(item))
        # lst.sort()
        return lst


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={"disable": ["E9959", "E1136"]})
