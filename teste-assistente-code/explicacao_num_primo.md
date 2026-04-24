# Explicação da Função eh_primo()

## O que é um Número Primo?

Um número primo é um número natural maior que 1 que possui apenas dois divisores: 1 e ele mesmo.

**Exemplos:**
- 2, 3, 5, 7, 11, 13, 17, 19 são primos
- 4, 6, 8, 9, 10, 12 NÃO são primos (possuem outros divisores)

---

## Análise do Código

### Definição da Função

```python
def eh_primo(numero):
```
Define uma função chamada `eh_primo` que recebe um parâmetro `numero` (o número a ser verificado).

### Verificação 1: Números Menores que 2

```python
if numero < 2:
    return False
```
- Números menores que 2 (negativos, 0 e 1) NÃO são primos
- Retorna `False` imediatamente

### Verificação 2: O Número 2

```python
if numero == 2:
    return True
```
- 2 é o único número par que é primo
- Retorna `True`

### Verificação 3: Números Pares

```python
if numero % 2 == 0:
    return False
```
- Se o número é divisível por 2 (resto 0), não é primo
- Todos os pares maiores que 2 têm 2 como divisor
- Retorna `False`

### Verificação 4: Divisibilidade por Números Ímpares

```python
for i in range(3, int(numero**0.5) + 1, 2):
    if numero % i == 0:
        return False
```

**Como funciona:**
- `range(3, int(numero**0.5) + 1, 2)` gera números ímpares de 3 até a raiz quadrada do número
- `numero**0.5` calcula a raiz quadrada
- O passo `2` garante que verificamos apenas números ímpares (3, 5, 7, 9...)

**Por que até a raiz quadrada?**
- Se um número não é primo, ele tem um divisor ≤ sua raiz quadrada
- Exemplo: 36 = 6 × 6, então não precisamos verificar além de 6

- Se encontrar um divisor, retorna `False`
- Se nenhum divisor for encontrado, o número é primo

### Retorno Final

```python
return True
```
- Se passou por todas as verificações, o número é primo

---

## Exemplos de Execução

| Número | Resultado | Motivo |
|--------|-----------|--------|
| 2 | Primo ✓ | Único número par primo |
| 3 | Primo ✓ | Divisível apenas por 1 e 3 |
| 4 | Não primo ✗ | Divisível por 2 |
| 5 | Primo ✓ | Divisível apenas por 1 e 5 |
| 10 | Não primo ✗ | Divisível por 2, 5 |
| 17 | Primo ✓ | Divisível apenas por 1 e 17 |
| 29 | Primo ✓ | Divisível apenas por 1 e 29 |
| 100 | Não primo ✗ | Divisível por 2, 5, 10, 20, 25, 50 |

---

## Complexidade

- **Melhor caso:** O(1) - quando o número é par ou menor que 2
- **Pior caso:** O(√n) - quando precisamos verificar todos os números ímpares até a raiz quadrada
- **Espaço:** O(1) - não usa estruturas de dados adicionais

---

## Como Usar

```python
# Verificar se 17 é primo
eh_primo(17)  # Retorna: True

# Verificar se 20 é primo
eh_primo(20)  # Retorna: False
```
