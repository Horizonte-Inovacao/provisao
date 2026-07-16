// ============================================================
// PróVisão — firmware V1 (2026.1) — PRESERVADO COMO HISTÓRICO
// Esta é a versão apresentada na disciplina e demonstrada à
// ACACE, exatamente como rodou na protoboard. Não usar em
// builds novos: a V1.5 (firmware/src/) corrige a sobretensão
// dos motores, o limiar de partida da vibração e a falha
// silenciosa de sensor. Mantemos o arquivo pelo registro
// cronológico do projeto.
// ============================================================

#include <Wire.h>
#include "Adafruit_VL53L0X.h"

// ==========================================
// MAPA DE PINOS DEFINITIVO PARA PROTOBOARD
// (Baseado na serigrafia real do ESP32-C3)
// ==========================================
#define MOTOR_ESQ 0     // Transistor Esq (Furo D8)
#define MOTOR_DIR 1     // Transistor Dir (Furo D7)
#define PINO_BUZZER 3   // Transistor Buzzer (Furo D5)

#define PINO_SDA 4      // I2C Dados (Furos B4/C4)
#define PINO_SCL 5      // I2C Clock (Furo J1)
#define XSHUT_ESQ 6     // Desligamento Esq (Furo J2)
#define XSHUT_DIR 7     // Desligamento Dir (Furo J3)

// ==========================================
// CONFIGURAÇÕES DE DISTÂNCIA (em milímetros)
// ==========================================
const int DISTANCIA_MAXIMA = 1500; // 150 cm - Começa a vibrar
const int DISTANCIA_MINIMA = 200;  // 20 cm - Vibração máxima
const int DISTANCIA_CRITICA = 300; // 30 cm - Ativa o Buzzer

Adafruit_VL53L0X sensorEsq = Adafruit_VL53L0X();
Adafruit_VL53L0X sensorDir = Adafruit_VL53L0X();

unsigned long tempoAnterior = 0;
const long intervaloLeitura = 50;

void setup() {
  Serial.begin(115200);

  pinMode(MOTOR_ESQ, OUTPUT);
  pinMode(MOTOR_DIR, OUTPUT);
  pinMode(PINO_BUZZER, OUTPUT);

  analogWrite(MOTOR_ESQ, 0);
  analogWrite(MOTOR_DIR, 0);
  digitalWrite(PINO_BUZZER, LOW);

  pinMode(XSHUT_ESQ, OUTPUT);
  pinMode(XSHUT_DIR, OUTPUT);

  digitalWrite(XSHUT_ESQ, LOW);
  digitalWrite(XSHUT_DIR, LOW);
  delay(10);

  Wire.begin(PINO_SDA, PINO_SCL);

  digitalWrite(XSHUT_ESQ, HIGH);
  delay(10);
  if (!sensorEsq.begin(0x30)) {
    Serial.println(F("ERRO: Falha no Sensor Esquerdo!"));
    while(1);
  }

  digitalWrite(XSHUT_DIR, HIGH);
  delay(10);
  if (!sensorDir.begin(0x29)) {
    Serial.println(F("ERRO: Falha no Sensor Direito!"));
    while(1);
  }

  Serial.println(F("Sistema Inicializado. Iniciando medições..."));
}

void loop() {
  unsigned long tempoAtual = millis();

  if (tempoAtual - tempoAnterior >= intervaloLeitura) {
    tempoAnterior = tempoAtual;

    VL53L0X_RangingMeasurementData_t medidaEsq;
    VL53L0X_RangingMeasurementData_t medidaDir;

    sensorEsq.rangingTest(&medidaEsq, false);
    sensorDir.rangingTest(&medidaDir, false);

    int distEsq = medidaEsq.RangeStatus != 4 ? medidaEsq.RangeMilliMeter : 8000;
    int distDir = medidaDir.RangeStatus != 4 ? medidaDir.RangeMilliMeter : 8000;

    int forcaMotorEsq = 0;
    int forcaMotorDir = 0;

    if (distEsq <= DISTANCIA_MAXIMA && distEsq > 0) {
      if (distEsq <= DISTANCIA_MINIMA) {
        forcaMotorEsq = 255;
      } else {
        forcaMotorEsq = map(distEsq, DISTANCIA_MAXIMA, DISTANCIA_MINIMA, 50, 255);
      }
    }

    if (distDir <= DISTANCIA_MAXIMA && distDir > 0) {
      if (distDir <= DISTANCIA_MINIMA) {
        forcaMotorDir = 255;
      } else {
        forcaMotorDir = map(distDir, DISTANCIA_MAXIMA, DISTANCIA_MINIMA, 50, 255);
      }
    }

    analogWrite(MOTOR_ESQ, forcaMotorEsq);
    analogWrite(MOTOR_DIR, forcaMotorDir);

    if ((distEsq <= DISTANCIA_CRITICA && distEsq > 0) || (distDir <= DISTANCIA_CRITICA && distDir > 0)) {
      digitalWrite(PINO_BUZZER, HIGH);
    } else {
      digitalWrite(PINO_BUZZER, LOW);
    }
  }
}
