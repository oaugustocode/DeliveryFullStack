# Roadmap: Delivery Full Stack (FastAPI + React + Stripe + Clerk + Resend)

Marque cada item com `[x]` ao concluir. Uma fase por vez, cada feature em um branch próprio, commits pequenos.

## Visão do projeto

Aplicação de delivery full stack. O cliente vê o cardápio, monta o carrinho, paga online e acompanha o pedido. O admin gerencia produtos e o status dos pedidos.

| Peça | Tecnologia | Papel |
|---|---|---|
| API | FastAPI + SQLAlchemy + Alembic | Regras de negócio, pedidos, produtos |
| Banco | SQLite (dev) → PostgreSQL | Persistência |
| Pagamentos | **Stripe** (Checkout + webhooks) | Cobrar o pedido e confirmar o pagamento |
| Autenticação / SSO | **Clerk** | Login, cadastro e login social no front; a API valida o token do Clerk |
| E-mails | **Resend** | Confirmação de pedido, pagamento e mudança de status |
| Front-end | React + Vite | Cardápio, carrinho, acompanhamento, painel admin |

Fluxo completo do pedido:

```
carrinho → POST /pedidos (preço calculado no servidor) → Stripe Checkout
        → webhook checkout.session.completed → pedido PAGO → e-mail (Resend)
        → admin: PREPARANDO → SAIU_PARA_ENTREGA → ENTREGUE → e-mail a cada etapa
```

## Regras de estudo

- Antes de olhar a solução, tente escrever sozinho.
- Ao fim de cada aula ou feature, reescreva a rota principal de memória.
- Quebre de propósito (remova um `Depends`, mande token inválido) e conserte.
- Escreva 3 a 5 linhas explicando o que cada parte faz.
- Mantenha um caderno de erros: erro, causa, solução.
- Use a IA para explicar e revisar, não para escrever tudo.

## Fase 0: Curso (Hashtag Programação, aulas 1 a 10)

- [x] Aulas 1 a 6
- [x] Aula 7: Bloqueio de endpoints para usuários autenticados
- [x] Aula 8: Níveis de acesso e lazy loading
- [x] Aula 9: Adicionar item em pedido e relationship em models
- [x] Aula 10: Finalização e schemas de resposta
- [x] Teste final: rota de listar pedidos de um usuário (`/pedidos/listar/pedidos-usuario`)

## Fase 1: Fundação de qualidade

- [ ] Reorganizar em pastas: `routers/`, `models/`, `schemas/`
- [x] Alembic: primeira migração e uma mudança de model aplicada por ela
- [ ] `.env.example` no repositório (`SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`), `.env` no `.gitignore`
- [ ] Remover o token hardcoded de `testes.py` do repositório e trocar o `SECRET_KEY`
- [ ] Atualizar o `README.md` (hoje descreve só `/auth/criar_conta` e `/order/pedidos`)
- [ ] `pytest` + `TestClient`: testar login
- [ ] Testar criação de pedido
- [ ] Testar permissões (usuário comum x admin)
- [ ] Renomear as duas funções `listar_pedidos` de `order_routes.py` (a segunda sobrescreve a primeira)

## Fase 2: Autenticação própria (base para o Clerk)

- [x] Login com senha em hash (bcrypt) e JWT
- [x] Refresh token (`/auth/refresh`)
- [x] Rotas de pedido protegidas por `verificar_token`, com checagem de admin ou dono
- [ ] Cadastro com validações (e-mail único, senha mínima)
- [ ] Expiração de token tratada com erro claro
- [ ] Padronizar status HTTP: 403 para "sem permissão" (hoje algumas rotas usam 401)
- [ ] Desafio opcional: logout / invalidação de token

> O JWT próprio fica como aprendizado. Na Fase 7 ele é substituído pelo Clerk, e a lógica de `admin` e de dono do pedido continua valendo.

## Fase 3: Funcionalidades do delivery

