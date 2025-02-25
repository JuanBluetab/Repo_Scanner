# Repo Scanner Project

## Descripción

Este proyecto contiene scripts para clonar repositorios, escanearlos en busca de archivos de configuración y dependencias, y exportar los resultados a una base de datos PostgreSQL.

## Scripts

### clone_repos.py

Este script clona los repositorios especificados en un archivo de configuración.

#### Uso

```bash
python clone_repos.py --config_path ../config/repos_to_clone.yaml --clone_path ../repositories
```

#### Parámetros

- `--config_path`: Ruta al archivo de configuración que contiene las URLs de los repositorios.
- `--clone_path`: Ruta donde se clonarán los repositorios.

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

### Clonar Repositorios

```bash
python clone_repos.py --config_path ../config/repos_to_clone.yaml --clone_path ../repositories
```

### Escanear Repositorios

```bash
python scanner.py --base_path ../repositories --json_output_path ../output/scan_results.json --txt_output_path ../output/scan_results.txt
```

### Exportar Datos a la Base de Datos

```bash
python export_to_db.py --json_path ../output/scan_results.json --db_host localhost --db_port 5432 --db_name postgres --db_user postgres --db_password mysecretpassword --schema my_schema --table_name repository_data
```

## Configuración de la Base de Datos PostgreSQL con Podman

Para levantar una base de datos PostgreSQL utilizando Podman, puedes usar los siguientes comandos:

```bash
podman pod create --name mypod -p 5432:5432
podman run -d --name mypostgres --pod mypod -e POSTGRES_PASSWORD=mysecretpassword postgres:latest
```

Estos comandos crearán un pod llamado `mypod` y un contenedor PostgreSQL llamado `mypostgres` con la contraseña `mysecretpassword`.

## Conexión a la Base de Datos con un Cliente

Para conectarse a la base de datos PostgreSQL utilizando un cliente, puedes usar los siguientes parámetros de conexión:

- **Host**: localhost
- **Port**: 5432
- **Database**: postgres
- **Nombre de usuario**: postgres
- **Contraseña**: mysecretpassword
