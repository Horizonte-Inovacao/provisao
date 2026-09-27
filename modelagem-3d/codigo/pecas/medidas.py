"""
Todas as medidas das peças 3D da PróVisão V1.5, em milímetros.

Combinamos que nenhum arquivo de peça tem número solto: tudo o que depende de
componente, da impressora ou do boné fica aqui. Assim, quando uma medida real
for diferente, trocamos só neste arquivo e geramos as peças de novo.

Os valores marcados com [MEDIR] são típicos de mercado. Confira com o
paquímetro no componente que vocês têm antes de imprimir a versão final.
"""

# --------------------------------------------------------------------------
# Impressão
# --------------------------------------------------------------------------
FOLGA = 0.3            # folga peça x componente (PETG, bico 0.4)
PAREDE = 2.0           # parede dos cases
PISO = 2.0             # piso dos cases
TAMPA = 2.0            # espessura da tampa
R_CANTO = 4.0          # raio dos cantos verticais externos
R_BORDA = 1.2          # arredondamento das bordas externas

# --------------------------------------------------------------------------
# Boné
# --------------------------------------------------------------------------
R_COPA = 100.0         # [MEDIR] raio horizontal da copa na região dos cases
BASE_T_MIN = 3.0       # espessura mínima da base curva (no centro)
ABA_ESPESSURA = 4.0    # [MEDIR] espessura da aba do boné
PLACA_INTERNA_T = 1.6  # placa interna: fina para se moldar à cabeça
ESPUMA_PLACA_T = 3.0   # almofada de EVA colada no lado da cabeça das placas internas
ESPUMA_MOTOR_T = 2.0   # anel de EVA em volta de cada motor

# --------------------------------------------------------------------------
# Parafusos M2 (padrão único no projeto inteiro)
# --------------------------------------------------------------------------
M2_PILOTO = 1.7        # furo para rosquear M2 direto no PETG
M2_PASSANTE = 2.3
M2_CABECA_D = 4.4      # cabeça panela (3.8) + folga
M2_CABECA_H = 1.6
M2_ESCAREADO_D = 4.2   # cabeça chata/escareada 90 graus
M2_PORCA_S = 4.3       # porca M2: 4.0 entre faces + folga
M2_PORCA_H = 1.8

# --------------------------------------------------------------------------
# Case A: placa ilhada + ESP32-C3 + TP4056 + chave
# --------------------------------------------------------------------------
PLACA_X = 50.0         # placa ilhada cortada (5x7 -> 5x4)
PLACA_Y = 40.0
PLACA_T = 1.6
PLACA_FURO_INSET = 2.5 # centro dos furos de fixação a partir das bordas
PLACA_ESPACADOR = 3.0  # altura dos espaçadores (solda embaixo da placa)
# altura acima da placa: barra fêmea 8.5 + ESP32-C3 1.0 + USB-C 3.2 + margem 1.0
ALTURA_ACIMA_PLACA = 13.7

BUZZER_POS = (40.0, 30.0)   # centro do buzzer em coordenadas da placa
BUZZER_D = 12.0

TP_X = 17.3            # [MEDIR] largura do módulo TP4056 USB-C
TP_Y = 29.0            # [MEDIR] comprimento (borda do USB até o fim da placa)
TP_PCB_T = 1.2
TP_TRILHO_H = 1.5      # trilhos embaixo do módulo
USB_W = 9.0            # receptáculo USB-C
USB_H = 3.3
USB_ALTURA_CENTRO = 1.6  # centro do USB acima da face da placa do TP4056
USB_BALANCO = 0.8      # quanto o USB passa da borda da placa
PLUGUE_W = 13.0        # rebaixo externo para a capa do plugue
PLUGUE_H = 7.4
TP_LEDS = [(-2.5, 12.0), (2.5, 12.0)]  # [MEDIR] (x a partir do centro, y a partir da borda do USB)

CHAVE_CORTE_Y = 9.0    # KCD11: recorte 13.5 x 9
CHAVE_CORTE_Z = 13.5
CHAVE_PROF = 17.0      # corpo + terminais atrás do painel

CABO_SENSOR_D = 4.0    # cabo de 5 vias de cada sensor
CABO_MOTOR_D = 3.0
CABO_BAT_D = 3.5

