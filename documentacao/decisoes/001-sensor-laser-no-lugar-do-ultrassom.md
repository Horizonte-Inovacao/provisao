# 001. Sensor a laser no lugar do sensor ultrassônico

**Situação:** aceita · **Data:** março de 2026

## Contexto

No planejamento inicial íamos usar o HC-SR04, o sensor ultrassônico clássico dos projetos com microcontrolador: barato e fácil de achar. Durante a especificação, esbarramos em três problemas para o nosso caso:

1. Ele é grande para a aba de um acessório de cabeça (tem dois "olhos" de 16 mm) e precisaríamos de dois.
2. O som se espalha num cone largo. Fica difícil separar "obstáculo à esquerda" de "obstáculo à direita", e avisar o lado era justamente o que os associados da ACACE mais valorizavam.
3. Em superfícies macias, como roupas e folhas, o eco volta fraco e a leitura fica instável.

## Decisão

Devido a esses três pontos, optamos por dois sensores **VL53L0X**. Eles medem a distância pelo tempo que um feixe de luz infravermelha leva para ir e voltar. Têm precisão de 1 mm, enxergam num cone estreito de uns 25 graus (o que permite uma leitura separada para cada lado) e são minúsculos. Os dois dividem os mesmos fios de comunicação com a placa, e a placa dá um endereço diferente para cada um toda vez que liga.

## Consequências

**O que ganhamos:** precisão de milímetros, noção real de lado e um equipamento menor e mais leve.

**O que aceitamos perder:** sensores de luz infravermelha perdem alcance sob sol direto (de uns 2 m para algo entre 60 e 80 cm). Por isso a validação de campo acontece em ambiente interno ou na sombra, e colocamos o uso ao ar livre como meta da V3, em vez de fingir que esse limite não existe.

Essa troca também mudou o formato do produto: os sensores pequenos permitiram sair dos "óculos" e ir para uma viseira. Mais tarde, a viseira virou boné (veja a [decisão 002](002-bone-no-lugar-da-viseira.md)).
