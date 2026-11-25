# Prisma Growth Engine
## Plano-mestre do projeto

**Versão:** 1.0

**Data:** 16/11/2026

**Primeiro produto:** Precifica Fácil

**Operação:** Prisma Dados

> Este documento registra a visão, as decisões, o escopo e o roadmap estratégico
> do Prisma Growth Engine. Ele descreve a missão desejada e não substitui os
> status operacionais verificados no código, no banco de dados ou nas plataformas
> externas.

---

# 1. Visão do projeto

O **Prisma Growth Engine** é o projeto de construção de uma estrutura própria para desenvolver, organizar, comercializar e evoluir produtos digitais.

A ideia é criar uma operação que permita lançar produtos com baixo custo inicial, processos repetíveis e o máximo possível de automação.

Em vez de tratar cada produto como um projeto isolado, queremos construir uma estrutura central que permita:

1. Identificar oportunidades de produtos digitais.
2. Desenvolver produtos com escopo controlado.
3. Gerenciar produtos, versões, ofertas e conteúdos.
4. Criar páginas comerciais profissionais.
5. Integrar plataformas de checkout e distribuição.
6. Controlar aprovação e publicação.
7. Acompanhar vendas e desempenho.
8. Aprimorar produtos com base em dados.
9. Repetir o processo para novos produtos.

**Objetivo central:** transformar a Prisma Dados em uma operação enxuta de criação e comercialização de produtos digitais, com processos cada vez mais padronizados e automatizados.

## Princípios do projeto

- Começar pequeno e validar antes de escalar.
- Evitar custos fixos desnecessários.
- Priorizar produtos simples, úteis e comercializáveis.
- Não publicar produtos sem validação.
- Separar conteúdo, produto, oferta e checkout.
- Automatizar processos repetitivos sem perder controle.
- Manter rastreabilidade das alterações e aprovações.
- Não prometer resultados que o produto não pode garantir.

---

# 2. O primeiro produto: Precifica Fácil

## 2.1. Proposta

**Precifica Fácil — Planilha de Precificação para MEIs**

Produto digital voltado a MEIs, pequenos comerciantes e pessoas que precisam calcular preços de venda com mais clareza.

A proposta é ajudar o usuário a entender quanto custa produzir ou adquirir um produto, considerar despesas e taxas, definir uma margem desejada e simular preços e descontos.

A comunicação comercial aprovada utiliza a proposta:

> Precifique seus produtos com mais clareza.

Subheadline:

> Uma planilha prática para MEIs e pequenos comerciantes calcularem preços de venda e simularem descontos.

## 2.2. Formato

- Arquivo Excel `.xlsx`.
- Produto digital de utilização imediata.
- Planilha protegida para reduzir alterações acidentais nas fórmulas.
- Versão inicial identificada como v1.0.

Não estamos construindo um SaaS de precificação neste primeiro momento. O MVP é uma planilha comercializável.

## 2.3. Estrutura da planilha

A versão inicial possui quatro abas:

| Aba | Objetivo |
|---|---|
| Instruções | Orientar o preenchimento e a utilização |
| Precificador | Calcular custos e sugerir preço de venda |
| Simulador de Descontos | Avaliar descontos e seus impactos |
| Exemplos | Apresentar situações ilustrativas de utilização |

### Funcionalidades previstas no MVP

- Registro dos custos envolvidos.
- Consideração de despesas e taxas informadas pelo usuário.
- Definição de margem ou markup.
- Cálculo de preço sugerido.
- Estimativa de lucro.
- Simulação de descontos.
- Visualização do impacto dos descontos sobre o resultado.
- Alertas para situações relevantes de precificação.

### Fora do escopo da v1.0

- Cálculo automático de impostos.
- Integração com ERP.
- Processamento de pagamentos.
- Inteligência artificial.
- Garantia de lucro ou de resultados financeiros.

Essas exclusões são importantes para manter o produto simples, compreensível e tecnicamente confiável.

