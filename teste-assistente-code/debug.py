# CÓDIGO AJUSTADO

from typing import Sequence


def ler_valores_produtos() -> Sequence[float]:
    """Lê a quantidade e o preço de três produtos do usuário."""
    valores = []

    for numero_item in range(1, 4):
        quantidade = int(input(f"Quantidade do item {numero_item}: "))
        preco = float(input(f"Preço do item {numero_item}: "))
        valores.append(quantidade * preco)

    return valores


def aplicar_desconto(subtotal: float) -> float:
    """Lê o cupom de desconto e calcula o valor do desconto."""
    desconto_percentual = float(input("Você tem um cupom de desconto? (Digite o percentual ou 0): "))
    return subtotal * (desconto_percentual / 100), desconto_percentual


def imprimir_relatorio(cliente: str, totais: Sequence[float], subtotal: float, imposto: float, desconto: float, desconto_percentual: float) -> None:
    """Imprime o relatório com os valores calculados."""
    linha = "=" * 31
    separador = "-" * 31

    print(linha)
    print(f" Cliente: {cliente}")
    print(linha)
    for index, total_item in enumerate(totais, start=1):
        print(f" Item {index}:        R$ {total_item:.2f}")
    print(separador)
    print(f" Subtotal:      R$ {subtotal:.2f}")
    print(f" Imposto (10%): R$ {imposto:.2f}")

    if desconto > 0:
        print(f" Desconto ({desconto_percentual:.0f}%): -R$ {desconto:.2f}")

    total = subtotal + imposto - desconto
    print(linha)
    print(f" TOTAL:         R$ {total:.2f}")
    print(linha)


def main() -> None:
    cliente = input("Qual é seu nome? ")
    totais_itens = ler_valores_produtos()
    subtotal = sum(totais_itens)
    imposto = subtotal * 0.10
    desconto, desconto_percentual = aplicar_desconto(subtotal)

    imprimir_relatorio(cliente, totais_itens, subtotal, imposto, desconto, desconto_percentual)


if __name__ == "__main__":
    main()
