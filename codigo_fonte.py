"""
Nucleo Cognitivo da Aurora Siger (NCAS)

Protótipo acadêmico para registrar, consultar e interpretar informações
operacionais de uma colônia espacial.

Integrante: Pedro Henrique Canavezi
RM: 570298

O projeto utiliza apenas a biblioteca padrão do Python.
"""

import copy
import json
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_JSON = os.path.join(BASE_DIR, "dados_colonia.json")
ARQUIVO_TEXTO = os.path.join(BASE_DIR, "registros_colonia.txt")


DADOS_INICIAIS = {
    "metadados": {
        "sistema": "Núcleo Cognitivo da Aurora Siger",
        "sigla": "NCAS",
        "versao": "1.0",
        "descricao": "Protótipo para apoio às operações da colônia Aurora Siger.",
    },
    "modulos": [
        {
            "id": "MOD-001",
            "nome": "Suporte de Vida",
            "setor": "Essencial",
            "ativo": True,
            "seguranca_ok": True,
            "dados_consistentes": True,
            "status": "operacional",
        },
        {
            "id": "MOD-002",
            "nome": "Reator de Energia",
            "setor": "Essencial",
            "ativo": True,
            "seguranca_ok": False,
            "dados_consistentes": True,
            "status": "degradado",
        },
        {
            "id": "MOD-003",
            "nome": "Comunicações",
            "setor": "Operacional",
            "ativo": True,
            "seguranca_ok": True,
            "dados_consistentes": True,
            "status": "operacional",
        },
    ],
    "alertas": [
        {
            "id": "ALT-001",
            "modulo_id": "MOD-002",
            "tipo": "Superaquecimento",
            "prioridade": "critica",
            "falha": True,
            "critico": True,
            "resolvido": False,
            "data": "2026-08-09T18:00:00-03:00",
            "mensagem": "Temperatura do reator 18% acima do limite seguro.",
        },
        {
            "id": "ALT-002",
            "modulo_id": "MOD-003",
            "tipo": "Latência elevada",
            "prioridade": "media",
            "falha": True,
            "critico": False,
            "resolvido": False,
            "data": "2026-08-09T18:05:00-03:00",
            "mensagem": "Atraso de 420 ms no enlace com o centro de controle.",
        },
    ],
    "interacoes": [],
    "configuracao_assistente": {
        "idioma": "pt-BR",
        "formato_saida": "JSON",
        "exigir_revisao_humana": True,
        "api_externa": False,
    },
}


LINHAS_INICIAIS = [
    "REGISTROS OPERACIONAIS - AURORA SIGER\n",
    "Formato: data | categoria | módulo | mensagem\n",
    "2026-08-09T18:00:00-03:00 | ALERTA | Reator de Energia | "
    "Superaquecimento detectado.\n",
    "2026-08-09T18:05:00-03:00 | ALERTA | Comunicações | "
    "Latência acima do padrão.\n",
]


def agora_iso():
    """Retorna data e hora local no formato ISO 8601."""
    return datetime.now().astimezone().isoformat(timespec="seconds")


def inicializar_arquivos():
    """
    Cria os arquivos somente quando ainda não existem.

    O modo 'x' demonstra criação exclusiva. O método writelines() grava
    várias linhas no arquivo texto de uma vez.
    """
    try:
        with open(ARQUIVO_TEXTO, "x", encoding="utf-8") as arquivo:
            arquivo.writelines(LINHAS_INICIAIS)
    except FileExistsError:
        pass

    try:
        with open(ARQUIVO_JSON, "x", encoding="utf-8") as arquivo:
            json.dump(DADOS_INICIAIS, arquivo, ensure_ascii=False, indent=2)
    except FileExistsError:
        pass


def carregar_dados():
    """Carrega o arquivo JSON usando o modo de leitura 'r'."""
    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        inicializar_arquivos()
        return copy.deepcopy(DADOS_INICIAIS)
    except json.JSONDecodeError as erro:
        print(f"\n[ERRO] O JSON está inválido: {erro}")
        print("Uma cópia dos dados iniciais será usada apenas nesta execução.")
        return copy.deepcopy(DADOS_INICIAIS)


