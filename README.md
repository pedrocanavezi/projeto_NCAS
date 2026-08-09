# Núcleo Cognitivo da Aurora Siger (NCAS)

**Integrante:** Pedro Henrique Canavezi  
**RM:** 570298

## Visão geral

O NCAS é um protótipo em Python para registrar, organizar, consultar e
interpretar informações operacionais da colônia espacial Aurora Siger. O
sistema funciona pelo terminal, preserva dados em arquivos TXT e JSON e simula
um assistente inteligente sem utilizar APIs externas.

## Como executar

1. Instale Python 3.10 ou superior.
2. Mantenha todos os arquivos na mesma pasta.
3. Abra o terminal nessa pasta.
4. Execute `python codigo_fonte.py` (ou `python3 codigo_fonte.py`).

O sistema usa apenas módulos da biblioteca padrão do Python.

## Organização e justificativa dos dados

- **registros_colonia.txt:** guarda logs sequenciais e legíveis por pessoas.
  TXT é adequado porque cada nova ocorrência pode ser acrescentada ao final
  com o modo append, sem necessidade de reorganizar os registros anteriores.
- **dados_colonia.json:** guarda módulos, alertas, configurações e interações em
  listas de dicionários. JSON é adequado para dados estruturados, pois preserva
  chaves, valores, números, textos e booleanos, além de facilitar buscas por ID.

## Funcionalidades do menu

1. Cadastra registros no arquivo texto com `open(..., "a")`.
2. Consulta registros usando `readline()` e `readlines()`.
3. Cadastra alertas e salva listas de dicionários em JSON.
4. Carrega e exibe os dados estruturados do JSON.
5. Analisa um alerta com regras booleanas simplificadas.
6. Gera tabelas-verdade para comprovar as equivalências lógicas.
7. Exibe prompts zero-shot, few-shot e uma saída estruturada.
8. Simula uma resposta inteligente e preserva o histórico no JSON.
9. Compara um prompt vago e um prompt otimizado por meio do MSE.
10. Relaciona o projeto a memória, armazenamento e fluxo de dados.

Na inicialização, o modo `x` cria arquivos ausentes. O modo `w` sobrescreve o
JSON após uma atualização, `r` realiza leituras, `a` acrescenta logs e `r+`
permite conferir e ajustar a quebra de linha final. O gerenciador `with` fecha
os arquivos mesmo se uma operação falhar.

## Regras lógicas

### Regra de geração de alerta

Forma original:

`ALERTA = (FALHA AND CRITICO) OR (FALHA AND NOT CRITICO)`

Simplificação:

`ALERTA = FALHA AND (CRITICO OR NOT CRITICO)`  
`ALERTA = FALHA AND 1`  
`ALERTA = FALHA`

Logo, uma falha gera alerta independentemente de ser crítica. O grau crítico é
usado depois para definir a prioridade da resposta.

### Regra de bloqueio por De Morgan

`BLOQUEAR = NOT (SEGURANCA_OK AND DADOS_CONSISTENTES)`  
`BLOQUEAR = (NOT SEGURANCA_OK) OR (NOT DADOS_CONSISTENTES)`

Uma operação é bloqueada se pelo menos uma das duas condições necessárias não
for satisfeita.

## Prompts e simulação de IA

O protótipo não treina nem chama um modelo real. Ele demonstra conceitos de
engenharia de prompt e produz respostas determinísticas com regras locais. O
zero-shot fornece instruções sem exemplos. O few-shot inclui exemplos de
entrada e saída. Ambos definem contexto, restrições e formato JSON.

A comparação de prompts usa notas didáticas de clareza, aderência ao formato e
segurança. O erro quadrático médio (MSE) diminui quando o prompt é aprimorado.
Isso representa uma avaliação de qualidade, não treinamento real do modelo.

## Memória, armazenamento e fluxo

As entradas ficam temporariamente na RAM durante a execução. Ao gravar TXT ou
JSON, os dados são codificados em bytes, transportados entre processador,
memória e dispositivo de armazenamento e permanecem no disco após o programa
ser fechado. Em uma leitura posterior, os bytes voltam à memória, o Python
reconstrói textos, listas e dicionários, e o processador aplica as regras.

## Diversidade, ética e responsabilidade

O NCAS nunca deve substituir a decisão humana em situações críticas. Dados
históricos incompletos ou enviesados podem produzir prioridades injustas,
inclusive ignorando necessidades de grupos minoritários da tripulação. A equipe
de desenvolvimento deve ser diversa, revisar linguagem discriminatória, testar
o sistema com cenários variados, registrar justificativas e permitir contestar
decisões. Por isso, a saída estruturada sempre inclui `revisao_humana: true`.
Nenhuma característica étnica, racial ou pessoal é usada para priorizar
atendimento; a decisão considera apenas condições técnicas e risco operacional.

## Checklist antes de entregar

- Confirmar nome completo e RM nos documentos do projeto.
- Executar o sistema e confirmar as opções principais.
- Gravar um vídeo de no máximo 5 minutos usando o roteiro incluído.
- Publicar o vídeo no YouTube como **Não listado**.
- Substituir o marcador de `link_video.txt` pelo link verdadeiro.
- Compactar novamente a pasta depois de inserir o link.
