def text_generate_for_embedding(tinta):
    return f"""
    Tinta {tinta.nome}. {tinta.descricao or ''}. Cor: {tinta.cor}.
    Tipo: {tinta.tipo_tinta}. Superfície: {tinta.superficie}. Ambiente: {tinta.ambiente}.
    Acabamento: {tinta.acabamento}. Linha: {tinta.linha}. Odor: {tinta.nivel_odor}.
    Lavável: {'Sim' if tinta.lavavel else 'Não'}. Anti-mofo: {'Sim' if tinta.anti_mofo else 'Não'}.
    """.strip()
