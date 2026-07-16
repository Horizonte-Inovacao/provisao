# Testes de campo — PróVisão

Roteiro que vamos aplicar nas sessões de validação com os voluntários da ACACE (5 a 10 participantes). O objetivo é sair de cada sessão com dados comparáveis entre versões, não só impressões.

## Preparação

- Percurso **interno ou sombreado** (limite do sensor IR sob sol direto), pré-definido e seguro, com obstáculos "aéreos" catalogados na altura de tronco e cabeça (fixados em suportes, sem pontas).
- TCLE impresso e assinado antes de qualquer atividade; autorização de imagem à parte.
- Dispositivo aprovado no checklist pré-teste: carga completa, bipes de "pronto" ao ligar, lateralização conferida, 30 min de operação sem reset no dia anterior.
- Cada participante recebe um **código de sessão** (ex.: `S03`); todos os registros usam o código, nunca o nome.

## Estrutura da sessão (por participante)

1. **Ambientação (5–10 min):** o participante conhece a viseira pelo tato, sente os três níveis de vibração com a mão e depois na cabeça, entende o bipe crítico e o bipe de erro.
2. **Percurso baseline:** só com a bengala, acompanhado. Registramos tempo e contatos com obstáculos aéreos.
3. **Percurso com a viseira:** bengala + viseira, mesmo trajeto (ou espelhado, para reduzir efeito de memória). Mesmos registros.
4. **Teste de direção:** parado, apresentamos obstáculo à esquerda/direita em ordem aleatória (8 apresentações); o participante aponta o lado que sentiu.
5. **Questionário:** SUS (abaixo) + perguntas abertas de conforto.

## O que medimos

| Indicador | Como | Meta |
|---|---|---|
| Contatos com obstáculos aéreos | contagem por percurso (baseline × com viseira) | redução clara vs. baseline |
| Tempo de percurso | cronômetro | não piorar significativamente |
| Acerto direcional | acertos / 8 apresentações | ≥ 7 de 8 |
| Tempo de adaptação | minutos até o participante declarar conforto | registrar (sem meta na 1ª rodada) |
| SUS | questionário de 10 itens | > 68 (média de referência) |
| Conforto físico (peso/pressão/calor) | Likert 1–5 | ≥ 4 |
| Falhas do dispositivo na sessão | resets, bipes de erro, quedas de leitura | zero |

## SUS — System Usability Scale (versão que aplicamos)

Cada item de 1 (discordo totalmente) a 5 (concordo totalmente):

1. Eu usaria esta viseira com frequência.
2. Achei a viseira desnecessariamente complexa.
3. Achei a viseira fácil de usar.
4. Eu precisaria de ajuda de uma pessoa técnica para conseguir usar.
5. As funções da viseira funcionam bem juntas.
6. A viseira se comportou de forma inconsistente.
7. Imagino que a maioria das pessoas aprenderia a usá-la rapidamente.
8. Achei a viseira desajeitada/incômoda de usar.
9. Me senti confiante usando a viseira.
10. Precisei aprender muitas coisas antes de conseguir usar.

Cálculo: itens ímpares (nota − 1), itens pares (5 − nota); soma × 2,5 → escala 0–100.

## Registro

- Planilha de coleta por sessão (código, data, versão do firmware/hardware, medidas acima).
- Fotos/vídeos apenas com autorização — arquivos em `media/` seguindo a convenção de nomes de lá.
- Resumo de cada rodada entra no `CHANGELOG.md`, é assim que o repositório conta a evolução do produto.

<!-- [MÍDIA] após a primeira rodada na ACACE: adicionar foto do percurso montado e (com autorização) registro da sessão -->
