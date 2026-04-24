from typing import List


def eh_primo(numero: int) -> bool:
    """Retorna True se o número for primo, caso contrário False."""
    if numero < 2:
        return False
    if numero == 2:
        return True
    if numero % 2 == 0:
        return False

    limite = int(numero**0.5) + 1
    for divisor in range(3, limite, 2):
        if numero % divisor == 0:
            return False

    return True


def main() -> None:
    numeros_teste: List[int] = [2, 3, 4, 5, 10, 17, 20, 29, 100]

    for numero in numeros_teste:
        resultado = "primo" if eh_primo(numero) else "não primo"
        print(f"{numero} é {resultado}")


if __name__ == "__main__":
    main()
