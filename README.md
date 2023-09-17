# Training FYG Backend

Un ecommerce genial de FYG Solutions

## Prerequisitos

- Versión estable de [Docker](https://docs.docker.com/get-docker)

## Comandos básicos

Compilar el proyecto

```bash
docker-compose -f docker-compose.local.yml build
```

Levantar el servicio de django para que se carguen las migraciones.

```bash
docker-compose -f docker-compose.local.yml up django
```

Al terminar, podemos generar el SuperUsuario, ya sea deteniendo el servicio actual o en otra terminal

```bash
docker-compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser
```

Ahora ya podremos levantar el stack completo

```bash
docker-compose -f docker-compose.local.yml up
```

## Borrado de volúmenes

Listar los volumenes

```bash
docker volume ls
```

Eliminar los volúmenes

```bash
docker volume rm fyg-training_local_postgres_data fyg-training_local_postgres_data_backups
```

Borrar los contenedores con los primero 3 dígitos mostrados en consola

```bash
docker rm 01a
```

Borrar volúmenes nuevamente

```bash
docker volume rm fyg-training_local_postgres_data fyg-training_local_postgres_data_backups
```

Levantar el proyecto y compilar

```bash
docker-compose -f docker-compose.local.yml up --build
```

Si existen nuevos cambios en los paquetes de NPM, borrar volumenes temporales.

```bash
docker-compose -f docker-compose.local.yml up --build --remove-orphans -V
```

Ejecutar pruebas unitarias

```bash
docker-compose -f docker-compose.local.yml run --rm django pytest -p no:warnings
```

Crear variable de entorno `COMPOSE_FILE` para colocar la bandera del archivo del `docker-compose.local.yml`

- Windows

  ```bash
  set COMPOSE_FILE=docker-compose.local.yml
  ```

- Linux/Mac

  ```bash
  export COMPOSE_FILE=docker-compose.local.yml
  ```

Crear fixture

```bash
docker-compose -f docker-compose.local.yml run --rm django python manage.py dumpdata app_name.ModelName --format json --output file_name_example.json
```

Cargar fixture existente

```bash
docker-compose -f docker-compose.local.yml run --rm django python manage.py loaddata --app app_name file_name_example.json -v 1 --traceback
```

Crear nueva migracion manual vacía

  ```bash
  docker-compose -f docker-compose.local.yml run --rm django python manage.py makemigrations app-name --name migration_example --empty
  ```

## Pytest

Ejecutar pruebas unitarias

  ```bash
  docker-compose -f docker-compose.local.yml run --rm django pytest -p no:warnings
  ```

## Pre-commit

### Instalación pre-commit

Se requiere tener instalado virtualenv, si no se tiene, se puede instalar así:

```bash
pip install virtualenv
```

Instalar un entorno virtual y activarlo

```bash
virtualenv venv
```

Activación en windows

```bash
venv\Scripts\activate.bat
```

Activación en Unix/Linux

```bash
. venv/bin/activate
```

Instalar los hooks de pre-commit al repositorio local para que se desencadenen al realizar commits y push::

```bash
pip install pre-commit
pre-commit install --hook-type pre-commit --hook-type pre-push
pre-commit run --all-files
```

Para actualizar dependencias de pre-commit

```bash
pre-commit autoupdate
pre-commit run --all-files
```

Para ejecutar en linux

```bash
pre-commit run all-files pip-compile || (($? == 0 || $1 == 1))
```

### Posibles problemas

<table>
<tr>
<th> Problema </th> <th> Posible solución </th>
</tr>
<tr>
<td>

```bash
An error has occurred: InvalidManifestError:
=====> C:\..\pre-commit-hooks.yaml is not a file
```

</td>
<td>

```bash
rm -rf ~/.cache/pre-commit
```

</td>
</tr>
</table>

## Backups

- Crear backup

  ```bash
  docker-compose exec postgres backup
  ```

- Listar backups

  ```bash
  docker-compose exec postgres backups
  ```

  Arrojará los backups, por ejemplo: `backup_2021_02_08T02_44_03.sql.gz`

- Restaurar backup

  ```bash
  docker-compose exec postgres restore backup_2021_02_08T02_44_03.sql.gz
  ```

- Backup hacia AWS S3

  ```shell
  docker-compose run --rm awscli upload
  docker-compose run --rm awscli download babackup_2021_02_08T02_44_03.sql.gz
  ```
