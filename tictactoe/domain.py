from dataclasses import dataclass

LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
         (2, 5, 8), (0, 4, 8), (2, 4, 6))


@dataclass(frozen=True)
class Board:
    cells: tuple[str, ...] = ('',) * 9

    def __post_init__(self):
        if not isinstance(self.cells, tuple) or len(self.cells) != 9 or any(c not in ('', 'X', 'O') for c in self.cells):
            raise ValueError('Tabuleiro inválido')
        x, o = self.cells.count('X'), self.cells.count('O')
        winners = {self.cells[a] for a, b, c in LINES if self.cells[a] and self.cells[a] == self.cells[b] == self.cells[c]}
        if x not in (o, o + 1) or len(winners) > 1:
            raise ValueError('Estado impossível')
        if ('X' in winners and x != o + 1) or ('O' in winners and x != o):
            raise ValueError('Contagem incompatível com vencedor')

    @property
    def turn(self):
        return 'X' if self.cells.count('X') == self.cells.count('O') else 'O'

    @property
    def result(self):
        for a, b, c in LINES:
            if self.cells[a] and self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a]
        return 'draw' if all(self.cells) else None

    def moves(self):
        return tuple(i for i in (4, 0, 2, 6, 8, 1, 3, 5, 7) if not self.cells[i]) if self.result is None else ()

    def play(self, index):
        if type(index) is not int or index not in self.moves():
            raise ValueError('Jogada inválida')
        return Board(self.cells[:index] + (self.turn,) + self.cells[index + 1:])
