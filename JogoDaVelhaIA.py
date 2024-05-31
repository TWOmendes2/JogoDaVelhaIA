import tkinter as tk
import random

class EstadoJogoDaVelha:
    def __init__(self, tabuleiro=None, jogador_atual='X'):
        self.tabuleiro = tabuleiro if tabuleiro else [[' ']*3 for _ in range(3)]
        self.jogador_atual = jogador_atual

    def acoes_possiveis(self):
        return [(i, j) for i in range(3) for j in range(3) if self.tabuleiro[i][j] == ' ']

    def transicao(self, acao):
        novo_tabuleiro = [linha[:] for linha in self.tabuleiro]
        i, j = acao
        novo_tabuleiro[i][j] = self.jogador_atual
        proximo_jogador = 'O' if self.jogador_atual == 'X' else 'X'
        return EstadoJogoDaVelha(novo_tabuleiro, proximo_jogador)

    def teste_objetivo(self):
        for i in range(3):
            if self.tabuleiro[i][0] == self.tabuleiro[i][1] == self.tabuleiro[i][2] != ' ':
                return self.tabuleiro[i][0]
            if self.tabuleiro[0][i] == self.tabuleiro[1][i] == self.tabuleiro[2][i] != ' ':
                return self.tabuleiro[0][i]
        if self.tabuleiro[0][0] == self.tabuleiro[1][1] == self.tabuleiro[2][2] != ' ':
            return self.tabuleiro[0][0]
        if self.tabuleiro[0][2] == self.tabuleiro[1][1] == self.tabuleiro[2][0] != ' ':
            return self.tabuleiro[0][2]
        if all(self.tabuleiro[i][j] != ' ' for i in range(3) for j in range(3)):
            return 'Empate'
        return None

class JogoDaVelhaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Velha")

        self.tabuleiro = [[' ']*3 for _ in range(3)]
        self.jogador_atual = 'X'

        self.botoes = [[None]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.botoes[i][j] = tk.Button(root, text=' ', font=('Helvetica', 20), width=5, height=2,
                                               command=lambda row=i, col=j: self.realizar_jogada(row, col))
                self.botoes[i][j].grid(row=i, column=j)

    def realizar_jogada(self, row, col):
        if self.tabuleiro[row][col] == ' ':
            self.tabuleiro[row][col] = self.jogador_atual
            self.botoes[row][col].config(text=self.jogador_atual)
            if self.verificar_vitoria() or self.verificar_empate():
                self.root.quit()
            else:
                self.jogador_atual = 'O' if self.jogador_atual == 'X' else 'X'
                if self.jogador_atual == 'O':
                    self.jogada_ia()

    def jogada_ia(self):
        melhor_jogada = self.minimax(EstadoJogoDaVelha(self.tabuleiro, 'O'), True)[1]
        if melhor_jogada:
            row, col = melhor_jogada
            self.tabuleiro[row][col] = 'O'
            self.botoes[row][col].config(text='O')
            if self.verificar_vitoria() or self.verificar_empate():
                self.root.quit()
            else:
                self.jogador_atual = 'X'

    def verificar_vitoria(self):
        for i in range(3):
            if self.tabuleiro[i][0] == self.tabuleiro[i][1] == self.tabuleiro[i][2] != ' ':
                self.mostrar_vencedor(self.tabuleiro[i][0])
                return True
            if self.tabuleiro[0][i] == self.tabuleiro[1][i] == self.tabuleiro[2][i] != ' ':
                self.mostrar_vencedor(self.tabuleiro[0][i])
                return True
        if self.tabuleiro[0][0] == self.tabuleiro[1][1] == self.tabuleiro[2][2] != ' ':
            self.mostrar_vencedor(self.tabuleiro[0][0])
            return True
        if self.tabuleiro[0][2] == self.tabuleiro[1][1] == self.tabuleiro[2][0] != ' ':
            self.mostrar_vencedor(self.tabuleiro[0][2])
            return True
        return False

    def verificar_empate(self):
        if all(self.tabuleiro[i][j] != ' ' for i in range(3) for j in range(3)):
            self.mostrar_empate()
            return True
        return False

    def mostrar_vencedor(self, jogador):
        tk.messagebox.showinfo("Fim de jogo", f"O jogador '{jogador}' venceu!")
    
    def mostrar_empate(self):
        tk.messagebox.showinfo("Fim de jogo", "O jogo terminou em empate.")

    def minimax(self, estado, maximizando):
        resultado = estado.teste_objetivo()
        if resultado == 'X':
            return -1, None
        elif resultado == 'O':
            return 1, None
        elif resultado == 'Empate':
            return 0, None

        if maximizando:
            melhor_valor = -float('inf')
            melhor_jogada = None
            for acao in estado.acoes_possiveis():
                valor, _ = self.minimax(estado.transicao(acao), False)
                if valor > melhor_valor:
                    melhor_valor = valor
                    melhor_jogada = acao
            return melhor_valor, melhor_jogada
        else:
            pior_valor = float('inf')
            pior_jogada = None
            for acao in estado.acoes_possiveis():
                valor, _ = self.minimax(estado.transicao(acao), True)
                if valor < pior_valor:
                    pior_valor = valor
                    pior_jogada = acao
            return pior_valor, pior_jogada

# Iniciar o jogo
root = tk.Tk()
app = JogoDaVelhaGUI(root)
root.mainloop()
