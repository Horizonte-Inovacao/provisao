// ============================================================
// PróVisão — firmware V1.5
// Horizonte Inovação Assistiva · 2026
//
// Evolução de segurança sobre a V1 (preservada em firmware/legado/):
//  1. Teto de PWM nos motores — os vibracall são de 1–3 V e o
//     trilho é a tensão da bateria; a V1 mandava 100% do duty.
//  2. Níveis DISCRETOS de vibração com kick-start — a rampa
//     contínua da V1 gerava duty abaixo do limiar de partida do
//     motor, e o usuário não sentia nada na faixa distante.
//  3. Falha de sensor agora é AUDÍVEL e recuperável — a V1
//     travava em silêncio (while(1)), e para um usuário cego um
//     dispositivo mudo é indistinguível de um funcionando.
// ============================================================

#include <Wire.h>
#include "Adafruit_VL53L0X.h"
#include "config.h"

Adafruit_VL53L0X sensorEsq = Adafruit_VL53L0X();
Adafruit_VL53L0X sensorDir = Adafruit_VL53L0X();

// Estado de cada motor para controlar nível e kick-start
struct EstadoMotor {
  uint8_t  pino;
  uint8_t  nivel;       // 0 (desligado) a 3 (forte)
  uint32_t inicioKick;  // millis() em que o nível subiu
};

EstadoMotor motorEsq = { MOTOR_ESQ, 0, 0 };
EstadoMotor motorDir = { MOTOR_DIR, 0, 0 };

uint32_t tempoAnterior = 0;

// ------------------------------------------------------------
// Padrão sonoro de erro: 3 bipes longos.
// Usado quando um sensor não inicializa — o usuário precisa
// SABER que o dispositivo não está protegendo.
// ------------------------------------------------------------
void bipeDeErro() {
  for (int i = 0; i < 3; i++) {
    digitalWrite(PINO_BUZZER, HIGH);
    delay(400);
    digitalWrite(PINO_BUZZER, LOW);
    delay(200);
  }
}

// Dois bipes curtos: sistema pronto.
void bipeDePronto() {
  for (int i = 0; i < 2; i++) {
    digitalWrite(PINO_BUZZER, HIGH);
    delay(80);
    digitalWrite(PINO_BUZZER, LOW);
    delay(80);
  }
}

// ------------------------------------------------------------
// Sequência de inicialização dos dois VL53L0X.
// Eles nascem com o mesmo endereço (0x29), então usamos os
// pinos XSHUT para acordá-los um de cada vez e dar um endereço
// novo ao primeiro. Retorna false se qualquer um falhar.
// ------------------------------------------------------------
bool iniciarSensores() {
  digitalWrite(XSHUT_ESQ, LOW);
  digitalWrite(XSHUT_DIR, LOW);
  delay(10);

  digitalWrite(XSHUT_ESQ, HIGH);
  delay(10);
  if (!sensorEsq.begin(ADDR_SENSOR_ESQ)) {
    Serial.println(F("ERRO: sensor esquerdo nao respondeu."));
    return false;
  }

  digitalWrite(XSHUT_DIR, HIGH);
  delay(10);
  if (!sensorDir.begin(ADDR_SENSOR_DIR)) {
    Serial.println(F("ERRO: sensor direito nao respondeu."));
    return false;
  }
  return true;
}

// Converte distância (mm) em nível de vibração (0 a 3).
uint8_t nivelPorDistancia(int dist_mm) {
  if (dist_mm <= 0)            return 0;   // leitura inválida
  if (dist_mm <= DIST_NIVEL_3) return 3;
  if (dist_mm <= DIST_NIVEL_2) return 2;
  if (dist_mm <= DIST_NIVEL_1) return 1;
  return 0;
}

// ------------------------------------------------------------
// Aplica o nível ao motor com kick-start: ao ENTRAR num nível
// mais alto, o motor recebe um pulso curto em duty máximo para
// vencer a inércia e então assenta no duty do nível.
// ------------------------------------------------------------
void atualizarMotor(EstadoMotor &m, uint8_t novoNivel, uint32_t agora) {
  if (novoNivel > m.nivel) {
    m.inicioKick = agora;  // subiu de nível: dispara o empurrão
  }
  m.nivel = novoNivel;

  uint8_t duty;
  if (m.nivel > 0 && (agora - m.inicioKick) < KICK_MS) {
    duty = DUTY_KICK;
  } else {
    duty = DUTY_NIVEL[m.nivel];
  }
  analogWrite(m.pino, duty);
}

void setup() {
  Serial.begin(115200);

  pinMode(MOTOR_ESQ, OUTPUT);
  pinMode(MOTOR_DIR, OUTPUT);
  pinMode(PINO_BUZZER, OUTPUT);
  pinMode(XSHUT_ESQ, OUTPUT);
  pinMode(XSHUT_DIR, OUTPUT);

  analogWrite(MOTOR_ESQ, 0);
  analogWrite(MOTOR_DIR, 0);
  digitalWrite(PINO_BUZZER, LOW);

  Wire.begin(PINO_SDA, PINO_SCL);

  // Diferente da V1: se um sensor falhar, o dispositivo AVISA
  // com bipes e tenta de novo — nunca trava em silêncio.
  while (!iniciarSensores()) {
    bipeDeErro();
    delay(RETRY_SENSOR_MS);
  }

  Serial.println(F("PróVisão V1.5 iniciada."));
  bipeDePronto();
}

void loop() {
  uint32_t agora = millis();
  if (agora - tempoAnterior < INTERVALO_LEITURA_MS) return;
  tempoAnterior = agora;

  VL53L0X_RangingMeasurementData_t medidaEsq;
  VL53L0X_RangingMeasurementData_t medidaDir;
  sensorEsq.rangingTest(&medidaEsq, false);
  sensorDir.rangingTest(&medidaDir, false);

  // RangeStatus 4 = fora de alcance; tratamos como "longe".
  int distEsq = (medidaEsq.RangeStatus != 4) ? medidaEsq.RangeMilliMeter : 8000;
  int distDir = (medidaDir.RangeStatus != 4) ? medidaDir.RangeMilliMeter : 8000;

  atualizarMotor(motorEsq, nivelPorDistancia(distEsq), agora);
  atualizarMotor(motorDir, nivelPorDistancia(distDir), agora);

  // Proximidade crítica em qualquer lado dispara o buzzer.
  bool critico = (distEsq > 0 && distEsq <= DIST_CRITICA) ||
                 (distDir > 0 && distDir <= DIST_CRITICA);
  digitalWrite(PINO_BUZZER, critico ? HIGH : LOW);

  // TODO (V2): interface ITelemetry — registrar distâncias,
  // níveis e tensão da bateria para análise pós-teste.
}
