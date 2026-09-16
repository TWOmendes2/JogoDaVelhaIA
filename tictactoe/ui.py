import tkinter as tk
from tkinter import ttk
from .domain import Board
from .ai import Minimax


def main():
    root = tk.Tk()
    root.title('Jogo da Velha v2')
    board, engine = Board(), Minimax()
    mode = tk.StringVar(value='Pessoa × IA')
    status = tk.StringVar()

    def render():
        for i, button in enumerate(buttons):
            button.configure(text=board.cells[i], state='normal' if i in board.moves() else 'disabled')
        status.set('Empate' if board.result == 'draw' else f'Vencedor: {board.result}' if board.result else f'Vez de {board.turn}')

    def reset(*_):
        nonlocal board
        board = Board()
        render()

    def play(index):
        nonlocal board
        board = board.play(index)
        if mode.get() == 'Pessoa × IA' and not board.result:
            board = board.play(engine.choose(board))
        render()

    selector = ttk.Combobox(root, textvariable=mode, values=('Pessoa × IA', 'Pessoa × Pessoa'), state='readonly')
    selector.grid(row=0, column=0, columnspan=3, sticky='ew')
    selector.bind('<<ComboboxSelected>>', reset)
    buttons = []
    for i in range(9):
        button = tk.Button(root, width=6, height=3, font=('Arial', 22), command=lambda i=i: play(i))
        button.grid(row=1 + i // 3, column=i % 3)
        buttons.append(button)
    ttk.Label(root, textvariable=status).grid(row=4, column=0, columnspan=3)
    ttk.Button(root, text='Reiniciar', command=reset).grid(row=5, column=0, columnspan=3)
    render()
    root.mainloop()
