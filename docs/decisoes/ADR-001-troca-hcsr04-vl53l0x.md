# ADR-001 — Troca do HC-SR04 pelo VL53L0X

**Status:** aceita · **Data:** março/2026

## Contexto

O planejamento inicial do projeto previa um sensor ultrassônico HC-SR04, o clássico dos projetos com microcontrolador, barato e fácil de achar. Durante a especificação, esbarramos em três limitações para o nosso caso de uso:

1. O HC-SR04 é volumoso para a aba de uma viseira (dois "olhos" de 16 mm), e usaríamos dois;
2. O cone de detecção do ultrassom é largo e impreciso para separar "obstáculo à esquerda" de "obstáculo à direita", e a lateralização era a funcionalidade que os associados da ACACE mais valorizavam;
3. Leituras ultrassônicas em superfícies macias (roupas, folhagem) retornam eco fraco e instável.

## Decisão

Adotamos dois sensores **VL53L0X** (tempo de voo a laser infravermelho, I²C): resolução de 1 mm, feixe estreito (~25°) que permite leitura independente por lado, tamanho minúsculo e leitura que não depende do material do obstáculo na mesma medida que o ultrassom. Os dois convivem no mesmo barramento I²C com endereços distintos, remapeados no boot via pinos XSHUT.

## Consequências

**Ganhamos:** precisão milimétrica, lateralização real, dispositivo mais compacto e leve.

**Aceitamos como trade-off:** sensores infravermelhos perdem alcance sob luz solar direta (de ~2 m para ~60–80 cm). Por isso a validação de campo acontece em ambiente interno/sombreado, e o sensoriamento para ambientes externos entrou no roadmap (V3) em vez de fingirmos que o limite não existe.

Essa troca também mudou a apresentação do produto: de "óculos" para "viseira", uma base mais modular e confortável para fixar sensores e eletrônica.