def salvar_dados(dados):
    """Sobrescreve o JSON no modo 'w' com uma estrutura válida e indentada."""
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def garantir_quebra_linha_final():
    """
    Usa o modo 'r+': lê e, se necessário, escreve no mesmo arquivo.
    O sinal '+' permite leitura e escrita sem apagar o conteúdo existente.
    """
    with open(ARQUIVO_TEXTO, "r+", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
        if conteudo and not conteudo.endswith("\n"):
            arquivo.write("\n")


def adicionar_linha_registro(categoria, modulo, mensagem):
    """Acrescenta uma linha ao final do TXT usando o modo append 'a'."""
    garantir_quebra_linha_final()
    linha = f"{agora_iso()} | {categoria} | {modulo} | {mensagem.strip()}\n"
    with open(ARQUIVO_TEXTO, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)


def ler_sim_nao(mensagem, padrao=True):
    """Lê uma resposta booleana com validação simples."""
    sufixo = " [S/n]: " if padrao else " [s/N]: "
    while True:
        resposta = input(mensagem + sufixo).strip().lower()
        if resposta == "":
            return padrao
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("Digite S para sim ou N para não.")


def proximo_id(itens, prefixo):
    """Gera um identificador sequencial, como ALT-003."""
    numeros = []
    for item in itens:
        try:
            numeros.append(int(item.get("id", "").split("-")[-1]))
        except (ValueError, AttributeError):
            continue
    return f"{prefixo}-{max(numeros, default=0) + 1:03d}"


def obter_modulo(dados, modulo_id):
    return next(
        (modulo for modulo in dados.get("modulos", []) if modulo["id"] == modulo_id),
        None,
    )


def selecionar_modulo(dados):
    modulos = dados.get("modulos", [])
    if not modulos:
        print("Nenhum módulo cadastrado.")
        return None

    print("\nMódulos disponíveis:")
    for indice, modulo in enumerate(modulos, start=1):
        print(f"  {indice}. {modulo['nome']} ({modulo['id']})")

    while True:
        escolha = input("Escolha o módulo: ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(modulos):
            return modulos[int(escolha) - 1]
        print("Opção inválida.")


def selecionar_alerta(dados):
    alertas = dados.get("alertas", [])
    if not alertas:
        print("Nenhum alerta cadastrado.")
        return None

    print("\nAlertas disponíveis:")
    for indice, alerta in enumerate(alertas, start=1):
        situacao = "resolvido" if alerta.get("resolvido") else "aberto"
        print(
            f"  {indice}. {alerta['id']} - {alerta['tipo']} "
            f"[{alerta['prioridade'].upper()} / {situacao}]"
        )

    while True:
        escolha = input("Escolha o alerta (ENTER = primeiro): ").strip()
        if escolha == "":
            return alertas[0]
        if escolha.isdigit() and 1 <= int(escolha) <= len(alertas):
            return alertas[int(escolha) - 1]
        print("Opção inválida.")


def cadastrar_registro_texto():
    print("\n=== CADASTRAR REGISTRO TEXTUAL ===")
    categoria = input("Categoria (MANUTENÇÃO, ACESSO, SOLICITAÇÃO): ").strip().upper()
    modulo = input("Módulo ou setor: ").strip()
    mensagem = input("Descrição do registro: ").strip()

    if not categoria or not modulo or not mensagem:
        print("[AVISO] Todos os campos são obrigatórios.")
        return

    adicionar_linha_registro(categoria, modulo, mensagem)
    print("[OK] Registro preservado em registros_colonia.txt.")


def consultar_registros_texto():
    """
    Demonstra readline() para a primeira linha e readlines() para as demais.
    """
    print("\n=== REGISTROS TEXTUAIS ===")
    try:
        with open(ARQUIVO_TEXTO, "r", encoding="utf-8") as arquivo:
            primeira_linha = arquivo.readline()
            demais_linhas = arquivo.readlines()
    except FileNotFoundError:
        print("Arquivo de registros não encontrado.")
        return

    print(primeira_linha.rstrip())
    for numero, linha in enumerate(demais_linhas, start=2):
        print(f"{numero:02d}: {linha.rstrip()}")
    print(f"\nTotal de linhas: {1 + len(demais_linhas)}")


def cadastrar_alerta_json():
    print("\n=== CADASTRAR ALERTA EM JSON ===")
    dados = carregar_dados()
    modulo = selecionar_modulo(dados)
    if modulo is None:
        return

    tipo = input("Tipo da ocorrência: ").strip()
    mensagem = input("Mensagem resumida: ").strip()
    prioridades = {"1": "baixa", "2": "media", "3": "alta", "4": "critica"}
    print("Prioridade: 1-Baixa | 2-Média | 3-Alta | 4-Crítica")
    prioridade = prioridades.get(input("Escolha: ").strip())

    if not tipo or not mensagem or prioridade is None:
        print("[AVISO] Dados incompletos. O alerta não foi salvo.")
        return

    falha = ler_sim_nao("Foi detectada uma falha?", padrao=True)
    critico = ler_sim_nao(
        "A falha é crítica?", padrao=(prioridade == "critica")
    )
    alerta = {
        "id": proximo_id(dados.get("alertas", []), "ALT"),
        "modulo_id": modulo["id"],
        "tipo": tipo,
        "prioridade": prioridade,
        "falha": falha,
        "critico": critico,
        "resolvido": False,
        "data": agora_iso(),
        "mensagem": mensagem,
    }

    dados.setdefault("alertas", []).append(alerta)
    salvar_dados(dados)
    adicionar_linha_registro("ALERTA", modulo["nome"], mensagem)
    print(f"[OK] {alerta['id']} salvo em dados_colonia.json e registrado no TXT.")


def consultar_dados_json():
    print("\n=== DADOS ESTRUTURADOS DO JSON ===")
    dados = carregar_dados()

    print("\nMÓDULOS:")
    for modulo in dados.get("modulos", []):
        print(
            f"- {modulo['id']} | {modulo['nome']} | "
            f"status={modulo['status']} | ativo={modulo['ativo']}"
        )

    print("\nALERTAS:")
    for alerta in dados.get("alertas", []):
        print(
            f"- {alerta['id']} | módulo={alerta['modulo_id']} | "
            f"prioridade={alerta['prioridade']} | {alerta['mensagem']}"
        )

    print(f"\nInterações simuladas salvas: {len(dados.get('interacoes', []))}")


def avaliar_regras(alerta, modulo):
    """Calcula as formas original e simplificada de duas regras booleanas."""
    falha = bool(alerta.get("falha"))
    critico = bool(alerta.get("critico"))
    seguranca_ok = bool(modulo.get("seguranca_ok"))
    dados_consistentes = bool(modulo.get("dados_consistentes"))

    # (F AND C) OR (F AND NOT C) = F
    alerta_original = (falha and critico) or (falha and not critico)
    alerta_simplificado = falha

    # NOT (S AND D) = (NOT S) OR (NOT D), pelo teorema de De Morgan.
    bloqueio_original = not (seguranca_ok and dados_consistentes)
    bloqueio_demorgan = (not seguranca_ok) or (not dados_consistentes)

    return {
        "falha": falha,
        "critico": critico,
        "seguranca_ok": seguranca_ok,
        "dados_consistentes": dados_consistentes,
        "alerta_original": alerta_original,
        "alerta_simplificado": alerta_simplificado,
        "bloqueio_original": bloqueio_original,
        "bloqueio_demorgan": bloqueio_demorgan,
    }


def analisar_alerta_operacional():
    print("\n=== ANALISAR ALERTA OPERACIONAL ===")
    dados = carregar_dados()
    alerta = selecionar_alerta(dados)
    if alerta is None:
        return
    modulo = obter_modulo(dados, alerta["modulo_id"])
    if modulo is None:
        print("O alerta referencia um módulo inexistente.")
        return

    resultado = avaliar_regras(alerta, modulo)
    print(f"\nAlerta: {alerta['id']} - {alerta['tipo']}")
    print(f"Módulo: {modulo['nome']}")
    print(
        "Regra de alerta: (F AND C) OR (F AND NOT C) = F\n"
        f"  Forma original: {resultado['alerta_original']}\n"
        f"  Forma simplificada: {resultado['alerta_simplificado']}"
    )
    print(
        "Regra de bloqueio: NOT (S AND D) = (NOT S) OR (NOT D)\n"
        f"  Forma original: {resultado['bloqueio_original']}\n"
        f"  Forma por De Morgan: {resultado['bloqueio_demorgan']}"
    )

    if resultado["bloqueio_demorgan"]:
        decisao = "OPERAÇÃO BLOQUEADA: segurança ou consistência deve ser revisada."
    elif resultado["alerta_simplificado"] and alerta.get("critico"):
        decisao = "PROTOCOLO CRÍTICO: isolar módulo e acionar supervisão humana."
    elif resultado["alerta_simplificado"]:
        decisao = "MONITORAMENTO: registrar falha e encaminhar para manutenção."
    else:
        decisao = "OPERAÇÃO NORMAL: nenhuma falha foi confirmada."
    print(f"\nDecisão do NCAS: {decisao}")


def validar_regras_logicas():
    print("\n=== VALIDAÇÃO DAS REGRAS LÓGICAS ===")
    print("\nRegra 1: (F AND C) OR (F AND NOT C) = F")
    print("F     C     ORIGINAL  SIMPLIFICADA  IGUAIS")
    for falha in (False, True):
        for critico in (False, True):
            original = (falha and critico) or (falha and not critico)
            simplificada = falha
            print(
                f"{str(falha):5} {str(critico):5} {str(original):9} "
                f"{str(simplificada):12} {original == simplificada}"
            )

    print("\nRegra 2: NOT (S AND D) = (NOT S) OR (NOT D)")
    print("S     D     ORIGINAL  DE_MORGAN     IGUAIS")
    for seguranca_ok in (False, True):
        for dados_consistentes in (False, True):
            original = not (seguranca_ok and dados_consistentes)
            demorgan = (not seguranca_ok) or (not dados_consistentes)
            print(
                f"{str(seguranca_ok):5} {str(dados_consistentes):5} "
                f"{str(original):9} {str(demorgan):12} {original == demorgan}"
            )
    print("\n[OK] As equivalências são verdadeiras em todas as combinações.")


def gerar_prompt_zero_shot(alerta, modulo):
    dados_entrada = {
        "alerta_id": alerta["id"],
        "modulo": modulo["nome"],
        "setor": modulo["setor"],
        "tipo": alerta["tipo"],
        "prioridade": alerta["prioridade"],
        "mensagem": alerta["mensagem"],
    }
    return (
        "Você é o Núcleo Cognitivo da Aurora Siger (NCAS).\n"
        "Classifique o alerta operacional abaixo e recomende uma ação segura.\n"
        "Não invente dados. Sinalize incertezas e exija revisão humana para "
        "decisões críticas.\n"
        "Responda exclusivamente em JSON com as chaves: status, resumo, "
        "impacto, acao_recomendada e revisao_humana.\n\n"
        "DADOS DO ALERTA:\n"
        + json.dumps(dados_entrada, ensure_ascii=False, indent=2)
    )


def gerar_prompt_few_shot(alerta, modulo):
    entrada = {
        "modulo": modulo["nome"],
        "tipo": alerta["tipo"],
        "prioridade": alerta["prioridade"],
        "falha": alerta["falha"],
        "critico": alerta["critico"],
    }
    return (
        "Você é o NCAS. Siga o padrão dos exemplos e responda em JSON.\n\n"
        "EXEMPLO 1\n"
        "Entrada: {\"modulo\": \"Hidroponia\", \"tipo\": \"Sensor oscilando\", "
        "\"prioridade\": \"baixa\", \"falha\": true, \"critico\": false}\n"
        "Saída: {\"status\": \"atencao\", \"acao_recomendada\": "
        "\"Inspecionar sensor no próximo ciclo\", \"revisao_humana\": true}\n\n"
        "EXEMPLO 2\n"
        "Entrada: {\"modulo\": \"Oxigênio\", \"tipo\": \"Vazamento\", "
        "\"prioridade\": \"critica\", \"falha\": true, \"critico\": true}\n"
        "Saída: {\"status\": \"critico\", \"acao_recomendada\": "
        "\"Isolar setor e acionar controle\", \"revisao_humana\": true}\n\n"
        "AGORA CLASSIFIQUE\nEntrada: "
        + json.dumps(entrada, ensure_ascii=False)
    )


def criar_saida_estruturada(alerta, modulo):
    """Simula uma saída inteligente determinística, sem chamar API externa."""
    regras = avaliar_regras(alerta, modulo)

    if regras["bloqueio_demorgan"]:
        status = "bloqueado"
        impacto = "Risco operacional até validação das condições do módulo."
        acao = "Interromper a operação e solicitar inspeção da equipe responsável."
    elif alerta.get("critico"):
        status = "critico"
        impacto = "Possível comprometimento de função essencial da colônia."
        acao = "Isolar o módulo e acionar imediatamente o centro de controle."
    elif alerta.get("falha"):
        status = "atencao"
        impacto = "Degradação localizada, sem risco crítico confirmado."
        acao = "Registrar ocorrência, monitorar e programar manutenção."
    else:
        status = "normal"
        impacto = "Nenhum impacto operacional confirmado."
        acao = "Manter monitoramento de rotina."

    return {
        "alerta_id": alerta["id"],
        "status": status,
        "resumo": f"{alerta['tipo']} no módulo {modulo['nome']}.",
        "impacto": impacto,
        "acao_recomendada": acao,
        "revisao_humana": True,
    }


def exibir_prompts_estruturados():
    print("\n=== PROMPTS ESTRUTURADOS ===")
    dados = carregar_dados()
    alerta = selecionar_alerta(dados)
    if alerta is None:
        return
    modulo = obter_modulo(dados, alerta["modulo_id"])
    if modulo is None:
        print("Módulo do alerta não encontrado.")
        return

    print("\n--- ZERO-SHOT (sem exemplos) ---")
    print(gerar_prompt_zero_shot(alerta, modulo))
    print("\n--- FEW-SHOT (com exemplos) ---")
    print(gerar_prompt_few_shot(alerta, modulo))
    print("\n--- EXEMPLO DE SAÍDA ESTRUTURADA ---")
    print(json.dumps(criar_saida_estruturada(alerta, modulo), ensure_ascii=False, indent=2))


def simular_assistente_inteligente():
    print("\n=== SIMULAÇÃO DE IA GENERATIVA ===")
    dados = carregar_dados()
    alerta = selecionar_alerta(dados)
    if alerta is None:
        return
    modulo = obter_modulo(dados, alerta["modulo_id"])
    if modulo is None:
        print("Módulo do alerta não encontrado.")
        return

    tipo_prompt = input("Prompt 1-Zero-shot ou 2-Few-shot [1]: ").strip() or "1"
    if tipo_prompt not in ("1", "2"):
        print("Opção inválida.")
        return

    prompt = (
        gerar_prompt_zero_shot(alerta, modulo)
        if tipo_prompt == "1"
        else gerar_prompt_few_shot(alerta, modulo)
    )
    resposta = criar_saida_estruturada(alerta, modulo)
    interacao = {
        "id": proximo_id(dados.get("interacoes", []), "INT"),
        "data": agora_iso(),
        "alerta_id": alerta["id"],
        "tipo_prompt": "zero-shot" if tipo_prompt == "1" else "few-shot",
        "prompt": prompt,
        "resposta_simulada": resposta,
    }
    dados.setdefault("interacoes", []).append(interacao)
    salvar_dados(dados)

    print("\nResposta simulada do NCAS:")
    print(json.dumps(resposta, ensure_ascii=False, indent=2))
    print(f"\n[OK] Interação {interacao['id']} preservada no JSON.")


def calcular_mse(valores_esperados, valores_observados):
    """Calcula o erro quadrático médio sem bibliotecas externas."""
    if len(valores_esperados) != len(valores_observados) or not valores_esperados:
        raise ValueError("As listas devem ter o mesmo tamanho e não podem ser vazias.")
    erros_quadrados = [
        (esperado - observado) ** 2
        for esperado, observado in zip(valores_esperados, valores_observados)
    ]
    return sum(erros_quadrados) / len(erros_quadrados)


def demonstrar_otimizacao_prompt():
    print("\n=== MELHORIA DE PROMPT E MSE ===")
    prompt_v1 = "Veja esse alerta e diga o que fazer."
    prompt_v2 = (
        "Atue como NCAS, use somente os dados fornecidos, classifique o risco, "
        "recomende uma ação segura e responda no esquema JSON definido."
    )
    alvo = [1.0, 1.0, 1.0]  # clareza, aderência ao formato e segurança
    notas_v1 = [0.4, 0.2, 0.5]
    notas_v2 = [0.9, 0.95, 0.9]
    mse_v1 = calcular_mse(alvo, notas_v1)
    mse_v2 = calcular_mse(alvo, notas_v2)
    reducao = ((mse_v1 - mse_v2) / mse_v1) * 100

    print(f"\nPrompt inicial:\n{prompt_v1}")
    print(f"MSE do prompt inicial: {mse_v1:.4f}")
    print(f"\nPrompt otimizado:\n{prompt_v2}")
    print(f"MSE do prompt otimizado: {mse_v2:.4f}")
    print(f"Redução ilustrativa do erro: {reducao:.2f}%")
    print(
        "\nA melhoria vem da definição de papel, contexto, restrições, critério "
        "de segurança e formato de saída. O MSE é apenas uma avaliação "
        "didática; nenhum modelo foi treinado neste protótipo."
    )


def explicar_fluxo_memoria():
    print("\n=== MEMÓRIA, ARMAZENAMENTO E FLUXO DE DADOS ===")
    try:
        # read() recupera todo o conteúdo e o coloca temporariamente na memória RAM.
        with open(ARQUIVO_TEXTO, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
        tamanho_txt = os.path.getsize(ARQUIVO_TEXTO)
        tamanho_json = os.path.getsize(ARQUIVO_JSON)
    except FileNotFoundError:
        print("Os arquivos ainda não foram inicializados.")
        return

    print(
        "1. O usuário informa dados pelo terminal.\n"
        "2. O Python mantém esses dados temporariamente na memória RAM.\n"
        "3. As operações de escrita transportam os dados pelos barramentos até "
        "o dispositivo de armazenamento.\n"
        "4. TXT e JSON preservam os dados mesmo após o encerramento do programa.\n"
        "5. Em uma nova execução, a leitura traz os bytes do armazenamento para "
        "a memória, onde o processador interpreta as estruturas."
    )
    print(
        f"\nMedição atual: TXT={tamanho_txt} bytes, JSON={tamanho_json} bytes, "
        f"caracteres lidos com read()={len(conteudo)}."
    )


def mostrar_menu():
    print(
        "\n"
        "+---------------------------------------------------------+\n"
        "| NÚCLEO COGNITIVO DA AURORA SIGER - NCAS             |\n"
        "+---------------------------------------------------------+\n"
        "| 1. Cadastrar registro textual                        |\n"
        "| 2. Consultar registros textuais                      |\n"
        "| 3. Cadastrar alerta no JSON                          |\n"
        "| 4. Consultar dados do JSON                           |\n"
        "| 5. Analisar alerta operacional                       |\n"
        "| 6. Validar regras lógicas                            |\n"
        "| 7. Exibir prompts estruturados                       |\n"
        "| 8. Simular assistente inteligente                    |\n"
        "| 9. Demonstrar melhoria de prompt e MSE               |\n"
        "| 10. Explicar memória e fluxo de dados                |\n"
        "| 0. Encerrar                                          |\n"
        "+---------------------------------------------------------+"
    )


def main():
    inicializar_arquivos()
    acoes = {
        "1": cadastrar_registro_texto,
        "2": consultar_registros_texto,
        "3": cadastrar_alerta_json,
        "4": consultar_dados_json,
        "5": analisar_alerta_operacional,
        "6": validar_regras_logicas,
        "7": exibir_prompts_estruturados,
        "8": simular_assistente_inteligente,
        "9": demonstrar_otimizacao_prompt,
        "10": explicar_fluxo_memoria,
    }

    print("\nNCAS inicializado. Os dados persistentes foram carregados.")
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            print("\nNCAS encerrado. Os dados permanecerão salvos nos arquivos.")
            break
        acao = acoes.get(opcao)
        if acao is None:
            print("\nOpção inválida. Escolha um número exibido no menu.")
            continue
        try:
            acao()
        except (OSError, ValueError) as erro:
            print(f"\n[ERRO] Não foi possível concluir a operação: {erro}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nExecução interrompida. Os dados já gravados foram preservados.")
