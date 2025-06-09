import duckdb
import numpy as np
from faker import Faker
import uuid
import random
import os
import time
import pandas as pd

# Configurações iniciais
start_time = time.time()
fake = Faker('pt_BR')
random.seed(42)
np.random.seed(42)

# Caminhos
SEEDS_PATH = './seeds/'
os.makedirs(SEEDS_PATH, exist_ok=True)
DB_PATH = os.path.join(SEEDS_PATH, 'data.duckdb')

# Conectar ao DuckDB (cria o banco se não existir)
con = duckdb.connect(DB_PATH)

def criar_tabelas():
    """Cria as tabelas no banco DuckDB."""
    con.execute("""
    CREATE TABLE IF NOT EXISTS cadastros (
        id UUID PRIMARY KEY,
        nome VARCHAR,
        data_nascimento DATE,
        cpf VARCHAR(14) UNIQUE,
        cep VARCHAR(9),
        cidade VARCHAR(100),
        estado VARCHAR(2),
        pais VARCHAR(50),
        genero CHAR(1),
        telefone VARCHAR(20),
        email VARCHAR(100) UNIQUE,
        data_cadastro DATE
    )
    """)
    
    con.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id_pedido UUID PRIMARY KEY,
        cpf VARCHAR(14),
        valor_pedido DECIMAL(10,2),
        valor_frete DECIMAL(10,2),
        valor_desconto DECIMAL(10,2),
        cupom VARCHAR(50),
        endereco_entrega_logradouro VARCHAR(100),
        endereco_entrega_numero VARCHAR(10),
        endereco_entrega_bairro VARCHAR(100),
        endereco_entrega_cidade VARCHAR(100),
        endereco_entrega_estado CHAR(2),
        endereco_entrega_pais VARCHAR(50),
        status_pedido VARCHAR(30),
        data_pedido DATE,
        FOREIGN KEY (cpf) REFERENCES cadastros(cpf)
    )
    """)

def get_cpfs_existentes():
    """Retorna um conjunto com todos os CPFs já cadastrados."""
    result = con.execute("SELECT cpf FROM cadastros").fetchall()
    return {row[0] for row in result} if result else set()

def gerar_lote_cadastros(tamanho_lote):
    """Gera um lote de dados de cadastro usando Faker e retorna um DataFrame."""
    print(f"  Gerando {tamanho_lote} cadastros...")
    
    # Gera os dados em lotes menores para evitar sobrecarga de memória
    chunk_size = 10000
    chunks = []
    
    for chunk_start in range(0, tamanho_lote, chunk_size):
        chunk_end = min(chunk_start + chunk_size, tamanho_lote)
        chunk_data = []
        
        for _ in range(chunk_start, chunk_end):
            cpf = fake.bothify(text='###.###.###-##')
            chunk_data.append({
                'id': str(uuid.uuid4()),
                'nome': fake.name(),
                'data_nascimento': fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
                'cpf': cpf,
                'cep': fake.postcode(),
                'cidade': fake.city(),
                'estado': fake.state_abbr(),
                'pais': 'Brasil',
                'genero': random.choice(['M', 'F']),
                'telefone': fake.phone_number(),
                'email': f"{cpf.replace('.', '').replace('-', '')}@exemplo.com.br",
                'data_cadastro': fake.date_between(start_date='-2y', end_date='today').isoformat()
            })
        
        # Cria um DataFrame com o chunk atual
        df_chunk = pd.DataFrame(chunk_data)
        
        # Remove duplicatas de CPF dentro deste chunk
        df_chunk = df_chunk.drop_duplicates(subset=['cpf'])
        
        # Adiciona à lista de chunks
        chunks.append(df_chunk)
        
        print(f"  Gerados {chunk_end}/{tamanho_lote} registros...")
    
    # Concatena todos os chunks em um único DataFrame
    if chunks:
        df = pd.concat(chunks, ignore_index=True)
        # Remove duplicatas entre chunks
        df = df.drop_duplicates(subset=['cpf'])
        return df.head(tamanho_lote)  # Garante o tamanho máximo solicitado
    return pd.DataFrame()

def gerar_lote_pedidos(cpfs, tamanho_lote):
    """Gera um lote de pedidos para os CPFs fornecidos usando Pandas para melhor desempenho."""
    try:
        print(f"  Gerando {tamanho_lote} pedidos...")
        
        # Gera os dados em lotes menores
        chunk_size = 10000
        chunks = []
        
        for chunk_start in range(0, tamanho_lote, chunk_size):
            chunk_end = min(chunk_start + chunk_size, tamanho_lote)
            chunk_data = []
            
            for _ in range(chunk_start, chunk_end):
                try:
                    # Seleciona um CPF aleatório
                    cpf = random.choice(cpfs)
                    
                    # Gera dados do pedido
                    valor_total = round(random.uniform(50, 2000), 2)
                    tem_desconto = random.random() < 0.2  # 20% de chance de ter desconto
                    valor_desconto = round(valor_total * random.uniform(0.05, 0.2), 2) if tem_desconto else 0.0
                    
                    # Gera um código de cupom único baseado em UUID se houver desconto
                    cupom = f"CUPOM{str(uuid.uuid4())[:8].upper()}" if tem_desconto else None
                    
                    chunk_data.append({
                        'id_pedido': str(uuid.uuid4()),
                        'cpf': cpf,
                        'valor_pedido': valor_total,
                        'valor_frete': round(random.uniform(5, 100), 2),
                        'valor_desconto': valor_desconto,
                        'cupom': cupom,
                        'endereco_entrega_logradouro': fake.street_name(),
                        'endereco_entrega_numero': fake.building_number(),
                        'endereco_entrega_bairro': fake.neighborhood(),
                        'endereco_entrega_cidade': fake.city(),
                        'endereco_entrega_estado': fake.state_abbr(),
                        'endereco_entrega_pais': 'Brasil',
                        'status_pedido': random.choice(['pendente', 'pago', 'enviado', 'entregue', 'cancelado']),
                        'data_pedido': fake.date_between(start_date='-2y', end_date='today').isoformat()
                    })
                except Exception as e:
                    print(f"  Erro ao gerar pedido: {str(e)}")
                    continue
            
            if not chunk_data:
                continue
                
            try:
                # Cria um DataFrame com o chunk atual
                df_chunk = pd.DataFrame(chunk_data)
                chunks.append(df_chunk)
                
                print(f"  Gerados {chunk_end}/{tamanho_lote} pedidos...")
            except Exception as e:
                print(f"  Erro ao criar DataFrame do chunk: {str(e)}")
                continue
        
        # Concatena todos os chunks em um único DataFrame
        if chunks:
            df = pd.concat(chunks, ignore_index=True)
            print(f"  Total de {len(df)} pedidos gerados com sucesso.")
            return df
        return pd.DataFrame()
        
    except Exception as e:
        print(f"Erro crítico em gerar_lote_pedidos: {str(e)}")
        return pd.DataFrame()

def inserir_em_lote(tabela, df):
    """Insere dados em lote usando Pandas DataFrame."""
    if df.empty:
        return
    
    # Converte para o formato do DuckDB
    con.register('temp_df', df)
    
    try:
        # Insere os dados, ignorando duplicatas
        con.execute(f"""
            INSERT OR IGNORE INTO {tabela} 
            SELECT * FROM temp_df
        """)
        
        # Conta quantos registros foram inseridos
        result = con.execute("SELECT COUNT(*) as inseridos FROM temp_df").fetchone()[0]
        print(f"  {result} registros inseridos na tabela {tabela}")
        
    except Exception as e:
        print(f"Erro ao inserir dados na tabela {tabela}: {str(e)}")
        raise
    finally:
        # Remove o DataFrame temporário
        con.unregister('temp_df')

def exportar_para_csv():
    """Exporta as tabelas para arquivos CSV."""
    con.execute(f"EXPORT DATABASE '{SEEDS_PATH}' (FORMAT CSV)")

def main():
    print("Iniciando geração de dados com DuckDB...")
    
    try:
        # Criar tabelas se não existirem
        criar_tabelas()
        
        # Garante que as tabelas estejam vazias
        con.execute("DELETE FROM pedidos")
        con.execute("DELETE FROM cadastros")
        
        # Gerar cadastros (1 milhão de registros)
        print("Gerando cadastros...")
        total_cadastros = 10_000
        lote_cadastros = 5_000  # Tamanho maior para melhor desempenho
        
        for i in range(0, total_cadastros, lote_cadastros):
            tamanho_atual = min(lote_cadastros, total_cadastros - i)
            print(f"Processando cadastros {i+1}-{i+tamanho_atual}...")
            
            # Gera e insere o lote de cadastros
            df_cadastros = gerar_lote_cadastros(tamanho_atual)
            if not df_cadastros.empty:
                inserir_em_lote('cadastros', df_cadastros)
        
        # Obtém os CPFs dos clientes cadastrados
        cpfs = con.execute("SELECT cpf FROM cadastros").fetchdf()['cpf'].tolist()
        
        # Gerar pedidos (5 milhões de registros)
        print("\nGerando pedidos...")
        total_pedidos = 50_000
        lote_pedidos = 5_000  # Tamanho do lote para processamento
        
        for i in range(0, total_pedidos, lote_pedidos):
            print(f"Processando pedidos {i+1}-{min(i+lote_pedidos, total_pedidos)}...")
            dados = gerar_lote_pedidos(cpfs, min(lote_pedidos, total_pedidos - i))
            inserir_em_lote('pedidos', dados)
        
        # Estatísticas
        print("\nEstatísticas:")
        total_cad = con.execute("SELECT COUNT(*) FROM cadastros").fetchone()[0]
        total_ped = con.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
        media_pedidos = total_ped / total_cad if total_cad > 0 else 0
        
        print(f"- Total de cadastros gerados: {total_cad:,}")
        print(f"- Total de pedidos gerados: {total_ped:,}")
        print(f"- Média de pedidos por cliente: {media_pedidos:.2f}")
        
        # Exportar para CSV
        print("\nExportando para CSV...")
        exportar_para_csv()
        
    finally:
        # Fechar conexão
        con.close()
        
        # Remover arquivo temporário do DuckDB
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        
        # Remover arquivos temporários (load.sql e schema.sql da pasta seeds)
        if os.path.exists(SEEDS_PATH + 'load.sql'):
            os.remove(SEEDS_PATH + 'load.sql')
        if os.path.exists(SEEDS_PATH + 'schema.sql'):
            os.remove(SEEDS_PATH + 'schema.sql')
    
    elapsed_time = time.time() - start_time
    print(f"\nTempo total de execução: {elapsed_time:.2f} segundos")

if __name__ == "__main__":
    main()