# Explicação da Função eh_primo()

## O que é um Número Primo?

Um número primo é um número natural maior que 1 que possui apenas dois divisores: 1 e ele mesmo.

**Exemplos:**
- 2, 3, 5, 7, 11, 13, 17, 19 são primos
- 4, 6, 8, 9, 10, 12 NÃO são primos (possuem outros divisores)

---

## Estrutura do Código

O código foi organizado para ficar mais limpo e fácil de entender:

- `eh_primo(numero: int) -> bool` retorna `True` ou `False`
- `main()` contém os exemplos de uso
- `if __name__ == "__main__":` mantém a execução do código apenas quando o arquivo é executado diretamente

---

## Passo a Passo da Função

### 1. Validação inicial

```python
if numero < 2:
    return False
```

- Números menores que 2 não são primos

### 2. Caso especial do número 2

```python
if numero == 2:
    return True
```

- 2 é o único número par que é primo

### 3. Eliminar pares maiores que 2

```python
if numero % 2 == 0:
    return False
```

- Todos os pares maiores que 2 têm pelo menos o divisor 2

### 4. Verificar divisores ímpares até a raiz quadrada

```python
limite = int(numero**0.5) + 1
for divisor in range(3, limite, 2):
    if numero % divisor == 0:
        return False
```

- O código calcula um `limite` claro e usa apenas números ímpares
- Isso melhora a legibilidade e evita repetição de lógica no loop

---

## Por que este código é mais limpo?

- Usa nomes de variáveis descritivos: `numero`, `limite`, `divisor`
- Separa a lógica principal da execução de exemplo em `main()`
- Adiciona tipagem `int` e `bool` para facilitar leitura e manutenção
- Mantém o comportamento igual ao original

---

## Exemplos de execução

| Número | Resultado | Motivo |
|--------|-----------|--------|
| 2 | Primo ✓ | Único número par primo |
| 3 | Primo ✓ | Não tem divisores além de 1 e 3 |
| 4 | Não primo ✗ | Divisível por 2 |
| 5 | Primo ✓ | Não tem divisores além de 1 e 5 |
| 10 | Não primo ✗ | Divisível por 2 |
| 17 | Primo ✓ | Não tem divisores além de 1 e 17 |
| 29 | Primo ✓ | Não tem divisores além de 1 e 29 |
| 100 | Não primo ✗ | Divisível por 2 e 5 |

---

## Complexidade

- **Tempo:** O(√n) no pior caso
- **Espaço:** O(1)

---

## Como usar

```python
from teste_assistente_code.num_primos import eh_primo

print(eh_primo(17))  # True
print(eh_primo(20))  # False
```
