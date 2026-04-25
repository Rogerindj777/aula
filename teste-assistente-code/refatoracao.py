from typing import Sequence, Tuple


def calcular_estatisticas(numeros: Sequence[int]) -> Tuple[int, float, int, int]:
    """Calcula soma, média, maior e menor valor de uma lista de números."""
    if not numeros:
        raise ValueError("A lista de números não pode ser vazia")

    total = sum(numeros)
    media = total / len(numeros)
    maior_valor = max(numeros)
    menor_valor = min(numeros)

    return total, media, maior_valor, menor_valor


def main() -> None:
    valores = [23, 7, 45, 2, 67, 12, 89, 34, 56, 11]
    total, media, maior, menor = calcular_estatisticas(valores)

    print("total:", total)
    print("media:", media)
    print("maior:", maior)
    print("menor:", menor)


if __name__ == "__main__":
    main()
