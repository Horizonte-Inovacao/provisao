# 006. Licenças abertas e recíprocas, com proteção da marca

**Situação:** aceita · **Data:** setembro de 2026

## Contexto

Queremos garantir que ninguém se aproprie do trabalho técnico da PróVisão. Quando revisamos o repositório com esse objetivo, percebemos que as licenças que escolhemos em julho iam no sentido contrário. MIT no programa, CERN-OHL-P 2.0 na eletrônica e nas peças 3D e CC BY-SA 4.0 na documentação são licenças **permissivas**: deixam qualquer pessoa copiar, modificar e até vender o projeto, desde que mantenha o nosso crédito.

Encontramos também três inconsistências:

1. O arquivo `LICENSE` da raiz trazia a licença MIT sem dizer que ela valia só para o programa da placa. Quem abrisse o repositório no GitHub entenderia que o projeto inteiro era MIT.
2. O README dizia que a documentação estava sob CC BY-SA 4.0, mas não havia no repositório nenhum arquivo com essa licença.
3. Nenhum arquivo de código tinha aviso de autoria e de licença no topo.

Antes de decidir, estudamos o que uma licença consegue e o que ela não consegue fazer:

- **Nenhuma licença impede fisicamente a cópia de um repositório público.** Ela define o que é permitido e dá base para cobrar depois. Os próprios termos de uso do GitHub (seção D.5) deixam qualquer pessoa ver um repositório público e fazer uma cópia dele dentro do site (o chamado fork).
- **O que já publicamos continua valendo.** O repositório está público desde 16 de julho de 2026, e as licenças daquela época não podem ser retiradas de quem obteve os arquivos. A CC BY-SA 4.0 se declara irrevogável e diz que parar de distribuir não encerra a licença (seções 2(a)(1) e 6(c)). A CERN-OHL-P 2.0 ainda concede, a quem recebeu o projeto, uma licença de patente gratuita sobre o que foi publicado (seção 6.1).
- **O direito autoral já existe sem registro.** O programa é protegido por 50 anos, contados a partir do ano seguinte à publicação, e essa proteção independe de registro (Lei 9.609/1998, art. 2º, §§ 2º e 3º). Os textos, as fotos e os desenhos também são protegidos sem registro (Lei 9.610/1998, art. 18). Mas o direito autoral protege a forma, o código e o texto, e não a ideia (Lei 9.610/1998, art. 8º, inciso I). A ideia de um boné com sensores que avisa por vibração só teria proteção com uma patente.

## Decisão

Optamos por manter o projeto aberto, mas **recíproco**, desta versão em diante. Recíproco quer dizer que quem distribuir uma versão modificada precisa devolver as melhorias à comunidade, abertas e sob a mesma licença.

| Parte do projeto | Antes | Agora | Por que escolhemos |
|---|---|---|---|
| Programa da placa (`firmware/`) | MIT | GNU GPL 3.0 (GPL-3.0-only) | Quem distribuir uma versão modificada do programa, inclusive gravada num produto, precisa publicar o código-fonte dela sob a GPL |
| Eletrônica e peças 3D (`eletronica/`, `modelagem-3d/`) | CERN-OHL-P 2.0 | CERN-OHL-S 2.0 | A variante "S", fortemente recíproca, obriga quem fabricar e distribuir um produto baseado no projeto a publicar o projeto completo, com as melhorias |
| Documentação, fotos e vídeos | CC BY-SA 4.0 | CC BY-NC-SA 4.0 | Acrescentamos a cláusula NãoComercial (NC): ninguém pode usar nossos textos e imagens para ganhar dinheiro sem falar com a gente |

Alguns detalhes da decisão:

- **Escolhemos "GPL 3.0 somente" (GPL-3.0-only)** em vez de "GPL 3.0 ou posterior" porque preferimos decidir nós mesmos se vamos adotar uma versão futura da licença.
- **A V1 do programa continua sob MIT.** O arquivo `firmware/legado/viseira_v1.cpp` já foi publicado assim, então guardamos o texto original em `firmware/legado/LICENSE-MIT`. Como a MIT permite incorporar o código num trabalho sob GPL, desde que o aviso dela seja mantido, o programa da V1.5 pode seguir sob GPL.
- **Um arquivo de licença por área.** O `LICENSE` da raiz virou um índice que diz qual licença vale para cada pasta. Os textos completos ficam em `firmware/LICENSE`, `eletronica/LICENCA-HARDWARE.md` (que vale também para `modelagem-3d/`) e `documentacao/LICENCA-DOCUMENTACAO.md`.
- **Avisos de autoria nos arquivos de código.** Colocamos no topo de cada arquivo duas linhas no padrão SPDX, uma forma padronizada de declarar autor e licença que pessoas e ferramentas automáticas conseguem ler.
- **Nome e logo ficam fora das licenças abertas.** Declaramos isso no índice e na licença da documentação.

Decidimos também seguir três proteções que não dependem da licença:

