RDF - Formato dos dados em NT:
Na pasta utils está o ficheiro moviesDB.nt que contém os triplos usados no nosso trabalho.
Nessa pasta também está o ficheiro streamData.csv original e o programa main.py e edit.py criado por nós para converter o ficheiro CSV num ficheiro NT.

Triplestore GraphDB:
É necessário criar um novo repositório no GraphDB chamado 'moviesDB' e importar o ficheiro moviesDB.nt (diretório edcproject2/utils) e instalar as bibliotecas necessárias.

SPARQL:
Utilizámos várias queries, nomeadamente SELECTS (para listagem de filmes, series e informaçao relacionada a estes), INSERTS (para a criação de novas relações entre dados, como a atribuição de rating e de 'watched' e novas inferências) e DELETE (para remoção de dados)

Inferências:
- Ao atribuir o rating a um filme/serie, consideramos ser um bom filme se tiver um rating de 4 ou 5, mau filme se tiver 1 ou 2 e mediano se tiver 3. Pode ser visto na pagina do filme, após atribuir um rating.
- Nomeamos um ator ou diretor como popular se tiver participado ou realizado mais de 10 filmes (presentes na base de dados). Pode ser visto no separador (navbar) dos atores ou diretores.

RDFa:
Implementámos RDFa em todas as páginas que contém informação escrita, como as do filme, ator, diretor, país e categoria.
