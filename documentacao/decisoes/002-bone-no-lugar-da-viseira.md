# 002. Boné no lugar da viseira e motores perto da nuca

**Situação:** aceita · **Data:** setembro de 2026

## Contexto

A V1 foi montada numa viseira, com os fios presos por fita. Funcionou bem para a apresentação em sala, mas percebemos dois problemas para o teste com usuários reais:

1. A viseira não é um acessório comum no dia a dia. Quem usa o equipamento acaba andando com algo que chama atenção.
2. Os motores de vibração ficavam nas têmporas, e ali a vibração causava um desconforto forte.

## Decisão

Optamos pelo **boné de aba curva com regulagem atrás**, porque é um objeto que as pessoas já usam no dia a dia e porque a aba é um lugar natural para os sensores.

Junto com o boné, definimos:

- **Motores perto da nuca**, um de cada lado, dentro da faixa interna do boné (a carneira). O lado da vibração continua claro e o incômodo das têmporas some.
- **Uma canaleta costurada por fora**, de ponta a ponta do boné, por onde passam os fios dos sensores, dos motores e da bateria. Os fios ficam protegidos e o boné fica com acabamento limpo.
- **Dois cases em laterais opostas**: o da eletrônica do lado esquerdo e o da bateria do lado direito. Concluímos essa divisão por dois motivos: o peso fica equilibrado e a bateria fica longe da placa.
- **Sensores na aba**, 50 mm para cada lado do centro e um pouco atrás da borda, que protege o suporte de batidas de frente.

## Consequências

**O que ganhamos:** um produto mais discreto, fios protegidos, peso equilibrado e vibração sem incômodo.

**O que aceitamos:** o case da eletrônica fica entre 26 e 31 mm saltado da lateral do boné. Com a placa de circuito própria da V2, essa altura vai diminuir bastante. Além disso, cada modelo de boné tem uma curva diferente, então é preciso medir o boné real antes da impressão final (explicamos como em [`modelagem-3d/README.md`](../../modelagem-3d/README.md)).
