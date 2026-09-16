from .domain import Board


class Minimax:
    def __init__(self):
        self.cache = {}
        self.nodes = 0
        self.cache_hits = 0

    def score(self, board: Board, alpha=-2, beta=2):
        self.nodes += 1
        if board.result:
            return 0 if board.result == 'draw' else -1
        original_alpha, original_beta = alpha, beta
        entry = self.cache.get(board)
        if entry:
            self.cache_hits += 1
            value, kind = entry
            if kind == 'exact':
                return value
            if kind == 'lower':
                alpha = max(alpha, value)
            else:
                beta = min(beta, value)
            if alpha >= beta:
                return value
        value = -2
        for move in board.moves():
            value = max(value, -self.score(board.play(move), -beta, -alpha))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        kind = 'upper' if value <= original_alpha else 'lower' if value >= original_beta else 'exact'
        self.cache[board] = (value, kind)
        return value

    def choose(self, board: Board):
        if board.result is not None:
            return None
        return max(board.moves(), key=lambda move: -self.score(board.play(move)))
