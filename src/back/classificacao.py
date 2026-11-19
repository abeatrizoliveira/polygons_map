
# Tipos de área aceitos
TIPO = ("escolar", "industrial", "residencial") # tupla -> parecida com uma lista, mas é imutável (usada para os tipos)

# validação do cadastro
def validar_tipo(tipo):
    # Aceita somente um tipo válido de área por cadastro
    if not isinstance(tipo, str) or tipo not in TIPO:
        raise ValueError(
            "Tipo inválido. Escolha escolar, industrial ou residencial."
        )

    return tipo
