# CAMADA DE PERSISTÊNCIA - SISTEMA RU UNB
# Este módulo implementa a camada de acesso a dados para o sistema do RU da UNB
# Gerencia 3 entidades principais em relacionamento hierárquico:
# USUARIO → PEDIDO → PAGAMENTO
# Características técnicas:
# - Conexão com PostgreSQL/Supabase
# - Chaves estrangeiras compostas
# - Validação de integridade referencial
# - Tratamento de constraints únicas

import psycopg2
import os
from datetime import datetime

def get_db_config(file_path='.env'):
    """
    CONFIGURAÇÃO DE CONEXÃO COM BANCO DE DADOS
    
    Lê as credenciais de conexão do arquivo .env para manter segurança.
    Suporta múltiplas codificações para compatibilidade.
    
    Variáveis esperadas no .env:
    - DB_NAME: Nome do banco
    - DB_USER: Usuário  
    - DB_PASSWORD: Senha
    - DB_HOST: Endereço do servidor
    - DB_PORT: Porta de conexão
    """
    config = {}
    base_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_file_path = os.path.join(base_dir, file_path)
    
    try:
        # Tenta diferentes codificações para compatibilidade cross-platform
        encodings = ['utf-8', 'latin-1', 'cp1252']
        for encoding in encodings:
            try:
                with open(absolute_file_path, 'r', encoding=encoding) as f:
                    # Parse das variáveis de ambiente no formato KEY=VALUE
                    for line in f:
                        line = line.strip()
                        # Ignora linhas vazias e comentários
                        if line and not line.startswith('#'):
                            if '=' in line:
                                key, value = line.split('=', 1)
                                config[key.strip()] = value.strip()
                break
            except UnicodeDecodeError:
                continue
    except FileNotFoundError:
        print(f"Erro: Arquivo de configuração '{absolute_file_path}' não encontrado.")
        return {}
    except Exception as e:
        print(f"Erro ao ler arquivo de configuração: {e}")
        return {}
        
    return config

def connect():
    """
    ESTABELECE CONEXÃO COM POSTGRESQL/SUPABASE
    
    Cria conexão segura com o banco de dados usando as credenciais do .env.
    Implementa tratamento de erro para falhas de conexão.
    
    Returns:
        psycopg2.connection: Objeto de conexão ativa ou None se falhar
    """
    config = get_db_config()

    if not config or not all(k in config for k in ["DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"]):
        print("Arquivo de configuração .env está incompleto ou ausente.")
        return None

    try:
        dsn = f"dbname='{config.get('DB_NAME')}' user='{config.get('DB_USER')}' host='{config.get('DB_HOST')}' password='{config.get('DB_PASSWORD')}' port='{config.get('DB_PORT')}' client_encoding='utf8'"
        conn = psycopg2.connect(dsn)
        print("[SUCESSO] Conexão com PostgreSQL estabelecida!")
        return conn
    except psycopg2.OperationalError as e:
        print(f"[ERRO] Erro ao conectar ao PostgreSQL: {e}")
        return None

