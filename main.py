# Sistema CRUD - 3 Tabelas Relacionadas
# Usuario -> Pedido -> Pagamento
import tui
import database
import time
import questionary
import psycopg2

def main():
    # Conecta ao banco de dados
    conn = database.connect()
    if not conn:
        return

    # Verifica se as tabelas existem (usando nomes reais do Supabase)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM Usuario LIMIT 1;")
            table_exists = True
    except psycopg2.Error:
        table_exists = False

    if not table_exists:
        print("Tabelas não encontradas. Configurando o esquema do banco de dados...")
        database.setup_database_schema(conn)
        database.populate_sample_data(conn)
        print("Configuração concluída. Pressione Enter para continuar...")
        input()
    else:
        print("Base de dados Supabase detectada. Carregando dados existentes...")
        database.setup_database_schema(conn)  # Apenas verifica estrutura
        database.populate_sample_data(conn)   # Apenas verifica dados
        time.sleep(1)

    while True:
        main_choice = tui.main_menu()

        if main_choice == "Sair":
            print("Saindo do sistema...")
            break
            
        elif main_choice == "Gerenciar Usuários":
            handle_usuario_crud(conn)
            
        elif main_choice == "Gerenciar Pedidos":
            handle_pedido_crud(conn)
            
        elif main_choice == "Gerenciar Pagamentos":
            handle_pagamento_crud(conn)

    conn.close()

def handle_usuario_crud(conn):
    """Gerencia o CRUD de usuários"""
    while True:
        user_choice = tui.user_management_menu()

        if user_choice == "Voltar ao Menu Principal":
            break
            
        elif user_choice == "Cadastrar Usuário":
            user_data = tui.get_user_data()
            if user_data:
                try:
                    database.add_user(conn, user_data)
                    print("\n[SUCESSO] Usuário cadastrado com sucesso!\n")
                except psycopg2.Error as e:
                    print(f"\n[ERRO] Erro ao cadastrar usuário: {e}\n")
            else:
                print("\n[CANCELADO] Cadastro cancelado.\n")
            input("Pressione Enter para continuar...")
            
        elif user_choice == "Listar Usuários":
            users = database.get_all_users(conn)
            tui.display_users(users)
            input("Pressione Enter para continuar...")
            
        elif user_choice == "Atualizar Usuário":
            user_id = tui.get_user_id("atualizar")
            if user_id:
                existing_user = database.get_user_by_id(conn, user_id)
                if existing_user:
                    tui.show_current_user_data(existing_user)
                    updated_data = tui.get_user_data(existing_user)
                    if updated_data:
                        try:
                            database.update_user(conn, user_id, updated_data)
                            print("\n[SUCESSO] Usuário atualizado com sucesso!\n")
                        except psycopg2.Error as e:
                            print(f"\n[ERRO] Erro ao atualizar usuário: {e}\n")
                    else:
                        print("\n[CANCELADO] Atualização cancelada.\n")
                else:
                    print("\n[ERRO] Usuário não encontrado.\n")
            input("Pressione Enter para continuar...")
            
        elif user_choice == "Deletar Usuário":
            user_id = tui.get_user_id("deletar")
            if user_id:
                confirm = questionary.confirm(
                    f"[AVISO] Tem certeza que deseja deletar o usuário ID {user_id}? Esta ação é irreversível."
                ).ask()
                if confirm:
                    try:
                        database.delete_user(conn, user_id)
                        print("\n[SUCESSO] Usuário deletado com sucesso!\n")
                    except psycopg2.Error as e:
                        print(f"\n[ERRO] Erro ao deletar usuário: {e}\n")
                else:
                    print("\n[CANCELADO] Exclusão cancelada.\n")
            input("Pressione Enter para continuar...")

