# Esquema elétrico — PróVisão V1 (protoboard)

Este é o mapeamento da montagem V1, como funcionou na protoboard durante a disciplina. Ele continua sendo a referência de ligações para a V1.5 (placa soldada), as diferenças da V1.5 estão listadas no fim.

> Nota de nomenclatura: na V1 chamávamos o trilho dos motores de "5 V", mas com o dispositivo em bateria esse trilho é a **tensão da célula (3,3–4,2 V)** — os 5 V só existem com o USB conectado. A partir daqui, o nome correto é **VBAT**.

## 1. Microcontrolador

- ESP32-C3 Super Mini com o conector USB-C apontado para fora da placa.

## 2. Barramentos de energia

| Trilho | Origem | Alimenta |
|---|---|---|
| GND | GND do ESP32 | tudo (terra comum unificado) |
| VBAT | bateria → chave liga/desliga | motores e buzzer (via transistores) |
| 3V3 | regulador do ESP32 | os dois sensores VL53L0X |

## 3. Mapa de pinos (ESP32-C3)

| GPIO | Função |
|---|---|
| 0 | Motor esquerdo (base do transistor, via 1 kΩ) |
| 1 | Motor direito (base do transistor, via 1 kΩ) |
| 3 | Buzzer (base do transistor, via 1 kΩ) |
| 4 | SDA — dados I²C (os dois sensores) |
| 5 | SCL — clock I²C (os dois sensores) |
| 6 | XSHUT do sensor esquerdo |
| 7 | XSHUT do sensor direito |

## 4. Atuadores (chaveamento low-side)

Cada atuador (2 motores + buzzer) é chaveado por um transistor 2N2222:

- GPIO → resistor 1 kΩ → base;
- emissor → GND;
- fio negativo do atuador → coletor; fio positivo → VBAT;
- diodo flyback (1N4148/1N4007) em antiparalelo com cada **motor** — faixa (catodo) para o lado do VBAT.

## 5. Sensores VL53L0X

| Pino do sensor | Liga em |
|---|---|
| VIN | 3V3 |
| GND | GND |
| SDA | GPIO 4 (barramento compartilhado) |
| SCL | GPIO 5 (barramento compartilhado) |
| XSHUT | GPIO 6 (esq) / GPIO 7 (dir) |

Os breakouts já têm pull-ups de I²C, não é preciso adicionar.

## 6. Carga da bateria

Li-Po 3,7 V 300 mAh → módulo TP4056 com proteção. **Atenção:** o R_PROG de fábrica (1,2 kΩ) carrega a 1 A, acima do que a célula de 300 mAh suporta; na V1.5 ele é trocado por 4,7 kΩ (~250 mA). Detalhes no guia de construção do grupo.

## O que muda na V1.5 (placa soldada)

1. R_PROG do TP4056 trocado (item acima).
2. Capacitores novos: 470 µF entre VBAT e GND junto aos motores; 100 nF junto a cada conector de sensor.
3. Sensores, motores, buzzer e bateria ligados por **conectores JST**, não solda direta.
4. ESP32-C3 encaixado em barras de pinos fêmea (removível).

<!-- [MÍDIA] adicionar foto da montagem na protoboard (V1) e, quando pronta, foto da placa soldada (V1.5) -->