def setup_database_schema(conn):
    """Verifica se as tabelas existem - não cria pois já existem no Supabase"""
    try:
        with conn.cursor() as cur:
            # Verifica se as tabelas principais existem
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('usuario', 'pedido', 'pagamento', 'cardapio', 'categoria_usuario')
                ORDER BY table_name;
            """)
            existing_tables = [row[0] for row in cur.fetchall()]
            
            print(f"[INFO] Tabelas encontradas no Supabase: {', '.join(existing_tables)}")
            
            if len(existing_tables) >= 3:
                print("[SUCESSO] Base de dados Supabase detectada e pronta para uso!")
            else:
                print("[AVISO] Algumas tabelas podem estar faltando. Verificar configuração.")
                
    except psycopg2.Error as e:
        print(f"[ERRO] Erro ao verificar schema: {e}")
        conn.rollback()

def populate_sample_data(conn):
    """Verifica dados existentes - não insere pois já existem no Supabase"""
    try:
        with conn.cursor() as cur:
            # Conta registros existentes
            cur.execute("SELECT COUNT(*) FROM Usuario;")
            usuarios_count = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM Pedido;")
            pedidos_count = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM Pagamento;")
            pagamentos_count = cur.fetchone()[0]
            
            print(f"[INFO] Dados existentes no Supabase:")
            print(f"   - Usuários: {usuarios_count}")
            print(f"   - Pedidos: {pedidos_count}")
            print(f"   - Pagamentos: {pagamentos_count}")
            
            if usuarios_count > 0:
                print("[SUCESSO] Base de dados já populada e pronta para uso!")
            else:
                print("[AVISO] Não foram encontrados dados. Verificar se a base foi populada corretamente.")
                
    except psycopg2.Error as e:
        print(f"[ERRO] Erro ao verificar dados existentes: {e}")

# CRUD USUARIO (ESTRUTURA REAL DO SUPABASE)

def add_user(conn, user_data):
    """Adiciona um novo usuário usando estrutura real do Supabase"""
    sql = """
    INSERT INTO Usuario (matricula_usuario, CPF_usuario, nome_usuario, email_usuario, telefone_usuario, status_usuario) 
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id_usuario;
    """
    with conn.cursor() as cur:
        cur.execute(sql, (
            user_data['matricula_usuario'], 
            user_data['CPF_usuario'], 
            user_data['nome_usuario'], 
            user_data['email_usuario'], 
            user_data['telefone_usuario'], 
            user_data['status_usuario']
        ))
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id

def get_all_users(conn):
    """Busca todos os usuários usando estrutura real do Supabase"""
    try:
        sql = """
        SELECT id_usuario, matricula_usuario, CPF_usuario, nome_usuario, email_usuario, telefone_usuario, status_usuario 
        FROM Usuario 
        ORDER BY id_usuario;
        """
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
    except psycopg2.Error as e:
        print(f"[ERRO] Erro ao buscar usuários: {e}")
        conn.rollback()
        return []

def get_user_by_id(conn, user_id):
    """Busca um usuário por ID usando estrutura real do Supabase"""
    sql = """
    SELECT id_usuario, matricula_usuario, CPF_usuario, nome_usuario, email_usuario, telefone_usuario, status_usuario 
    FROM Usuario 
    WHERE id_usuario = %s;
    """
    with conn.cursor() as cur:
        cur.execute(sql, (user_id,))
        return cur.fetchone()

def update_user(conn, user_id, user_data):
    """Atualiza um usuário usando estrutura real do Supabase"""
    sql = """
    UPDATE Usuario 
    SET matricula_usuario = %s, CPF_usuario = %s, nome_usuario = %s, email_usuario = %s, telefone_usuario = %s, status_usuario = %s 
    WHERE id_usuario = %s;
    """
    with conn.cursor() as cur:
        cur.execute(sql, (
            user_data['matricula_usuario'], 
            user_data['CPF_usuario'], 
            user_data['nome_usuario'], 
            user_data['email_usuario'], 
            user_data['telefone_usuario'], 
            user_data['status_usuario'], 
            user_id
        ))
        conn.commit()

def delete_user(conn, user_id):
    """Deleta um usuário usando estrutura real do Supabase"""
    sql = "DELETE FROM Usuario WHERE id_usuario = %s;"
    with conn.cursor() as cur:
        cur.execute(sql, (user_id,))
        conn.commit()

# CRUD PEDIDO (ESTRUTURA REAL SUPABASE)

def add_pedido(conn, pedido_data):
    """Adiciona um novo pedido usando estrutura real do Supabase"""
    sql = """
    INSERT INTO Pedido (pedido_usuario, ped_cardapio, status_do_pedido) 
    VALUES (%s, %s, %s)
    RETURNING id_pedido;
    """
    with conn.cursor() as cur:
        cur.execute(sql, (
            pedido_data['pedido_usuario'], 
            pedido_data['ped_cardapio'], 
            pedido_data['status_do_pedido']
        ))
        pedido_id = cur.fetchone()[0]
        conn.commit()
        return pedido_id

def get_all_pedidos(conn):
    """Busca todos os pedidos com dados do usuário usando estrutura real do Supabase"""
    try:
        sql = """
        SELECT p.id_pedido, p.pedido_usuario, u.nome_usuario, p.data_hora, p.status_do_pedido, 
               c.tipo as tipo_cardapio, c.observacao
        FROM Pedido p
        JOIN Usuario u ON p.pedido_usuario = u.id_usuario
        LEFT JOIN Cardapio c ON p.ped_cardapio = c.id_cardapio
        ORDER BY p.data_hora DESC;
        """
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
    except psycopg2.Error as e:
        print(f"[ERRO] Erro ao buscar pedidos: {e}")
        conn.rollback()
        return []

def get_pedidos_pendentes(conn):
    """Busca pedidos pendentes de pagamento usando estrutura real do Supabase"""
    try:
        sql = """
        SELECT p.id_pedido, p.pedido_usuario, u.nome_usuario, p.data_hora, p.status_do_pedido,
               c.tipo as tipo_cardapio
        FROM Pedido p
        JOIN Usuario u ON p.pedido_usuario = u.id_usuario
        LEFT JOIN Cardapio c ON p.ped_cardapio = c.id_cardapio
        WHERE p.status_do_pedido IN ('pendente', 'pago')
          AND p.id_pedido NOT IN (
              SELECT pg.pag_pedido FROM Pagamento pg WHERE pg.pag_pedido IS NOT NULL
          )
        ORDER BY p.data_hora;
        """
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
    except psycopg2.Error as e:
        print(f"[ERRO] Erro ao buscar pedidos pendentes: {e}")
        conn.rollback()
        return []

def get_pedido_by_id(conn, pedido_id):
    """Busca um pedido por ID usando estrutura real do Supabase"""
    sql = """
    SELECT p.id_pedido, p.pedido_usuario, u.nome_usuario, p.data_hora, p.status_do_pedido,
           p.ped_cardapio, c.tipo as tipo_cardapio
    FROM Pedido p
    JOIN Usuario u ON p.pedido_usuario = u.id_usuario
    LEFT JOIN Cardapio c ON p.ped_cardapio = c.id_cardapio
    WHERE p.id_pedido = %s;
    """
    with conn.cursor() as cur:
        cur.execute(sql, (pedido_id,))
        return cur.fetchone()

def update_pedido(conn, pedido_id, pedido_data):
    """Atualiza um pedido usando estrutura real do Supabase"""
    sql = """
    UPDATE Pedido 
    SET pedido_usuario = %s, ped_cardapio = %s, status_do_pedido = %s 
    WHERE id_pedido = %s;
    """
    with conn.cursor() as cur:
        cur.execute(sql, (
            pedido_data['pedido_usuario'], 
            pedido_data['ped_cardapio'], 
            pedido_data['status_do_pedido'], 
            pedido_id
        ))
        conn.commit()

def delete_pedido(conn, pedido_id):
    """Deleta um pedido usando estrutura real do Supabase"""
    sql = "DELETE FROM Pedido WHERE id_pedido = %s;"
    with conn.cursor() as cur:
        cur.execute(sql, (pedido_id,))
        conn.commit()

#  CRUD PAGAMENTO (ESTRUTURA REAL SUPABASE)

def add_pagamento(conn, pagamento_data):
    """
    FUNÇÃO PRINCIPAL: CADASTRO DE PAGAMENTO
    
    Esta é a função mais complexa do sistema, implementando:
    
    1. VALIDAÇÃO DE UNICIDADE: Impede pagamentos duplicados por pedido
    2. CHAVE ESTRANGEIRA COMPOSTA: (pag_categoria_usuario, pag_categoria_nome) 
       → CATEGORIA_USUARIO(id_usuario, nome_categoria)
    3. VERIFICAÇÃO AUTOMÁTICA DE CATEGORIA: Verifica se a categoria do usuário existe
    4. INTEGRIDADE REFERENCIAL: Garante consistência entre tabelas relacionadas
    
    Fluxo de execução:
    - FASE 1: Verificação de duplicação de pagamento
    - FASE 2: Validação de categoria de usuário  
    - FASE 3: Inserção do pagamento com FK composta
    
    Args:
        conn: Conexão ativa com PostgreSQL
        pagamento_data: Dict com dados do pagamento
        
    Returns:
        int: ID do pagamento criado
        
    Raises:
        psycopg2.Error: Para violações de constraint ou erros de BD
    """
    try:
        user_id = pagamento_data['pag_categoria_usuario']
        categoria_nome = pagamento_data['pag_categoria_nome']
        pedido_id = pagamento_data['pag_pedido']
        
        # FASE 1: VALIDAÇÃO DE UNICIDADE DE PAGAMENTO
        # O sistema permite apenas UM pagamento por pedido (constraint UNIQUE)
        # Esta verificação prévia evita violação de constraint e melhora UX (experiencia do usuário)
        
        with conn.cursor() as cur:
            cur.execute("SELECT id_pagamento FROM Pagamento WHERE pag_pedido = %s", (pedido_id,))
            existing_payment = cur.fetchone()
            
            if existing_payment:
                raise psycopg2.Error(f"Pagamento duplicado: já existe pagamento para o pedido {pedido_id}")
        
        # FASE 2: VALIDAÇÃO DE CATEGORIA DE USUÁRIO  
        # A FK composta exige que (id_usuario, nome_categoria) exista em CATEGORIA_USUARIO
        
        
        # Verificar se a categoria já existe para este usuário
        categoria_existente = get_categoria_usuario(conn, user_id, categoria_nome)
        
        if not categoria_existente:
            # Tentativa de criação automática da categoria
            categoria_criada = create_categoria_usuario_if_not_exists(conn, user_id, categoria_nome)
            
            if not categoria_criada:
                raise psycopg2.Error(f"Não foi possível criar categoria ({user_id}, {categoria_nome})")
            
            # Verificação dupla: confirmar que a categoria foi realmente criada
            categoria_existente = get_categoria_usuario(conn, user_id, categoria_nome)
            if not categoria_existente:
                raise psycopg2.Error(f"Categoria ({user_id}, {categoria_nome}) não foi criada corretamente")
        
        # FASE 3: INSERÇÃO DO PAGAMENTO COM CHAVE ESTRANGEIRA COMPOSTA
        # Agora que garantimos a existência da categoria, podemos inserir o pagamento
        # A FK composta (pag_categoria_usuario, pag_categoria_nome) será válida
        sql = """
        INSERT INTO Pagamento (pag_pedido, valor_pago, forma_de_pagamento, pag_categoria_usuario, pag_categoria_nome) 
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_pagamento;
        """
        
        with conn.cursor() as cur:
            cur.execute(sql, (
                pedido_id, 
                pagamento_data['valor_pago'], 
                pagamento_data['forma_de_pagamento'], 
                user_id,  # FK composta - parte 1: id_usuario
                categoria_nome  # FK composta - parte 2: nome_categoria  
            ))
            pagamento_id = cur.fetchone()[0]
            conn.commit()
            # SUCESSO: Pagamento inserido com integridade referencial preservada
            return pagamento_id
        
    except psycopg2.Error as e:
        print(f"[ERRO] Erro ao adicionar pagamento: {e}")
        conn.rollback()
        raise e  # Relança o erro original sem fallback que pode violar NOT NULL

def get_all_pagamentos(conn):
    """Busca todos os pagamentos com dados do pedido e usuário usando estrutura real do Supabase"""
    try:
        sql = """
        SELECT pg.id_pagamento, pg.pag_pedido, u.nome_usuario, pg.valor_pago, 
               pg.forma_de_pagamento, pg.data_pagamento, pg.pag_categoria_nome,
               p.status_do_pedido
        FROM Pagamento pg
        JOIN Pedido p ON pg.pag_pedido = p.id_pedido
        JOIN Usuario u ON p.pedido_usuario = u.id_usuario
        ORDER BY pg.data_pagamento DESC;
        """
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
    except psycopg2.Error as e:
        print(f"[ERRO] Erro ao buscar pagamentos: {e}")
        conn.rollback()
        return []

def get_pagamento_by_id(conn, pagamento_id):
    """Busca um pagamento por ID usando estrutura real do Supabase"""
    sql = """
    SELECT pg.id_pagamento, pg.pag_pedido, u.nome_usuario, pg.valor_pago, 
           pg.forma_de_pagamento, pg.data_pagamento, pg.pag_categoria_nome,
           p.status_do_pedido
    FROM Pagamento pg
    JOIN Pedido p ON pg.pag_pedido = p.id_pedido
    JOIN Usuario u ON p.pedido_usuario = u.id_usuario
    WHERE pg.id_pagamento = %s;
    """
    with conn.cursor() as cur:
        cur.execute(sql, (pagamento_id,))
        return cur.fetchone()

def update_pagamento(conn, pagamento_id, pagamento_data):
    """Atualiza um pagamento usando estrutura real do Supabase"""
    sql = """
    UPDATE Pagamento 
    SET pag_pedido = %s, valor_pago = %s, forma_de_pagamento = %s, 
        pag_categoria_usuario = %s, pag_categoria_nome = %s 
    WHERE id_pagamento = %s;
    """
    with conn.cursor() as cur:
        cur.execute(sql, (
            pagamento_data['pag_pedido'], 
            pagamento_data['valor_pago'], 
            pagamento_data['forma_de_pagamento'], 
            pagamento_data['pag_categoria_usuario'], 
            pagamento_data['pag_categoria_nome'], 
            pagamento_id
        ))
        conn.commit()

def delete_pagamento(conn, pagamento_id):
    """Deleta um pagamento usando estrutura real do Supabase"""
    sql = "DELETE FROM Pagamento WHERE id_pagamento = %s;"
    with conn.cursor() as cur:
        cur.execute(sql, (pagamento_id,))
        conn.commit()

# ==================== FUNÇÕES AUXILIARES ====================

def get_cardapios_disponiveis(conn):
    """Busca cardápios disponíveis para vincular pedidos"""
    sql = """
    SELECT id_cardapio, tipo, data_inicio, data_fim, observacao 
    FROM Cardapio 
    ORDER BY data_inicio DESC;
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()

