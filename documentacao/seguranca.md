# Segurança: leia antes de usar

Escrevemos esta página porque a PróVisão é usada por pessoas que não conseguem conferir, pela visão, o estado do equipamento. Isso muda o nosso nível de exigência. Aqui, segurança não é uma seção obrigatória de manual: é uma regra de projeto.

## O que a PróVisão é (e o que não é)

- É um **protótipo experimental** em fase de validação, que complementa a bengala branca.
- **Não substitui a bengala**, o cão-guia nem nenhum outro recurso de mobilidade que a pessoa já usa. Nos nossos testes, o participante sempre usa a bengala junto com o boné.
- Não é um dispositivo médico certificado. Todo uso acontece em **teste acompanhado**, com uma pessoa da equipe junto, num percurso conhecido e seguro.

## Regras da bateria

Trocamos a bateria da V1 (uma célula mole, tipo "pastilha") por uma bateria 14500 com carcaça de aço e proteção interna. Mesmo assim, algumas regras não mudam:

1. **Nunca carregar com o boné na cabeça.** Carregue com o boné em cima de uma superfície firme e que não pegue fogo, como uma mesa ou um piso.
2. **Carregador esquentando além de morno:** tire da tomada e investigue antes de usar de novo. Ajustamos o carregador para 400 mA, que é a corrente certa para essa bateria.
3. **Bateria amassada, estufada, vazando ou esquentando sozinha:** ela sai de uso na hora e vai para o descarte de pilhas e baterias (ecoponto).
4. **Os furinhos do case da bateria não podem ser tampados.** Eles ficam em cima do polo positivo e apontam para fora da cabeça. Se a bateria algum dia precisar soltar gás, ele sai para longe do usuário.
5. **Nunca soldar com a bateria conectada.** Desencaixe o conector da bateria antes de qualquer solda.
6. **No cabo da bateria existe um fusível que se rearma sozinho.** Se acontecer um curto, ele corta a corrente e volta a funcionar quando esfria. Não retire esse fusível.

## Regra da gravação do programa

A placa ESP32-C3 tem uma entrada USB-C própria, que fica fechada dentro do case de propósito. **Só grave o programa com a chave do boné desligada ou com a bateria desconectada.** Com a chave ligada, a energia do cabo USB encontra a energia da bateria no mesmo circuito, e isso pode danificar a bateria.

## Conforto e higiene

- Nenhuma peça de plástico impresso encosta direto na pele. As placas internas têm uma almofada de EVA, e os motores ficam dentro de um bolsinho de tecido costurado na faixa interna.
- Entre um participante e outro, limpe a faixa interna, as almofadas e os bolsinhos com álcool 70%.
- Depois de cada sessão, **alguém da equipe confere a pele do participante** nos pontos de contato (nuca e laterais da cabeça). A pessoa não consegue ver uma marca vermelha, então essa conferência é nossa.

## Como o boné avisa que algo deu errado

O boné **avisa quando não está protegendo**:

- **dois bipes curtos ao ligar:** tudo pronto;
- **três bipes longos repetidos:** um sensor falhou. O boné fica tentando se recuperar e os bipes param quando ele volta;
- **ligou e ficou em silêncio:** considere o boné desligado ou com defeito, e não use.

## Privacidade nos testes

Dados de pessoas com deficiência são dados pessoais sensíveis pela Lei Geral de Proteção de Dados (LGPD). Por isso, nos testes:

- o participante sempre assina o Termo de Consentimento Livre e Esclarecido antes de começar;
- fotos e vídeos só com autorização de imagem assinada, à parte;
- os resultados são identificados só por um código de sessão (por exemplo, S03). A lista que liga nome e código fica guardada fora deste repositório.

## Encontrou um risco que não mapeamos?

Abra uma Issue com o rótulo `seguranca`. Esse tipo de contribuição passa na frente de qualquer outra.
