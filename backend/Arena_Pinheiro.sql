BEGIN;


CREATE TABLE Cliente
(
    CPF character varying,
    Nome character varying,
    Email character varying,
    Tipo character varying,
    Id_Usuario_Cadastrou integer,
    PRIMARY KEY (CPF)
);

CREATE TABLE Usuario
(
    Id_Usuario integer,
    Nome character varying,
    Senha character varying,
    Tipo_Usuario character varying,
    PRIMARY KEY (Id_Usuario)
);

CREATE TABLE Item_Comanda
(
    Id_Comanda integer,
    Id_Produto integer,
    Quantidade integer,
    Preco_Unitario numeric,
    PRIMARY KEY (Id_Comanda, Id_Produto)
);

CREATE TABLE Pag_Comanda
(
    Id_Pagamento integer NOT NULL,
    Id_Comanda integer NOT NULL,
    PRIMARY KEY (Id_Pagamento),
    UNIQUE (Id_Comanda)
);

CREATE TABLE Pagamento
(
    Id_Pagamento integer NOT NULL,
    Valor numeric,
    Forma character varying,
    Tipo_Pagamento character varying,
    Id_Usuario_Cadastrou integer,
    PRIMARY KEY (Id_Pagamento)
);

CREATE TABLE Campo
(
    Id_Campo integer,
    Numero integer,
    Status character varying,
    PRIMARY KEY (Id_Campo)
);

CREATE TABLE Reserva
(
    Id_Reserva integer NOT NULL,
    Data date,
    Quant_Horas integer,
    Status character varying,
    CPF_Cliente character varying,
    Id_Campo integer,
    Id_Usuario_Cadastrou integer,
    PRIMARY KEY (Id_Reserva)
);

CREATE TABLE Pag_Compra
(
    Id_Pagamento integer,
    Id_Compra integer,
    PRIMARY KEY (Id_Pagamento),
    UNIQUE (Id_Compra)
);

CREATE TABLE Pag_Reserva
(
    Id_Pagamento integer,
    Id_Reserva integer,
    CPF_Cliente character varying,
    Porcentagem real,
    PRIMARY KEY (Id_Pagamento),
    UNIQUE (Id_Reserva)
);

CREATE TABLE Comanda
(
    Id_Comanda integer NOT NULL,
    Data date,
    Status character varying,
    Numero_Mesa integer,
    CPF_Cliente character varying,
    Id_Funcionario integer,
    PRIMARY KEY (Id_Comanda),
    UNIQUE (Numero_Mesa)
);

CREATE TABLE Mesa
(
    Numero integer NOT NULL,
    Status character varying,
    PRIMARY KEY (Numero)
);

CREATE TABLE Item_Compra
(
    Id_Compra integer,
    Id_Produto integer,
    Quantidade integer,
    Preco_Unitario numeric,
    PRIMARY KEY (Id_Compra, Id_Produto)
);

CREATE TABLE Compra
(
    Id_Compra integer NOT NULL,
    Data date,
    Valor_Total numeric,
    CPF_Cliente character varying,
    Id_Usuario_Cadastrou integer,
    PRIMARY KEY (Id_Compra)
);

CREATE TABLE Funcionario
(
    Id_Usuario integer,
    Id_Admin_Cadastrou integer,
    PRIMARY KEY (Id_Usuario)
);

CREATE TABLE Administrador
(
    Id_Usuario integer,
    PRIMARY KEY (Id_Usuario)
);

CREATE TABLE Produto
(
    Id_Produto integer NOT NULL,
    Nome character varying,
    Preco numeric,
    Validade date,
    Quant_Min_Estoque integer,
    Id_Admin_Cadastrou integer,
    PRIMARY KEY (Id_Produto)
);

CREATE TABLE Estoque
(
    Id_Estoque integer,
    Id_Produto integer,
    Quant_Present integer,
    PRIMARY KEY (Id_Estoque),
    UNIQUE (Id_Produto)
);

CREATE TABLE Movimenta
(
    Id_Movimenta integer,
    Id_Estoque integer,
    Tipo character varying,
    Quantidade integer,
    Data date,
    PRIMARY KEY (Id_Movimenta)
);

ALTER TABLE Cliente
    ADD FOREIGN KEY (Id_Usuario_Cadastrou)
    REFERENCES Usuario (Id_Usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Item_Comanda
    ADD FOREIGN KEY (Id_Produto)
    REFERENCES Produto (Id_Produto) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Item_Comanda
    ADD FOREIGN KEY (Id_Comanda)
    REFERENCES Comanda (Id_Comanda) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Pag_Comanda
    ADD FOREIGN KEY (Id_Comanda)
    REFERENCES Comanda (Id_Comanda) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Pag_Comanda
    ADD FOREIGN KEY (Id_Pagamento)
    REFERENCES Pagamento (Id_Pagamento) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Pagamento
    ADD FOREIGN KEY (Id_Usuario_Cadastrou)
    REFERENCES Usuario (Id_Usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Reserva
    ADD FOREIGN KEY (Id_Usuario_Cadastrou)
    REFERENCES Usuario (Id_Usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Reserva
    ADD FOREIGN KEY (Id_Campo)
    REFERENCES Campo (Id_Campo) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Reserva
    ADD FOREIGN KEY (CPF_Cliente)
    REFERENCES Cliente (CPF) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Pag_Compra
    ADD FOREIGN KEY (Id_Pagamento)
    REFERENCES Pagamento (Id_Pagamento) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Pag_Compra
    ADD FOREIGN KEY (Id_Compra)
    REFERENCES Compra (Id_Compra) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Pag_Reserva
    ADD FOREIGN KEY (Id_Reserva)
    REFERENCES Reserva (Id_Reserva) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Pag_Reserva
    ADD FOREIGN KEY (Id_Pagamento)
    REFERENCES Pagamento (Id_Pagamento) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Comanda
    ADD FOREIGN KEY (CPF_Cliente)
    REFERENCES Cliente (CPF) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Comanda
    ADD FOREIGN KEY (Id_Funcionario)
    REFERENCES Funcionario (Id_Usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Comanda
    ADD FOREIGN KEY (Numero_Mesa)
    REFERENCES Mesa (Numero) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Item_Compra
    ADD FOREIGN KEY (Id_Compra)
    REFERENCES Compra (Id_Compra) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Item_Compra
    ADD FOREIGN KEY (Id_Produto)
    REFERENCES Produto (Id_Produto) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Compra
    ADD FOREIGN KEY (Id_Usuario_Cadastrou)
    REFERENCES Usuario (Id_Usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Compra
    ADD FOREIGN KEY (CPF_Cliente)
    REFERENCES Cliente (CPF) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Funcionario
    ADD FOREIGN KEY (Id_Usuario)
    REFERENCES Usuario (Id_Usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Funcionario
    ADD FOREIGN KEY (Id_Admin_Cadastrou)
    REFERENCES Administrador (Id_Usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Administrador
    ADD FOREIGN KEY (Id_Usuario)
    REFERENCES Usuario (Id_Usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Produto
    ADD FOREIGN KEY (Id_Admin_Cadastrou)
    REFERENCES Administrador (Id_Usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Estoque
    ADD FOREIGN KEY (Id_Produto)
    REFERENCES Produto (Id_Produto) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE Movimenta
    ADD FOREIGN KEY (Id_Estoque)
    REFERENCES Estoque (Id_Estoque) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;