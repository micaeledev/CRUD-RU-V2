-- ============================================
-- SCRIPT SQL COMPLETO - SISTEMA RU DA UNB
-- Para executar no DBeaver
-- ============================================

-- ============================================
-- CRIAÇÃO DAS TABELAS PRINCIPAIS (10 ENTIDADES)
-- ============================================

-- 1. USUARIO (entidade forte)
CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    matricula_usuario BIGINT UNIQUE NOT NULL,
    CPF_usuario VARCHAR(14) UNIQUE NOT NULL,
    nome_usuario VARCHAR(100) NOT NULL,
    email_usuario VARCHAR(100) UNIQUE NOT NULL,
    telefone_usuario VARCHAR(15),
    status_usuario VARCHAR(20) DEFAULT 'ativo' CHECK (status_usuario IN ('ativo', 'trancado', 'formado', 'jubilado', 'suspenso'))
);

-- 2. CATEGORIA_USUARIO (entidade fraca)
CREATE TABLE Categoria_Usuario (
    id_usuario INTEGER NOT NULL,
    nome_categoria VARCHAR(50) NOT NULL,
    grupo INTEGER NOT NULL CHECK (grupo IN (1, 2, 3)),
    subsidio VARCHAR(20) NOT NULL CHECK (subsidio IN ('total', 'parcial', 'sem_subsidio')),
    beneficio VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_usuario, nome_categoria),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE
);

-- 3. CARDAPIO
CREATE TABLE Cardapio (
    id_cardapio SERIAL PRIMARY KEY,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('cafe', 'almoco', 'jantar')),
    observacao TEXT,
    CHECK (data_fim >= data_inicio)
);

-- 4. UNIDADE
CREATE TABLE Unidade (
    id_unidade SERIAL PRIMARY KEY,
    nome_unidade VARCHAR(100) NOT NULL,
    localizacao VARCHAR(150) NOT NULL,
    telefone_unidade VARCHAR(15) NOT NULL,
    capacidade INTEGER NOT NULL CHECK (capacidade > 0),
    id_cardapio INTEGER NOT NULL,
    FOREIGN KEY (id_cardapio) REFERENCES Cardapio(id_cardapio)
);

-- 5. FUNCIONARIOS
CREATE TABLE Funcionarios (
    id_funcionario SERIAL PRIMARY KEY,
    CPF_func VARCHAR(14) UNIQUE NOT NULL,
    nome_func VARCHAR(100) NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    status_funcionario VARCHAR(20) DEFAULT 'ativo' CHECK (status_funcionario IN ('ativo', 'dispensado', 'licenca', 'ferias', 'suspenso')),
    horario VARCHAR(50),
    telefone_func VARCHAR(15),
    email_func VARCHAR(100),
    id_unidade INTEGER NOT NULL,
    FOREIGN KEY (id_unidade) REFERENCES Unidade(id_unidade)
);

-- 6. REFEICAO
CREATE TABLE Refeicao (
    id_refeicao SERIAL PRIMARY KEY,
    nome_refeicao VARCHAR(100) NOT NULL,
    funcao_prato VARCHAR(50) NOT NULL CHECK (funcao_prato IN ('prato principal', 'guarnição', 'sobremesa', 'suco', 'salada')),
    estilo_alimentar VARCHAR(50) CHECK (estilo_alimentar IN ('vegano', 'tradicional', 'vegetariano')),
    periodo_de_oferta VARCHAR(50) DEFAULT 'regular' CHECK (periodo_de_oferta IN ('regular', 'natal', 'festa_junina', 'pascoa', 'carnaval')),
    valor_nutricional_ref TEXT,
    descricao_refeicao TEXT
);

-- 7. INGREDIENTE
CREATE TABLE Ingrediente (
    id_ingrediente SERIAL PRIMARY KEY,
    nome_ingrediente VARCHAR(100) NOT NULL,
    unidade_de_medida VARCHAR(10) NOT NULL CHECK (unidade_de_medida IN ('kg', 'g', 'litros', 'ml', 'unidades', 'dentes', 'colheres')),
    valor_nutricional_ingr TEXT,
    categoria_ingrediente VARCHAR(50) CHECK (categoria_ingrediente IN ('grãos', 'carnes', 'vegetais', 'temperos', 'laticínios', 'frutas', 'oleaginosas'))
);