## 2.4. Situação do produto

### Concluído

- Planilha v1.0 desenvolvida.
- Estrutura das quatro abas implementada.
- Proteção das fórmulas.
- Validação da planilha no Excel Web.
- Arquivo enviado à Hotmart.
- Conteúdo comercial cadastrado no Prisma Growth Engine.
- Headline, descrição, cinco benefícios e três perguntas frequentes definidos.
- Página de prévia implementada.

### Em andamento

- Acompanhamento da operação após a publicação.
- Coleta inicial de visitas, cliques e vendas.

### Futuro

- Acompanhar aceitação do produto.
- Identificar dúvidas e dificuldades dos compradores.
- Corrigir problemas encontrados.
- Planejar uma versão 1.1 a partir de evidências reais.

---

# 3. Estratégia comercial inicial

## 3.1. Oferta

| Item | Definição atual |
|---|---|
| Produto | Precifica Fácil |
| Plataforma | Hotmart |
| Preço | R$ 29,90 |
| Garantia | 7 dias |
| Formato | Produto digital XLSX |
| Checkout | `https://pay.hotmart.com/K108503525R` |

A oferta já foi cadastrada no ambiente local do Prisma Growth Engine.

**Importante:** a análise cadastral foi concluída e o checkout está acessível na verificação atual. Por decisão operacional, pagamento e entrega são assumidos como funcionais nesta etapa e não serão submetidos a teste controlado.

Portanto, cadastro de oferta não significa produto liberado para venda.

## 3.2. Critérios para começar a vender

O produto só deve ser publicado quando:

- [x] A Hotmart concluir a análise cadastral.
- [x] O produto estiver liberado comercialmente.
- [x] O checkout estiver acessível.
- [x] O pagamento for assumido como funcional para esta etapa.
- [x] A entrega automática do arquivo for assumida como funcional para esta etapa.
- [ ] A página comercial estiver revisada.
- [ ] O preço, a garantia e as informações da oferta estiverem corretos.
- [ ] O fluxo completo de compra estiver validado.

Não devemos ativar a oferta no Prisma antes dessas verificações.

## 3.3. Primeira estratégia de aquisição

A prioridade inicial é validar a comercialização sem adicionar despesas relevantes.

A sequência de trabalho será:

1. Colocar o produto em condições reais de venda.
2. Disponibilizar a página comercial.
3. Apresentar o produto ao público-alvo.
4. Observar visitas, cliques e compras.
5. Identificar objeções e dúvidas.
6. Ajustar comunicação, apresentação e produto.
7. Avaliar se existe demanda suficiente para investir em divulgação.

Não devemos confundir visualizações ou curtidas com validação comercial. O indicador mais importante será a conversão em vendas.

---

# 4. Arquitetura do Prisma Growth Engine

A arquitetura atual já possui uma base técnica funcional.

## 4.1. Visão geral

| Camada | Tecnologia | Responsabilidade |
|---|---|---|
| Backend | Python / FastAPI | Regras de negócio e API |
| Banco de dados | PostgreSQL | Persistência dos dados |
| Migrações | Alembic | Evolução do banco |
| Frontend comercial | Astro | Landing pages |
| Catálogo | JSON exportado | Distribuição de produtos publicados |
| Checkout | Hotmart | Pagamento e comercialização |
| Testes | Pytest | Validação automatizada |
| Qualidade | Ruff | Padronização e análise estática |

## 4.2. Backend

O backend é responsável por centralizar as informações e regras do negócio.

Entre as responsabilidades já implementadas:

- Cadastro e gerenciamento de produtos.
- Gerenciamento de ofertas.
- Armazenamento de conteúdo comercial.
- Controle de status.
- Aprovação de páginas.
- Proteção do fluxo de publicação.
- Registro de eventos por meio de outbox.

### Conteúdo comercial

