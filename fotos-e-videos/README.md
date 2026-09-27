# Fotos e vídeos do projeto

Aqui ficam as fotos e os vídeos que contam a história da PróVisão. Antes de colocar qualquer arquivo, combinamos duas regras:

1. **Pessoas que dá para reconhecer só entram com autorização de imagem assinada.** Isso vale para participantes da ACACE, colegas e professores. Sem autorização, a foto não é publicada.
2. **Reduza o arquivo antes de subir.** Foto com até 1 MB, vídeo curto ou convertido em GIF. Os arquivos originais, pesados, ficam na pasta `fotos-e-videos/originais/`, que o Git ignora de propósito.

## Como nomear os arquivos

`ANO-MES-DIA-descricao-curta.extensao`, por exemplo `2026-05-20-apresentacao-em-sala.jpg`.

## O que já temos para adicionar

- [ ] Fotos da apresentação final em sala (2026.1, nota máxima)
- [ ] Vídeos de colegas usando o dispositivo em sala
- [ ] Fotos do protótipo V1 na placa de testes (bancada)
- [ ] Registros da atividade com a ACACE *(conferir as autorizações antes)*
- [ ] Logo e aplicações do manual de marca (exportar do PDF)
- [ ] Fotos da montagem da V1.5 no boné

## Onde cada mídia aparece

| Mídia | Aparece em |
|---|---|
| Foto principal do protótipo em uso | `README.md` (topo). Copie também para `documentacao/imagens/prototipo-em-uso.jpg` |
| GIF do boné funcionando | `README.md`, na seção "Registro em imagens" |
| Fotos de bancada e do percurso | `HISTORICO.md` e `documentacao/protocolo-de-testes.md` |
| Logo | `README.md` (topo) |

Depois de adicionar um arquivo, procure pelas marcações `[MÍDIA]` no repositório (`grep -r "MÍDIA" .`). Elas mostram todos os lugares que estão esperando uma imagem.
