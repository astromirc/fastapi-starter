# FastAPI Starter

Plantilla base para proyectos FastAPI con PostgreSQL y Docker.

## Características

- **Creación de superusuarios**: Comando interactivo para registrar administradores desde la terminal.
- **Autenticación y Recuperación de Contraseña**: Flujos preconfigurados de inicio de sesión JWT y restablecimiento de contraseña por correo electrónico.
- **Base de datos de pruebas aislada**: Las pruebas automatizadas se ejecutan en su propia base de datos independiente, evitando alterar los datos de desarrollo.
- **Lista para producción**: CORS, manejo centralizado de excepciones y variables de entorno preconfiguradas. Solo necesitas definir las variables de entorno.

## Estructura del proyecto

```text
fastapi-starter/
├── app/
│   ├── <feature_name>/
│   │   ├── dependencies.py
│   │   ├── models.py
│   │   ├── routers.py
│   │   ├── services.py
│   │   └── tasks.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   └── security.py
│   ├── shared/
│   │   ├── dependencies.py
│   │   ├── errors.py
│   │   └── timezone.py
│   ├── cli.py
│   ├── templates/
│   └── main.py
├── alembic/
├── bin/
├── tests/
│   ├── <feature_name>/
│   │   └── test_<endpoint_name>.py
│   ├── conftest.py
│   └── helpers.py
├── alembic.ini
└── pyproject.toml
```

## Requisitos

- Docker

## Instalación (Build de contenedores)

```bash
# Desarrollo
$ docker compose build

# Producción
$ docker compose -f compose.yml build
```

> **Nota:** Si usas Dev Containers al desarrollar, el build y arranque son automáticos. Evita usar `docker compose down` ya que destruye los contenedores y obliga a reconstruir el entorno al reconectar; en su lugar, usa `docker compose stop` para pausar y `docker compose start` para reanudar.

## Configuración

1. Copia el archivo `env.example` y guárdalo con el nombre `.env`.
2. Ajusta las variables de entorno del archivo `.env` según sea necesario.
3. Aplica las migraciones pendientes.

> **Nota:** En modo de desarrollo, el valor de `POSTGRES_HOST` debe ser `postgres`, que es el nombre del contenedor donde está corriendo el servidor de PostgreSQL. El resto de variables definen la base de datos y credenciales que se crearán automáticamente al levantar el servicio.

## Comandos

Comandos para gestionar el entorno desde la terminal:

```bash
# Iniciar / Levantar contenedores en segundo plano
$ docker compose up -d

# Pausar contenedores (mantiene datos e instancias)
$ docker compose stop

# Reanudar contenedores pausados
$ docker compose start

# Destruir contenedores y redes
$ docker compose down

# Entrar al contenedor del backend
$ docker compose exec backend bash
```

> **Nota:** En producción, especifica el archivo base pasando `-f compose.yml` (ej. `docker compose -f compose.yml up -d`).

## Comandos de la aplicación

Comandos disponibles dentro del contenedor:

```bash
# Crear superusuario
$ createsuperuser

# Crear migraciones
$ migration generate "nombre_de_la_migracion"

# Aplicar migraciones
$ migration upgrade

# Revertir migraciones
$ migration downgrade <revision>

# Ejecutar tests
$ tests

# Ejecutar linter
$ linter
```

## Conexión a PostgreSQL desde la máquina anfitriona

Puedes conectarte a PostgreSQL desde la máquina anfitriona utilizando `localhost` como host y el puerto `5432`. Esto permite acceder a la base de datos mediante herramientas como gestores de bases de datos o clientes SQL.

## Stack Tecnológico

- **Framework**: FastAPI
- **ORM & Validación**: SQLModel y Pydantic
- **Base de datos**: PostgreSQL
- **Migraciones**: Alembic
