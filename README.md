# Repo Scanner Project

## Descripción

Este proyecto contiene scripts para clonar repositorios, escanearlos en busca de archivos de configuración y dependencias, exportar los resultados a una base de datos PostgreSQL y copiar los repositorios actualizando la versión de Spark en sus dependencias.

## Scripts

### clone_repos.py

Este script clona los repositorios habilitados para escaneo desde la base de datos PostgreSQL.

#### Uso

```bash
python clone_repos.py --db_host localhost --db_port 5432 --db_name postgres --db_user postgres --db_password mysecretpassword --schema my_schema --clone_path ../repositories
```

#### Parámetros

- `--db_host`: Host de la base de datos.
- `--db_port`: Puerto de la base de datos.
- `--db_name`: Nombre de la base de datos.
- `--db_user`: Usuario de la base de datos.
- `--db_password`: Contraseña de la base de datos.
- `--schema`: Esquema donde se encuentran las tablas.
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

### update_spark_version.py

Este script copia los repositorios a una nueva ubicación y actualiza las dependencias de Spark a la versión especificada en el archivo de configuración.

#### Uso

```bash
python update_spark_version.py --base_path ../repositories --new_base_path ../updated_repositories --scan_results_path ../output/scan_results.json --config_path ../config/config.yaml
```

#### Parámetros

- `--base_path`: Ruta base a los repositorios originales.
- `--new_base_path`: Nueva ruta base para los repositorios copiados.
- `--scan_results_path`: Ruta al archivo JSON que contiene los resultados del escaneo.
- `--config_path`: Ruta al archivo de configuración que contiene la versión de Spark y el sufijo de artifactId.

### export_to_db.py

Este script exporta los datos JSON a una base de datos PostgreSQL, creando las tablas si no existen.

#### Uso

```bash
python export_to_db.py --json_path ../output/scan_results.json --db_host localhost --db_port 5432 --db_name postgres --db_user postgres --db_password mysecretpassword --schema my_schema --table_name repository_data
```

#### Parámetros

- `--json_path`: Ruta al archivo JSON que contiene los resultados del escaneo.
- `--db_host`: Host de la base de datos.
- `--db_port`: Puerto de la base de datos.
- `--db_name`: Nombre de la base de datos.
- `--db_user`: Usuario de la base de datos.
- `--db_password`: Contraseña de la base de datos.
- `--schema`: Esquema donde se encuentran las tablas.
- `--table_name`: Nombre de la tabla principal a crear e insertar datos.

### Estructura de la Base de Datos

El script `export_to_db.py` crea las siguientes tablas en la base de datos PostgreSQL:

- `repository_data`: Almacena información básica del repositorio y la fecha de ejecución.
- `yaml_files`: Almacena los archivos YAML asociados a cada repositorio.
- `dependencies`: Almacena las dependencias de cada repositorio.
- `requirements`: Almacena los requisitos de cada repositorio.

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
