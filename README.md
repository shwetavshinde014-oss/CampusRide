# CampusRide — College Bus Tracking System
> *Campus transportation, made predictable.*  
> **Course**: Third Year B.Tech Agile Software Development  
> **Project Assignment**: Problem Statement 7 — Scrum-Based Development  
> **Evaluation Mode**: B.Tech Academic Jury Demonstration  

---

## Executive Overview
**CampusRide** is a full-stack, production-quality college transportation and bus tracking web application designed according to strict Agile Scrum principles across four 2-week sprints. It addresses campus commuter uncertainty, transit overcrowding, and lack of schedule predictability by coupling an interactive OpenStreetMap tracking view with a real-time GPS simulation engine, dynamic Haversine ETA arrival forecasting, and an administrative fleet operations hub.

The visual system is designed to the standards of modern operational platforms such as Linear and Notion, utilizing a warm off-white canvas (`#F8F9FA`), deep charcoal typography (`#0F172A`), restrained teal accents (`#0D9488`), and an 8px spatial grid.

---

## Demonstration Credentials

The application provides real, server-verified role-based authorization (JWT tokens signed with bcrypt-hashed credentials stored in SQLite):

| Role | Email Address | Password | Intended Capabilities |
|:---|:---|:---|:---|
| **Student** | `student@campusride.edu` | `Student@123` | Interactive bus tracking, route stops timeline, live ETA countdown, schedule browser. |
| **Transport Admin** | `admin@campusride.edu` | `Admin@123` | Fleet management (Add/Edit/Delete buses), Route & Stop topology editor, schedule configuration, telemetry health. |

> **Jury Convenience**: The login screen and navigation bar include a one-click **"Demo Role Switcher"** allowing evaluators to instantaneously switch between Student and Transport Administrator perspectives without retyping credentials.

---

## 3 Quick Commands for Local Setup

```bash
# 1. Install all dependencies (one command)
npm install

# 2. Initialize and seed SQLite database with campus fixtures (one command)
npm run seed

# 3. Build & start the application (one command)
npm run build && npm start
```

*Open your browser and navigate to:* **`http://localhost:4000`**

*(For development with Vite hot module replacement: `npm run dev` on port 3000)*

---

## Technology Stack

| Layer | Technologies Selected | Justification |
|:---|:---|:---|
| **Frontend Framework** | React 18, TypeScript, Vite | Fast build times, type safety, modular component architecture. |
| **Styling & Design** | Tailwind CSS, Lucide Icons | Clean 8px spacing system, minimal SaaS aesthetic, zero CSS bloat. |
| **Mapping Engine** | Leaflet, OpenStreetMap | Lightweight, open-source cartography with zero vendor API lock-in. |
| **Backend Runtime** | Node.js (v20+), Express.js | Synchronous high-throughput REST API with middleware architecture. |
| **Demonstration DB** | SQLite via `better-sqlite3` | Zero-configuration local database with Write-Ahead Logging (WAL) and foreign key integrity. |
| **Authentication** | JSON Web Tokens (JWT), `bcryptjs` | Role-based authorization (`student` vs `admin`) enforced server-side. |
| **Test Runner** | Vitest v2.1.9 | High-speed unit and integration test suite executing in &lt;400ms. |

---

## Key Features

### 1. Student Transit Experience
- **Interactive Live Map**: Real-time vehicle marker with heading rotation, route polyline matching corridor color, and numbered stop markers.
- **Dynamic Stop-Level ETA**: Uses Haversine distance summation along remaining road waypoints divided by effective bus speed (clamped between 22 and 50 km/h) to provide minute-level arrival predictions (`Arriving Now`, `5 mins`, `12 mins`).
- **Telemetry Heartbeat & Stale Warning**: If GPS updates cease for &gt;40 seconds (or when simulated signal loss is activated), an amber warning banner alerts students that data is stale.
- **Bus Fleet Directory**: Searchable, filterable list of all college buses with driver contacts, seating capacity, and current status.
- **Route Timetables**: Complete schedule of morning pickup slots, evening campus departures, and intra-campus loops.

### 2. Transport Administrator Console
- **Fleet Operations Hub**: Real-time operational metrics: Total Fleet, Active on Road, Vehicles in Maintenance, Punctuality Index (94.2%), and live telemetry logs.
- **Vehicle Management (CRUD)**: Add, edit, and delete buses with duplicate registration number prevention and driver assignment.
- **Route & Stop Editor**: Create corridors, configure path distances, assign stop sequences, and modify geographic coordinates.
- **Schedule Manager**: Configure timetables across morning, evening, and shuttle slots.
- **Role-Guarded Security**: Student tokens attempting administrative mutations are blocked at the backend with `HTTP 403 Forbidden`.

