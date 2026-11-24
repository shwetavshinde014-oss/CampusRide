"""
CampusRide Streamlit - Database Module
SQLite connection, schema initialization, and query helpers.
"""

import sqlite3
import os
import hashlib
from typing import List, Dict, Any, Optional

DB_FILENAME = "campusride_streamlit.db"

def get_db_path() -> str:
    """Returns absolute path to the database file within streamlit_app folder."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, DB_FILENAME)

def get_connection() -> sqlite3.Connection:
    """Returns a SQLite connection with foreign keys enabled and row factory set to Row."""
    conn = sqlite3.connect(get_db_path(), check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    """Returns SHA-256 hash of password for secure demo comparison."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_db():
    """Creates the SQLite database schema if not already present."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('student', 'admin')),
        department TEXT,
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS routes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        color TEXT DEFAULT '#0D9488',
        total_distance_km REAL DEFAULT 0,
        estimated_duration_mins INTEGER DEFAULT 0,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS stops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        landmark TEXT,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS route_stops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_id INTEGER NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
        stop_id INTEGER NOT NULL REFERENCES stops(id) ON DELETE CASCADE,
        stop_order INTEGER NOT NULL,
        time_offset_mins INTEGER NOT NULL DEFAULT 0,
        UNIQUE(route_id, stop_order),
        UNIQUE(route_id, stop_id)
    );

    CREATE TABLE IF NOT EXISTS route_waypoints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_id INTEGER NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
        sequence INTEGER NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL
    );

    CREATE TABLE IF NOT EXISTS buses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bus_number TEXT UNIQUE NOT NULL,
        registration_number TEXT UNIQUE NOT NULL,
        capacity INTEGER NOT NULL DEFAULT 50,
        driver_name TEXT NOT NULL,
        driver_phone TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'in_transit', 'idle', 'maintenance', 'delayed')),
        current_route_id INTEGER REFERENCES routes(id) ON DELETE SET NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bus_id INTEGER NOT NULL REFERENCES buses(id) ON DELETE CASCADE,
        route_id INTEGER NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
        trip_type TEXT NOT NULL DEFAULT 'morning' CHECK(trip_type IN ('morning', 'evening', 'shuttle')),
        departure_time TEXT NOT NULL,
        arrival_time TEXT NOT NULL,
        days_of_week TEXT NOT NULL DEFAULT 'Mon-Fri',
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS gps_updates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bus_id INTEGER NOT NULL REFERENCES buses(id) ON DELETE CASCADE,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        speed_kmh REAL DEFAULT 0,
        heading REAL DEFAULT 0,
        current_stop_id INTEGER REFERENCES stops(id),
        next_stop_id INTEGER REFERENCES stops(id),
        waypoint_index INTEGER DEFAULT 0,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_simulated INTEGER DEFAULT 1,
        status_message TEXT
    );

    CREATE INDEX IF NOT EXISTS idx_gps_bus_time ON gps_updates(bus_id, timestamp DESC);
    CREATE INDEX IF NOT EXISTS idx_route_stops ON route_stops(route_id, stop_order);
    CREATE INDEX IF NOT EXISTS idx_waypoints_route ON route_waypoints(route_id, sequence);
    """)

    conn.commit()
    conn.close()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# QUERY HELPER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_buses() -> List[Dict[str, Any]]:
    conn = get_connection()
    query = """
        SELECT 
            b.*,
            r.route_code,
            r.name as route_name,
            r.color as route_color,
            g.latitude as current_latitude,
            g.longitude as current_longitude,
            g.speed_kmh as current_speed,
            g.heading as current_heading,
            g.timestamp as last_gps_time,
            g.is_simulated as is_simulated,
            g.status_message as gps_status_message
        FROM buses b
        LEFT JOIN routes r ON b.current_route_id = r.id
        LEFT JOIN (
            SELECT gu1.*
            FROM gps_updates gu1
            JOIN (
                SELECT bus_id, MAX(id) as max_id
                FROM gps_updates
                GROUP BY bus_id
            ) gu2 ON gu1.id = gu2.max_id
        ) g ON b.id = g.bus_id
        ORDER BY b.bus_number ASC
    """
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_bus_by_id(bus_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    row = conn.execute("""
        SELECT b.*, r.route_code, r.name as route_name, r.color as route_color,
               r.total_distance_km, r.estimated_duration_mins
        FROM buses b
        LEFT JOIN routes r ON b.current_route_id = r.id
        WHERE b.id = ?
    """, (bus_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_routes() -> List[Dict[str, Any]]:
    conn = get_connection()
    query = """
        SELECT 
            r.*,
            COUNT(DISTINCT rs.stop_id) as stop_count,
            COUNT(DISTINCT b.id) as assigned_bus_count
        FROM routes r
        LEFT JOIN route_stops rs ON r.id = rs.route_id
        LEFT JOIN buses b ON r.id = b.current_route_id
        GROUP BY r.id
        ORDER BY r.route_code ASC
    """
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_route_by_id(route_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    row = conn.execute("SELECT * FROM routes WHERE id = ?", (route_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_stops_for_route(route_id: int) -> List[Dict[str, Any]]:
    conn = get_connection()
    query = """
        SELECT s.*, rs.stop_order, rs.time_offset_mins
        FROM route_stops rs
        JOIN stops s ON rs.stop_id = s.id
        WHERE rs.route_id = ?
        ORDER BY rs.stop_order ASC
    """
    rows = conn.execute(query, (route_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_stops() -> List[Dict[str, Any]]:
    conn = get_connection()
    query = """
        SELECT s.*, COUNT(DISTINCT rs.route_id) as route_count
        FROM stops s
        LEFT JOIN route_stops rs ON s.id = rs.stop_id
        GROUP BY s.id
        ORDER BY s.name ASC
    """
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_waypoints_for_route(route_id: int) -> List[Dict[str, Any]]:
    conn = get_connection()
    query = """
        SELECT sequence, latitude, longitude
        FROM route_waypoints
        WHERE route_id = ?
        ORDER BY sequence ASC
    """
    rows = conn.execute(query, (route_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_schedules(route_id: Optional[int] = None, bus_id: Optional[int] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    query = """
        SELECT 
            s.*,
            b.bus_number,
            b.driver_name,
            r.route_code,
            r.name as route_name,
            r.color as route_color
        FROM schedules s
        JOIN buses b ON s.bus_id = b.id
        JOIN routes r ON s.route_id = r.id
        WHERE 1=1
    """
    params = []
    if route_id:
        query += " AND s.route_id = ?"
        params.append(route_id)
    if bus_id:
        query += " AND s.bus_id = ?"
        params.append(bus_id)
    query += " ORDER BY s.departure_time ASC"

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_latest_gps(bus_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    row = conn.execute("""
        SELECT * FROM gps_updates
        WHERE bus_id = ?
        ORDER BY timestamp DESC, id DESC
        LIMIT 1
    """, (bus_id,)).fetchone()
    conn.close()
    return dict(row) if row else None
