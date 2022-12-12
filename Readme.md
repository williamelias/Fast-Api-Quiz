# Desafio Backend - fast api

Esse projeto se baseia em um desafio encontrado em <link>, com o diferencial de ser feito com Fast API.

## Informações do servidor

Url base (base_url): http://localhost:8082

-> Para executar 
    make stop
    make build
    make start

- acesso: base_url

-> Visualizar documentação - gerada automaticamente

    ->  base_url/docs (swagger)
    ->  base_url/redoc (redoc)

## Sobre a aplicação

A aplicação deverá prover o registro e autenticação de dois tipos de usuários:
- Admin
- Player

Cada quiz é composto por:

- 10 perguntas com 3 respostas onde apenas 1 é correta.
- Cada resposta correta acumula a 1 ponto.
- Cada resposta errada perde 1 ponto. A menor pontuação possível é 0.
- Uma categoria.

Ao iniciar o jogo:

- O player deve escolher uma categoria válida e receber um quiz com perguntas aleatórias referentes a categoria escolhida.

Ao finalizar o jogo:

- O player deve receber a contabilização dos seus pontos juntamente com a sua posição atual no ranking global. Não há limitação de quantos quizzes o player pode responder.

O ranking:

- É a contabilização dos pontos acumulados por cada player.
- Ranking geral considera todas as categorias.
- Ranking por categoria agrupa por categorias.
- Este requisito é desejável mas não obrigatório.

Permissões:

- Todos os endpoints devem estar protegidos por autenticação.
- Usuários do tipo Admin tem permissão para criar perguntas e respostas para os quizzes.
- Usuários do tipo Player tem permissão para jogar e consultar o ranking.


## Informações extras

Visualize aqui: ![notas](notes.md)