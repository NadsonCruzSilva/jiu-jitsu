"""
algoritmo_biconexo.py
=====================
Implementação do algoritmo de identificação de articulações (pontos de articulação)
e verificação de biconexidade em grafos, aplicado ao contexto de um clube de jiu-jitsu.

Algoritmo: DFS com descoberta e low-link (Tarjan, 1972)
Complexidade: O(V + E)

Contexto:
  - Vértices: alunos/professores (J01, J02, J03, J04, J05)
  - Arestas: treinaram juntos >= 3 sessões no mês
  - Objetivo: identificar "pontos de dependência" (articulações) na rede de treino
"""

from collections import defaultdict


class Grafo:
    """
    Representa um grafo não-dirigido com listas de adjacência.
    Suporta rótulos de vértices (strings como 'J01', 'J02', etc.).
    """

    def __init__(self):
        """Inicializa o grafo vazio."""
        # Lista de adjacência: dicionário {vértice: [vizinhos]}
        self.adj = defaultdict(list)
        # Lista de todos os vértices
        self.vertices = []
        # Lista de todas as arestas (pares)
        self.arestas = []
        # Número de vértices
        self.num_vertices = 0

    def carregar_txt(self, arquivo):
        """
        Carrega o grafo a partir de um arquivo .txt.

        Formato do arquivo:
          Linha 1: número de vértices (inteiro)
          Linhas seguintes: pares de rótulos separados por espaço (ex: 'J01 J02')

        Args:
            arquivo (str): caminho para o arquivo .txt
        """
        self.adj = defaultdict(list)
        self.vertices = []
        self.arestas = []

        with open(arquivo, 'r', encoding='utf-8') as f:
            linhas = [l.strip() for l in f if l.strip()]

        # Primeira linha: número de vértices
        self.num_vertices = int(linhas[0])

        # Restante: arestas
        vertices_set = set()
        for linha in linhas[1:]:
            partes = linha.split()
            if len(partes) == 2:
                u, v = partes[0], partes[1]
                # Adiciona aresta em ambas as direções (grafo não-dirigido)
                self.adj[u].append(v)
                self.adj[v].append(u)
                self.arestas.append((u, v))
                vertices_set.add(u)
                vertices_set.add(v)

        # Mantém ordem de inserção dos vértices (aparecem nas arestas)
        # para consistência no trace da DFS
        seen = set()
        self.vertices = []
        for linha in linhas[1:]:
            for v in linha.split():
                if v not in seen:
                    self.vertices.append(v)
                    seen.add(v)

        print(f"  Grafo carregado: {len(self.vertices)} vértices, {len(self.arestas)} arestas")
        print(f"  Vértices: {self.vertices}")
        print(f"  Arestas:  {self.arestas}")

    def dfs_articulacoes(self):
        """
        Implementa DFS com low-link para identificar articulações.

        Conceito:
          - descoberta[u]: tempo de descoberta do vértice u na DFS
          - low[u]: menor tempo de descoberta alcançável a partir da subárvore de u
                    (incluindo arestas de retorno)
          - Um vértice u NÃO-RAIZ é articulação se existe filho v na árvore DFS
            com low[v] >= descoberta[u]  (v não pode "escapar" de u por aresta de retorno)
          - A RAIZ da DFS é articulação se tiver >= 2 filhos na árvore DFS

        Returns:
            tuple: (articulacoes, passos)
              - articulacoes: set com vértices articulação
              - passos: lista de dicts com o trace passo a passo
        """
        # Inicializa estruturas
        descoberta = {}   # tempo de descoberta
        low = {}          # low-link
        pai = {}          # pai na árvore DFS
        visitado = set()  # vértices já visitados
        articulacoes = set()
        passos = []       # registro passo a passo para o teste de mesa
        self.contador_tempo = [0]  # uso de lista para mutabilidade em closures
        self.contador_passo = [0]

        def registrar(acao, vertice, pai_v, desc_v, low_v, art=""):
            """Registra um passo no trace da DFS."""
            self.contador_passo[0] += 1
            passos.append({
                'passo': self.contador_passo[0],
                'acao': acao,
                'vertice': vertice,
                'pai': pai_v if pai_v is not None else '-',
                'desc': desc_v,
                'low': low_v,
                'articulacao': art
            })

        def dfs(u, pai_u):
            """
            Função recursiva de DFS.

            Args:
                u (str): vértice atual
                pai_u (str ou None): pai de u na árvore DFS
            """
            visitado.add(u)
            descoberta[u] = self.contador_tempo[0]
            low[u] = self.contador_tempo[0]
            self.contador_tempo[0] += 1
            filhos_dfs = 0  # conta filhos na ÁRVORE DFS (não todos os vizinhos)

            # Registra visita ao vértice
            registrar(
                acao="Visitar",
                vertice=u,
                pai_v=pai_u,
                desc_v=descoberta[u],
                low_v=low[u]
            )

            for v in self.adj[u]:
                if v not in visitado:
                    # v é filho de u na árvore DFS
                    filhos_dfs += 1
                    pai[v] = u
                    dfs(v, u)

                    # Atualiza low[u] com base no retorno de v
                    low[u] = min(low[u], low[v])

                    # Verifica condição de articulação para NÃO-RAIZ
                    # u é articulação se low[v] >= descoberta[u]
                    if pai_u is not None and low[v] >= descoberta[u]:
                        articulacoes.add(u)
                        registrar(
                            acao=f"Retorno {v}→{u}",
                            vertice=u,
                            pai_v=pai_u,
                            desc_v=descoberta[u],
                            low_v=low[u],
                            art=f"✓ {u} é ARTICULAÇÃO (low[{v}]={low[v]} >= desc[{u}]={descoberta[u]})"
                        )
                    else:
                        registrar(
                            acao=f"Retorno {v}→{u}",
                            vertice=u,
                            pai_v=pai_u,
                            desc_v=descoberta[u],
                            low_v=low[u],
                            art=f"low[{v}]={low[v]}, desc[{u}]={descoberta[u]}"
                        )

                elif v != pai_u:
                    # v já foi visitado e não é o pai → aresta de retorno
                    # Atualiza low[u] com descoberta de v
                    low[u] = min(low[u], descoberta[v])
                    registrar(
                        acao=f"Aresta retorno {u}→{v}",
                        vertice=u,
                        pai_v=pai_u,
                        desc_v=descoberta[u],
                        low_v=low[u],
                        art=f"low[{u}] = min(low[{u}], desc[{v}]) = {low[u]}"
                    )

            # Verifica condição de articulação para a RAIZ
            if pai_u is None and filhos_dfs > 1:
                articulacoes.add(u)
                registrar(
                    acao="Raiz com múltiplos filhos",
                    vertice=u,
                    pai_v=None,
                    desc_v=descoberta[u],
                    low_v=low[u],
                    art=f"✓ {u} é ARTICULAÇÃO (raiz com {filhos_dfs} filhos)"
                )

        # Executa DFS a partir do primeiro vértice
        raiz = self.vertices[0]
        dfs(raiz, None)

        # Trata grafos desconexos (DFS a partir de outras componentes)
        for v in self.vertices:
            if v not in visitado:
                dfs(v, None)

        return articulacoes, passos

    def eh_biconexo(self):
        """
        Verifica se o grafo é biconexo.

        Um grafo é biconexo se:
          1. É conexo (apenas uma componente conexa)
          2. Não possui articulações (pontos de articulação)
          3. Possui pelo menos 3 vértices (por definição)

        Returns:
            tuple: (bool, articulacoes, passos)
              - bool: True se biconexo, False caso contrário
              - articulacoes: set com articulações encontradas
              - passos: trace da DFS
        """
        articulacoes, passos = self.dfs_articulacoes()

        # Verifica conectividade: todos os vértices foram alcançados pela DFS
        # (já garantido pelo método dfs_articulacoes com tratamento de desconexo)
        # Verificação simples: existe algum componente?
        if len(self.vertices) < 3:
            return False, articulacoes, passos

        biconexo = (len(articulacoes) == 0)
        return biconexo, articulacoes, passos

    def simular_remocao(self, vertice):
        """
        Simula a remoção de um vértice e verifica se o grafo permanece conexo.

        Args:
            vertice (str): rótulo do vértice a remover

        Returns:
            tuple: (ainda_conexo, componentes)
              - ainda_conexo: True se o grafo sem 'vertice' ainda é conexo
              - componentes: lista de conjuntos com as componentes conexas
        """
        if vertice not in self.vertices:
            print(f"  Vértice '{vertice}' não encontrado no grafo.")
            return True, []

        # Vértices restantes após remoção
        vertices_restantes = [v for v in self.vertices if v != vertice]

        if not vertices_restantes:
            return True, []

        # BFS/DFS nos vértices restantes para encontrar componentes conexas
        visitado = set()
        componentes = []

        def bfs(inicio):
            """BFS a partir de 'inicio', ignorando 'vertice' removido."""
            componente = set()
            fila = [inicio]
            visitado.add(inicio)
            componente.add(inicio)
            while fila:
                u = fila.pop(0)
                for v in self.adj[u]:
                    if v not in visitado and v != vertice:
                        visitado.add(v)
                        componente.add(v)
                        fila.append(v)
            return componente

        for v in vertices_restantes:
            if v not in visitado:
                comp = bfs(v)
                componentes.append(comp)

        ainda_conexo = (len(componentes) == 1)
        return ainda_conexo, componentes


