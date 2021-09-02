"""
CSC148, Winter 2021
Assignment 2: Automatic Puzzle Solver
==============================
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Jonathan Calver, Sophia Huynh,
         Maryam Majedi, and Jaisie Sin.

All of the files in this directory are:
Copyright (c) 2021 Diane Horton, Jonathan Calver, Sophia Huynh,
                   Maryam Majedi, and Jaisie Sin.

=== Module Description ===

This module contains the abstract Solver class and its two subclasses, which
find solutions to puzzles, step by step.
"""

from __future__ import annotations

from typing import List, Optional, Set

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
        # handle the base case
        if not seen:
            seen = set()
        if puzzle.is_solved() and str(puzzle) not in seen:
            return [puzzle]
        if puzzle.fail_fast():
            seen.add(str(puzzle))

        if str(puzzle) not in seen:
            seen.add(str(puzzle))
            possible_moves = puzzle.extensions()
            for move in possible_moves:
                if str(move) in seen:
                    possible_moves.remove(move)
            while possible_moves:
                possible_move = possible_moves.pop(0)
                following_moves = self.solve(possible_move, seen)
                if following_moves and following_moves[-1].is_solved() \
                        and str(following_moves[-1]) not in seen:
                    return [puzzle] + following_moves
            return []
        else:
            return []


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
        if not seen:
            seen = set()
        if str(puzzle) in seen:
            return []
        possible_paths = [[puzzle]]
        while possible_paths and not possible_paths[0][-1].is_solved():
            if str(possible_paths[0][-1]) not in seen and \
                    not possible_paths[0][-1].fail_fast():
                curr_path = possible_paths.pop(0)
                curr_puzzle = curr_path[-1]
                seen.add(str(curr_puzzle))
                possible_moves = curr_puzzle.extensions()
                for possible_move in possible_moves:
                    possible_paths.append(curr_path + [possible_move]
                                          if str(possible_move) not in seen
                                          else None)
                possible_paths = [possible_path for possible_path
                                  in possible_paths if possible_path]
            else:
                possible_paths.pop(0)

        if possible_paths:
            if len(possible_paths[0]) != 1:
                return possible_paths[0]
            elif len(possible_paths[0]) == 1 \
                    and str(possible_paths[0][0]) not in seen:
                return possible_paths[0]
        return []


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

    # from word_ladder_puzzle import WordLadderPuzzle
    # word_set = {'a', 'b', 'c', 'aa', 'ab', 'ac', 'ba', 'bb',
    #             'bc', 'ca', 'cb', 'cc', 'aaa',
    #             'aba', 'abc',
    #             'aca', 'acb', 'acc'}
    # ladder = WordLadderPuzzle('aaa', 'abc', word_set)
    # bfs_solver = BfsSolver()
    # act = bfs_solver.solve(ladder)
    # print('---------------------')
    # acc = set()
    # print(len(act) == 3)
    # for a in act:
    #     print(str(a))
    # print(act[-1].is_solved())
