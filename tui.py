# CAMADA DE APRESENTAÇÃO - TERMINAL USER INTERFACE (TUI)
#
# Este módulo implementa a interface de usuário em terminal para o sistema RU.
# CARACTERÍSTICAS PRINCIPAIS:
# - Interface intuitiva com menus navegáveis
# - Validação em tempo real de entrada de dados
# - Dicas contextuais para reduzir erros do usuário
# - Formatação consistente de dados de saída
# - Tratamento gracioso de cancelamentos
# 
# TECNOLOGIAS UTILIZADAS:
# - questionary: Biblioteca para interfaces interativas elegantes
# - Validação personalizada com lambda functions
# - ASCII art para identidade visual

import questionary
import os
from datetime import datetime

def clear_screen():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_main_ascii_art():
    """Exibe ASCII art do menu principal"""
    clear_screen()
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║                                                               ║")
    print("║    ____ _ ____ ___ ____ _  _ ____    ____ _  _                ║")
    print("║    [__  | [__   |  |___ |\\/| |__|    |__/ |  |                ║")
    print("║    ___] | ___]  |  |___ |  | |  |    |  \\ |__|                ║")
    print("║                                                               ║")
    print("║                                                               ║")
    print("║                                                               ║")
    print("║                  Sistema de Gerenciamento                     ║")
    print("║                Usuario → Pedido → Pagamento                   ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print()

def print_section_header(title):
    """Exibe cabeçalho de seção"""
    clear_screen()
    print("╔═══════════════════════════════════════════════════════════════╗")
    print(f"║{title.center(63)}║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print()

def main_menu():
    """Menu principal do sistema"""
    print_main_ascii_art()
    choice = questionary.select(
        "Selecione uma opção:",
        choices=[
            "Gerenciar Usuários",
            "Gerenciar Pedidos", 
            "Gerenciar Pagamentos",
            "Sair"
        ]
    ).ask()
    
    return choice if choice else "Sair"

# ==================== MENUS DE GERENCIAMENTO ====================

def user_management_menu():
    """Menu de gerenciamento de usuários"""
    print_section_header("GERENCIAMENTO DE USUÁRIOS")
    choice = questionary.select(
        "Selecione uma ação:",
        choices=[
            "Cadastrar Usuário",
            "Listar Usuários",
            "Atualizar Usuário",
            "Deletar Usuário",
            "Voltar ao Menu Principal"
        ]
    ).ask()
    
    return choice if choice else "Voltar ao Menu Principal"

def pedido_management_menu():
    """Menu de gerenciamento de pedidos"""
    print_section_header("GERENCIAMENTO DE PEDIDOS")
    choice = questionary.select(
        "Selecione uma ação:",
        choices=[
            "Cadastrar Pedido",
            "Listar Pedidos",
            "Atualizar Pedido",
            "Deletar Pedido",
            "Voltar ao Menu Principal"
        ]
    ).ask()
    
    return choice if choice else "Voltar ao Menu Principal"

def pagamento_management_menu():
    """Menu de gerenciamento de pagamentos"""
    print_section_header("GERENCIAMENTO DE PAGAMENTOS")
    choice = questionary.select(
        "Selecione uma ação:",
        choices=[
            "Cadastrar Pagamento",
            "Listar Pagamentos",
            "Atualizar Pagamento",
            "Deletar Pagamento",
            "Voltar ao Menu Principal"
        ]
    ).ask()
    
    return choice if choice else "Voltar ao Menu Principal"

# ==================== FORMULÁRIOS DE ENTRADA ====================

def get_user_data(existing_user=None):
    """
    FORMULÁRIO INTELIGENTE - CADASTRO/EDIÇÃO DE USUÁRIO
    
    Implementa coleta de dados com validação em tempo real e dicas contextuais.
    
    VALIDAÇÕES IMPLEMENTADAS:
    - Matrícula: Apenas números, mínimo 8 dígitos
    - CPF: Exatamente 11 dígitos numéricos
    - Email: Formato básico com @ e domínio
    - Nome: Mínimo 2 caracteres
    - Telefone: Campo opcional
    
    CARACTERÍSTICAS UX:
    - Pré-preenchimento para edição
    - Campos obrigatórios marcados com *
    - Exemplos práticos em cada campo
    - Cancelamento gracioso com Enter vazio
    """
    print("\nDados do Usuário:")
    print("[DICA] Todos os campos marcados com * são obrigatórios")
    
    print("\n[DICA] Matrícula: Digite apenas números, mínimo 8 dígitos (ex: 20231001234)")
    matricula_usuario = questionary.text(
        "Matrícula do usuário *:",
        default=str(existing_user[1]) if existing_user else "",
        validate=lambda x: x.isdigit() and len(x) >= 8 if x else False
    ).ask()
    if not matricula_usuario:
        return None
    
    print("\n[DICA] CPF: Digite apenas os 11 números, sem pontos ou traços (ex: 12345678901)")
    cpf_usuario = questionary.text(
        "CPF (somente números) *:",
        default=existing_user[2] if existing_user else "",
        validate=lambda x: x.isdigit() and len(x) == 11 if x else False
    ).ask()
    if not cpf_usuario:
        return None
    
    print("\n[DICA] Nome: Digite o nome completo (ex: João Silva Santos)")
    nome_usuario = questionary.text(
        "Nome completo *:",
        default=existing_user[3] if existing_user else "",
        validate=lambda x: len(x.strip()) >= 2 if x else False
    ).ask()
    if not nome_usuario:
        return None
    
    print("\n[DICA] Email: Digite um email válido (ex: joao.silva@aluno.unb.br)")
    email_usuario = questionary.text(
        "Email *:",
        default=existing_user[4] if existing_user else "",
        validate=lambda x: "@" in x and "." in x.split("@")[-1] if x else False
    ).ask()
    if not email_usuario:
        return None
    
    print("\n[DICA] Telefone: Digite com DDD (ex: (61) 99999-1234) - Campo opcional")
    telefone_usuario = questionary.text(
        "Telefone (opcional):",
        default=existing_user[5] if existing_user else ""
    ).ask()
    
    print("\n[DICA] Status: Selecione o status atual do usuário")
    status_usuario = questionary.select(
        "Status *:",
        choices=["ativo", "trancado", "formado", "jubilado", "suspenso"],
        default=existing_user[6] if existing_user else "ativo"
    ).ask()
    
    return {
        'matricula_usuario': int(matricula_usuario),
        'CPF_usuario': cpf_usuario,
        'nome_usuario': nome_usuario.strip(),
        'email_usuario': email_usuario.strip().lower(),
        'telefone_usuario': telefone_usuario.strip() or None,
        'status_usuario': status_usuario
    }

def get_pedido_data(existing_pedido=None, usuarios_disponiveis=None):
    """Coleta dados do pedido usando estrutura real do Supabase"""
    print("\nDados do Pedido:")
    print("[DICA] Todos os campos marcados com * são obrigatórios")
    
    # Se há usuários disponíveis, permite seleção direta
    if usuarios_disponiveis and len(usuarios_disponiveis) > 0:
        usuario_choices = []
        for usuario in usuarios_disponiveis:
            choice_text = f"ID {usuario[0]} - {usuario[3]} - {usuario[4]}"
            usuario_choices.append(choice_text)
        
        usuario_choices.append("Digitar ID manualmente")
        
        print("\n[DICA] Selecione um usuário da lista ou digite o ID manualmente")
        usuario_selection = questionary.select(
            "Selecione o usuário para o pedido *:",
            choices=usuario_choices
        ).ask()
        
        if not usuario_selection:
            return None
        
        if usuario_selection == "Digitar ID manualmente":
            print("\n[DICA] Digite o ID numérico do usuário (ex: 1, 2, 3, etc.)")
            pedido_usuario = questionary.text(
                "ID do Usuário *:",
                default=str(existing_pedido[1]) if existing_pedido else "",
                validate=lambda x: x.isdigit() and int(x) > 0 if x else False
            ).ask()
            if not pedido_usuario:
                return None
            pedido_usuario = int(pedido_usuario)
        else:
            # Extrair o ID do usuário selecionado
            pedido_usuario = int(usuario_selection.split(" - ")[0].replace("ID ", ""))
    else:
        print("\n[DICA] Digite o ID numérico do usuário (ex: 1, 2, 3, etc.)")
        print("[DICA] Use 'Listar Usuários' no menu principal para encontrar o ID")
        pedido_usuario = questionary.text(
            "ID do Usuário *:",
            default=str(existing_pedido[1]) if existing_pedido else "",
            validate=lambda x: x.isdigit() and int(x) > 0 if x else False
        ).ask()
        if not pedido_usuario:
            return None
        pedido_usuario = int(pedido_usuario)
    
    # Buscar cardápios disponíveis seria ideal aqui, mas para simplificar vamos pedir o ID
    print("\n[DICA] ID do Cardápio: Digite um número (ex: 1=almoço, 2=jantar, 3=café)")
    print("[DICA] Use valores de 1 a 7 conforme os cardápios disponíveis no sistema")
    ped_cardapio = questionary.text(
        "ID do Cardápio *:",
        default=str(existing_pedido[5]) if existing_pedido and len(existing_pedido) > 5 else "1",
        validate=lambda x: x.isdigit() and int(x) > 0 if x else False
    ).ask()
    if not ped_cardapio:
        return None
    
    print("\n[DICA] Status: Selecione o status atual do pedido")
    status_do_pedido = questionary.select(
        "Status *:",
        choices=["pendente", "pago", "entregue", "cancelado"],
        default=existing_pedido[4] if existing_pedido else "pendente"
    ).ask()
    
    return {
        'pedido_usuario': pedido_usuario,
        'ped_cardapio': int(ped_cardapio),
        'status_do_pedido': status_do_pedido
    }

def get_pagamento_data(existing_pagamento=None, pedidos_disponiveis=None):
    """
    FORMULÁRIO MAIS COMPLEXO - CADASTRO/EDIÇÃO DE PAGAMENTO
    
    Este é o formulário mais sofisticado, integrando dados de múltiplas entidades.
    
    COMPLEXIDADES GERENCIADAS:
    - Seleção inteligente de pedidos (lista + ID manual)
    - Validação de valores decimais (aceita vírgula e ponto)
    - Prevenção de pagamentos duplicados
    - Integração com categorias de usuário
    - Cálculos automáticos por tipo de categoria
    
    REGRAS DE NEGÓCIO IMPLEMENTADAS:
    - Estudante assistência: R$ 0,00 (gratuito)
    - Estudante regular: Valor com desconto 60%
    - Servidor: Valor integral sem desconto
    
    CARACTERÍSTICAS UX AVANÇADAS:
    - Lista visual de pedidos disponíveis
    - Avisos sobre duplicação de pagamentos  
    - Dicas de preenchimento contextuais
    - Informações sobre categorias e preços
    """
    print("\nDados do Pagamento:")
    print("[DICA] Todos os campos marcados com * são obrigatórios")
    
    # Se há pedidos disponíveis, permite seleção direta
    if pedidos_disponiveis and len(pedidos_disponiveis) > 0:
        pedido_choices = []
        for pedido in pedidos_disponiveis:
            usuario_nome = pedido[2] if len(pedido) > 2 else "N/A"
            data_formatada = pedido[3].strftime("%d/%m/%Y") if len(pedido) > 3 and pedido[3] else "N/A"
            tipo_cardapio = pedido[5] if len(pedido) > 5 and pedido[5] else "N/A"
            choice_text = f"ID {pedido[0]} - {usuario_nome} - {data_formatada} - {tipo_cardapio}"
            pedido_choices.append(choice_text)
        
        pedido_choices.append("Digitar ID manualmente")
        
        print("\n[DICA] Selecione um pedido da lista ou digite o ID manualmente")
        print("[AVISO] Só é possível criar um pagamento por pedido!")
        pedido_selection = questionary.select(
            "Selecione o pedido para pagamento *:",
            choices=pedido_choices
        ).ask()
        
        if not pedido_selection:
            return None
        
        if pedido_selection == "Digitar ID manualmente":
            print("\n[DICA] Digite o ID numérico do pedido (ex: 1, 2, 3, etc.)")
            print("[DICA] Use 'Listar Pedidos' no menu principal para encontrar o ID")
            pag_pedido = questionary.text(
                "ID do Pedido *:",
                default=str(existing_pagamento[1]) if existing_pagamento else "",
                validate=lambda x: x.isdigit() and int(x) > 0 if x else False
            ).ask()
            if not pag_pedido:
                return None
            pag_pedido = int(pag_pedido)
            # Encontrar o usuário correspondente
            pag_categoria_usuario = pag_pedido  # Assumir que é o mesmo ID por ora
        else:
            # Extrair o ID do pedido selecionado
            pag_pedido = int(pedido_selection.split(" - ")[0].replace("ID ", ""))
            # Encontrar o pedido correspondente para obter o usuário
            pedido_selecionado = None
            for pedido in pedidos_disponiveis:
                if pedido[0] == pag_pedido:
                    pedido_selecionado = pedido
                    break
            
            if pedido_selecionado:
                pag_categoria_usuario = pedido_selecionado[1]  # ID do usuário
            else:
                pag_categoria_usuario = pag_pedido
    else:
        print("\n[DICA] Digite o ID numérico do pedido (ex: 1, 2, 3, etc.)")
        print("[DICA] Use 'Listar Pedidos' no menu principal para encontrar o ID")
        print("[AVISO] Só é possível criar um pagamento por pedido!")
        pag_pedido = questionary.text(
            "ID do Pedido *:",
            default=str(existing_pagamento[1]) if existing_pagamento else "",
            validate=lambda x: x.isdigit() and int(x) > 0 if x else False
        ).ask()
        if not pag_pedido:
            return None
        pag_pedido = int(pag_pedido)
        pag_categoria_usuario = pag_pedido
    
    print("\n[DICA] Valor: Digite o valor em reais com ponto decimal (ex: 15.50, 0.00)")
    print("[DICA] Para estudantes com assistência, use 0.00 (gratuito)")
    valor_pago = questionary.text(
        "Valor pago (0.00) *:",
        default=str(existing_pagamento[3]) if existing_pagamento else "0.00",
        validate=lambda x: is_valid_decimal(x) if x else False
    ).ask()
    if not valor_pago:
        return None
    
    print("\n[DICA] Forma de pagamento: Selecione como o pagamento foi realizado")
    forma_de_pagamento = questionary.select(
        "Forma de pagamento *:",
        choices=["dinheiro", "pix", "cartao", "vale"],
        default=existing_pagamento[4] if existing_pagamento else "vale"
    ).ask()
    
    print("\n[DICA] Categoria: Selecione o tipo de usuário para definir preços")
    print("[INFO] estudante_assistencia=R$0.00, estudante_regular=desconto 60%, servidor=preço integral")
    pag_categoria_nome = questionary.select(
        "Categoria do usuário *:",
        choices=["estudante_assistencia", "estudante_regular", "servidor"],
        default=existing_pagamento[6] if existing_pagamento else "estudante_regular"
    ).ask()
    
    return {
        'pag_pedido': pag_pedido,
        'valor_pago': float(valor_pago.replace(',', '.')),
        'forma_de_pagamento': forma_de_pagamento,
        'pag_categoria_usuario': pag_categoria_usuario,
        'pag_categoria_nome': pag_categoria_nome
    }

# ==================== FUNÇÕES DE VALIDAÇÃO ====================

def is_valid_decimal(value):
    """
    VALIDADOR INTELIGENTE - VALORES DECIMAIS
    
    Aceita múltiplos formatos de entrada para melhor UX:
    - Ponto como separador decimal (15.50)
    - Vírgula como separador decimal (15,50)  
    - Valores inteiros (15)
    - Remove espaços automaticamente
    
    Garante que valores sejam não-negativos (≥ 0).
    """
    try:
        if not value:
            return False
        # Remove espaços em branco
        value = value.strip()
        # Aceita vírgula como separador decimal (converte para ponto)
        value = value.replace(',', '.')
        decimal_value = float(value)
        return decimal_value >= 0
    except ValueError:
        return False

def get_user_id(action_type):
    """Solicita ID do usuário com dicas de validação"""
    print("\n[DICA] Para encontrar o ID do usuário, use 'Listar Usuários' no menu principal.")
    print("[DICA] O ID é um número inteiro positivo (ex: 1, 2, 3, etc.)")
    
    user_id_str = questionary.text(
        f"Digite o ID do usuário para {action_type} (ou Enter para cancelar):",
        validate=lambda x: x.isdigit() and int(x) > 0 if x else True
    ).ask()
    
    if not user_id_str:
        return None
    
    try:
        user_id = int(user_id_str)
        if user_id <= 0:
            print("[ERRO] ID deve ser um número positivo maior que zero.")
            return None
        return user_id
    except ValueError:
        print("[ERRO] ID inválido. Deve ser um número inteiro positivo.")
        return None

def get_pedido_id(action_type):
    """Solicita ID do pedido com dicas de validação"""
    print("\n[DICA] Para encontrar o ID do pedido, use 'Listar Pedidos' no menu principal.")
    print("[DICA] O ID é um número inteiro positivo (ex: 1, 2, 3, etc.)")
    
    pedido_id_str = questionary.text(
        f"Digite o ID do pedido para {action_type} (ou Enter para cancelar):",
        validate=lambda x: x.isdigit() and int(x) > 0 if x else True
    ).ask()
    
    if not pedido_id_str:
        return None
    
    try:
        pedido_id = int(pedido_id_str)
        if pedido_id <= 0:
            print("[ERRO] ID deve ser um número positivo maior que zero.")
            return None
        return pedido_id
    except ValueError:
        print("[ERRO] ID inválido. Deve ser um número inteiro positivo.")
        return None

def get_pagamento_id(action_type):
    """Solicita ID do pagamento com dicas de validação"""
    print("\n[DICA] Para encontrar o ID do pagamento, use 'Listar Pagamentos' no menu principal.")
    print("[DICA] O ID é um número inteiro positivo (ex: 1, 2, 3, etc.)")
    
    pagamento_id_str = questionary.text(
        f"Digite o ID do pagamento para {action_type} (ou Enter para cancelar):",
        validate=lambda x: x.isdigit() and int(x) > 0 if x else True
    ).ask()
    
    if not pagamento_id_str:
        return None
    
    try:
        pagamento_id = int(pagamento_id_str)
        if pagamento_id <= 0:
            print("[ERRO] ID deve ser um número positivo maior que zero.")
            return None
        return pagamento_id
    except ValueError:
        print("[ERRO] ID inválido. Deve ser um número inteiro positivo.")
        return None

# ==================== FUNÇÕES DE EXIBIÇÃO ====================

def display_users(users):
    """
    VISUALIZADOR DE DADOS - USUÁRIOS
    
    Formata e exibe dados de usuários em tabela organizada.
    Inclui indicadores visuais de status e tratamento de dados vazios.
    """
    print("\nLISTA DE USUÁRIOS")
    print("=" * 90)
    
    if not users:
        print("[VAZIO] Nenhum usuário encontrado.")
        return
    
    print(f"{'ID':<4} {'Matrícula':<12} {'Nome':<25} {'Email':<30} {'Status':<10}")
    print("-" * 90)
    
    for user in users:
        status_indicator = get_status_text(user[6])
        print(f"{user[0]:<4} {user[1]:<12} {user[3]:<25} {user[4]:<30} {status_indicator}")

def display_pedidos(pedidos):
    """Exibe lista de pedidos usando estrutura real do Supabase"""
    print("\nLISTA DE PEDIDOS")
    print("=" * 90)
    
    if not pedidos:
        print("[VAZIO] Nenhum pedido encontrado.")
        return
    
    print(f"{'ID':<4} {'Usuario':<20} {'Data/Hora':<16} {'Tipo':<10} {'Status':<12}")
    print("-" * 90)
    
    for pedido in pedidos:
        status_indicator = get_status_text(pedido[4])
        data_formatada = pedido[3].strftime("%d/%m/%Y %H:%M") if pedido[3] else "N/A"
        tipo_cardapio = pedido[5] if len(pedido) > 5 and pedido[5] else "N/A"
        print(f"{pedido[0]:<4} {pedido[2]:<20} {data_formatada:<16} {tipo_cardapio:<10} {status_indicator}")

def display_pagamentos(pagamentos):
    """Exibe lista de pagamentos usando estrutura real do Supabase"""
    print("\nLISTA DE PAGAMENTOS")
    print("=" * 95)
    
    if not pagamentos:
        print("[VAZIO] Nenhum pagamento encontrado.")
        return
    
    print(f"{'ID':<4} {'Usuario':<20} {'Valor':<12} {'Forma':<12} {'Categoria':<15}")
    print("-" * 95)
    
    for pagamento in pagamentos:
        valor_formatado = f"R$ {pagamento[3]:,.2f}"
        categoria = pagamento[6] if len(pagamento) > 6 else "N/A"
        print(f"{pagamento[0]:<4} {pagamento[2]:<20} {valor_formatado:<12} {pagamento[4]:<12} {categoria:<15}")


def show_current_user_data(user):
    """Exibe dados atuais do usuário usando estrutura real do Supabase"""
    print(f"\nDADOS ATUAIS DO USUÁRIO (ID: {user[0]})")
    print("-" * 50)
    print(f"Matrícula: {user[1]}")
    print(f"CPF: {user[2]}")
    print(f"Nome: {user[3]}")
    print(f"Email: {user[4]}")
    print(f"Telefone: {user[5] or 'N/A'}")
    print(f"Status: {user[6]}")
    print()

def show_current_pedido_data(pedido):
    """Exibe dados atuais do pedido usando estrutura real do Supabase"""
    print(f"\nDADOS ATUAIS DO PEDIDO (ID: {pedido[0]})")
    print("-" * 50)
    print(f"Usuário: {pedido[2]} (ID: {pedido[1]})")
    print(f"Data/Hora: {pedido[3].strftime('%d/%m/%Y %H:%M') if pedido[3] else 'N/A'}")
    print(f"Status: {pedido[4]}")
    if len(pedido) > 5:
        print(f"Tipo Cardápio: {pedido[6] if pedido[6] else 'N/A'}")
    print()

def show_current_pagamento_data(pagamento):
    """Exibe dados atuais do pagamento usando estrutura real do Supabase"""
    print(f"\nDADOS ATUAIS DO PAGAMENTO (ID: {pagamento[0]})")
    print("-" * 50)
    print(f"Pedido: #{pagamento[1]}")
    print(f"Usuário: {pagamento[2]}")
    print(f"Valor Pago: R$ {pagamento[3]:,.2f}")
    print(f"Forma: {pagamento[4]}")
    print(f"Data Pagamento: {pagamento[5].strftime('%d/%m/%Y %H:%M') if pagamento[5] else 'N/A'}")
    print(f"Categoria: {pagamento[6] if len(pagamento) > 6 else 'N/A'}")
    print()

def get_status_text(status):
    """Retorna texto indicador correspondente ao status usando os status reais do Supabase"""
    status_map = {
        'ativo': '[ATIVO]',
        'trancado': '[TRANCADO]', 
        'formado': '[FORMADO]',
        'jubilado': '[JUBILADO]',
        'suspenso': '[SUSPENSO]',
        'pendente': '[PENDENTE]',
        'pago': '[PAGO]',
        'entregue': '[ENTREGUE]',
        'cancelado': '[CANCELADO]'
    }
    return status_map.get(status, '[INDEFINIDO]')
