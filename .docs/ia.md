# Funcionalidade planejada — revisão assistida da coleta

**Status:** planejada

## Objetivo

Ajudar a conferir se os materiais agendados pela moradora correspondem aos materiais registrados na pesagem, explicando possíveis diferenças antes da confirmação final da entrega.

## Problema atendido

Joana agenda uma coleta com determinados materiais. Depois, Osmar registra o que foi pesado. Quando os dois registros divergem, a pessoa precisa perceber a diferença e decidir se os dados estão corretos.

Esta funcionalidade reduz a conferência manual e torna os pontos mais compreensíveis para a moradora.

## Personas e responsabilidades

### Joana — moradora

- agenda a coleta;
- lê a revisão apresentada;
- confirma a entrega por um botão;
- pode discordar e devolver a coleta para revisão.

### Osmar — cooperativa

- registra os materiais e os quilos;
- recebe a coleta devolvida para revisão;
- corrige os dados da pesagem quando necessário.

### Backend

- calcula os pontos pela regra oficial;
- controla os estados da coleta;
- valida a resposta da IA;
- grava a confirmação e a revisão;
- não aceita que a IA altere diretamente pontos ou pesagens.

### IA

- compara os materiais agendados com os materiais pesados;
- identifica possíveis divergências;
- produz uma explicação curta em linguagem clara;
- sugere a mensagem exibida para Joana.

## Fluxo planejado

1. Joana agenda endereço, dia e materiais.
2. Osmar registra cada material e seu peso.
3. O backend calcula os pontos automaticamente.
4. A coleta muda para `aguardando_confirmacao`.
5. O backend envia à IA somente os dados estruturados necessários para a revisão.
6. A IA retorna divergências e uma explicação.
7. A explicação aparece na tela de detalhes e no histórico da coleta.
8. Joana escolhe o botão **Confirmar entrega** ou **Solicitar revisão**.
9. Se confirmar, a coleta passa para `coletada` e os pontos tornam-se definitivos.
10. Se solicitar revisão, Osmar corrige a pesagem.
11. A nova revisão substitui a mensagem visível anterior.
12. As versões anteriores ficam guardadas internamente para consulta e auditoria.

## Dados enviados à IA

Somente dados da coleta em revisão:

- materiais informados no agendamento;
- materiais pesados;
- quilos registrados;
- pontos calculados pelo backend;
- situação atual da coleta.

Não enviar senhas, tokens, chaves de API ou dados de outras pessoas.

## Regra que permanece no serviço

A IA não calcula nem decide a pontuação. O backend continua aplicando:

- papel: 1 ponto por quilo;
- vidro: 1 ponto por quilo;
- plástico: 2 pontos por quilo;
- metal: 4 pontos por quilo.

Uma sugestão da IA precisa de revisão humana. Se a IA não responder, o fluxo manual de Osmar continua disponível.

## Integração prevista

A primeira versão pode usar uma chamada única ao modelo, feita pelo backend depois da pesagem. O backend prepara os dados, envia a solicitação, valida a resposta e grava a revisão. Não há justificativa atual para separar o trabalho em múltiplos agentes.

O provedor será escolhido principalmente por facilidade técnica e custo. OpenAI, Claude, Gemini ou outro provedor compatível são candidatos; a decisão depende de uma comparação atual de API, custo, qualidade em português e política de dados. ?

## Decisões confirmadas

- haverá o estado `aguardando_confirmacao`;
- a confirmação será feita por botão;
- Joana é responsável pela confirmação;
- discordância devolve a coleta para Osmar;
- a correção substitui a mensagem visível;
- versões anteriores ficam armazenadas internamente;
- os pontos são provisórios até a confirmação;
- a mensagem aparece na tela e no histórico;
- a IA não altera dados automaticamente;
- a regra de pontuação permanece no backend.

## Pontos ainda não confirmados

- Qual formato terá o histórico de versões? ?
- Por quanto tempo as revisões anteriores serão mantidas? ?
- O que acontece se Joana nunca confirmar a coleta? ?
- Qual provedor será escolhido após a comparação de facilidade técnica e custo? ?
- Qual modelo de dados representará a mensagem e suas versões no backend? ?

