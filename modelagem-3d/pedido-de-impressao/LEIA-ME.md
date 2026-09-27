# Pedido de impressão 3D

Este é o pacote que mandamos para o serviço de impressão. Comece pela [`ficha-do-pedido.pdf`](ficha-do-pedido.pdf): ela explica o material, a configuração e o que vamos conferir na entrega.

- [`lote-1-teste-de-encaixe/`](lote-1-teste-de-encaixe/): poucas peças, para conferir os encaixes com os componentes reais.
- [`lote-2-kit-completo/`](lote-2-kit-completo/): todas as peças de um boné.

Cada lote tem um arquivo 3MF por material (PETG e TPU), com as peças já distribuídas na mesa, e a pasta `stl` com uma peça por arquivo. O número depois de `_x` no nome é a quantidade.

Para refazer este pacote depois de mudar alguma medida, rode `python3 gerar_pecas.py` e depois `python3 gerar_pedido_impressao.py` na pasta [`codigo/`](../codigo/).
