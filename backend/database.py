import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
from config import config

class Database:
    def __init__(self):
        self.connection: Optional[psycopg2.extensions.connection] = None
    
    def connect(self):
        """Cria conexão com o banco de dados"""
        try:
            self.connection = psycopg2.connect(**config.DB_CONFIG)
            return self.connection
        except Exception as e:
            print(f"Erro ao conectar ao banco: {e}")
            raise
    
    def get_connection(self):
        """Retorna a conexão existente ou cria uma nova"""
        if self.connection is None or self.connection.closed:
            return self.connect()
        return self.connection
    
    def _map_keys(self, row):
        """Mapeia chaves PascalCase para snake_case"""
        mapping = {
            'Id_Usuario': 'id_usuario',
            'Nome': 'nome',
            'Senha': 'senha',
            'Tipo_Usuario': 'tipo_usuario',
            'CPF': 'cpf',
            'Email': 'email',
            'Tipo': 'tipo',
            'Id_Usuario_Cadastrou': 'id_usuario_cadastrou',
            'Id_Campo': 'id_campo',
            'Numero': 'numero',
            'Status': 'status',
            'Id_Reserva': 'id_reserva',
            'Data': 'data',
            'Quant_Horas': 'quant_horas',
            'CPF_Cliente': 'cpf_cliente',
            'Id_Produto': 'id_produto',
            'Preco': 'preco',
            'Validade': 'validade',
            'Quant_Min_Estoque': 'quant_min_estoque',
            'Id_Admin_Cadastrou': 'id_admin_cadastrou',
            'Id_Estoque': 'id_estoque',
            'Quant_Present': 'quant_present',
            'Id_Movimenta': 'id_movimenta',
            'Quantidade': 'quantidade',
            'Id_Comanda': 'id_comanda',
            'Preco_Unitario': 'preco_unitario',
            'Numero_Mesa': 'numero_mesa',
            'Id_Funcionario': 'id_funcionario',
            'Id_Compra': 'id_compra',
            'Valor_Total': 'valor_total',
            'Id_Pagamento': 'id_pagamento',
            'Valor': 'valor',
            'Forma': 'forma',
            'Tipo_Pagamento': 'tipo_pagamento',
            'Porcentagem': 'porcentagem',
            'next_id': 'next_id'
        }
        if isinstance(row, dict):
            return {mapping.get(k, k.lower()): v for k, v in row.items()}
        return row

    def execute_query(self, query: str, params: tuple = None, fetch: bool = True):
        """Executa uma query e retorna os resultados"""
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(query, params)
            if fetch:
                result = cursor.fetchall()
                return [self._map_keys(dict(row)) for row in result]
            else:
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def execute_insert(self, query: str, params: tuple = None):
        """Executa um INSERT e retorna o ID gerado"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def close(self):
        """Fecha a conexão"""
        if self.connection and not self.connection.closed:
            self.connection.close()

# Instância global do banco
db = Database()