-- 8. PEDIDO
CREATE TABLE Pedido (
    id_pedido SERIAL PRIMARY KEY,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_do_pedido VARCHAR(20) DEFAULT 'pendente' CHECK (status_do_pedido IN ('pendente', 'pago', 'entregue', 'cancelado')),
    pedido_usuario INTEGER NOT NULL,
    ped_cardapio INTEGER NOT NULL,
    FOREIGN KEY (pedido_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (ped_cardapio) REFERENCES Cardapio(id_cardapio)
);

-- 9. PAGAMENTO (com campo binário para comprovantes)
CREATE TABLE Pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    data_pagamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor_pago DECIMAL(8,2) NOT NULL CHECK (valor_pago >= 0),
    comprovante BYTEA, -- Campo para armazenar arquivos PDF/imagens
    forma_de_pagamento VARCHAR(30) NOT NULL CHECK (forma_de_pagamento IN ('dinheiro', 'pix', 'cartao', 'vale')),
    pag_pedido INTEGER UNIQUE NOT NULL,
    pag_categoria_usuario INTEGER NOT NULL,
    pag_categoria_nome VARCHAR(50) NOT NULL,
    FOREIGN KEY (pag_pedido) REFERENCES Pedido(id_pedido),
    FOREIGN KEY (pag_categoria_usuario, pag_categoria_nome) REFERENCES Categoria_Usuario(id_usuario, nome_categoria)
);

-- 10. FEEDBACK
CREATE TABLE Feedback (
    id_feedback SERIAL PRIMARY KEY,
    nota INTEGER NOT NULL CHECK (nota >= 1 AND nota <= 5),
    comentarios TEXT,
    data_feedback TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    feed_usuario INTEGER NOT NULL,
    FOREIGN KEY (feed_usuario) REFERENCES Usuario(id_usuario)
);

-- ============================================
-- TABELAS DE RELACIONAMENTO N:N
-- ============================================

-- CARDAPIO ↔ REFEICAO (N:N)
CREATE TABLE Cardapio_Refeicao (
    id_cardapio INTEGER NOT NULL,
    id_refeicao INTEGER NOT NULL,
    PRIMARY KEY (id_cardapio, id_refeicao),
    FOREIGN KEY (id_cardapio) REFERENCES Cardapio(id_cardapio) ON DELETE CASCADE,
    FOREIGN KEY (id_refeicao) REFERENCES Refeicao(id_refeicao) ON DELETE CASCADE
);

-- REFEICAO ↔ INGREDIENTE (N:N)
CREATE TABLE Refeicao_Ingrediente (
    id_refeicao INTEGER NOT NULL,
    id_ingrediente INTEGER NOT NULL,
    PRIMARY KEY (id_refeicao, id_ingrediente),
    FOREIGN KEY (id_refeicao) REFERENCES Refeicao(id_refeicao) ON DELETE CASCADE,
    FOREIGN KEY (id_ingrediente) REFERENCES Ingrediente(id_ingrediente) ON DELETE CASCADE
);

-- ============================================
-- COMENTÁRIOS NAS TABELAS
-- ============================================

COMMENT ON TABLE Usuario IS 'Usuários do sistema (estudantes, servidores, visitantes)';
COMMENT ON TABLE Categoria_Usuario IS 'Categorias de usuários conforme Resolução 27/2018 CAD/UnB - Entidade Fraca';
COMMENT ON TABLE Cardapio IS 'Cardápios semanais por tipo de refeição';
COMMENT ON TABLE Unidade IS 'Unidades físicas do RU (Darcy, Ceilândia, Gama, Planaltina, FAL)';
COMMENT ON TABLE Funcionarios IS 'Funcionários que trabalham nas unidades do RU';
COMMENT ON TABLE Refeicao IS 'Refeições/pratos oferecidos no RU';
COMMENT ON TABLE Ingrediente IS 'Ingredientes que compõem as refeições';
COMMENT ON TABLE Pedido IS 'Pedidos realizados pelos usuários';
COMMENT ON TABLE Pagamento IS 'Pagamentos dos pedidos com comprovantes em formato binário';
COMMENT ON TABLE Feedback IS 'Avaliações dos usuários sobre o serviço';

