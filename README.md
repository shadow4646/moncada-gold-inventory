# Moncada Gold — Sistema de Inventario de Joyas

Sistema de gestión de inventario para **Moncada Gold**, empresa de joyería en oro laminado 18k y plata 925.

> **Entrega 1 — Semana 3**  
> Módulo: Énfasis Profesional I (Integración Continua) | POLIGRAN — Grupo B04

---

## Arquitectura

Dos contenedores Docker comunicados a través de la red interna `moncada-network`:

```
          Internet
              │
              ▼ :5000
┌─────────────────────────────────────────┐
│           moncada-network (bridge)       │
│                                         │
│  ┌───────────────┐   ┌───────────────┐  │
│  │  moncada_app  │   │  moncada_db   │  │
│  │  Flask :5000  │──▶│  PostgreSQL   │  │
│  │  (público)    │   │  (interno)    │  │
│  └───────────────┘   └───────────────┘  │
│                       volumen: pg_data  │
└─────────────────────────────────────────┘
```

| Contenedor    | Imagen                | Puerto  | Rol                          |
|---------------|-----------------------|---------|------------------------------|
| `moncada_app` | `python:3.12-slim`    | 5000    | API REST Flask (público)     |
| `moncada_db`  | `postgres:16-alpine`  | interno | Base de datos PostgreSQL     |

La comunicación entre contenedores ocurre por nombre de servicio (`db`) dentro de la red bridge `moncada-network`. El puerto 5432 de PostgreSQL **no** está expuesto al host.

---

## Estructura del proyecto

```
moncada-gold-inventory/
├── app/
│   ├── app.py            # API REST Flask - factory + rutas CRUD
│   ├── models.py         # Modelo SQLAlchemy - tabla productos
│   ├── requirements.txt  # Dependencias Python de producción
│   └── Dockerfile        # Imagen del contenedor Flask
├── db/
│   └── init.sql          # Schema PostgreSQL + 10 productos semilla
├── tests/
│   ├── test_api.py       # Suite pytest - todos los endpoints
│   └── requirements-test.txt
├── docker-compose.yml    # Orquestación de contenedores
├── .env.example          # Plantilla de variables de entorno
└── README.md
```

---

## Requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) >= 24.x
- Docker Compose >= 2.x (incluido en Docker Desktop)

---

## Inicio rápido

```bash
# 1. Clonar el repositorio
git clone https://github.com/shadow4646/moncada-gold-inventory.git
cd moncada-gold-inventory

# 2. (Opcional) Configurar variables de entorno
cp .env.example .env

# 3. Levantar los contenedores
docker-compose up --build -d

# 4. Verificar que ambos contenedores están activos
docker-compose ps
```

---

## Verificación de comunicación entre contenedores

```bash
# Health check - verifica que Flask está conectado a PostgreSQL
curl http://localhost:5000/health
# { "status": "ok", "db": "connected" }

# Listar los 10 productos semilla de Moncada Gold
curl http://localhost:5000/productos

# Inspeccionar la red y confirmar ambos contenedores
docker network inspect moncada-network
```

---

## Endpoints de la API

| Método   | Ruta                  | Descripción                        |
|----------|-----------------------|------------------------------------|
| `GET`    | `/health`             | Estado de la app y conexión a DB   |
| `GET`    | `/productos`          | Listar todo el inventario          |
| `GET`    | `/productos/<id>`     | Obtener un producto por ID         |
| `POST`   | `/productos`          | Crear un nuevo producto            |
| `PUT`    | `/productos/<id>`     | Actualizar un producto existente   |
| `DELETE` | `/productos/<id>`     | Eliminar un producto               |

### Ejemplo — agregar joya al inventario

```bash
curl -X POST http://localhost:5000/productos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Anillo Gala",
    "categoria": "anillos",
    "material": "Oro laminado 18k",
    "precio": 90000,
    "stock": 5
  }'
```

### Respuesta

```json
{
  "id": 11,
  "nombre": "Anillo Gala",
  "categoria": "anillos",
  "material": "Oro laminado 18k",
  "precio": 90000.0,
  "stock": 5,
  "created_at": "2026-05-26T10:30:00"
}
```

---

## Tests

Los tests usan SQLite en memoria (no requieren Docker):

```bash
# Instalar dependencias de test
pip install -r tests/requirements-test.txt

# Ejecutar suite completa
pytest tests/ -v
```

Cobertura: 10 tests — health, listar, crear, obtener, actualizar, eliminar, casos 404.

---

## Variables de entorno

| Variable            | Valor por defecto | Descripción               |
|---------------------|-------------------|---------------------------|
| `POSTGRES_USER`     | `moncada`         | Usuario PostgreSQL         |
| `POSTGRES_PASSWORD` | `moncada123`      | Contraseña PostgreSQL      |
| `POSTGRES_DB`       | `moncada_gold`    | Nombre de la base de datos |

---

## Roadmap CI/CD

| Entrega        | Herramienta             | Estado         |
|----------------|-------------------------|----------------|
| 1 — Semana 3   | Docker + Docker Compose | ✅ Completado  |
| 2 — Semana 5   | Jenkins                 | 🔜 Próximo     |
| 3 — Semanas 7-8| Travis CI + Codeship    | 🔜 Próximo     |

---

## Tecnologías

- **Python 3.12** + **Flask 3.x** — API REST
- **SQLAlchemy 3.x** — ORM para PostgreSQL
- **PostgreSQL 16** — Base de datos relacional
- **Docker** + **Docker Compose** — Contenedores e integración continua
- **pytest** — Suite de pruebas automatizadas
