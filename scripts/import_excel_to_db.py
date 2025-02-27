import pandas as pd
import psycopg2
from psycopg2 import sql
import yaml
import argparse
import logging

def read_excel(file_path):
    """
    Leer el archivo Excel y extraer las hojas de organizaciones, repositorios y reuniones.
    
    :param file_path: Ruta del archivo Excel.
    :return: DataFrames de organizaciones, repositorios y reuniones.
    """
    logging.info(f"Leyendo el archivo Excel: {file_path}")
    xls = pd.ExcelFile(file_path)
    orgs_df = pd.read_excel(xls, 'organizations')
    repos_df = pd.read_excel(xls, 'repositories')
    meetings_df = pd.read_excel(xls, 'meetings')
    return orgs_df, repos_df, meetings_df

def connect_db(db_config):
    """
    Conectar a la base de datos PostgreSQL.
    
    :param db_config: Diccionario con la configuración de la base de datos.
    :return: Conexión a la base de datos.
    """
    logging.info("Conectando a la base de datos PostgreSQL")
    conn = psycopg2.connect(**db_config)
    return conn

def insert_organizations(conn, df):
    """
    Insertar datos en la tabla de organizaciones y devolver un diccionario con los IDs generados.
    
    :param conn: Conexión a la base de datos.
    :param df: DataFrame con los datos a insertar.
    :return: Diccionario con los nombres de las organizaciones y sus IDs generados.
    """
    logging.info("Insertando datos en la tabla: organizations")
    cursor = conn.cursor()
    org_ids = {}
    for index, row in df.iterrows():
        columns = list(row.index)
        values = [row[col] for col in columns]
        insert_statement = sql.SQL(
            'INSERT INTO my_schema.organizations ({}) VALUES ({}) RETURNING id'
        ).format(
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        cursor.execute(insert_statement, values)
        org_id = cursor.fetchone()[0]
        org_ids[row['name']] = org_id
    conn.commit()
    cursor.close()
    return org_ids

def insert_repositories(conn, df, org_ids):
    """
    Insertar datos en la tabla de repositorios.
    
    :param conn: Conexión a la base de datos.
    :param df: DataFrame con los datos a insertar.
    :param org_ids: Diccionario con los nombres de las organizaciones y sus IDs generados.
    """
    logging.info("Insertando datos en la tabla: repositories")
    cursor = conn.cursor()
    for index, row in df.iterrows():
        columns = ['organization_id', 'name', 'link', 'scan', 'last_scan_date']
        values = [org_ids[row['organization']], row['name'], row['link'], row['scan'], None]
        insert_statement = sql.SQL(
            'INSERT INTO my_schema.repositories ({}) VALUES ({})'
        ).format(
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        cursor.execute(insert_statement, values)
    conn.commit()
    cursor.close()

def insert_meetings(conn, df, org_ids):
    """
    Insertar datos en la tabla de reuniones.
    
    :param conn: Conexión a la base de datos.
    :param df: DataFrame con los datos a insertar.
    :param org_ids: Diccionario con los nombres de las organizaciones y sus IDs generados.
    """
    logging.info("Insertando datos en la tabla: meetings")
    cursor = conn.cursor()
    for index, row in df.iterrows():
        columns = ['organization_id', 'date', 'description']
        values = [org_ids[row['organization']], row['date'], row['description']]
        insert_statement = sql.SQL(
            'INSERT INTO my_schema.meetings ({}) VALUES ({})'
        ).format(
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        cursor.execute(insert_statement, values)
    conn.commit()
    cursor.close()

def main():
    """
    Función principal para leer el archivo Excel y exportar los datos a la base de datos.
    """
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description='Importar datos de un archivo Excel a la base de datos PostgreSQL.')
    parser.add_argument('--config_path', type=str, required=True, help='Ruta del archivo de configuración.')
    parser.add_argument('--db_host', type=str, required=True, help='Host de la base de datos.')
    parser.add_argument('--db_port', type=int, required=True, help='Puerto de la base de datos.')
    parser.add_argument('--db_name', type=str, required=True, help='Nombre de la base de datos.')
    parser.add_argument('--db_user', type=str, required=True, help='Usuario de la base de datos.')
    parser.add_argument('--db_password', type=str, required=True, help='Contraseña de la base de datos.')
    args = parser.parse_args()

    try:
        with open(args.config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        file_path = config['excel_file_path']
        orgs_df, repos_df, meetings_df = read_excel(file_path)
        
        db_config = {
            'host': args.db_host,
            'port': args.db_port,
            'dbname': args.db_name,
            'user': args.db_user,
            'password': args.db_password
        }
        
        conn = connect_db(db_config)
        try:
            org_ids = insert_organizations(conn, orgs_df)
            insert_repositories(conn, repos_df, org_ids)
            insert_meetings(conn, meetings_df, org_ids)
        finally:
            conn.close()
    except Exception as e:
        logging.error(f"Error en la función principal: {e}")

if __name__ == "__main__":
    main()