Foi implementada a entidade `ProductPage`, responsável por armazenar o conteúdo estruturado da página de cada produto.

O fluxo possui:

- `GET /v1/products/{id}/page`
- `PUT /v1/products/{id}/page`
- `POST /v1/products/{id}/page/approve`

A aprovação é invalidada quando o conteúdo é editado novamente.

Produtos publicados ou arquivados possuem restrições de edição.

Eventos registrados na outbox:

- `product.page_saved`
- `product.page_approved`

Isso permite evoluir futuramente para integrações e processos assíncronos.

## 4.3. Banco de dados

O PostgreSQL armazena as entidades do sistema.

As migrações são controladas pelo Alembic.

Já existe, entre outras estruturas, a migration:

`0003_product_page_content`

O banco mantém a separação entre produto, oferta e conteúdo comercial.

## 4.4. Frontend e páginas comerciais

O frontend utiliza Astro.

Componente principal:

`apps/web/src/components/LandingPage.astro`

A página recebe os dados do produto e monta a experiência comercial a partir do conteúdo cadastrado.

Isso evita que cada landing page precise ser construída do zero.

A intenção é reutilizar o mesmo componente para vários produtos, mantendo personalizações específicas quando necessário.

## 4.5. Catálogo e publicação

O projeto possui uma separação entre:

- Catálogo público.
- Catálogo de prévias.

O exportador:

`scripts/export_catalog.py`

Gera os dados consumidos pelo frontend.

O build público não deve incluir produtos que ainda não foram liberados.

No estado atual verificado em 16/11/2026:

- Catálogo público: um produto.
- Catálogo de prévia: um produto.
- Precifica Fácil: `live`.
- Oferta local: ativa.
- Conteúdo comercial: cadastrado e aprovado no ambiente local.

A prévia está disponível em:

`http://localhost:4321/preview/precifica-facil`

A página pública do produto está disponível em:

`https://prismadados.pages.dev/p/precifica-facil/`

---

# 5. Regras de governança e segurança

Uma das partes mais importantes do projeto é impedir que um produto seja publicado prematuramente.

## 5.1. Ciclo de vida do produto

Fluxo conceitual:

1. Criação.
2. Cadastro das informações.
3. Desenvolvimento do produto.
4. Cadastro do conteúdo comercial.
5. Revisão.
6. Aprovação.
7. Configuração da oferta.
8. Validação do checkout.
9. Publicação.
10. Acompanhamento.

Os estados e transições precisam ser controlados pelo backend, não apenas pela interface.

## 5.2. Regras obrigatórias

- Produto em rascunho não aparece no catálogo público.
- Conteúdo não aprovado não pode ser publicado.
- Alterações no conteúdo invalidam a aprovação anterior.
- Oferta desativada não pode ser utilizada como oferta comercial.
- Produto arquivado não deve voltar a ser publicado sem o fluxo adequado.
- Prévia não pode oferecer compra real.
- Publicação deve respeitar as condições comerciais e técnicas.

## 5.3. Qualidade

A cada evolução relevante, manter:

- Testes automatizados.
- Verificação de lint.
- Build de produção.
- Teste de renderização.
- Verificação de SEO.
- Revisão visual em desktop e celular.

Estado de referência da suíte:

- 25 testes passando.
- Ruff sem erros.
- Teste de renderização e SEO aprovado.

---

# 6. Experiência comercial do Precifica Fácil

A landing page precisa transmitir confiança e demonstrar o funcionamento real da planilha.

## 6.1. Estrutura atual

A página possui:

- Cabeçalho.
- Headline.
- Subheadline.
- CTA.
- Descrição.
- Benefícios.
- Perguntas frequentes.
- Rodapé.
- Aviso de prévia no ambiente interno.

A comunicação deve ser objetiva e evitar promessas exageradas.

## 6.2. Demonstração visual

As três imagens reais foram adicionadas ao projeto:

`apps/web/public/images/precifica-facil/`

