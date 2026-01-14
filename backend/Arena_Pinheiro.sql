
BEGIN;

CREATE TABLE cliente
(
    id_cliente SERIAL PRIMARY KEY,
    cpf character varying UNIQUE,
    nome character varying,
    email character varying,
    tipo character varying,
    id_usuario_cadastrou integer
);

CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY, 
    nome VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo_usuario VARCHAR(20) NOT NULL
);

CREATE TABLE item_comanda
(
    id_item_comanda SERIAL PRIMARY KEY,
    id_comanda integer,
    id_produto integer,
    quantidade integer,
    preco_unitario numeric
);

CREATE TABLE pag_comanda
(
    id_pag_comanda SERIAL PRIMARY KEY,
    id_pagamento integer NOT NULL,
    id_comanda integer NOT NULL,
    UNIQUE (id_comanda)
);

CREATE TABLE pagamento
(
    id_pagamento SERIAL PRIMARY KEY,
    valor numeric,
    forma character varying,
    tipo_pagamento character varying,
    id_usuario_cadastrou integer NULL
);

CREATE TABLE campo
(
    id_campo SERIAL PRIMARY KEY,
    numero integer,
    status character varying
);

CREATE TABLE reserva
(
    id_reserva SERIAL PRIMARY KEY,
    data date,
    quant_horas integer,
    status character varying,
    cpf_cliente character varying,
    id_campo integer,
    id_usuario_cadastrou integer NULL
);

CREATE TABLE pag_compra
(
    id_pag_compra SERIAL PRIMARY KEY,
    id_pagamento integer,
    id_compra integer,
    UNIQUE (id_compra)
);

CREATE TABLE pag_reserva
(
    id_pag_reserva SERIAL PRIMARY KEY,
    id_pagamento integer,
    id_reserva integer,
    cpf_cliente character varying,
    porcentagem real,
    UNIQUE (id_reserva)
);

CREATE TABLE comanda
(
    id_comanda SERIAL PRIMARY KEY,
    data date,
    status character varying,
    numero_mesa integer,
    cpf_cliente character varying,
    id_funcionario integer NULL,
    UNIQUE (numero_mesa)
);

CREATE TABLE mesa
(
    id_mesa SERIAL PRIMARY KEY,
    numero integer NOT NULL UNIQUE,
    status character varying
);

CREATE TABLE item_compra
(
    id_item_compra SERIAL PRIMARY KEY,
    id_compra integer,
    id_produto integer,
    quantidade integer,
    preco_unitario numeric
);

CREATE TABLE compra
(
    id_compra SERIAL PRIMARY KEY,
    data date,
    valor_total numeric,
    cpf_cliente character varying,
    id_usuario_cadastrou integer NULL
);

CREATE TABLE funcionario
(
    id_usuario integer,
    id_admin_cadastrou integer NULL,
    PRIMARY KEY (id_usuario)
);

CREATE TABLE administrador
(
    id_usuario integer PRIMARY KEY
);

CREATE TABLE produto
(
    id_produto SERIAL PRIMARY KEY,
    nome character varying,
    preco numeric,
    validade date,
    quant_min_estoque integer,
    id_admin_cadastrou integer NULL
);

CREATE TABLE estoque
(
    id_estoque SERIAL PRIMARY KEY,
    id_produto integer,
    quant_present integer,
    UNIQUE (id_produto)
);

CREATE TABLE movimenta
(
    id_movimenta SERIAL PRIMARY KEY,
    id_estoque integer,
    tipo character varying,
    quantidade integer,
    data date
);

