from datetime import datetime
import re


def validar_cpf(cpf):
    cpf = re.sub(r"\D", "", cpf)

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        raise ValueError("CPF inválido!")

    for tamanho in (9, 10):
        soma = 0

        for indice in range(tamanho):
            soma += int(cpf[indice]) * (tamanho + 1 - indice)

        digito = (soma * 10) % 11

        if digito == 10:
            digito = 0

        if digito != int(cpf[tamanho]):
            raise ValueError("CPF inválido!")

    return cpf


def validar_placa(placa):
    placa = placa.upper().replace("-", "").replace(" ", "")

    placa_antiga = r"[A-Z]{3}[0-9]{4}"
    placa_mercosul = r"[A-Z]{3}[0-9][A-Z][0-9]{2}"

    if not (
        re.fullmatch(placa_antiga, placa)
        or re.fullmatch(placa_mercosul, placa)
    ):
        raise ValueError("Placa inválida!")

    return placa


def validar_ano(ano):
    try:
        ano = int(ano)
    except (TypeError, ValueError):
        raise ValueError("Informe um ano válido!")

    ano_atual = datetime.now().year

    if ano < 1900 or ano > ano_atual:
        raise ValueError("Ano inválido!")

    return ano