Arquivos:

- `precificador.png`
- `simulador.png`
- `exemplos.png`

A próxima evolução é criar uma seção de demonstração do produto na landing page.

A seção deve:

- Exibir as três imagens.
- Preservar a proporção original das capturas.
- Permitir ampliar ou abrir a imagem.
- Ter boa apresentação em desktop e celular.
- Ser exibida somente no Precifica Fácil.
- Não alterar a apresentação de outros produtos.

O objetivo é permitir que o visitante veja o que está comprando antes de tomar a decisão.

## 6.3. Diretrizes de design

- Aparência profissional.
- Hierarquia visual clara.
- Boa legibilidade.
- Espaçamento consistente.
- Responsividade.
- CTA evidente.
- Imagens reais do produto.
- Ausência de elementos desnecessários.
- Carregamento eficiente.

---

# 7. O que queremos construir no longo prazo

A visão é evoluir de uma estrutura que publica um produto para uma plataforma interna de operação de produtos digitais.

As funcionalidades abaixo representam a direção de evolução, não funcionalidades que já estejam implementadas.

## 7.1. Gestão centralizada de produtos

Um painel para visualizar todos os produtos da Prisma.

Informações desejadas:

- Nome.
- Identificador.
- Categoria.
- Versão.
- Status.
- Preço.
- Plataforma de venda.
- Situação da oferta.
- Aprovação do conteúdo.
- Data de criação.
- Data da última atualização.

## 7.2. Gestão de ofertas

Centralizar as informações comerciais:

- Preços.
- Condições de pagamento.
- Garantias.
- Links de checkout.
- Plataformas.
- Ativação e desativação.
- Histórico de alterações.

## 7.3. Gestão de páginas comerciais

Evoluir a estrutura atual para permitir:

- Criação de páginas a partir de modelos.
- Edição de conteúdo.
- Gestão de imagens.
- Pré-visualização.
- Aprovação.
- Publicação.
- Versionamento.
- SEO.
- Personalização por produto.

## 7.4. Integração com plataformas de venda

A Hotmart é a primeira integração comercial.

Uma evolução desejável é centralizar no Prisma:

- Identificação das ofertas.
- Links de checkout.
- Eventos de venda.
- Aprovação de pagamentos.
- Reembolsos.
- Cancelamentos.
- Informações de compradores, respeitando as regras de privacidade.
- Conciliação entre vendas externas e registros internos.

A implementação de webhooks e sincronização de vendas ainda precisa ser planejada e validada.

## 7.5. Analytics e indicadores

Construir uma visão de desempenho dos produtos.

Indicadores desejados:

- Visitas às páginas.
- Cliques nos CTAs.
- Taxa de conversão.
- Vendas.
- Receita bruta.
- Receita líquida.
- Reembolsos.
- Taxa de reembolso.
- Desempenho por produto.
- Desempenho por campanha.

A ideia é permitir decisões baseadas em dados, e não apenas em impressões.

## 7.6. Marketing e aquisição

Evoluir para uma estrutura de apoio à comercialização:

- Gestão de campanhas.
- Identificação de origem do tráfego.
- Parâmetros UTM.
- Conteúdos de divulgação.
- Materiais comerciais.
- Testes de comunicação.
- Análise de conversão.

A automação de marketing deve vir depois de termos um produto validado e dados suficientes para orientar as decisões.

## 7.7. Automação operacional

A arquitetura deverá permitir automatizar processos como:

- Preparação de páginas.
- Exportação de catálogos.
- Validações antes da publicação.
- Notificações de eventos.
- Atualizações de status.
- Relatórios de desempenho.
- Rotinas de acompanhamento.

A outbox já é uma base técnica útil para evoluir nessa direção.

## 7.8. Gestão de portfólio

Com mais produtos, queremos ter uma visão consolidada:

- Produtos em desenvolvimento.
- Produtos em revisão.
- Produtos publicados.
- Produtos com vendas.
- Produtos que precisam de melhorias.
- Produtos que devem ser descontinuados.