-- ============================================
-- INSERÇÃO DE DADOS DE EXEMPLO
-- ============================================

-- Inserir Cardápios
INSERT INTO Cardapio (data_inicio, data_fim, tipo, observacao) VALUES
('2024-01-15', '2024-01-21', 'almoco', 'Cardápio almoço - Janeiro 2024'),
('2024-01-15', '2024-01-21', 'jantar', 'Cardápio jantar - Janeiro 2024'),
('2024-01-15', '2024-01-21', 'cafe', 'Cardápio café da manhã - Janeiro 2024'),
('2024-01-22', '2024-01-28', 'almoco', 'Cardápio almoço - Janeiro 2024'),
('2024-01-22', '2024-01-28', 'jantar', 'Cardápio jantar - Janeiro 2024'),
('2024-01-29', '2024-02-04', 'almoco', 'Cardápio almoço - Fevereiro 2024'),
('2024-01-29', '2024-02-04', 'cafe', 'Cardápio café da manhã - Fevereiro 2024');

-- Inserir Unidades
INSERT INTO Unidade (nome_unidade, localizacao, telefone_unidade, capacidade, id_cardapio) VALUES
('Darcy Ribeiro', 'Campus Universitário Darcy Ribeiro - Asa Norte', '(61) 3107-1234', 500, 1),
('Ceilândia', 'Campus Ceilândia - QNN 14 Área Especial', '(61) 3107-5678', 200, 2),
('Gama', 'Campus Gama - Setor Leste (Gama Leste)', '(61) 3107-9012', 150, 3),
('Planaltina', 'Campus Planaltina - Área Universitária n° 1', '(61) 3107-3456', 180, 4),
('Fazenda Água Limpa', 'Fazenda Água Limpa - Núcleo Rural', '(61) 3107-7890', 100, 5);

-- Inserir Usuários
INSERT INTO Usuario (matricula_usuario, CPF_usuario, nome_usuario, email_usuario, telefone_usuario, status_usuario) VALUES
(2023001001, '12345678901', 'João Silva Santos', 'joao.santos@aluno.unb.br', '(61) 99999-1111', 'ativo'),
(2023001002, '23456789012', 'Maria Oliveira Costa', 'maria.costa@aluno.unb.br', '(61) 99999-2222', 'ativo'),
(2023001003, '34567890123', 'Pedro Ferreira Lima', 'pedro.lima@aluno.unb.br', '(61) 99999-3333', 'ativo'),
(1998001001, '45678901234', 'Ana Carolina Souza', 'ana.souza@unb.br', '(61) 99999-4444', 'ativo'),
(1995001001, '56789012345', 'Carlos Eduardo Pereira', 'carlos.pereira@unb.br', '(61) 99999-5555', 'ativo');

-- Inserir Categorias de Usuário
INSERT INTO Categoria_Usuario (id_usuario, nome_categoria, grupo, subsidio, beneficio) VALUES
(1, 'estudante_assistencia', 1, 'total', 'Assistência Estudantil - Isento'),
(2, 'estudante_regular', 2, 'parcial', 'Estudante Regular - 60% subsídio'),
(3, 'estudante_regular', 2, 'parcial', 'Estudante Regular - 60% subsídio'),
(4, 'servidor', 3, 'sem_subsidio', 'Servidor - Sem subsídio'),
(5, 'servidor', 3, 'sem_subsidio', 'Servidor - Sem subsídio');

