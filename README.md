# Queueing System 🚀

[cite_start]A multi-branch queueing management system designed to streamline client flow through walk-in ticket generation and online pre-registration[cite: 6]. [cite_start]Built with a modern Python stack, this project features real-time updates for staff and a dynamic lobby display[cite: 7].

---

## 🏗️ Project Overview

* [cite_start]**Project Type:** Learning Project (March 2026)[cite: 4, 8].
* [cite_start]**Framework:** Django (Python 3.14)[cite: 8, 113].
* [cite_start]**Database:** PostgreSQL[cite: 8].
* [cite_start]**Frontend:** Tailwind CSS & HTMX for real-time auto-refresh[cite: 8].
* [cite_start]**Key Feature:** Supports multiple branches with unique service configurations[cite: 8, 15].

---

## 📁 Project Structure

[cite_start]The project is organized into modular Django apps, each handling a specific domain of the system[cite: 10, 11]:

* [cite_start]**`config/`**: Project settings and root URL configurations[cite: 12].
* [cite_start]**`accounts/`**: Custom user models, authentication, and role-based access[cite: 12, 13].
* [cite_start]**`branches/`**: Management of physical branch locations[cite: 12, 13].
* [cite_start]**`services/`**: Definition of service types available per branch[cite: 12, 13].
* [cite_start]**`counters/`**: Physical counter management and staff assignment[cite: 12, 13].
* [cite_start]**`queue/`**: Core engine for ticket generation and queue flow logic[cite: 12, 13].
* [cite_start]**`display/`**: TV display screen logic for branch lobbies[cite: 12, 13].

```
linia/
├── .venv/                         # Python virtual environment (uv)
├── accounts/                      # App: Authentication + user roles
├── branches/                      # App: Branch/Location management
├── config/                        # Main Django Project Directory
│   ├── django/                    # Environment-specific settings
│   │   ├── base.py                # Base settings (Shared)
│   │   ├── dev.py                 # Development-specific settings
│   │   └── prod.py                # Production-specific settings
│   ├── settings/                  # Modular settings (e.g., Unfold, third-party)
│   │   ├── __init__.py
│   │   └── django_envrion.py      # Environment variable configuration
│   ├── __init__.py
│   ├── asgi.py                    # ASGI config for async/websockets
│   ├── env.py                     # Environment loading logic
│   ├── urls.py                    # Main URL routing
│   └── wsgi.py                    # WSGI config for web servers
├── counters/                      # App: Counter management (Queueing)
├── display/                       # App: Real-time TV/Display logic
├── queueing/                      # App: Core queueing logic & ticket generation
├── services/                      # App: Service-specific configurations
├── static/css/                    # Global static files (Compiled CSS)
├── templates/                     # Global HTML templates
├── .env                           # Local environment variables (Secret)
├── .env.example                   # Template for environment variables
├── .gitignore                     # Git exclusion rules
├── .python-version                # Python version pin (3.12/3.13)
├── main.py                        # Alternative entry point (if used)
├── manage.py                      # Django management CLI
├── pyproject.toml                 # Project metadata and dependencies (uv/ruff)
├── README.md                      # Project documentation
└── uv.lock                        # Lockfile for dependencies
```

---

## 🛠️ Database Architecture

### Accounts (`CustomUser`)
[cite_start]Extends `AbstractUser` to include specialized roles (Admin, Staff, Client) and branch assignments[cite: 17, 18]. [cite_start]**Note:** This model must be defined before initial migrations[cite: 17, 121].

### Queueing Logic
* [cite_start]**Priority Levels:** Automated sorting based on client type: PWD (1), Senior (2), Pregnant (3), and Regular (4)[cite: 28, 31].
* [cite_start]**Ticket Numbers:** Auto-generated strings using service prefixes (e.g., B-001 for Billing)[cite: 23, 28].
* [cite_start]**Service States:** Services use an `is_active` toggle to preserve historical data instead of hard-deleting records[cite: 22, 51].

---

## 👥 User Roles & Permissions

| Role | Capabilities |
| :--- | :--- |
| **Admin** | [cite_start]Manage branches, services, counters, and staff; view real-time reports[cite: 33]. |
| **Staff** | [cite_start]Operate assigned counters, call next tickets, and manage ticket status (No-show/Complete)[cite: 33]. |
| **Client** | [cite_start]Register, get walk-in tickets, pre-register online, and track ticket status[cite: 33]. |

---

## 📺 TV Display System
[cite_start]The TV display is a read-only lobby interface that auto-refreshes every 5 seconds using **HTMX polling**[cite: 53, 63].
* [cite_start]Displays "Now Serving" tickets per counter[cite: 56].
* [cite_start]Shows real-time waiting counts and estimated wait times per service[cite: 58, 60].
* [cite_start]Indicates counter availability (Open, Closed, or Break)[cite: 59].

---

## 🚀 Build Roadmap

1.  [cite_start]**Phase 1: Foundation** - Environment setup with `uv`, PostgreSQL, and Custom User Model[cite: 69, 73].
2.  [cite_start]**Phase 2: Queue Core** - Ticket model implementation and priority logic[cite: 77, 81].
3.  [cite_start]**Phase 3: Staff Interface** - Counter dashboard and ticket handling actions[cite: 83, 85].
4.  [cite_start]**Phase 4: Client Interface** - Online registration and ticket generation forms[cite: 91, 94].
5.  [cite_start]**Phase 5: TV Display** - Lobby screen with HTMX auto-refresh logic[cite: 97, 102].
6.  [cite_start]**Phase 6: Admin & Reports** - Management CRUDs and daily queue statistics[cite: 103, 109].

---

## ⚙️ Installation & Setup

### Requirements
* [cite_start]**Python 3.14** [cite: 113]
* [cite_start]**uv** (Package Manager) [cite: 113]
* [cite_start]**PostgreSQL** [cite: 113]

### Quick Start
```bash
# Initialize environment
uv init queueing-system --python 3.14
uv add django django-extensions psycopg2-binary python-decouple pillow

# Start project
uv run django-admin startproject config .

# Create Apps
uv run manage.py startapp accounts
uv run manage.py startapp branches
uv run manage.py startapp services
uv run manage.py startapp counters
uv run manage.py startapp queue
uv run manage.py startapp display