O objetivo é administrar um portfólio, não apenas uma sequência de lançamentos isolados.

---

# 8. Roadmap

## Fase 1 — Finalizar o primeiro produto

**Prioridade máxima | Em andamento**

- [x] Desenvolver a planilha Precifica Fácil v1.0.
- [x] Proteger fórmulas.
- [x] Validar a planilha no Excel Web.
- [x] Cadastrar o produto na Hotmart.
- [x] Cadastrar preço de R$ 29,90.
- [x] Cadastrar garantia de 7 dias.
- [x] Enviar documentos para análise cadastral.
- [x] Cadastrar conteúdo comercial no Prisma.
- [x] Implementar prévia da landing page.
- [x] Criar as três imagens de demonstração.
- [x] Inserir as imagens na landing page.
- [x] Revisar desktop e celular.
- [x] Confirmar aprovação da Hotmart.
- [x] Aceitar operacionalmente o checkout e o pagamento como funcionais.
- [x] Aceitar operacionalmente a entrega automática como funcional.
- [x] Liberar oferta no Prisma.
- [x] Publicar produto.

**Critério de conclusão:** produto disponível para compra, com pagamento e entrega aceitos operacionalmente.

## Fase 2 — Validar comercialmente

**Após a publicação**

- [ ] Apresentar o produto ao público-alvo.
- [ ] Medir visitas publicamente (instrumentação pronta; API pública ainda não configurada).
- [ ] Medir cliques publicamente (instrumentação pronta; API pública ainda não configurada).
- [ ] Acompanhar vendas.
- [ ] Registrar dúvidas e objeções.
- [ ] Avaliar conversão.
- [ ] Corrigir problemas encontrados.
- [ ] Decidir sobre a próxima versão.

**Critério de conclusão:** ter evidências suficientes para decidir se o produto deve ser mantido, melhorado ou reposicionado.

## Fase 3 — Consolidar o painel de gestão

- [ ] Criar painel administrativo.
- [ ] Listar produtos.
- [ ] Exibir status e ofertas.
- [ ] Gerenciar conteúdos.
- [ ] Gerenciar aprovações.
- [ ] Facilitar prévias.
- [ ] Centralizar informações comerciais.

**Critério de conclusão:** conseguir administrar os produtos sem depender de alterações manuais no banco de dados.

## Fase 4 — Integrar vendas e indicadores

- [ ] Estudar e implementar integração de eventos da Hotmart.
- [ ] Receber notificações de vendas.
- [ ] Registrar eventos no backend.
- [ ] Sincronizar status.
- [ ] Tratar reembolsos e cancelamentos.
- [ ] Construir indicadores comerciais.
- [ ] Criar relatórios por produto.

**Critério de conclusão:** ter uma visão confiável do desempenho comercial dentro do Prisma.

## Fase 5 — Estruturar aquisição e marketing

- [ ] Padronizar campanhas.
- [ ] Registrar origem do tráfego.
- [ ] Implementar acompanhamento de UTM.
- [ ] Medir conversão das páginas.
- [ ] Criar processo de produção de materiais comerciais.
- [ ] Testar canais de aquisição.
- [ ] Avaliar custo de aquisição quando houver investimento.

**Critério de conclusão:** estabelecer um processo mensurável e repetível de aquisição de clientes.

## Fase 6 — Escalar o portfólio

- [ ] Identificar novas oportunidades.
- [ ] Criar processo de avaliação de ideias.
- [ ] Padronizar desenvolvimento de produtos.
- [ ] Reutilizar componentes comerciais.
- [ ] Criar fluxo de lançamento.
- [ ] Comparar desempenho entre produtos.
- [ ] Priorizar produtos com melhor potencial.

**Critério de conclusão:** conseguir lançar e administrar novos produtos com menor esforço operacional por lançamento.

