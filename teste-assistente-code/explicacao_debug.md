# Explicação dos Erros e Correções em debug.py

## Erros identificados

1. `item1 = float(input(Preço do item 1? ))`
   - Causa: a string de prompt não estava entre aspas.
   - Resultado: erro de sintaxe ao interpretar o texto como código.

2. `desconto_cupom = (input("Você tem um cupom de desconto? (Digite o percentual ou 0): "))`
   - Erro: o valor retornado por `input()` é uma string.
   - Resultado: ao usar `desconto_cupom / 100`, ocorre um erro de tipo `TypeError`.

3. `if desconto_cupom > 0:`
   - Erro: comparação entre `str` e `int` se `desconto_cupom` não for convertido.
   - Resultado: outra fonte de `TypeError` antes de chegar à condição.

4. `print(" Item 2:        R$ {total_item2:.2f}")`
   - Erro: falta do `f` antes da string formatada.
   - Resultado: a saída imprime o texto literal com chaves, não o valor calculado.

5. Indentação incorreta no bloco `if desconto_cupom > 0:`:
   - `print(f" Desconto ({desconto_cupom:.0f}%): -R$ {desconto:.2f}")` não estava indentado.
   - Resultado: `IndentationError` ou comportamento inesperado.

## Correções aplicadas

- Corrigi a string do `input()` do preço do item 1.
- Converto o valor do cupom de desconto para `float` imediatamente.
- Separei a lógica em funções para melhorar legibilidade:
  - `ler_valores_produtos()`
  - `aplicar_desconto()`
  - `imprimir_relatorio()`
- Usei `sum()` para calcular `subtotal` e `max()`/`min()` não eram necessários aqui.
- Adicionei validação implícita com tipagem e nomes claros.

## Código ajustado

O código atualizado agora funciona corretamente e mantém a seguinte sequência:

1. Lê o nome do cliente.
2. Lê quantidade e preço de cada item.
3. Calcula o subtotal e o imposto de 10%.
4. Lê o percentual de desconto e calcula o valor do desconto.
5. Imprime o recibo com valores formatados.

## Observações de legibilidade

- Usei nomes de função e variável descritivos.
- Separei a leitura de dados, o cálculo e a exibição em funções distintas.
- Mantive a lógica de impressão em um único lugar.
- O uso de `f-strings` garante formatação correta de valores monetários.