def imprimir_tabela_dfs(passos):
    """
    Imprime os passos da DFS em formato de tabela no console.

    Args:
        passos (list): lista de dicts com os campos do trace
    """
    sep = "─" * 110
    cab = f"{'PASSO':^6} │ {'AÇÃO':<28} │ {'VÉRTICE':^8} │ {'PAI':^6} │ {'DESC':^5} │ {'LOW':^5} │ ARTICULAÇÃO"
    print()
    print(sep)
    print(cab)
    print(sep)
    for p in passos:
        linha = (
            f"{p['passo']:^6} │ "
            f"{p['acao']:<28} │ "
            f"{p['vertice']:^8} │ "
            f"{str(p['pai']):^6} │ "
            f"{str(p['desc']):^5} │ "
            f"{str(p['low']):^5} │ "
            f"{p['articulacao']}"
        )
        print(linha)
    print(sep)
    print()


def main():
    """
    Função principal que demonstra o uso do algoritmo.

    Fluxo:
      1. Carrega grafo_original.txt e analisa articulações
      2. Simula remoção de J03
      3. Carrega grafo_biconexo.txt (com J02-J04) e confirma biconexidade
    """

    # =========================================================================
    # PARTE 1: GRAFO ORIGINAL
    # =========================================================================
    print("=" * 70)
    print("  CLUBE DE JIU-JITSU — ANÁLISE DE GRAFO BICONEXO")
    print("=" * 70)
    print()
    print("▶ PARTE 1: Grafo Original (grafo_original.txt)")
    print("-" * 70)

    grafo_orig = Grafo()
    grafo_orig.carregar_txt("grafo_original.txt")

    print()
    print("  Executando DFS com identificação de articulações...")
    print("  Raiz da DFS:", grafo_orig.vertices[0])

    biconexo, articulacoes, passos = grafo_orig.eh_biconexo()

    # Imprime tabela do teste de mesa
    print()
    print("  TESTE DE MESA — Trace da DFS:")
    imprimir_tabela_dfs(passos)

    # Resumo de articulações
    if articulacoes:
        print(f"  ⚠  Articulações encontradas: {sorted(articulacoes)}")
    else:
        print("  ✓  Nenhuma articulação encontrada.")

    if biconexo:
        print("  ✓  O grafo É BICONEXO.")
    else:
        print("  ✗  O grafo NÃO É BICONEXO.")

    # =========================================================================
    # PARTE 2: SIMULAÇÃO DE REMOÇÃO DE J03
    # =========================================================================
    print()
    print("▶ PARTE 2: Simulação de remoção de J03")
    print("-" * 70)

    ainda_conexo, componentes = grafo_orig.simular_remocao("J03")

    print(f"  Removendo J03 do grafo original...")
    if ainda_conexo:
        print("  ✓  O grafo permanece CONEXO após remoção de J03.")
    else:
        print("  ✗  O grafo FICOU DESCONEXO após remoção de J03.")
        print(f"  Componentes conexas formadas ({len(componentes)}):")
        for i, comp in enumerate(componentes, 1):
            print(f"    Componente {i}: {sorted(comp)}")
    print()
    print("  Interpretação prática:")
    print("  → J03 é um 'ponto de dependência': se esse membro parar de treinar,")
    print("    a rede se divide em grupos isolados que perdem contato entre si.")

    # =========================================================================
    # PARTE 3: GRAFO BICONEXO (COM ARESTA J02-J04)
    # =========================================================================
    print()
    print("▶ PARTE 3: Grafo Biconexo (grafo_biconexo.txt)")
    print("-" * 70)
    print("  Estratégia: adicionar aresta J02-J04 para eliminar a articulação J03.")
    print()

    grafo_bic = Grafo()
    grafo_bic.carregar_txt("grafo_biconexo.txt")

    print()
    print("  Executando DFS com identificação de articulações...")

    biconexo2, articulacoes2, passos2 = grafo_bic.eh_biconexo()

    print()
    print("  TESTE DE MESA — Trace da DFS (grafo biconexo):")
    imprimir_tabela_dfs(passos2)

    if articulacoes2:
        print(f"  ⚠  Articulações encontradas: {sorted(articulacoes2)}")
    else:
        print("  ✓  Nenhuma articulação encontrada.")

    if biconexo2:
        print("  ✓  O grafo É BICONEXO! Nenhum membro é ponto de dependência.")
    else:
        print("  ✗  O grafo NÃO É BICONEXO.")

    print()
    print("=" * 70)
    print("  FIM DA ANÁLISE")
    print("=" * 70)


if __name__ == "__main__":
    main()