ALTER TABLE cliente
    ADD FOREIGN KEY (id_usuario_cadastrou)
    REFERENCES usuario (id_usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE item_comanda
    ADD FOREIGN KEY (id_produto)
    REFERENCES produto (id_produto) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE item_comanda
    ADD FOREIGN KEY (id_comanda)
    REFERENCES comanda (id_comanda) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE pag_comanda
    ADD FOREIGN KEY (id_comanda)
    REFERENCES comanda (id_comanda) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE pag_comanda
    ADD FOREIGN KEY (id_pagamento)
    REFERENCES pagamento (id_pagamento) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE pagamento
    ADD FOREIGN KEY (id_usuario_cadastrou)
    REFERENCES usuario (id_usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE reserva
    ADD FOREIGN KEY (id_usuario_cadastrou)
    REFERENCES usuario (id_usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE reserva
    ADD FOREIGN KEY (id_campo)
    REFERENCES campo (id_campo) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE reserva
    ADD FOREIGN KEY (cpf_cliente)
    REFERENCES cliente (cpf) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE pag_compra
    ADD FOREIGN KEY (id_pagamento)
    REFERENCES pagamento (id_pagamento) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE pag_compra
    ADD FOREIGN KEY (id_compra)
    REFERENCES compra (id_compra) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE pag_reserva
    ADD FOREIGN KEY (id_reserva)
    REFERENCES reserva (id_reserva) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE pag_reserva
    ADD FOREIGN KEY (id_pagamento)
    REFERENCES pagamento (id_pagamento) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE comanda
    ADD FOREIGN KEY (cpf_cliente)
    REFERENCES cliente (cpf) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE comanda
    ADD FOREIGN KEY (id_funcionario)
    REFERENCES funcionario (id_usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE comanda
    ADD FOREIGN KEY (numero_mesa)
    REFERENCES mesa (numero) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE item_compra
    ADD FOREIGN KEY (id_compra)
    REFERENCES compra (id_compra) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE item_compra
    ADD FOREIGN KEY (id_produto)
    REFERENCES produto (id_produto) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE compra
    ADD FOREIGN KEY (id_usuario_cadastrou)
    REFERENCES usuario (id_usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE compra
    ADD FOREIGN KEY (cpf_cliente)
    REFERENCES cliente (cpf) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE funcionario
    ADD FOREIGN KEY (id_usuario)
    REFERENCES usuario (id_usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE funcionario
    ADD FOREIGN KEY (id_admin_cadastrou)
    REFERENCES administrador (id_usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE administrador
    ADD FOREIGN KEY (id_usuario)
    REFERENCES usuario (id_usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE produto
    ADD FOREIGN KEY (id_admin_cadastrou)
    REFERENCES administrador (id_usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE estoque
    ADD FOREIGN KEY (id_produto)
    REFERENCES produto (id_produto) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE movimenta
    ADD FOREIGN KEY (id_estoque)
    REFERENCES estoque (id_estoque) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

CREATE VIEW view_comandas_detalhadas AS
SELECT 
    c.id_comanda,
    c.data,
    c.status,
    c.numero_mesa,
    cl.nome AS nome_cliente,
    p.nome AS nome_produto,
    ic.quantidade,
    ic.preco_unitario
FROM comanda c
LEFT JOIN cliente cl ON c.cpf_cliente = cl.cpf
LEFT JOIN item_comanda ic ON c.id_comanda = ic.id_comanda
LEFT JOIN produto p ON ic.id_produto = p.id_produto;

CREATE VIEW view_reservas_detalhadas AS
SELECT 
    r.id_reserva,
    r.data,
    r.quant_horas,
    r.status,
    cl.nome AS nome_cliente,
    c.numero AS numero_campo,
    u.nome AS usuario_cadastrou
FROM reserva r
LEFT JOIN cliente cl ON r.cpf_cliente = cl.cpf
LEFT JOIN campo c ON r.id_campo = c.id_campo
LEFT JOIN usuario u ON r.id_usuario_cadastrou = u.id_usuario;

CREATE VIEW view_compras_detalhadas AS
SELECT 
    comp.id_compra,
    comp.data,
    comp.valor_total,
    cl.nome AS nome_cliente,
    p.nome AS nome_produto,
    ic.quantidade,
    ic.preco_unitario,
    u.nome AS usuario_cadastrou
FROM compra comp
LEFT JOIN cliente cl ON comp.cpf_cliente = cl.cpf
LEFT JOIN item_compra ic ON comp.id_compra = ic.id_compra
LEFT JOIN produto p ON ic.id_produto = p.id_produto
LEFT JOIN usuario u ON comp.id_usuario_cadastrou = u.id_usuario;

CREATE VIEW view_estoque_atual AS
SELECT 
    p.id_produto,
    p.nome,
    p.preco,
    p.validade,
    p.quant_min_estoque,
    e.quant_present,
    (e.quant_present - p.quant_min_estoque) AS diferenca_minimo
FROM produto p
LEFT JOIN estoque e ON p.id_produto = e.id_produto;

CREATE VIEW view_pagamentos_detalhados AS
SELECT 
    pag.id_pagamento,
    pag.valor,
    pag.forma,
    pag.tipo_pagamento,
    u.nome AS usuario_cadastrou,
    CASE 
        WHEN pc.id_compra IS NOT NULL THEN 'Compra'
        WHEN pr.id_reserva IS NOT NULL THEN 'Reserva'
        WHEN pcom.id_comanda IS NOT NULL THEN 'Comanda'
        ELSE 'Outro'
    END AS origem
FROM pagamento pag
LEFT JOIN usuario u ON pag.id_usuario_cadastrou = u.id_usuario
LEFT JOIN pag_compra pc ON pag.id_pagamento = pc.id_pagamento
LEFT JOIN pag_reserva pr ON pag.id_pagamento = pr.id_pagamento
LEFT JOIN pag_comanda pcom ON pag.id_pagamento = pcom.id_pagamento;

END;