### 3. GPS Telemetry Simulation Rig
- **Realistic Telemetry**: Buses step smoothly along dense Bangalore academic corridor waypoints every 2.5 seconds.
- **Interactive Controls**: Directly embedded in the navigation bar to **Play**, **Pause**, **Step** (advance 1 tick), and **Reset** bus coordinates.
- **Simulate GPS Loss**: Evaluators can drop telemetry for an active bus with a single click to test stale location alerts and fault tolerance.

---

## Agile Scrum Project Structure (Problem Statement 7)

The repository includes a comprehensive `docs/` folder containing all required Agile artifacts:

- [`01_PRODUCT_BACKLOG.md`](file:///Users/shwetashinde/.gemini/antigravity/scratch/campusride/docs/01_PRODUCT_BACKLOG.md): Prioritized Product Backlog with 14 PBIs and MoSCoW rankings.
- [`02_USER_STORIES.md`](file:///Users/shwetashinde/.gemini/antigravity/scratch/campusride/docs/02_USER_STORIES.md): Structured User Stories (`As a... I want... so that...`).
- [`03_INVEST_ANALYSIS.md`](file:///Users/shwetashinde/.gemini/antigravity/scratch/campusride/docs/03_INVEST_ANALYSIS.md): Rigorous Bill Wake INVEST assessment of core story `US-3.1` (Dynamic ETA).
- [`04_ACCEPTANCE_CRITERIA.md`](file:///Users/shwetashinde/.gemini/antigravity/scratch/campusride/docs/04_ACCEPTANCE_CRITERIA.md): Given-When-Then Gherkin acceptance criteria.
- [`05_STORY_POINT_ESTIMATION.md`](file:///Users/shwetashinde/.gemini/antigravity/scratch/campusride/docs/05_STORY_POINT_ESTIMATION.md): Planning Poker Fibonacci calibration (Total: 61 Story Points).
- [`06_SPRINT_PLANS.md`](file:///Users/shwetashinde/.gemini/antigravity/scratch/campusride/docs/06_SPRINT_PLANS.md): Four 2-week Sprint plans with Sprint Goals and target velocity.
- [`07_SPRINT_BACKLOG.md`](file:///Users/shwetashinde/.gemini/antigravity/scratch/campusride/docs/07_SPRINT_BACKLOG.md): Detailed task assignment and status matrix.
- [`08_DEFINITION_OF_DONE.md`](file:///Users/shwetashinde/.gemini/antigravity/scratch/campusride/docs/08_DEFINITION_OF_DONE.md): Definition of Done (DoD) verification criteria.
- [`09_TEST_CASES.md`](file:///Users/shwetashinde/.gemini/antigravity/scratch/campusride/docs/09_TEST_CASES.md): Automated and manual test scenario matrix.
- [`10_RISK_MANAGEMENT_PLAN.md`](file:///Users/shwetashinde/.gemini/antigravity/scratch/campusride/docs/10_RISK_MANAGEMENT_PLAN.md): Severity assessment ($R = L \times I$) and mitigation log.
- [`11_SPRINT_REVIEW_RETROSPECTIVE.md`](file:///Users/shwetashinde/.gemini/antigravity/scratch/campusride/docs/11_SPRINT_REVIEW_RETROSPECTIVE.md): Sprint review summaries and Start/Stop/Continue retrospectives.
- [`TEST_REPORT.md`](file:///Users/shwetashinde/.gemini/antigravity/scratch/campusride/docs/TEST_REPORT.md): Automated test execution report (**10/10 Passed**).

> **In-App Agile Dashboard**: Evaluators can also view the complete Sprint roadmap, story point breakdown, INVEST evaluation, and DoD checklist directly in the web application by clicking **"Scrum Dashboard & Metrics"** in the sidebar navigation.

---

## Four Sprint Delivery Summary

```
Sprint 1: Architecture, Authentication, Routes & Stops ──── 14 SP (Done)
Sprint 2: GPS Simulation Engine & Interactive Map ──────── 16 SP (Done)
Sprint 3: Dynamic ETA, Route Management & Admin Console ── 15 SP (Done)
Sprint 4: Fault Tolerance, Stale Detection & Jury Polish ─ 16 SP (Done)
────────────────────────────────────────────────────────────────────────
Total Planned & Delivered Velocity:                        61 SP (100%)
```

---

## Running the Automated Test Suite

To execute the 10 automated test scenarios covering authentication, role boundaries, GPS telemetry, ETA edge cases, and cascade deletions:

```bash
npm test
```

Expected output:
```
✓ tests/suite.test.ts (10)
  ✓ TC-01: Successful student login with valid credentials returns verified role and JWT token
  ✓ TC-02: Successful bus route and stops hierarchy viewing
  ✓ TC-03: Successful simulated GPS location update along route waypoints
  ✓ TC-04: Administrator route modification persists in SQLite database
  ✓ TC-05: Non-existent or invalid bus ID is properly handled without crashing
  ✓ TC-06: Student role is rejected when attempting administrator operations
  ✓ TC-07: GPS telemetry loss simulation activates stale location detection
  ✓ TC-08: ETA calculation accurately handles zero distance (<120m) and zero vehicle speed
  ✓ TC-09: Duplicate bus registration number prevention
  ✓ TC-10: Bus deletion safely removes associated GPS fixes and schedule entries

Test Files  1 passed (1)
     Tests  10 passed (10)
  Duration  ~370ms
```

---

## Project Structure

```
campusride/
├── docs/                                # Complete Agile Scrum documentation
│   ├── 01_PRODUCT_BACKLOG.md
│   ├── 02_USER_STORIES.md
│   ├── 03_INVEST_ANALYSIS.md
│   ├── 04_ACCEPTANCE_CRITERIA.md
│   ├── 05_STORY_POINT_ESTIMATION.md
│   ├── 06_SPRINT_PLANS.md
│   ├── 07_SPRINT_BACKLOG.md
│   ├── 08_DEFINITION_OF_DONE.md
│   ├── 09_TEST_CASES.md
│   ├── 10_RISK_MANAGEMENT_PLAN.md
│   ├── 11_SPRINT_REVIEW_RETROSPECTIVE.md
│   └── TEST_REPORT.md                   # Automated test execution report
├── server/                              # Node.js + Express backend
│   ├── auth.ts                          # JWT generation & requireRole middleware
│   ├── db.ts                            # SQLite database schema (WAL mode)
│   ├── index.ts                         # REST API endpoints & static server
│   ├── seed.ts                          # Initial demonstration dataset
│   └── simulation.ts                    # GPS simulation engine & Haversine ETA
├── src/                                 # React + TypeScript frontend
│   ├── components/                      # Reusable design system components
│   │   ├── BusMap.tsx                   # Leaflet interactive map with custom bus marker
│   │   ├── Modal.tsx                    # Accessible dialog component
│   │   ├── Navbar.tsx                   # Top bar with role switcher & simulation dock
│   │   ├── Sidebar.tsx                  # Persistent role-aware navigation
│   │   ├── SimulationControls.tsx       # Live simulation controls (Play/Pause/Step/Drop)
│   │   └── Toast.tsx                    # Toast notification provider
│   ├── context/
│   │   └── AuthContext.tsx              # Authentication state & role switching
│   ├── views/                           # Role-based dashboard views
│   │   ├── AdminBusesView.tsx           # Fleet management CRUD
│   │   ├── AdminOverviewView.tsx        # Fleet health & operations stats
│   │   ├── AdminRoutesView.tsx          # Corridors & stops editor
│   │   ├── AdminSchedulesView.tsx       # Transit timetable manager
│   │   ├── AgileDashboardView.tsx       # In-app Scrum board & jury metrics
│   │   ├── BusDirectoryView.tsx         # Searchable bus registry
│   │   ├── LoginView.tsx                # Role-based sign in with demo profiles
│   │   ├── RoutesSchedulesView.tsx      # Student corridors & timetables
│   │   └── StudentTrackingView.tsx      # Main live tracking & ETA view
│   ├── api.ts                           # Typed REST API client
│   ├── App.tsx                          # Root application container & routing
│   ├── index.css                        # Tailwind CSS directives & Leaflet styling
│   ├── main.tsx                         # DOM entry point
│   └── types.ts                         # Shared TypeScript interfaces
├── tests/
│   └── suite.test.ts                    # Vitest automated test suite (10 scenarios)
├── campusride.db                        # SQLite database file
├── index.html                           # Application HTML template
├── package.json                         # Project dependencies and npm scripts
├── tailwind.config.js                   # Custom design system tokens
├── tsconfig.json                        # Strict TypeScript compiler options
└── vite.config.ts                       # Vite bundler configuration
```
