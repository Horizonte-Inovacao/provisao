# Programa da placa (firmware)

Aqui fica o programa que roda na placa ESP32-C3 do boné. Mantivemos o nome da pasta e das subpastas em inglês porque a ferramenta que compila o programa, o PlatformIO, procura exatamente por `src/` e `include/`.

| Onde | O que tem |
|---|---|
| [`src/main.cpp`](src/main.cpp) | A lógica: lê os sensores, decide o nível de alerta, vibra os motores e toca o bipe |
| [`include/config.h`](include/config.h) | Todos os ajustes: pinos, distâncias de cada nível e força da vibração |
| [`platformio.ini`](platformio.ini) | Configuração da compilação (placa, bibliotecas, velocidade da comunicação) |
| [`legado/`](legado/) | O programa original da V1, guardado para consulta |

## Como compilar e gravar

Você precisa do [PlatformIO](https://platformio.org/) instalado (ele funciona sozinho ou dentro do VS Code).

```bash
cd firmware
pio run                 # compila
pio run -t upload       # grava na placa pelo cabo USB-C
pio device monitor      # mostra as mensagens da placa
```

**Antes de gravar, desligue a chave do boné** (ou desencaixe a bateria). A explicação está em [`documentacao/seguranca.md`](../documentacao/seguranca.md).

## Como calibrar

Tudo o que é ajuste fica em `include/config.h`. Por exemplo, para o boné começar a vibrar mais longe, aumente `DIST_NIVEL_1`. Para vibrar mais forte, aumente os valores de `DUTY_NIVEL`, lembrando que os motores são de 1 a 3 V e por isso existe um teto. Combinamos que a lógica em `main.cpp` não recebe números soltos: se é ajuste, vai para o `config.h`.

## Verificação automática

A cada alteração nesta pasta, o GitHub compila o programa sozinho (arquivo [`.github/workflows/firmware.yml`](../.github/workflows/firmware.yml)). Se a compilação falhar, a alteração aparece marcada com erro.

## Licença

O programa da V1.5 está sob a GNU GPL 3.0, com o texto completo em [`LICENSE`](LICENSE). A V1, guardada em `legado/`, continua sob a licença MIT com que foi publicada ([`legado/LICENSE-MIT`](legado/LICENSE-MIT)).
