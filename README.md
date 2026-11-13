# Trabalho 02 — Grafos Biconexos no Jiu-Jitsu

> **Instituto Federal do Espírito Santo (IFES) — Campus Cachoeiro de Itapemirim**  
> **Curso:** Bacharelado em Sistemas de Informação  
> **Disciplina:** Técnicas de Programação Avançada (TPA)  
> **Professor:** Rafael Vargas Mesquita  
> **Autores:** Nadson da Cruz Silva & José Carlos Ceccon  

---

## 📌 Sobre o Projeto

Este projeto aborda o desafio de **Grafos Biconexos e Pontos de Articulação** (Capítulo de Grafos / Sedgewick). O objetivo prático é identificar "membros de corte" (gargalos humanos) em uma rede de treinos de uma academia de Jiu-Jitsu, onde a ausência de um único praticante pode desconectar duas turmas independentes (manhã e noite).

O problema é resolvido com o **Algoritmo de Tarjan (1972)**, utilizando Busca em Profundidade (DFS) com cálculo dos tempos de descoberta (`desc[u]`) e low-link (`low[u]`), atingindo complexidade linear ótima $\mathcal{O}(V + E)$.

---

## 📂 Artefatos do Trabalho

Conforme exigido nas diretrizes do trabalho, todos os 6 artefatos foram desenvolvidos:

1. **Algoritmo Implementado:** [`jiu-jitsu/algoritmo_biconexo.py`](jiu-jitsu/algoritmo_biconexo.py) — Código Python modular com leitura de arquivos `.txt`, DFS de Tarjan, identificação de articulações e simulação de desconexão via BFS.
2. **Aplicação com Visualização Interativa:** [`jiu-jitsu/apresentacao.html`](jiu-jitsu/apresentacao.html) — Deck interativo com nós SVG dinâmicos, controle passo a passo da DFS e botão de simulação de remoção de nó.
3. **Apresentação Oral (18 a 20 minutos):** Roteiro sincronizado em [`jiu-jitsu/roteiro.txt`](jiu-jitsu/roteiro.txt), dividido entre Nadson e José Carlos.
4. **Arquivos de Grafo (.txt):**
   - [`jiu-jitsu/grafo_original.txt`](jiu-jitsu/grafo_original.txt) — 5 vértices, 6 arestas (Vulnerável: articulação $J03$).
   - [`jiu-jitsu/grafo_biconexo.txt`](jiu-jitsu/grafo_biconexo.txt) — 5 vértices, 7 arestas (Resiliente: aresta $J02-J04$ adicionada).
5. **Planilha de Teste de Mesa:** [`jiu-jitsu/teste_de_mesa_biconexo.xlsx`](jiu-jitsu/teste_de_mesa_biconexo.xlsx) — Tabela com o rastreamento linha a linha dos vetores `desc` e `low`, destacando a avaliação da condição $low[v] \ge desc[u]$.
6. **Imagens Conceituais de IA:**
   - [`jiu-jitsu/img_jiu_jitsu_grafo.jpg`](jiu-jitsu/img_jiu_jitsu_grafo.jpg) — Representação artística de nós de grafos sobre o tatame de treino.
   - [`jiu-jitsu/img_redes_resilientes.jpg`](jiu-jitsu/img_redes_resilientes.jpg) — Topologia de infraestrutura de rede resiliente com caminhos duplos disjuntos.

---

## 🚀 Como Executar

### 1. Executar o Algoritmo no Terminal
```bash
python jiu-jitsu/algoritmo_biconexo.py
```

### 2. Abrir a Apresentação Interativa
Abra o arquivo [`jiu-jitsu/apresentacao.html`](jiu-jitsu/apresentacao.html) em qualquer navegador moderno.  
- Use as teclas `←` e `→` ou `Espaço` para avançar e retroceder os slides.
- No **Slide 5**, utilize os botões interativos (*Próximo*, *Anterior*, *Auto*) para visualizar a DFS.
- No **Slide 10**, utilize os botões *Remover J03* e *Restaurar* para ver a simulação prática da desconexão.

### 3. Visualizar o Teste de Mesa
Abra o arquivo [`jiu-jitsu/teste_de_mesa_biconexo.xlsx`](jiu-jitsu/teste_de_mesa_biconexo.xlsx) no Excel ou LibreOffice Calc.

---

## 📊 Tabela de Complexidade (Padrão Sedgewick)

| Algoritmo | Restrição | Caso Típico | Pior Caso | Espaço Extra |
| :--- | :--- | :---: | :---: | :---: |
| **Tarjan (DFS + Low-Link)** | Grafo não-dirigido conexo | $\mathcal{O}(V + E)$ | $\mathcal{O}(V + E)$ | $\mathcal{O}(V)$ |
| **Força Bruta** | Testa remoção de cada vértice via BFS | $\mathcal{O}(V \cdot (V + E))$ | $\mathcal{O}(V \cdot (V + E))$ | $\mathcal{O}(V)$ |