-- Inserir Funcionários
INSERT INTO Funcionarios (CPF_func, nome_func, cargo, status_funcionario, horario, telefone_func, email_func, id_unidade) VALUES
('11111111111', 'José da Silva', 'Cozinheiro', 'ativo', '06:00-14:00', '(61) 98888-1111', 'jose.silva@terceirizada.com.br', 1),
('22222222222', 'Francisca Santos', 'Nutricionista', 'ativo', '08:00-17:00', '(61) 98888-2222', 'francisca.santos@terceirizada.com.br', 1),
('33333333333', 'Roberto Costa', 'Auxiliar de Cozinha', 'ativo', '05:30-13:30', '(61) 98888-3333', 'roberto.costa@terceirizada.com.br', 2),
('44444444444', 'Luciana Oliveira', 'Supervisora', 'ativo', '07:00-16:00', '(61) 98888-4444', 'luciana.oliveira@terceirizada.com.br', 3),
('55555555555', 'Marcos Pereira', 'Cozinheiro', 'ativo', '06:00-14:00', '(61) 98888-5555', 'marcos.pereira@terceirizada.com.br', 4);

-- Inserir Ingredientes
INSERT INTO Ingrediente (nome_ingrediente, unidade_de_medida, valor_nutricional_ingr, categoria_ingrediente) VALUES
('Arroz branco', 'kg', '130 kcal/100g, Carboidratos: 28g', 'grãos'),
('Feijão carioca', 'kg', '123 kcal/100g, Proteínas: 8g', 'grãos'),
('Carne bovina', 'kg', '250 kcal/100g, Proteínas: 26g', 'carnes'),
('Alho', 'dentes', '42 kcal/100g, Fibras: 2g', 'temperos'),
('Cebola', 'kg', '40 kcal/100g, Vitamina C: 7mg', 'vegetais'),
('Óleo de soja', 'litros', '884 kcal/100ml, Gorduras: 100g', 'oleaginosas'),
('Sal refinado', 'kg', '0 kcal/100g, Sódio: 40g', 'temperos'),
('Tomate', 'kg', '18 kcal/100g, Vitamina C: 14mg', 'vegetais'),
('Leite integral', 'litros', '61 kcal/100ml, Proteínas: 3.2g', 'laticínios'),
('Farinha de trigo', 'kg', '364 kcal/100g, Carboidratos: 76g', 'grãos');

-- Inserir Refeições
INSERT INTO Refeicao (nome_refeicao, funcao_prato, estilo_alimentar, periodo_de_oferta, valor_nutricional_ref, descricao_refeicao) VALUES
('Arroz com Alho', 'guarnição', 'tradicional', 'regular', '150 kcal/porção', 'Arroz branco refogado com alho dourado'),
('Feijão Carioca', 'guarnição', 'tradicional', 'regular', '120 kcal/porção', 'Feijão carioca temperado com cebola e alho'),
('Bife Grelhado', 'prato principal', 'tradicional', 'regular', '280 kcal/porção', 'Bife bovino grelhado temperado'),
('Salada de Tomate', 'salada', 'vegano', 'regular', '25 kcal/porção', 'Tomate fatiado temperado com sal'),
('Suco de Laranja', 'suco', 'vegano', 'regular', '60 kcal/copo', 'Suco natural de laranja'),
('Quiche de Legumes', 'prato principal', 'vegetariano', 'regular', '220 kcal/porção', 'Torta salgada com mix de vegetais'),
('Pudim de Leite', 'sobremesa', 'tradicional', 'regular', '180 kcal/porção', 'Pudim cremoso com calda de açúcar');

-- Inserir Pedidos
INSERT INTO Pedido (data_hora, status_do_pedido, pedido_usuario, ped_cardapio) VALUES
('2024-01-15 12:30:00', 'entregue', 1, 1),
('2024-01-15 12:45:00', 'entregue', 2, 1),
('2024-01-15 13:00:00', 'pago', 3, 1),
('2024-01-16 12:20:00', 'entregue', 4, 2),
('2024-01-16 18:30:00', 'entregue', 5, 2);

-- Inserir Pagamentos (sem comprovantes binários)
INSERT INTO Pagamento (valor_pago, comprovante, forma_de_pagamento, pag_pedido, pag_categoria_usuario, pag_categoria_nome) VALUES
(0.00, NULL, 'vale', 1, 1, 'estudante_assistencia'),
(6.10, NULL, 'pix', 2, 2, 'estudante_regular'),
(6.10, NULL, 'cartao', 3, 3, 'estudante_regular'),
(15.20, NULL, 'dinheiro', 4, 4, 'servidor'),
(6.10, NULL, 'pix', 5, 5, 'servidor');

