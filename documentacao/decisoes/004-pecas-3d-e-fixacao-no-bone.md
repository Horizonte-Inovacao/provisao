# 004. Peças 3D desenhadas em código e fixação no tecido

**Situação:** aceita · **Data:** setembro de 2026

## Contexto

Para o teste de campo precisávamos de cases para a eletrônica e para a bateria, suportes para os sensores na aba e berços para os motores. Tudo isso precisa se encaixar em componentes que ainda vamos medir com paquímetro, e em bonés que mudam de curva de um modelo para outro.

## Decisão

**Desenhamos as peças em código (Python, com a biblioteca CadQuery) em vez de desenhar à mão num programa de CAD.** Todas as medidas ficam num único arquivo, [`medidas.py`](../../modelagem-3d/codigo/pecas/medidas.py). Quando alguém mede um componente e a medida real é diferente, basta trocar o número e gerar as peças de novo. Um programa de verificação confere se alguma peça atravessa outra antes de qualquer impressão.

**A fixação no boné é um "sanduíche" através do tecido.** Por fora fica o case sobre uma base curva que acompanha a copa. Por dentro fica uma placa fina. Parafusos M2 atravessam o tecido e prendem as duas. Os parafusos ficam do lado de dentro, com a cabeça rente à placa, e nenhum deles fica perto da bateria.

**A base curva do case da eletrônica é uma peça separada.** Se o boné mudar, reimprimimos só a base, não o case inteiro.

**Os suportes dos sensores saem em três inclinações (0, 10 e 20 graus).** A aba aponta para baixo quando o boné está na cabeça, e o ângulo muda de pessoa para pessoa. No primeiro teste escolhemos a inclinação que deixa o sensor olhando reto para a frente.

**Padronizamos um único tamanho de parafuso (M2)** no projeto inteiro. Fica mais fácil comprar e montar.

## Consequências

**O que ganhamos:** peças que se ajustam trocando números, verificação automática de encaixe, arquivos abertos em formatos que qualquer programa de 3D lê e um pedido de impressão pronto para mandar a qualquer serviço.

**O que aceitamos:** para mexer na modelagem é preciso rodar Python. Para quem só quer ver ou medir, deixamos os arquivos prontos para abrir no FreeCAD, no Fusion ou no navegador.
