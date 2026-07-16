# Como contribuir

A PróVisão é um projeto aberto de tecnologia assistiva mantido por três estudantes de Caruaru-PE. Contribuições são bem-vindas — de código a relatos de teste.

## Por onde começar

- **Achou um problema ou tem uma ideia?** Abra uma [Issue](../../issues) descrevendo o contexto. Para bugs de firmware, inclua a saída do monitor serial.
- **Quer contribuir com código ou CAD?** Fork → branch descritiva (`correcao-leitura-i2c`, `case-tampa-snapfit`) → Pull Request pequeno e focado.
- **Testou o dispositivo?** Relatos de uso real valem muito para nós, abra uma Issue com o rótulo `relato-de-campo`.

## Regras da casa

1. O firmware compila com `pio run` antes de qualquer PR.
2. Ajustes de calibração vão em `firmware/include/config.h`, nunca espalhados pela lógica.
3. Mudança de hardware exige atualizar o esquemático e a BOM juntos.
4. Fotos de pessoas só entram no repositório com autorização de imagem assinada, sem exceção. Este projeto atende pessoas com deficiência visual e levamos privacidade a sério (LGPD).
5. Segurança vem antes de recurso novo: nada que comprometa o alerta ao usuário entra no produto.

## Contato

**Horizonte Inovação Assistiva** — Caruaru, PE.

* 📧 **E-mail:** [contato.horizonteinovacao@gmail.com](mailto:contato.horizonteinovacao@gmail.com)