---

# 9. Backlog imediato

Esta é a lista de trabalho mais próxima, em ordem de prioridade.

| Prioridade | Tarefa | Situação |
|---|---|---|
| P0 | Inserir imagens reais na landing page | Concluída |
| P0 | Revisar o restante do CSS do componente | Concluída |
| P0 | Validar a experiência em desktop e celular | Concluída |
| P0 | Acompanhar análise cadastral Hotmart | Concluída |
| P0 | Validar checkout e entrega | Aceitos operacionalmente; não testados |
| P0 | Publicar somente após todos os testes | Concluída por decisão operacional |
| P1 | Revisar favicon e detalhes finais da página | Pendente |
| P1 | Implementar captura de métricas de acesso e conversão | Backend concluído; ativação pública bloqueada pela publicação da API |
| P1 | Planejar integração de eventos Hotmart | Base local concluída; operação externa ainda não configurada |
| P2 | Construir painel administrativo | Futuro |
| P2 | Construir dashboard comercial | Futuro |
| P2 | Estruturar processo de aquisição | Futuro |
| P3 | Evoluir gestão de portfólio | Futuro |

---

# 10. Estrutura atual do repositório

Caminho local:

`~/Downloads/codigos/prisma-growth-engine`

Componentes relevantes:

```text
prisma-growth-engine/
├── apps/
│   ├── api/
│   │   ├── app/
│   │   └── tests/
│   └── web/
│       ├── public/
│       │   └── images/
│       │       └── precifica-facil/
│       └── src/
│           └── components/
│               └── LandingPage.astro
├── scripts/
│   ├── export_catalog.py
│   └── check_landing_render.py
└── ...
```

Arquivos importantes:

- `apps/web/src/components/LandingPage.astro`
- `scripts/export_catalog.py`
- `scripts/check_landing_render.py`

Prévia local:

`http://localhost:4321/preview/precifica-facil`

---

# 11. Critérios de qualidade do projeto

Toda evolução relevante deve preservar:

1. Código organizado e tipado quando aplicável.
2. Regras de negócio no backend.
3. Separação entre dados e apresentação.
4. Migrações controladas.
5. Testes automatizados.
6. Verificação de lint.
7. Build funcional.
8. Proteção contra publicação indevida.
9. Responsividade.
10. SEO adequado.
11. Rastreabilidade de alterações.
12. Documentação das decisões importantes.

O projeto não deve crescer em funcionalidades sem necessidade. Cada nova camada precisa resolver um problema real da operação.

---

# 12. Decisões que precisamos preservar

- O Precifica Fácil é o primeiro produto, não o produto final da Prisma.
- O MVP é uma planilha XLSX, não um sistema SaaS.
- A Hotmart é a primeira plataforma de comercialização.
- O preço inicial definido é R$ 29,90.
- A garantia cadastrada é de 7 dias.
- A página comercial é alimentada pelo conteúdo armazenado no backend.
- A publicação é controlada por regras de aprovação.
- A prévia deve permanecer separada do catálogo público.
- A oferta local permanece desativada até a validação comercial.
- Não devemos publicar antes da liberação da Hotmart e da aceitação operacional do fluxo de compra e entrega.
- A prioridade é colocar um produto real no mercado antes de ampliar excessivamente a plataforma.

---

# 13. Definição de sucesso

O sucesso do Prisma Growth Engine não será simplesmente ter uma arquitetura sofisticada.

Será conseguir:

- Criar produtos digitais úteis.
- Lançá-los com baixo custo.
- Comercializá-los com segurança.
- Medir seus resultados.
- Melhorá-los continuamente.
- Repetir o processo.
- Construir um portfólio rentável.

**Nossa primeira meta é simples: colocar o Precifica Fácil no mercado de forma profissional, validar sua demanda e usar o aprendizado para evoluir o Prisma Growth Engine.**

A plataforma deve crescer junto com a operação — não antes dela.
