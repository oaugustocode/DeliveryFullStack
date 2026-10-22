# Roadmap: Delivery Full Stack (FastAPI + React)

Marque cada item com `[x]` ao concluir. Uma fase por vez, cada feature em um branch próprio, commits pequenos.

## Regras de estudo

- Antes de olhar a solução, tente escrever sozinho.
- Ao fim de cada aula ou feature, reescreva a rota principal de memória.
- Quebre de propósito (remova um `Depends`, mande token inválido) e conserte.
- Escreva 3 a 5 linhas explicando o que cada parte faz.
- Mantenha um caderno de erros: erro, causa, solução.
- Use a IA para explicar e revisar, não para escrever tudo.

## Fase 0: Curso (Hashtag Programação, aulas 1 a 10)

- [x] Aulas 1 a 6
- [] Aula 7: Bloqueio de endpoints para usuários autenticados
- [ ] Aula 8: Níveis de acesso e lazy loading
- [ ] Aula 9: Adicionar item em pedido e relationship em models
- [ ] Aula 10: Finalização e schemas de resposta
- [ ] Teste final: criar uma rota nova (ex.: listar pedidos de um usuário) sem olhar o código do curso

## Fase 1: Fundação de qualidade

- [ ] Reorganizar em pastas: `routers/`, `models/`, `schemas/`
- [ ] Alembic: criar a primeira migração e aplicar uma mudança de model por ela
- [ ] `pytest` + `TestClient`: testar login
- [ ] Testar criação de pedido
- [ ] Testar permissões (usuário comum x admin)
- [ ] `.env.example` no repositório, `.env` no `.gitignore`

## Fase 2: Autenticação completa

- [ ] Cadastro com validações (e-mail único, senha mínima)
- [ ] Refresh token
- [ ] Expiração de token tratada com erro claro
- [ ] Desafio opcional: logout / invalidação de token

## Fase 3: Funcionalidades do delivery

- [ ] Models `Categoria` e `Produto`
- [ ] CRUD de produtos (somente admin)
- [ ] Pedido com itens ligados a produtos
- [ ] Preço total calculado no servidor
- [ ] Endereço de entrega do usuário
- [ ] Status do pedido com regras de transição (pendente, preparando, entregue, cancelado)
- [ ] Paginação e filtros nas listagens

## Fase 4: Infraestrutura

- [ ] PostgreSQL com Docker Compose
- [ ] Logs
- [ ] Tratamento global de erros
- [ ] CORS configurado para o front

## Fase 5: Front-end

- [ ] Escolher stack (React + Vite recomendado)
- [ ] Tela de login e cadastro (guardar o token)
- [ ] Cardápio
- [ ] Carrinho
- [ ] Finalizar pedido e acompanhar status
- [ ] Painel admin: lista de pedidos e troca de status

## Fase 6: Deploy e portfólio

- [ ] Deploy do back-end (Render ou Railway)
- [ ] Deploy do front-end (Vercel ou Netlify)
- [ ] README com prints e instruções para rodar
- [ ] Diagrama simples do banco de dados

## Padrão de commits

Formato: `tipo: descrição curta no imperativo`

| Tipo | Uso |
|---|---|
| `feat` | nova funcionalidade |
| `fix` | correção de bug |
| `refactor` | reorganização sem mudar comportamento |
| `config` | configuração, variáveis, dependências |
| `test` | testes |
| `docs` | documentação |

Exemplo: `feat: aula 7 - protege rotas de pedido com token`
