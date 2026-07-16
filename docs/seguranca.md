# Segurança — leia antes de usar

Escrevemos esta página porque a PróVisão é usada por pessoas que não podem conferir visualmente o estado do dispositivo. Isso muda o padrão de exigência: aqui, segurança não é seção obrigatória de manual, se torna um requisito de engenharia.

## O que a PróVisão é (e o que não é)

- É um **protótipo experimental** em fase de validação, complementar à bengala branca.
- **Não substitui a bengala**, o cão-guia nem qualquer recurso de mobilidade já usado. Nos nossos testes, o participante usa sempre a bengala junto com a viseira.
- Não é dispositivo médico certificado. Todo uso acontece em **teste supervisionado**, com acompanhante, em percurso conhecido e seguro.

## Regras da bateria (Li-Po)

1. **Nunca carregar com o dispositivo em uso ou na cabeça.** Carga é feita com a viseira sobre uma superfície firme e não inflamável.
2. A corrente de carga do módulo TP4056 foi ajustada para a célula de 300 mAh (~250 mA). Módulo esquentando além de "morno" = interromper e investigar.
3. A célula é do tipo pouch: não pode ser perfurada, dobrada nem comprimida (nem por parafuso do case). Célula estufada sai de uso imediatamente e vai para descarte em ecoponto.
4. Sem solda, nunca, com a bateria conectada.

## Comportamento em falha

O dispositivo **avisa quando não está protegendo**: se um sensor falha, o buzzer emite três bipes longos repetidos até a recuperação. Dois bipes curtos na ligação indicam sistema pronto. Se a viseira ligar em silêncio, considere-a inoperante.

## Privacidade nos testes (LGPD)

Dados de participantes com deficiência são dados pessoais sensíveis. Nos testes: termo de consentimento (TCLE) sempre; registros de imagem só com autorização expressa; dados de desempenho identificados apenas por código de sessão, com o mapeamento nome↔código guardado fora do repositório.

## Encontrou um risco que não mapeamos?

Abra uma Issue com o rótulo `seguranca`, esse tipo de contribuição tem prioridade sobre qualquer outra.