def get_categoria_usuario(conn, user_id, categoria_nome=None):
    """Busca categoria do usuário para vincular pagamentos"""
    try:
        if categoria_nome:
            # Busca categoria específica
            sql = """
            SELECT id_usuario, nome_categoria, grupo, subsidio, beneficio 
            FROM Categoria_Usuario 
            WHERE id_usuario = %s AND nome_categoria = %s;
            """
            with conn.cursor() as cur:
                cur.execute(sql, (user_id, categoria_nome))
                return cur.fetchone()
        else:
            # Busca qualquer categoria do usuário
            sql = """
            SELECT id_usuario, nome_categoria, grupo, subsidio, beneficio 
            FROM Categoria_Usuario 
            WHERE id_usuario = %s 
            LIMIT 1;
            """
            with conn.cursor() as cur:
                cur.execute(sql, (user_id,))
                return cur.fetchone()
    except psycopg2.Error as e:
        print(f"[ERRO] Erro ao buscar categoria do usuário: {e}")
        conn.rollback()
        return None

def create_categoria_usuario_if_not_exists(conn, user_id, categoria_nome):
    """
    FUNÇÃO AUXILIAR: CRIAÇÃO AUTOMÁTICA DE CATEGORIA DE USUÁRIO
    
    Esta função implementa criação inteligente de categorias com:
    
    1. VALIDAÇÃO DE USUÁRIO: Verifica se o usuário existe antes de criar categoria
    2. CHAVE PRIMÁRIA COMPOSTA: (id_usuario, nome_categoria)
    3. CONFIGURAÇÃO AUTOMÁTICA: Define valores padrão baseados no tipo de categoria
    4. TENTATIVAS MÚLTIPLAS: Estratégia de fallback para diferentes cenários
    
    Tipos de categoria suportados:
    - estudante_assistencia: Grupo 1, subsídio total
    - estudante_regular: Grupo 2, subsídio parcial  
    - servidor: Grupo 3, sem subsídio
    
    Args:
        conn: Conexão ativa com PostgreSQL
        user_id: ID do usuário (FK para USUARIO)
        categoria_nome: Nome da categoria a ser inserida
        
    Returns:
        bool: True se categoria foi inserida/existe, False caso contrário
    """
    try:
        # ETAPA 1: VALIDAÇÃO DE INTEGRIDADE REFERENCIAL
        # Não podemos inserir categoria para usuário inexistente (violaria FK)
        
        sql_check_user = "SELECT id_usuario FROM Usuario WHERE id_usuario = %s;"
        with conn.cursor() as cur:
            cur.execute(sql_check_user, (user_id,))
            user_exists = cur.fetchone()
            
        if not user_exists:
            return False  # Usuário não existe, não podemos inserir categoria
        
        # ETAPA 2: VERIFICAÇÃO DE EXISTÊNCIA
        # Se a categoria já existe, não precisamos inserir
        
        existing = get_categoria_usuario(conn, user_id, categoria_nome)
        if existing:
            return True  # Categoria já existe, missão cumprida
        
        # ETAPA 3: CONFIGURAÇÃO AUTOMÁTICA POR TIPO DE CATEGORIA
        # Baseado na Resolução 27/2018 CAD/UnB para preços do RU
        
        categoria_config = {
            'estudante_assistencia': {
                'grupo': 1,                    # Grupo prioritário
                'subsidio': 'total',           # 100% subsidiado (R$ 0,00)
                'beneficio': 'Desconto total - Assistência estudantil'
            },
            'estudante_regular': {
                'grupo': 2,                    # Grupo intermediário  
                'subsidio': 'parcial',         # 60% subsidiado
                'beneficio': 'Desconto parcial - Estudante regular'
            },
            'servidor': {
                'grupo': 3,                    # Sem prioridade
                'subsidio': 'sem_subsidio',    # Preço integral
                'beneficio': 'Preço integral - Servidor'
            }
        }
        
        # Configuração padrão para categorias não mapeadas
        config = categoria_config.get(categoria_nome, {
            'grupo': 2,                        # Padrão: grupo intermediário
            'subsidio': 'parcial',             # Padrão: subsídio parcial
            'beneficio': f'Categoria {categoria_nome}'
        })
        
        # ETAPA 4: ESTRATÉGIA DE INSERÇÃO COM FALLBACK
        # Tentamos diferentes abordagens caso o schema tenha restrições
        
        sqls_to_try = [
            # TENTATIVA 1: Inserção completa com todos os campos de negócio
            {
                'sql': """
                INSERT INTO Categoria_Usuario (id_usuario, nome_categoria, grupo, subsidio, beneficio)
                VALUES (%s, %s, %s, %s, %s);
                """,
                'params': (user_id, categoria_nome, config['grupo'], config['subsidio'], config['beneficio'])
            },
            # TENTATIVA 2: Inserção mínima (apenas chave primária composta)
            {
                'sql': """
                INSERT INTO Categoria_Usuario (id_usuario, nome_categoria)
                VALUES (%s, %s);
                """,
                'params': (user_id, categoria_nome)
            }
        ]
        
        # Execução das tentativas em ordem de prioridade
        for i, attempt in enumerate(sqls_to_try):
            try:
                with conn.cursor() as cur:
                    cur.execute(attempt['sql'], attempt['params'])
                    conn.commit()
                    # SUCESSO: Categoria criada com sucesso
                    return True
            except psycopg2.Error as e:
                conn.rollback()
                continue  # Tenta próxima abordagem
        
        # FALHA: Todas as tentativas falharam
        return False
            
    except psycopg2.Error as e:
        conn.rollback()
        return False