1. **Registrar as marcas PróVisão e Horizonte Inovação Assistiva** no Instituto Nacional da Propriedade Industrial (INPI). É a proteção mais forte contra alguém vender um produto com o nosso nome: o registro garante uso exclusivo em todo o país (Lei 9.279/1996, art. 129) por 10 anos, renováveis (art. 133). Pessoa física tem desconto de 50% nas taxas, mas só pode registrar a marca de uma atividade que exerça de fato (art. 128, § 1º). Por isso precisamos definir antes quem será o titular.
2. **Registrar o programa da placa no INPI.** O registro não é obrigatório, mas serve de prova de autoria se houver disputa na Justiça.
3. **Avaliar, com o núcleo de inovação da faculdade, um pedido de patente de modelo de utilidade.** A patente de modelo de utilidade vale 15 anos e a de invenção vale 20 (Lei 9.279/1996, art. 40). A lei dá 12 meses de "período de graça": uma divulgação feita pelos próprios inventores nos 12 meses anteriores ao pedido não conta contra a novidade (art. 12). Nossas divulgações públicas começaram com a demonstração à ACACE, em abril de 2026, e seguiram na apresentação da disciplina (maio), na publicação no GitHub (16 de julho) e na feira de profissões (17 de setembro). Na contagem mais conservadora, o pedido precisa ser feito até abril de 2027, e a nossa meta é março de 2027. Sabemos que existem produtos parecidos no mercado, então um especialista precisa avaliar se há algo novo o bastante para patentear. E a licença de patente que a CERN-OHL-P concedeu sobre o que publicamos em julho continua valendo para aquela versão.

## O que avaliamos e não fizemos

- **Manter as licenças permissivas.** Descartamos porque elas deixam uma empresa pegar o projeto, fechar as melhorias e vender o resultado sem devolver nada.
- **Código visível com todos os direitos reservados.** Descartamos porque contraria a proposta de hardware aberto que o projeto assumiu desde o começo, afasta quem quer contribuir e, na prática, não impede a cópia, já que o GitHub permite o fork de repositório público.
- **Repositório privado.** Protege mais, mas tira o projeto do alcance de outras pessoas e instituições que poderiam estudá-lo e replicá-lo, o que vai contra a origem do projeto como extensão universitária.

## Consequências

**O que ganhamos:** quem aproveitar a PróVisão num produto distribuído precisa manter o projeto aberto e dar o crédito, a documentação não pode ser vendida por terceiros e cada pasta diz com clareza qual licença vale para ela.

**O que aceitamos:**

- A licença continua sem impedir a cópia: ela só dá base para cobrar depois.
- As versões publicadas até agora seguem sob as licenças permissivas para quem as obteve.
- A GPL e a CERN-OHL-S só exigem abrir as melhorias quando alguém distribui o programa ou o produto. Uma empresa que use uma versão modificada só internamente não precisa publicar nada.
- O GitHub deixa de mostrar uma licença única no topo do repositório, porque o `LICENSE` da raiz agora é um índice.
- Quem contribuir precisa aceitar publicar a contribuição sob a licença da área que alterou. Deixamos isso claro no [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Pendências

- Conferir o regulamento de propriedade intelectual da UniFavip Wyden, porque o projeto nasceu numa disciplina de extensão, e confirmar se ele dá à instituição ou ao orientador algum direito sobre o projeto.
- Conferir os termos assinados com a ACACE (Carta de Apresentação e Termo de Aceite).
- Registrar por escrito a participação do colega que esteve na equipe até a conclusão da disciplina e o acordo dele com a mudança de licença do que ele ajudou a criar.
- Definir quem será o titular das marcas e dos registros no INPI.

Esta análise foi feita pela equipe e não substitui a orientação de um advogado nem do núcleo de inovação da faculdade.

## Fontes

- [Lei 9.279/1996, Lei da Propriedade Industrial](https://www.planalto.gov.br/ccivil_03/leis/l9279.htm)
- [Lei 9.609/1998, Lei do Software](https://www.planalto.gov.br/ccivil_03/leis/l9609.htm)
- [Lei 9.610/1998, Lei de Direitos Autorais](https://www.planalto.gov.br/ccivil_03/leis/l9610.htm)
- [INPI: perguntas frequentes sobre programas de computador](https://www.gov.br/inpi/pt-br/acesso-a-informacao/perguntas-frequentes/programas-de-computador)
- [INPI: descontos nas taxas](https://www.gov.br/inpi/pt-br/servicos/custos-e-pagamento/descontos)
- [Texto da CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en) e [da CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en)
- [Resumo da CERN-OHL-S 2.0](https://choosealicense.com/licenses/cern-ohl-s-2.0/) e texto da CERN-OHL-P 2.0 publicado em julho (seção 6.1, patentes), guardado no histórico do repositório em `hardware/LICENSE.md`
- [Termos de uso do GitHub, seção D.5](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service)
