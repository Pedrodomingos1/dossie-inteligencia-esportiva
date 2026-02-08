def calcular_valor_esperado(probabilidade_estimada, odd_casa, valor_apostado=1.0):
    """
    Calcula o Valor Esperado (EV) de uma aposta.

    Fórmula: EV = (Probabilidade * Lucro) - (Probabilidade de Perda * Valor Apostado)

    Args:
        probabilidade_estimada (float): Probabilidade de vencer (0.0 a 1.0).
        odd_casa (float): Odd oferecida pela casa de apostas (decimal).
        valor_apostado (float): Valor da aposta (padrão 1.0 unidade).

    Returns:
        float: O valor esperado da aposta.
    """
    lucro_potencial = (odd_casa - 1) * valor_apostado
    probabilidade_perda = 1.0 - probabilidade_estimada

    ev = (probabilidade_estimada * lucro_potencial) - (probabilidade_perda * valor_apostado)
    return ev
