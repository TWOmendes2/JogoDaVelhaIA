# Jogo da Velha v2

Estudo de decisões adversariais com Python: domínio imutável, Minimax/Negamax com
poda alpha-beta e tabela de transposição, interface Tkinter com reinício e dois modos.

## Executar

Python 3.11+ com Tkinter. Não há dependências externas.

```sh
python -m tictactoe
python -m unittest discover -s tests -v
```

`python JogoDaVelhaIA.py` continua como atalho. X começa; no modo IA a pessoa joga X.

## Arquitetura

- `domain.py`: estado imutável, validação, turnos, movimentos e resultado.
- `ai.py`: busca determinística, ordenação centro/cantos e cache de limites.
- `ui.py`: apresentação e interação; nenhuma regra de vitória ou busca duplicada.

A tabela distingue valores exatos de limites inferior/superior produzidos por poda;
tratar todo retorno podado como exato causaria decisões erradas. Pontuação é vitória,
empate ou derrota, sem preferência por vencer mais cedo.

## Evidência

A suíte compara todas as 5.478 posições alcançáveis com um solver sem poda e percorre
todas as respostas adversárias contra a IA como X e O. Também verifica imutabilidade,
jogadas ilegais e estados inválidos. A UI requer verificação manual em sessão gráfica.

## Evolução

Versão 2.0.0: nova API de domínio; o script de entrada foi preservado. A implementação
original permanece no histórico Git. Consulte [CHANGELOG](CHANGELOG.md).
