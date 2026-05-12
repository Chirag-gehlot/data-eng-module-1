# 🐳 Data Engineering Zoomcamp — Module 1: Containerization & Infrastructure as Code

> My hands-on work for **Module 1** of the [DataTalksClub Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) — a free 9-week course on building production-ready data pipelines.

---

## 📖 Module Overview

Module 1 covers the foundational tooling every data engineer needs: containerizing services with **Docker**, running a local data warehouse with **PostgreSQL**, querying data with **SQL**, and provisioning cloud infrastructure with **Terraform** on GCP. The NYC Yellow Taxi dataset is used throughout as the working dataset.

---

## 🗂️ What's Covered

### 1. Docker & Docker Compose

Running PostgreSQL and pgAdmin as containers using `docker-compose.yaml`:

- **PostgreSQL 18** container with the `ny_taxi` database, mounted to a persistent volume
- **pgAdmin 4** container for a browser-based database GUI, available at `http://localhost:8085`
- Named Docker volumes (`ny_taxi_postgres_data`, `pgadmin_data`) for data persistence across restarts
- Port mapping: PostgreSQL on `5434`, pgAdmin on `8085`

```bash
docker-compose up -d
```

### 2. Data Ingestion Pipeline

A production-style Python ingestion script (`pipeline/data_ingestion.py`) that:

- Downloads NYC Yellow Taxi CSV data directly from the DataTalksClub GitHub releases by **year** and **month**
- Streams data into PostgreSQL in **configurable chunks** (default 100k rows) using `pandas` + `SQLAlchemy`
- Tracks ingestion progress with a `tqdm` progress bar
- Uses precise **dtype mappings** for all columns (fares, distances, timestamps, IDs)
- Parses `tpep_pickup_datetime` and `tpep_dropoff_datetime` as proper datetime types
- Fully parameterized via **CLI flags** using `click`:

```bash
python pipeline/data_ingestion.py \
  --pg-user root \
  --pg-pass root \
  --pg-host localhost \
  --pg-port 5434 \
  --pg-db ny_taxi \
  --year 2021 \
  --month 1 \
  --target-table yellow_taxi_data
```

### 3. Dockerized Ingestion Script

The ingestion script is containerized in `pipeline/Dockerfile`:

- Built on `python:3.13.10-slim`
- Uses **`uv`** (from Astral) as the fast Python package manager/runner
- Installs system dependencies (`build-essential`, `libpq-dev`) for PostgreSQL drivers
- Syncs dependencies from `pyproject.toml` + `uv.lock` for fully reproducible installs
- Entrypoint runs `data_ingestion.py` directly via `uv run`

### 4. SQL Queries on NYC Taxi Data

Practiced SQL queries in `Sql/basics.sql` against the ingested data:

- **Implicit & Explicit INNER JOINs** — joining `yellow_taxi_trips` with a `zones` lookup table to resolve pickup/dropoff location names using `CONCAT(Borough, Zone)`
- **NULL checks** — filtering for trips with missing `PULocationID` or `DOLocationID`
- **Subquery filtering** — finding location IDs not present in the zones table using `NOT IN`
- **LEFT, RIGHT, and OUTER JOINs** — handling unmatched records when a zone is deleted
- **GROUP BY + ORDER BY** — aggregating trips by day, sorting by count (ASC/DESC)
- **Multi-column aggregations** — computing `COUNT`, `MAX(total_amount)`, `MAX(passenger_count)` per day
- **Grouping by multiple fields** — breakdown by day and `DOLocationID` together

### 5. Infrastructure as Code with Terraform

Terraform configuration in `terrademo/` provisions GCP resources:

- **Provider**: Google Cloud (`hashicorp/google` v7.31.0), authenticated via a service account JSON key
- **GCS Bucket**: `google_storage_bucket` for the data lake, deployed to the `ASIA` region
  - `force_destroy = true` for easy teardown
  - Lifecycle rule to abort incomplete multipart uploads after 1 day
- **Variables** (`variable.tf`): credentials path, project ID, region, bucket name, and location — all overridable
- Project region set to `asia-south1` (Mumbai)

```bash
cd terrademo/
terraform init
terraform plan
terraform apply
```

### 6. Classwork — Python Basics

`classwork/test/list_files.py` — a small utility script using `pathlib` to list and read files in the current working directory, skipping itself. Demonstrates Python's `Path` API for filesystem operations.

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.13 | Scripting & data ingestion |
| Docker / Docker Compose | — | Containerization |
| PostgreSQL | 18 | Local data warehouse |
| pgAdmin 4 | — | Database GUI |
| pandas | 3.x | Data loading & transformation |
| SQLAlchemy | 2.x | Database connection |
| click | 8.x | CLI interface for ingestion script |
| tqdm | 4.x | Progress tracking |
| uv | latest | Fast Python package manager |
| Terraform | — | Infrastructure as Code |
| Google Cloud Platform | — | Cloud provider (GCS bucket) |

---

## 📂 Repository Structure

```
.
├── docker-compose.yaml           # PostgreSQL + pgAdmin services
├── pipeline/
│   ├── Dockerfile                # Container for the ingestion script
│   ├── data_ingestion.py         # NYC Taxi data ingestion pipeline (CLI)
│   ├── data_ingestion.ipynb      # Notebook version for exploration
│   └── pipeline.py               # Simple parameterized pipeline demo (parquet output)
├── Sql/
│   └── basics.sql                # SQL queries — JOINs, aggregations, GROUP BY
├── classwork/
│   └── test/
│       ├── list_files.py         # Pathlib file listing utility
│       └── file1/2/3.txt         # Sample test files
├── terrademo/
│   ├── main.tf                   # GCS bucket Terraform resource
│   └── variable.tf               # Input variables (project, region, bucket, creds)
├── pyproject.toml                # Python project dependencies (uv)
├── uv.lock                       # Locked dependency versions
└── .python-version               # Python 3.13
```

---

## 🚀 Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- [Terraform](https://developer.hashicorp.com/terraform/install) installed
- A GCP project with a service account JSON key
- Python 3.13+ with [uv](https://docs.astral.sh/uv/) installed

### 1. Start PostgreSQL + pgAdmin

```bash
docker-compose up -d
```

Access pgAdmin at **http://localhost:8085**
- Email: `admin@admin.com`
- Password: `root`

Connect to PostgreSQL at `localhost:5434` with user `root` / password `root`.

### 2. Ingest NYC Taxi Data

```bash
python pipeline/data_ingestion.py \
  --pg-user root \
  --pg-pass root \
  --pg-host localhost \
  --pg-port 5434 \
  --pg-db ny_taxi \
  --year 2021 \
  --month 1
```

### 3. Provision GCP Infrastructure

```bash
cd terrademo/
# Place your service account key at terrademo/keys/my-cred.json
terraform init
terraform plan
terraform apply
```

---

## 📚 Resources

- [DataTalksClub DE Zoomcamp — Module 1](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform)
- [Course YouTube Playlist](https://www.youtube.com/playlist?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
- [NYC TLC Trip Data](https://github.com/DataTalksClub/nyc-tlc-data)
- [DataTalks.Club Slack](https://datatalks.club/slack.html)

---

## 🙌 Acknowledgements

Thanks to [Alexey Grigorev](https://linkedin.com/in/agrigorev) and the DataTalksClub team for building and maintaining this excellent free course.