-- Inserir Feedbacks
INSERT INTO Feedback (nota, comentarios, feed_usuario) VALUES
(5, 'Excelente qualidade da comida e atendimento!', 1),
(4, 'Comida muito boa, mas a fila estava grande.', 2),
(3, 'Comida ok, mas poderia ter mais opções vegetarianas.', 3),
(5, 'Ótimo custo-benefício, recomendo!', 4),
(4, 'Ambiente agradável e comida saborosa.', 5);

-- Inserir relacionamentos Cardapio_Refeicao
INSERT INTO Cardapio_Refeicao (id_cardapio, id_refeicao) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
(2, 1), (2, 6), (2, 7), (2, 4), (2, 5),
(3, 1), (3, 2), (3, 5), (3, 6), (3, 7),
(4, 1), (4, 2), (4, 3), (4, 4),
(5, 6), (5, 7), (5, 4), (5, 5);

-- Inserir relacionamentos Refeicao_Ingrediente
INSERT INTO Refeicao_Ingrediente (id_refeicao, id_ingrediente) VALUES
(1, 1), (1, 4), (1, 6),
(2, 2), (2, 5), (2, 4),
(3, 3), (3, 7),
(4, 8), (4, 7),
(6, 5), (6, 8), (6, 4),
(7, 8), (7, 6), (7, 9);

-- ============================================
-- CRIAÇÃO DA VIEW RELATÓRIO PAGAMENTOS
-- ============================================

CREATE OR REPLACE VIEW vw_relatorio_pagamentos AS
SELECT
    u.id_usuario,
    u.nome_usuario,
    u.matricula_usuario,
    u.email_usuario,
    cu.nome_categoria,
    cu.grupo,
    cu.subsidio,
    cu.beneficio,
    p.id_pedido,
    p.data_hora AS data_pedido,
    p.status_do_pedido,
    pg.id_pagamento,
    pg.data_pagamento,
    pg.valor_pago,
    pg.forma_de_pagamento,
    pg.pag_categoria_nome,
    un.nome_unidade,
    un.localizacao,
    c.tipo AS tipo_cardapio
FROM
    Usuario u
    JOIN Categoria_Usuario cu ON u.id_usuario = cu.id_usuario
    JOIN Pedido p ON u.id_usuario = p.pedido_usuario
    JOIN Pagamento pg ON p.id_pedido = pg.pag_pedido
    LEFT JOIN Cardapio c ON p.ped_cardapio = c.id_cardapio
    LEFT JOIN Unidade un ON c.id_cardapio = un.id_cardapio;

-- ============================================
-- CRIAÇÃO DA PROCEDURE
-- ============================================

