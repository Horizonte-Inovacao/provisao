# Registro de avanços — PróVisão

Mantemos aqui a linha do tempo do projeto, do primeiro diagnóstico até hoje. As entradas mais recentes ficam no topo. Sempre que um marco tiver foto ou vídeo, o link para a mídia entra junto, toda evidência faz parte da história.

## [Em andamento] — V1.5

- Iniciada a construção da V1.5: migração da protoboard para placa soldada e case impresso em 3D, seguindo o plano de ação e o guia de construção do grupo.
- Correções de segurança elétrica definidas: ajuste da corrente de carga do TP4056 para a célula de 300 mAh, capacitores de desacoplamento, teto de PWM nos motores e alerta sonoro em caso de falha de sensor.
- Firmware V1.5 publicado em `firmware/src/` com níveis discretos de vibração e recuperação de falha (a V1 original está preservada em `firmware/legado/`).
<!-- [MÍDIA] adicionar fotos da bancada de construção da V1.5 conforme o trabalho avançar -->

## 2026-07-11 — Decisões de produto

- O projeto ganhou nome: **PróVisão**, primeiro produto da Horizonte Inovação Assistiva.
- Licenças definidas: MIT (firmware), CERN-OHL-P 2.0 (hardware), CC BY-SA 4.0 (documentação).
- Identidade visual consolidada conforme o manual de marca (Petróleo `#1B6C79`, Coral `#E07A5F`, Âmbar Sol `#EBA84C`, tipografia Poppins).
- Definido que a validação da V2 será em percurso interno/sombreado, respeitando o limite físico do sensor ToF sob sol direto.

## 2026-05 — Validação e encerramento da disciplina

- Apresentação final do projeto na disciplina de Programação de Microcontroladores (UniFavip Wyden) — **Com o projeto recebendo nota máxima**.
- Relatório final de extensão entregue à coordenação.
<!-- [MÍDIA] adicionar: fotos da apresentação em sala | vídeo dos colegas operando o dispositivo | registros da atividade com a ACACE (somente com autorização de imagem) -->

## 2026-04 — Prototipagem física

- Montagem do circuito na protoboard e fixação na aba da viseira; integração do firmware no ESP32-C3 e calibração de distância e tempo de resposta em laboratório.
- Primeiro contato de alinhamento com a ACACE e formalização da parceria (Carta de Apresentação e Termo de Aceite, 30/04/2026).
- Aprendizado registrado: a fixação com fita e fios expostos funcionou para demonstração, mas não é segura nem confortável para teste com usuários reais, onde essa limitação originou a V1.5.
<!-- [MÍDIA] adicionar fotos do protótipo V1 montado na viseira -->

## 2026-03 — Especificação e simulação

- Levantamento de requisitos e compra dos componentes (premissa de baixo custo mantida desde o início).
- Decisão de engenharia importante: troca do sensor ultrassônico HC-SR04 pelos sensores ToF a laser VL53L0X, ganhando precisão milimétrica e leitura independente por lado. Registrada em [docs/decisoes/ADR-001](docs/decisoes/ADR-001-troca-hcsr04-vl53l0x.md).
- Validação da lógica em simulador (Wokwi/Tinkercad) antes da montagem física.

## 2026-02 — Diagnóstico

- Formação do grupo e definição da problemática: os "obstáculos aéreos" que a bengala branca não detecta.
- Escolha da ACACE (Associação Caruaruense de Cegos e Amblíopes) como parceira e público participante do projeto de extensão.
- Pesquisa de referencial teórico em tecnologia assistiva, sistemas embarcados e sensoriamento.
