# Mídias do projeto

Aqui ficam as fotos e vídeos que contam a história da PróVisão. Antes de subir qualquer arquivo, dois combinados:

1. **Pessoas identificáveis só entram com autorização de imagem assinada** (participantes da ACACE, colegas, professores). Sem autorização, a foto não é publicada.
2. Comprimir antes de subir (foto ≤ 1 MB, vídeo curto ou convertido em GIF). Os arquivos brutos ficam fora do Git (pasta local `media/brutas/`, já ignorada no `.gitignore`).

## Convenção de nomes

`AAAA-MM-DD-descricao-curta.ext` → exemplo: `2026-05-20-apresentacao-em-sala.jpg`

## O que já temos para adicionar (checklist do acervo atual)

- [ ] Fotos da apresentação final em sala (2026.1 — nota máxima) → `<!-- [MÍDIA] arquivos aqui -->`
- [ ] Vídeo(s) de colegas operando o dispositivo em sala → `<!-- [MÍDIA] arquivos aqui -->`
- [ ] Fotos do protótipo V1 na protoboard (bancada) → `<!-- [MÍDIA] arquivos aqui -->`
- [ ] Registros da atividade com a ACACE *(conferir autorizações antes)* → `<!-- [MÍDIA] arquivos aqui -->`
- [ ] Logo e aplicações do manual de marca (exportar do PDF) → `<!-- [MÍDIA] arquivos aqui -->`

## Onde cada mídia é usada

| Mídia | Aparece em |
|---|---|
| Foto principal do protótipo em uso | `README.md` (topo) — copiar para `docs/assets/prototipo-em-uso.jpg` |
| GIF do dispositivo funcionando | `README.md` (seção "Registro em imagens") |
| Fotos de bancada e percurso | `CHANGELOG.md` e `docs/protocolo-de-testes.md` |
| Logo | `README.md` (topo) |

Depois de adicionar um arquivo, procure pelos marcadores `[MÍDIA]` no repositório (`grep -r "MÍDIA" .`) para encontrar todos os lugares que estão esperando conteúdo.