CREATE OR REPLACE PROCEDURE VerificarCapacidadeUnidade(
    p_id_unidade INTEGER,
    p_data DATE,
    p_tipo_refeicao VARCHAR(20),
    OUT p_pode_atender BOOLEAN,
    OUT p_vagas_restantes INTEGER,
    OUT p_status_mensagem TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_capacidade_maxima INTEGER;
    v_pedidos_realizados INTEGER;
    v_nome_unidade VARCHAR(100);
    v_unidade_existe BOOLEAN := FALSE;
BEGIN
    p_pode_atender := FALSE;
    p_vagas_restantes := 0;
    p_status_mensagem := '';
    
    SELECT 
        u.capacidade, 
        u.nome_unidade,
        TRUE
    INTO 
        v_capacidade_maxima, 
        v_nome_unidade,
        v_unidade_existe
    FROM Unidade u
    WHERE u.id_unidade = p_id_unidade;
    
    IF NOT v_unidade_existe THEN
        RAISE EXCEPTION 'ERRO: Unidade com ID % não encontrada no sistema.', p_id_unidade;
    END IF;
    
    IF p_tipo_refeicao NOT IN ('cafe', 'almoco', 'jantar') THEN
        RAISE EXCEPTION 'ERRO: Tipo de refeição inválido. Use: cafe, almoco ou jantar.';
    END IF;
    
    IF p_data < CURRENT_DATE THEN
        p_status_mensagem := format(
            'AVISO: Data informada (%s) já passou. Verificação apenas para consulta.',
            p_data
        );
        RAISE WARNING '%', p_status_mensagem;
    END IF;
    
    SELECT COUNT(ped.id_pedido)
    INTO v_pedidos_realizados
    FROM Pedido ped
    JOIN Cardapio card ON ped.ped_cardapio = card.id_cardapio
    JOIN Unidade un ON card.id_cardapio = un.id_cardapio
    WHERE un.id_unidade = p_id_unidade
      AND card.tipo = p_tipo_refeicao
      AND DATE(ped.data_hora) = p_data
      AND ped.status_do_pedido IN ('pago', 'entregue');
    
    v_pedidos_realizados := COALESCE(v_pedidos_realizados, 0);
    p_vagas_restantes := v_capacidade_maxima - v_pedidos_realizados;
    
    IF p_vagas_restantes > 0 THEN
        p_pode_atender := TRUE;
        p_status_mensagem := format(
            'SUCESSO: Unidade "%s" pode atender mais pedidos. Vagas disponíveis: %s de %s.',
            v_nome_unidade, p_vagas_restantes, v_capacidade_maxima
        );
        RAISE NOTICE '%', p_status_mensagem;
    ELSE
        p_pode_atender := FALSE;
        p_vagas_restantes := 0;
        
        IF v_pedidos_realizados = v_capacidade_maxima THEN
            p_status_mensagem := format(
                'LIMITE: Unidade "%s" atingiu capacidade máxima (%s pedidos) para %s em %s.',
                v_nome_unidade, v_capacidade_maxima, p_tipo_refeicao, p_data
            );
        ELSE
            p_status_mensagem := format(
                'EXCESSO: Unidade "%s" excedeu capacidade! %s pedidos realizados (máx: %s) para %s em %s.',
                v_nome_unidade, v_pedidos_realizados, v_capacidade_maxima, p_tipo_refeicao, p_data
            );
        END IF;
        
        RAISE WARNING '%', p_status_mensagem;
    END IF;
    
    RAISE NOTICE 'DEBUG: Unidade=%, Data=%, Tipo=%, Pedidos=%, Capacidade=%, Disponível=%', 
        v_nome_unidade, p_data, p_tipo_refeicao, v_pedidos_realizados, v_capacidade_maxima, p_pode_atender;
        
EXCEPTION
    WHEN OTHERS THEN
        p_pode_atender := FALSE;
        p_vagas_restantes := 0;
        p_status_mensagem := format('ERRO INESPERADO: %s', SQLERRM);
        RAISE EXCEPTION '%', p_status_mensagem;
END;
$$;

-- ============================================
-- VERIFICAÇÃO DE INTEGRIDADE
-- ============================================

-- Verificar quantidade de registros em cada tabela
SELECT
    'Usuario' as tabela, COUNT(*) as registros FROM Usuario
UNION ALL SELECT 'Categoria_Usuario', COUNT(*) FROM Categoria_Usuario
UNION ALL SELECT 'Cardapio', COUNT(*) FROM Cardapio
UNION ALL SELECT 'Unidade', COUNT(*) FROM Unidade
UNION ALL SELECT 'Funcionarios', COUNT(*) FROM Funcionarios
UNION ALL SELECT 'Refeicao', COUNT(*) FROM Refeicao
UNION ALL SELECT 'Ingrediente', COUNT(*) FROM Ingrediente
UNION ALL SELECT 'Pedido', COUNT(*) FROM Pedido
UNION ALL SELECT 'Pagamento', COUNT(*) FROM Pagamento
UNION ALL SELECT 'Feedback', COUNT(*) FROM Feedback
UNION ALL SELECT 'Cardapio_Refeicao', COUNT(*) FROM Cardapio_Refeicao
UNION ALL SELECT 'Refeicao_Ingrediente', COUNT(*) FROM Refeicao_Ingrediente
ORDER BY tabela;

-- Testar a view
SELECT * FROM vw_relatorio_pagamentos LIMIT 5;

-- Testar a procedure 
CALL VerificarCapacidadeUnidade(1, '2024-07-15', 'almoco', NULL, NULL, NULL);
