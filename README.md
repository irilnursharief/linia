# Queueing System 🚀

A multi-branch queueing management system designed to streamline client flow through walk-in ticket generation and online pre-registration[cite: 6]. Built with a modern Python stack, this project features real-time updates for staff and a dynamic lobby display[cite: 7].

---

## 🏗️ Project Overview

* **Project Type:** Learning Project (March 2026)[cite: 4, 8].
* **Framework:** Django (Python 3.14)[cite: 8, 113].
* **Database:** PostgreSQL[cite: 8].
* **Frontend:** Tailwind CSS & HTMX for real-time auto-refresh[cite: 8].
* **Key Feature:** Supports multiple branches with unique service configurations[cite: 8, 15].

---

## 📁 Project Structure

The project is organized into modular Django apps, each handling a specific domain of the system[cite: 10, 11]:

* **`config/`**: Project settings and root URL configurations[cite: 12].
* **`accounts/`**: Custom user models, authentication, and role-based access[cite: 12, 13].
* **`branches/`**: Management of physical branch locations[cite: 12, 13].
* **`services/`**: Definition of service types available per branch[cite: 12, 13].
* **`counters/`**: Physical counter management and staff assignment[cite: 12, 13].
* **`queue/`**: Core engine for ticket generation and queue flow logic[cite: 12, 13].
* **`display/`**: TV display screen logic for branch lobbies[cite: 12, 13].

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
Extends `AbstractUser` to include specialized roles (Admin, Staff, Client) and branch assignments[cite: 17, 18]. **Note:** This model must be defined before initial migrations[cite: 17, 121].

### Queueing Logic
* **Priority Levels:** Automated sorting based on client type: PWD (1), Senior (2), Pregnant (3), and Regular (4)[cite: 28, 31].
* **Ticket Numbers:** Auto-generated strings using service prefixes (e.g., B-001 for Billing)[cite: 23, 28].
* **Service States:** Services use an `is_active` toggle to preserve historical data instead of hard-deleting records[cite: 22, 51].

---

## 👥 User Roles & Permissions

| Role | Capabilities |
| :--- | :--- |
| **Admin** | Manage branches, services, counters, and staff; view real-time reports[cite: 33]. |
| **Staff** | Operate assigned counters, call next tickets, and manage ticket status (No-show/Complete)[cite: 33]. |
| **Client** | Register, get walk-in tickets, pre-register online, and track ticket status[cite: 33]. |

---

## 📺 TV Display System
The TV display is a read-only lobby interface that auto-refreshes every 5 seconds using **HTMX polling**[cite: 53, 63].
* Displays "Now Serving" tickets per counter[cite: 56].
* Shows real-time waiting counts and estimated wait times per service[cite: 58, 60].
* Indicates counter availability (Open, Closed, or Break)[cite: 59].

---

## 🚀 Build Roadmap

1.  **Phase 1: Foundation** - Environment setup with `uv`, PostgreSQL, and Custom User Model[cite: 69, 73].
2.  **Phase 2: Queue Core** - Ticket model implementation and priority logic[cite: 77, 81].
3.  **Phase 3: Staff Interface** - Counter dashboard and ticket handling actions[cite: 83, 85].
4.  **Phase 4: Client Interface** - Online registration and ticket generation forms[cite: 91, 94].
5.  **Phase 5: TV Display** - Lobby screen with HTMX auto-refresh logic[cite: 97, 102].
6.  **Phase 6: Admin & Reports** - Management CRUDs and daily queue statistics[cite: 103, 109].

---

## ⚙️ Installation & Setup

### Requirements
* **Python 3.14** [cite: 113]
* **uv** (Package Manager) [cite: 113]
* **PostgreSQL** [cite: 113]

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