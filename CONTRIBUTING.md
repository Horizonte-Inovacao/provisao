# Como contribuir

A PróVisão é um projeto aberto de tecnologia assistiva, mantido por três estudantes de Caruaru-PE. Toda ajuda é bem-vinda, do código a um relato de teste.

## Por onde começar

- **Achou um problema ou teve uma ideia?** Abra uma [Issue](../../issues) explicando o contexto. Se for um problema no programa da placa, cole junto as mensagens que aparecem no monitor (`pio device monitor`).
- **Quer mexer no código ou nas peças 3D?** Faça uma cópia do repositório (fork), crie um ramo com um nome que explique a mudança (por exemplo `correcao-leitura-sensor` ou `tampa-com-encaixe`) e abra um pedido de alteração (Pull Request) pequeno e focado.
- **Testou o boné?** Relatos de uso real valem muito para nós. Abra uma Issue com o rótulo `relato-de-campo`.

## Nossos combinados

1. O programa da placa precisa compilar com `pio run` antes de qualquer pedido de alteração.
2. Ajustes de calibração vão em `firmware/include/config.h`, nunca espalhados pela lógica.
3. Mudou o circuito? Atualize juntos o [esquema elétrico](eletronica/esquema-eletrico.md) e a [lista de materiais](eletronica/lista-de-materiais.csv).
4. Mudou uma peça 3D? Troque a medida em [`medidas.py`](modelagem-3d/codigo/pecas/medidas.py), rode `python3 verificar_encaixes.py` e gere os arquivos de novo com `python3 gerar_pecas.py`.
5. Tomou uma decisão que muda o rumo do projeto? Registre em [`documentacao/decisoes/`](documentacao/decisoes/).
6. Fotos de pessoas só entram no repositório com autorização de imagem assinada, sem exceção. Este projeto atende pessoas com deficiência visual e levamos a privacidade a sério, como pede a Lei Geral de Proteção de Dados.
7. Segurança vem antes de funcionalidade nova: nada que comprometa o alerta ao usuário entra no produto.
8. Ao enviar uma contribuição, você concorda em publicá-la sob a licença da pasta que ela altera: GNU GPL 3.0 no programa da placa, CERN-OHL-S 2.0 na eletrônica e nas peças 3D e CC BY-NC-SA 4.0 na documentação. O resumo está no [LICENSE](LICENSE).
9. Arquivo novo de código começa com o aviso de autoria e licença no padrão SPDX, igual aos que já existem. Por exemplo, no programa da placa: `// SPDX-License-Identifier: GPL-3.0-only`.

## Como escrevemos

Escrevemos a documentação na primeira pessoa do plural, contando o que decidimos e por quê. Evitamos siglas e termos técnicos sem explicação visando uma comunicação mais clara e acessível, onde se um termo for inevitável, explicamos na primeira vez que ele aparece.

## Contato

**Horizonte Inovação Assistiva**, Caruaru, PE.

* **E-mail:** [contato.horizonteinovacao@gmail.com](mailto:contato.horizonteinovacao@gmail.com)
