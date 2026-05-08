# Projeto de Exercícios em Python

Este projeto reúne três scripts em Python e documentação explicativa para exercitar leitura, correção e refatoração de código.

## Estrutura do Projeto

- `teste-assistente-code/`
  - `num_primos.py` - Função para verificar se um número é primo e exemplos de execução.
  - `refatoracao.py` - Cálculo de soma, média, maior e menor valor de uma lista de números.
  - `debug.py` - Versão ajustada de um script de cálculo de valores de itens, imposto e desconto.
  - `explicacao_num_primo.md` - Explicação detalhada do código de verificação de números primos.
  - `explicacao_refatoracao.md` - Explicação detalhada do código refatorado de estatísticas.
  - `explicacao_debug.md` - Detalhamento dos erros encontrados e correções aplicadas em `debug.py`.

## Descrição dos Arquivos

### `teste-assistente-code/num_primos.py`

- Contém a função `eh_primo(numero: int) -> bool`.
- Verifica se um número é primo de forma eficiente, usando apenas divisores ímpares até a raiz quadrada.
- Inclui um bloco `main()` com exemplos de teste para vários valores.

### `teste-assistente-code/refatoracao.py`

- Define a função `calcular_estatisticas(numeros)`.
- Calcula total, média, maior e menor valor de uma sequência de números.
- Usa `sum()`, `max()` e `min()` para melhorar legibilidade.
- Inclui `main()` para impressão dos resultados com uma lista de valores exemplo.

### `teste-assistente-code/debug.py`

- Script corrigido de um código com erros originais.
- Lê nome do cliente, quantidade e preço de três itens.
- Calcula subtotal, aplica imposto de 10% e lê cupom de desconto.
- Exibe um relatório formatado com os valores finais.

### Documentação Markdown

- `explicacao_num_primo.md` descreve linha a linha a lógica de detecção de números primos.
- `explicacao_refatoracao.md` explica a refatoração de nomenclatura e cálculo de estatísticas.
- `explicacao_debug.md` relaciona os erros originais do script e as correções aplicadas.

## Como Executar

Você pode executar cada script diretamente com o Python, a partir da raiz do projeto:

```bash
python teste-assistente-code/num_primos.py
python teste-assistente-code/refatoracao.py
python teste-assistente-code/debug.py
```

> Observação: `debug.py` pede entrada do usuário pelo terminal para quantidade, preço e cupom de desconto.

## Boas Práticas Aplicadas

- Uso de funções pequenas e claras.
- Separação entre lógica de cálculo e execução principal (`main()`).
- Nomes descritivos para variáveis e funções.
- Documentação de código e explicações em Markdown.

## Notas

Este projeto é útil para aprender:

- verificação de números primos em Python
- refatoração de código para legibilidade
- tratamento de entrada de usuário e formatação de saída
- escrita de documentação técnica em Markdown