def handle_pedido_crud(conn):
    """Gerencia o CRUD de pedidos"""
    while True:
        pedido_choice = tui.pedido_management_menu()

        if pedido_choice == "Voltar ao Menu Principal":
            break
            
        elif pedido_choice == "Cadastrar Pedido":
            # Mostra usuários disponíveis
            print("\n[INFO] Usuários cadastrados:")
            users = database.get_all_users(conn)
            if users:
                tui.display_users(users)
                print("\n[INFO] Selecione um usuário da lista acima para criar o pedido.")
            else:
                print("\n[AVISO] Nenhum usuário encontrado.")
                print("Cadastre usuários antes de criar pedidos.")
                input("Pressione Enter para continuar...")
                continue
            
            pedido_data = tui.get_pedido_data(usuarios_disponiveis=users)
            if pedido_data:
                try:
                    database.add_pedido(conn, pedido_data)
                    print("\n[SUCESSO] Pedido cadastrado com sucesso!\n")
                except psycopg2.Error as e:
                    print(f"\n[ERRO] Erro ao cadastrar pedido: {e}\n")
            else:
                print("\n[CANCELADO] Cadastro cancelado.\n")
            input("Pressione Enter para continuar...")
            
        elif pedido_choice == "Listar Pedidos":
            pedidos = database.get_all_pedidos(conn)
            tui.display_pedidos(pedidos)
            input("Pressione Enter para continuar...")
            
        elif pedido_choice == "Atualizar Pedido":
            pedido_id = tui.get_pedido_id("atualizar")
            if pedido_id:
                existing_pedido = database.get_pedido_by_id(conn, pedido_id)
                if existing_pedido:
                    tui.show_current_pedido_data(existing_pedido)
                    # Buscar usuários para o update
                    users = database.get_all_users(conn)
                    updated_data = tui.get_pedido_data(existing_pedido, usuarios_disponiveis=users)
                    if updated_data:
                        try:
                            database.update_pedido(conn, pedido_id, updated_data)
                            print("\n[SUCESSO] Pedido atualizado com sucesso!\n")
                        except psycopg2.Error as e:
                            print(f"\n[ERRO] Erro ao atualizar pedido: {e}\n")
                    else:
                        print("\n[CANCELADO] Atualização cancelada.\n")
                else:
                    print("\n[ERRO] Pedido não encontrado.\n")
            input("Pressione Enter para continuar...")
            
        elif pedido_choice == "Deletar Pedido":
            pedido_id = tui.get_pedido_id("deletar")
            if pedido_id:
                confirm = questionary.confirm(
                    f"[AVISO] Tem certeza que deseja deletar o pedido ID {pedido_id}? Esta ação é irreversível."
                ).ask()
                if confirm:
                    try:
                        database.delete_pedido(conn, pedido_id)
                        print("\n[SUCESSO] Pedido deletado com sucesso!\n")
                    except psycopg2.Error as e:
                        print(f"\n[ERRO] Erro ao deletar pedido: {e}\n")
                else:
                    print("\n[CANCELADO] Exclusão cancelada.\n")
            input("Pressione Enter para continuar...")

def handle_pagamento_crud(conn):
    """Gerencia o CRUD de pagamentos"""
    while True:
        pagamento_choice = tui.pagamento_management_menu()

        if pagamento_choice == "Voltar ao Menu Principal":
            break
            
        elif pagamento_choice == "Cadastrar Pagamento":
            # Mostra pedidos pendentes
            print("\n[INFO] Pedidos pendentes de pagamento:")
            try:
                pedidos_pendentes = database.get_pedidos_pendentes(conn)
                if pedidos_pendentes:
                    tui.display_pedidos(pedidos_pendentes)
                    print("\n[INFO] Selecione um pedido da lista acima para processar o pagamento.")
                else:
                    print("\n[AVISO] Nenhum pedido pendente encontrado.")
                    print("Certifique-se de que existem pedidos cadastrados antes de processar pagamentos.")
                    input("Pressione Enter para continuar...")
                    continue
            except psycopg2.Error as e:
                print(f"\n[ERRO] Erro ao buscar pedidos pendentes: {e}")
                conn.rollback()
                input("Pressione Enter para continuar...")
                continue
            
            pagamento_data = tui.get_pagamento_data(pedidos_disponiveis=pedidos_pendentes)
            if pagamento_data:
                try:
                    database.add_pagamento(conn, pagamento_data)
                    print("\n[SUCESSO] Pagamento cadastrado com sucesso!\n")
                except psycopg2.Error as e:
                    print(f"\n[ERRO] Erro ao cadastrar pagamento: {e}\n")
            else:
                print("\n[CANCELADO] Cadastro cancelado.\n")
            input("Pressione Enter para continuar...")
            
        elif pagamento_choice == "Listar Pagamentos":
            pagamentos = database.get_all_pagamentos(conn)
            tui.display_pagamentos(pagamentos)
            input("Pressione Enter para continuar...")
            
        elif pagamento_choice == "Atualizar Pagamento":
            pagamento_id = tui.get_pagamento_id("atualizar")
            if pagamento_id:
                existing_pagamento = database.get_pagamento_by_id(conn, pagamento_id)
                if existing_pagamento:
                    tui.show_current_pagamento_data(existing_pagamento)
                    # Buscar pedidos pendentes para o update
                    pedidos_pendentes = database.get_pedidos_pendentes(conn)
                    updated_data = tui.get_pagamento_data(existing_pagamento, pedidos_disponiveis=pedidos_pendentes)
                    if updated_data:
                        try:
                            database.update_pagamento(conn, pagamento_id, updated_data)
                            print("\n[SUCESSO] Pagamento atualizado com sucesso!\n")
                        except psycopg2.Error as e:
                            print(f"\n[ERRO] Erro ao atualizar pagamento: {e}\n")
                    else:
                        print("\n[CANCELADO] Atualização cancelada.\n")
                else:
                    print("\n[ERRO] Pagamento não encontrado.\n")
            input("Pressione Enter para continuar...")
            
        elif pagamento_choice == "Deletar Pagamento":
            pagamento_id = tui.get_pagamento_id("deletar")
            if pagamento_id:
                confirm = questionary.confirm(
                    f"[AVISO] Tem certeza que deseja deletar o pagamento ID {pagamento_id}? Esta ação é irreversível."
                ).ask()
                if confirm:
                    try:
                        database.delete_pagamento(conn, pagamento_id)
                        print("\n[SUCESSO] Pagamento deletado com sucesso!\n")
                    except psycopg2.Error as e:
                        print(f"\n[ERRO] Erro ao deletar pagamento: {e}\n")
                else:
                    print("\n[CANCELADO] Exclusão cancelada.\n")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()