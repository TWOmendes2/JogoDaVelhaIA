import unittest
from functools import lru_cache
from tictactoe.domain import Board
from tictactoe.ai import Minimax


@lru_cache(None)
def oracle(board):
    if board.result:
        return 0 if board.result == 'draw' else -1
    return max(-oracle(board.play(m)) for m in board.moves())


class GameTests(unittest.TestCase):
    def test_illegal_moves_and_immutable_board(self):
        board = Board()
        played = board.play(4)
        self.assertEqual(board.cells, ('',) * 9)
        for move in (4, -1, 9, True):
            with self.assertRaises(ValueError):
                played.play(move)

    def test_invalid_states(self):
        for cells in [('O',) + ('',) * 8, ('X',) * 9, ('X', 'X', 'X', 'O', 'O', 'O', '', '', '')]:
            with self.assertRaises(ValueError):
                Board(cells)

    def test_all_reachable_states_match_unpruned_oracle(self):
        engine, seen = Minimax(), set()
        def walk(board):
            if board in seen:
                return
            seen.add(board)
            self.assertEqual(engine.score(board), oracle(board), board)
            move = engine.choose(board)
            if board.result:
                self.assertIsNone(move)
            else:
                self.assertEqual(-oracle(board.play(move)), oracle(board))
                for child in board.moves():
                    walk(board.play(child))
        walk(Board())
        self.assertEqual(len(seen), 5478)
        self.assertGreater(engine.cache_hits, 0)

    def test_ai_never_loses_as_either_player(self):
        for player in ('X', 'O'):
            engine, seen = Minimax(), set()
            def walk(board):
                if board in seen:
                    return
                seen.add(board)
                if board.result:
                    self.assertIn(board.result, (player, 'draw'))
                    return
                moves = (engine.choose(board),) if board.turn == player else board.moves()
                for move in moves:
                    walk(board.play(move))
            walk(Board())
