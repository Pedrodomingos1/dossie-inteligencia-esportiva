from scraper import buscar_jogos_do_dia, buscar_estatisticas_jogo
import json

def verificar_coletor():
    print("Testando buscar_jogos_do_dia()...")
    jogos = buscar_jogos_do_dia()
    print(f"Jogos encontrados: {len(jogos)}")
    if jogos:
        print(f"Primeiro jogo: {jogos[0]}")
        id_evento = jogos[0]['id']
        print(f"\nTestando buscar_estatisticas_jogo({id_evento})...")
        estatisticas = buscar_estatisticas_jogo(id_evento)
        if estatisticas:
             print("Estatísticas recuperadas com sucesso.")
             # print(json.dumps(estatisticas, indent=2))
        else:
             print("Falha ao recuperar estatísticas ou nenhuma estatística disponível ainda.")
    else:
        print("Nenhum jogo encontrado para hoje.")

if __name__ == "__main__":
    verificar_coletor()
