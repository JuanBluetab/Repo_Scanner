# Repo Scanner Project

## Descripción

Este proyecto contiene scripts para escanear repositorios en busca de archivos de configuración y dependencias, y exportar los resultados a una base de datos PostgreSQL.

## Scripts

### scanner.py

Este script escanea los repositorios en busca de archivos `config.yaml`, `pom.xml` y `requirements.txt`, y genera archivos de resultados en formato JSON y texto.

#### Uso

```bash
python scanner.py --base_path ../repositories --json_output_path ../output/scan_results.json --txt_output_path ../output/scan_results.txt
```

#### Parámetros

- `--base_path`: Ruta base a los repositorios.
- `--json_output_path`: Ruta al archivo de salida en formato JSON.
- `--txt_output_path`: Ruta al archivo de salida en formato de texto.

### export_to_db.py

Este script exporta los datos JSON a una base de datos PostgreSQL, creando la tabla si no existe.

#### Uso

```bash
python export_to_db.py --json_path ../output/scan_results.json --db_host localhost --db_port 5432 --db_name mydatabase --db_user myuser --db_password mypassword --schema my_schema --table_name repository_data
```

#### Parámetros

- `--json_path`: Ruta al archivo JSON que contiene los resultados del escaneo.
- `--db_host`: Host de la base de datos.
- `--db_port`: Puerto de la base de datos.
- `--db_name`: Nombre de la base de datos.
- `--db_user`: Usuario de la base de datos.
- `--db_password`: Contraseña de la base de datos.
- `--schema`: Esquema donde se encuentra la tabla.
- `--table_name`: Nombre de la tabla a crear e insertar datos.

## Ejemplo de Comandos

### Escanear Repositorios

```bash
python scanner.py --base_path ../repositories --json_output_path ../output/scan_results.json --txt_output_path ../output/scan_results.txt
```

### Exportar Datos a la Base de Datos

```bash
python export_to_db.py --json_path ../output/scan_results.json --db_host localhost --db_port 5432 --db_name mydatabase --db_user myuser --db_password mypassword --schema my_schema --table_name repository_data
```