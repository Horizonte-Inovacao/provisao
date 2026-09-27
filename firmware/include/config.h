// ============================================================
// PróVisão · configuração central do firmware
// Tudo que é ajuste de calibração fica aqui. A lógica não
// precisa ser tocada para mudar pino, distância ou intensidade.
// ============================================================
#pragma once

#include <Arduino.h>

// ---------- Pinos (ESP32-C3 Super Mini) ----------
#define MOTOR_ESQ    0   // vibracall esquerdo (via transistor)
#define MOTOR_DIR    1   // vibracall direito  (via transistor)
#define PINO_BUZZER  3   // buzzer ativo       (via transistor)
#define PINO_SDA     4   // I2C dados
#define PINO_SCL     5   // I2C clock
#define XSHUT_ESQ    6   // desligamento do sensor esquerdo
#define XSHUT_DIR    7   // desligamento do sensor direito

// ---------- Endereços I2C dos sensores ----------
#define ADDR_SENSOR_ESQ 0x30  // remapeado no boot
#define ADDR_SENSOR_DIR 0x29  // endereço padrão do VL53L0X

// ---------- Distâncias (milímetros) ----------
const int DIST_NIVEL_1   = 1500; // começa a vibrar (nível fraco)
const int DIST_NIVEL_2   = 1000; // vibração média
const int DIST_NIVEL_3   = 500;  // vibração forte
const int DIST_CRITICA   = 300;  // buzzer

// ---------- Vibração ----------
// Os motores são de 1–3 V e o trilho é a tensão da bateria
// (3,3–4,2 V), então limitamos o PWM para não sobrecarregá-los.
const uint8_t DUTY_NIVEL[4] = { 0, 90, 140, 180 }; // por nível (0 a 3)
const uint8_t DUTY_KICK     = 255;  // "empurrão" para vencer a inércia
const uint16_t KICK_MS      = 30;   // duração do empurrão

// ---------- Tempos ----------
const uint32_t INTERVALO_LEITURA_MS = 50;
const uint32_t RETRY_SENSOR_MS      = 5000; // nova tentativa após falha
