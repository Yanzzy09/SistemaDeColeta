# Briefing — Volta

## 1. Contexto do negócio

O Volta conecta moradores a uma cooperativa de coleta seletiva. A cooperativa busca os materiais recicláveis na casa do morador. Cada quilo pesado gera pontos, que futuramente poderão ser trocados por descontos no comércio do bairro.

Hoje, o agendamento acontece por telefone e os pontos são controlados em uma planilha que o morador não consegue consultar.

## 2. Objetivo do produto

Permitir que o morador agende e acompanhe suas coletas pelo celular e que a cooperativa organize a rota do dia e registre as pesagens pelo computador. O agendamento, a coleta, a pesagem e os pontos devem fazer parte do mesmo fluxo de dados.

## 3. Personas

### Joana — moradora

- 45 anos, professora, separa recicláveis em casa.
- Usa principalmente o celular.
- Precisa agendar uma coleta em poucos passos, informando endereço, dia e materiais.
- Quer acompanhar a situação de cada coleta.
- Quer consultar o que foi pesado e quantos pontos cada entrega rendeu.
- Problema central: depende de ligação e não consegue consultar a planilha de pontos.

### Osmar — coordenador da cooperativa

- Organiza a rota do caminhão e acompanha a balança no galpão.
- Usa principalmente o computador.
- Precisa visualizar as coletas de um dia e filtrar a rota.
- Registra o material e os quilos de cada pesagem.
- Confere o total de pontos calculado para cada coleta.
- Problema central: precisa organizar a operação e registrar a pesagem sem perder o controle dos pontos.

## 4. Fluxos principais

### Fluxo da moradora

1. Informa endereço, dia e materiais separados.
2. Envia o agendamento.
3. Consulta suas coletas e a situação de cada uma.
4. Abre uma coleta concluída.
5. Consulta materiais pesados, quilos e pontos.

### Fluxo da cooperativa

1. Seleciona ou filtra um dia.
2. Visualiza as coletas da rota.
3. Abre uma coleta na chegada do material.
4. Registra material e quilos.
5. Confere os pontos somados.

## 5. Entidades do domínio

- **Usuário:** pessoa que acessa o sistema, com tipo `morador` ou `cooperativa`.
- **Coleta:** pertence a um morador e guarda endereço, dia, materiais, situação e total de pontos.
- **Pesagem:** pertence a uma coleta e guarda material, quilos e pontos calculados.

## 6. Regra de pontuação

Uma coleta começa como **agendada**, com zero pontos. Ao registrar a primeira pesagem, passa para **coletada**.

| Material | Pontos por quilo |
| --- | ---: |
| Papel | 1 |
| Vidro | 1 |
| Plástico | 2 |
| Metal | 4 |

O serviço deve calcular os pontos. A interface pode apresentar o resultado, mas não deve substituir a regra do backend.

## 7. Telas previstas

### Moradora — celular

- **Agendar coleta:** formulário de endereço, dia e materiais.
- **Minhas coletas:** lista de coletas, situações, pesagens e pontos.

### Cooperativa — computador

- **A rota:** lista de coletas com filtro por dia e por morador.
- **A balança:** registro de material e quilos, com conferência dos pontos.

As telas devem funcionar nos dois tamanhos, com prioridade de usabilidade no dispositivo principal de cada persona.

## 8. Escopo atual

### Incluído

- Cadastro e identificação de usuários.
- Separação de permissões entre morador e cooperativa.
- Agendamento de coletas.
- Consulta de coletas e pesagens.
- Registro de pesagens.
- Cálculo de pontos no serviço.
- Persistência das entidades em banco de dados.

### Fora do escopo

- Troca de pontos por descontos.
- Mapa da rota.
- Pagamentos.
- Avisos por mensagem.

## 9. Evolução planejada

- **Ciclo 2:** retirar dados da memória e persistir no MySQL.
- **Ciclo 4:** autenticar usuários e restringir a moradora às próprias coletas.
- **Ciclo 5:** investigar e incluir uma funcionalidade de IA que ajude um problema real do fluxo, mantendo revisão humana antes de gravar qualquer resultado.

## 10. Critérios de sucesso

- Joana consegue agendar sem ligação ou planilha.
- Joana consegue acompanhar a situação e os pontos das próprias coletas.
- Osmar consegue organizar as coletas de um dia.
- Osmar registra pesagens sem recalcular pontos manualmente.
- O total de pontos é consistente entre pesagens, coleta e tela do morador.
- Um usuário não acessa dados de outro grupo fora das permissões definidas.

## Fonte

Este briefing consolida o conteúdo de `docs/CARTILHA.md` e `docs/CARTILHA_2 1.md`. As duas cartilhas apresentam o mesmo negócio, personas, entidades, telas, regras e limites de escopo.
