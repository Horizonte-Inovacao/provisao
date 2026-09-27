# Esquema elétrico da V1.5

Aqui estão todas as ligações do boné. Partimos do circuito que funcionou na placa de testes da V1 e registramos, no fim, o que mudou na V1.5.

Um aviso sobre nomes: na V1 chamávamos a linha que alimenta os motores de "5 V". Com o boné na bateria, essa linha tem a tensão da bateria (de 3,3 a 4,2 V), e os 5 V só existem com o cabo USB ligado. Por isso passamos a chamar essa linha de **linha da bateria**.

## 1. Placa principal

ESP32-C3 Super Mini, encaixada na placa ilhada por duas barras de pinos fêmea. Assim ela sai sem precisar dessoldar.

## 2. Linhas de energia

| Linha | De onde vem | O que alimenta |
|---|---|---|
| Terra (GND) | negativo comum de todo o circuito | tudo |
| Linha da bateria | bateria, depois do carregador e da chave | motores e bipe (pelos transistores) e a entrada de 5 V da placa |
| 3,3 V | regulador interno da placa ESP32-C3 | os dois sensores |

## 3. Caminho da energia, da bateria até a placa

1. **Bateria 14500**, no case do lado direito.
2. **Fusível rearmável de 500 mA** soldado no fio positivo, logo na saída da bateria. Se o cabo entrar em curto, ele corta a corrente.
3. **Cabo de 2 fios** contornando a nuca pela canaleta até o case da esquerda, com um conector JST no final.
4. **Carregador TP4056 USB-C**: a bateria entra nos pontos B+ e B-.
5. **Chave liga/desliga** entre a saída do carregador (OUT+) e a linha da bateria.

**Ajuste obrigatório no carregador:** de fábrica ele carrega a 1 A, forte demais para a bateria 14500. Trocamos o resistor que define a corrente de carga (marcado como R3 ou "Rprog" no módulo) por um de **3 kΩ**, e a carga cai para cerca de 400 mA.

## 4. Pinos da placa ESP32-C3

| Pino | Para que usamos |
|---|---|
| 0 | Motor esquerdo (pelo transistor) |
| 1 | Motor direito (pelo transistor) |
| 3 | Bipe (pelo transistor) |
| 4 | Dados dos sensores (SDA), compartilhado pelos dois |
| 5 | Relógio dos sensores (SCL), compartilhado pelos dois |
| 6 | Liga/desliga do sensor esquerdo (XSHUT) |
| 7 | Liga/desliga do sensor direito (XSHUT) |

## 5. Como a placa liga os motores e o bipe

A placa não fornece corrente suficiente para um motor. Por isso cada motor e o bipe são ligados por um transistor 2N2222, que funciona como um interruptor comandado pela placa:

- pino da placa → resistor de 1 kΩ → perna do meio do transistor (base);
- perna emissora do transistor → terra;
- fio negativo do motor (ou do bipe) → perna coletora do transistor; fio positivo → linha da bateria;
- em cada **motor**, um diodo 1N4148 ligado ao contrário, em paralelo, com a faixa do diodo virada para a linha da bateria. Quando o motor desliga, ele gera um pico de tensão, e o diodo absorve esse pico antes que ele chegue no transistor.

## 6. Sensores VL53L0X

| Pino do sensor | Liga em |
|---|---|
| VIN | 3,3 V |
| GND | terra |
| SDA | pino 4 (os dois sensores no mesmo fio) |
| SCL | pino 5 (os dois sensores no mesmo fio) |
| XSHUT | pino 6 (esquerdo) ou pino 7 (direito) |

As plaquinhas dos sensores já têm os resistores de que a comunicação precisa, então não é preciso colocar nenhum a mais.

Nos cabos dos sensores, torça o fio de dados (amarelo) e o de relógio (verde) junto com o terra (preto). O cabo do sensor direito passa dos 70 cm, e trançar os fios diminui a interferência.

## 7. Cores dos fios que combinamos

| Cor | Uso |
|---|---|
| vermelho | positivo (3,3 V nos sensores, linha da bateria nos motores e bateria) |
| preto | terra |
| amarelo | dados dos sensores (SDA) |
| verde | relógio dos sensores (SCL) |
| azul ou branco | liga/desliga de cada sensor (XSHUT) |

## O que mudou da V1 para a V1.5

1. **Bateria:** saiu a bateria mole de 300 mAh e entrou a 14500 de cerca de 800 mAh, com proteção e fusível rearmável. Explicamos o porquê na [decisão 003](../documentacao/decisoes/003-bateria-14500.md).
2. **Carregador:** resistor de carga trocado para 3 kΩ (cerca de 400 mA) e versão com entrada USB-C.
3. **Capacitores novos:** 470 µF entre a linha da bateria e o terra, perto dos motores, e 100 nF junto de cada conector de sensor. Sem eles, a placa da V1 reiniciava quando os motores ligavam.
4. **Conectores JST** em sensores, motores e bateria, no lugar de solda direta. Dá para tirar a eletrônica do boné para lavar.
5. **Placa ESP32-C3 encaixada** em barras de pinos fêmea, removível.

## Próximo passo planejado

Queremos que o boné avise a carga da bateria por vibração ao ligar. Para isso a placa precisa medir a tensão da bateria com dois resistores de 100 kΩ (que já estão na lista de compras). O pino 2, que parecia o candidato natural, é usado pela placa durante a partida e pode atrapalhar a inicialização. Por isso o plano é **passar o bipe do pino 3 para o pino 10 e usar o pino 3 para medir a bateria**. Essa mudança ainda não foi feita no programa.

## Cuidado ao gravar o programa

A entrada USB-C da própria placa ESP32-C3 fica fechada dentro do case. Com a chave ligada, a energia do cabo USB encontra a linha da bateria. Grave o programa só com a chave desligada ou com a bateria desconectada.

<!-- [MÍDIA] adicionar foto da montagem na placa de testes (V1) e, quando pronta, foto da placa soldada (V1.5) -->