- [ ] Models `Categoria` e `Produto` (nome, descrição, preço, imagem, disponível)
- [ ] CRUD de produtos e categorias (somente admin)
- [ ] `ItemPedido` ligado a `Produto` (trocar `sabor`/`tamanho`/`preco_unitario` vindos do cliente)
- [ ] Preço unitário lido do produto no servidor, nunca enviado pelo cliente
- [x] Preço total do pedido calculado no servidor (`calcular_preco`)
- [ ] Endereço de entrega do usuário (model `Endereco`, vinculado ao pedido)
- [ ] Taxa de entrega somada ao total
- [ ] Status do pedido com regras de transição: `PENDENTE → PAGO → PREPARANDO → SAIU_PARA_ENTREGA → ENTREGUE`, e `CANCELADO` só antes de preparar
- [ ] Usar `ChoiceType` ou `Enum` para o status em vez de string livre
- [ ] Paginação e filtros nas listagens (por status, data)

## Fase 4: Infraestrutura

- [ ] PostgreSQL com Docker Compose
- [ ] Logs
- [ ] Tratamento global de erros
- [ ] CORS configurado para o front
- [ ] Configuração centralizada das chaves externas via `.env` (`STRIPE_*`, `CLERK_*`, `RESEND_*`)

## Fase 5: Pagamentos com Stripe

- [ ] Conta Stripe em modo teste e chaves no `.env`
- [ ] Ler a documentação de Checkout Sessions e de webhooks antes de codar
- [ ] Rota `POST /pedidos/pedido/pagar/{id_pedido}`: cria uma Checkout Session com os itens do pedido e devolve a URL
- [ ] Guardar `stripe_session_id` e `stripe_payment_intent` no pedido (migração Alembic)
- [ ] Rota de webhook `POST /webhooks/stripe` com verificação da assinatura (`Stripe-Signature`)
- [ ] Tratar `checkout.session.completed`: pedido vai para `PAGO`
- [ ] Tratar `checkout.session.expired` e pagamento falho
- [ ] Idempotência: o mesmo evento chegando duas vezes não pode processar duas vezes
- [ ] Testar localmente com Stripe CLI (`stripe listen --forward-to ...`)
- [ ] Reembolso ao cancelar um pedido já pago (admin)
- [ ] Testes do webhook com payloads de exemplo

## Fase 6: E-mails com Resend

- [ ] Conta Resend, chave de API no `.env` e domínio de teste
- [ ] Serviço `enviar_email()` isolado em um módulo próprio
- [ ] E-mail de boas-vindas no cadastro
- [ ] E-mail de confirmação de pagamento, com resumo dos itens e total
- [ ] E-mail a cada mudança de status (preparando, saiu para entrega, entregue)
- [ ] Templates HTML simples
- [ ] Enviar em segundo plano (`BackgroundTasks`) para não travar a resposta
- [ ] Falha no envio é registrada em log e não derruba o pedido

## Fase 7: Front-end com Clerk

- [ ] Criar o projeto React + Vite
- [ ] Configurar o Clerk (`ClerkProvider`, login, cadastro e login social)
- [ ] Back-end: validar o JWT do Clerk (JWKS) em `verificar_token`
- [ ] Mapear `clerk_user_id` para o `Usuario` local, criando o usuário no primeiro acesso
- [ ] Definir admin pelo Clerk (`public_metadata.role`) ou pela tabela local
- [ ] Remover as rotas de login e senha próprias, ou mantê-las só em desenvolvimento
- [ ] Cardápio (lista de produtos por categoria)
- [ ] Carrinho (estado local, persistido no navegador)
- [ ] Finalizar pedido: endereço, resumo e redirecionamento ao Stripe Checkout
- [ ] Páginas de sucesso e de cancelamento do pagamento
- [ ] Acompanhar o status do pedido (polling ou atualização ao abrir a tela)
- [ ] Histórico de pedidos do usuário
- [ ] Painel admin: CRUD de produtos, lista de pedidos e troca de status

## Fase 8: Deploy e portfólio

- [ ] Deploy do back-end (Render ou Railway) com PostgreSQL gerenciado
- [ ] Deploy do front-end (Vercel ou Netlify)
- [ ] Webhook do Stripe apontando para a URL pública
- [ ] Domínio verificado no Resend para o envio real
- [ ] Variáveis de ambiente de produção (nada de chave de teste misturada)
- [ ] README com prints, instruções para rodar e fluxo de pagamento
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

Exemplo: `feat: cria checkout session do stripe para pagar pedido`