# --------------------------------------------------------------------------
# Case B: célula Li-ion 14500 com tabs
# --------------------------------------------------------------------------
CEL_D = 14.5           # [MEDIR] com PCM e termo
CEL_L = 53.0           # [MEDIR] com tabs soldados
EVA_T = 1.0            # forro de EVA em volta da célula
EVA_PONTA = 1.5        # calço de EVA em cada ponta
FOLGA_FIO_PONTA = 2.0  # dobra do tab/fio na ponta positiva
PAREDE_B = 2.0
FUNDO_B = 2.5          # parede da ponta fechada (+)
TAMPA_B_L = 10.0       # comprimento da tampa de fechamento (fusível)
CANAL_FIO_W = 2.5      # canal lateral do fio do polo +
CANAL_FIO_P = 2.0

# --------------------------------------------------------------------------
# Suporte do sensor (GY-530 / VL53L0X)
# --------------------------------------------------------------------------
GY_X = 25.0            # [MEDIR] largura da placa GY-530
GY_Z = 10.7            # [MEDIR] altura
GY_T = 1.6
GY_BORDA_APOIO = 1.0   # faixa da borda que encosta na parede frontal
GY_ALIVIO = 1.5        # rebaixo para chip e componentes da frente
CHIP_OFF_Y = 0.0       # [MEDIR] centro do VL53L0X relativo ao centro da placa
CHIP_OFF_Z = 2.0       # [MEDIR] (positivo = para cima)
JANELA_W = 7.0         # janela na face do chip (chip 4.4 x 2.4 + margem)
JANELA_H = 4.6
MEIO_ANGULO_FOV = 20.0 # FOV do VL53L0X = 25 graus total; 20 de meio ângulo dá margem
POD_PAREDE = 2.0
POD_FRENTE = 2.5       # parede frontal (alívio + janela)
POD_MOLDURA = 2.5      # quanto a moldura avança à frente da parede frontal
POD_CAVIDADE = 5.0     # espaço atrás da placa para os fios soldados
POD_COLUNA = 4.0       # colunas dos parafusos da tampa
POD_BASE_T = 2.5
POD_INCLINACOES = [0, 10, 20]   # variantes de inclinação para cima (graus)
POD_ABERTURA_LATERAL = 10.0     # giro para fora (graus)

# --------------------------------------------------------------------------
# Berço do motor (vibracall moeda 1027), impresso em TPU 95A
# --------------------------------------------------------------------------
MOTOR_D = 10.0         # [MEDIR]
MOTOR_H = 2.7
BERCO_ABA_D = 28.0     # aba larga para costurar e espalhar a pressão
BERCO_ABA_T = 1.0
BERCO_ALTURA = 3.4     # altura total do berço (antes era 4,4 mm)
MOTOR_SALTO = 0.3      # quanto o motor fica para fora do berço, virado para a cabeça

# --------------------------------------------------------------------------
# Boné de referência (só para a montagem visual, não é impresso)
# Copa = meio elipsoide. Circunferência na base ~57 cm (tamanho M/G).
# --------------------------------------------------------------------------
BONE_A = 100.0         # semi-eixo frente-trás na base da copa
BONE_B = 80.0          # semi-eixo lateral
BONE_C = 105.0         # altura da copa
BONE_T = 1.5           # espessura do tecido
CARNEIRA_H = 30.0      # altura da carneira (faixa interna)
CARNEIRA_T = 3.0
REGULAGEM_R = 28.0     # abertura de regulagem na nuca (meio círculo)

ABA_PROF = 75.0        # quanto a aba avança à frente da copa
ABA_R_CURVA = 200.0    # curvatura lateral da aba (aba curva)
ABA_INCL = 12.0        # inclinação da aba para baixo (graus)
ABA_PHI = 80.0         # até onde a aba abraça a copa (parâmetro da elipse)

CANALETA_D = 7.0       # canaleta costurada por fora
CANALETA_Z = 9.0       # altura da canaleta nas laterais
CANALETA_PHI = 62.0    # onde a canaleta começa na frente (dos dois lados)
CANALETA_SOBE = 32.0   # quanto ela sobe na nuca para passar por cima da regulagem

# posições na montagem (phi = parâmetro da elipse: 0 frente, 90 esquerda, 180 nuca)
POS_CASE_A = (110.0, 40.0)    # (phi, altura do centro)
POS_CASE_B = (-110.0, 40.0)
POS_SENSOR_Y = 50.0           # distância lateral do centro da aba
POS_SENSOR_RECUO = 5.0        # moldura do sensor atrás da borda da aba
POS_MOTOR = (150.0, 16.0)     # (phi, altura) dos berços na carneira
INCL_SENSOR_MONTAGEM = 10     # variante do suporte usada na montagem
