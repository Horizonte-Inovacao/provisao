# 005. Conforto no que encosta na cabeça

**Situação:** aceita · **Data:** setembro de 2026

## Contexto

Duas peças ficam do lado de dentro do boné, encostando na cabeça: as placas internas que prendem os cases e os berços dos motores. As duas são de plástico impresso, que tem cantos e marcas de camada. Os motores ainda precisam de contato firme, porque vibração sem contato não é sentida.

## Decisão

Seguimos uma regra só: **o plástico dá a estrutura e uma camada macia faz o contato com a pele.** Na prática:

**Placas internas**

- Ficaram mais finas (1,6 mm em vez de 2 mm) para se moldarem melhor à cabeça.
- A borda ficou toda arredondada.
- Recebem uma almofada de EVA de 3 mm colada do lado da cabeça, cobrindo também as cabeças dos parafusos.
- A parte de baixo da placa entra por trás da faixa interna do boné, que já é feita para encostar na testa.

**Berços dos motores**

- Passaram a ser impressos em TPU, um plástico flexível que cede e acompanha a curva da nuca.
- Ficaram mais baixos (3,4 mm em vez de 4,4 mm) e com uma aba maior (28 mm), para espalhar a pressão.
- O motor entra sob pressão no berço e fica só 0,3 mm para fora.
- Em volta do motor vai um anel de EVA de 2 mm.
- Tudo isso fica dentro de um bolsinho de tecido costurado na faixa interna. A pele encosta só no tecido, e a vibração passa por ele sem perder força.

## O que avaliamos e não fizemos

Pensamos em descer os cases uns 10 mm para a placa interna ficar inteira atrás da faixa interna. Descartamos porque a faixa tem 30 mm de altura e a placa tem 41 mm: mesmo descendo, uma parte ficaria de fora. E o case encostaria na canaleta dos fios. A almofada de EVA resolve o contato sem mexer na posição.

## Consequências

**O que ganhamos:** nenhuma peça dura em contato direto com a pele, pressão espalhada e peças fáceis de limpar com álcool 70%.

**O que aceitamos:** a lista de compras ganhou folhas de EVA e retalhos de tecido, e o berço do motor precisa ser impresso em TPU, que nem todo serviço de impressão tem. No teste de campo vamos medir o conforto aos 15 e aos 30 minutos e conferir a pele depois de cada sessão (veja o [roteiro de testes](../protocolo-de-testes.md)).
