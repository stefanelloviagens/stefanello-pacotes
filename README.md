# Pacotes Stefanello Viagens

Site estático de pacotes publicado em https://pacotes.stefanelloviagens.com.br

- `pacotes.json`: dados de cada pacote (o Claude atualiza este arquivo).
- `build.py`: gera `index.html` e uma página por pacote (`<slug>.html`). Pacotes com data de ida passada saem sozinhos.
- `img/`: artes dos posts.

Deploy automático pela Vercel a cada commit na branch `main`.
