"""
CampusRide Streamlit - GPS Simulation & ETA Engine
Calculates Haversine distances, route traversal, bearing, ETAs, and handles telemetry simulation.
"""

import math
from datetime import datetime, timezone
from typing import List, Dict, Any, Tuple, Optional
from database import get_connection

def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two coordinates in kilometers using Haversine formula."""
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return 0.0
    R = 6371.0  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2.0) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(max(0.0, min(1.0, a))), math.sqrt(max(0.0, min(1.0, 1.0 - a))))
    return R * c

def calculate_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates initial bearing (compass heading) from point 1 to point 2 in degrees."""
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return 0.0
    y = math.sin(math.radians(lon2 - lon1)) * math.cos(math.radians(lat2))
    x = (math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) -
         math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.cos(math.radians(lon2 - lon1)))
    initial_bearing = math.degrees(math.atan2(y, x))
    return round((initial_bearing + 360.0) % 360.0, 1)

def calculate_eta(current_lat: Optional[float], current_lon: Optional[float],
                  stop_lat: float, stop_lon: float,
                  remaining_waypoints: Any = None,
                  speed_kmh: float = 30.0,
                  is_dropped: bool = False) -> Dict[str, Any]:
    """
    Computes real-time dynamic arrival estimate (ETA) to a specific stop along remaining route waypoints.
    Handles zero distance, missing coordinates, and unavailable GPS gracefully.
    """
    # Handle GPS unavailable / signal loss state
    if is_dropped or current_lat is None or current_lon is None:
        return {
            "distance_km": None,
            "eta_minutes": None,
            "status": "GPS Unavailable",
            "display_time": "Unavailable",
            "detail": "Location signal lost — waiting for telemetry update",
            "badge_color": "#92400E",
            "badge_bg": "#FEF3C7",
            "badge_border": "#FCD34D"
        }

    direct_dist = calculate_distance_km(current_lat, current_lon, stop_lat, stop_lon)

    # Proximity threshold: if within 120m, the bus is arriving at the stop platform
    if direct_dist <= 0.12:
        return {
            "distance_km": round(direct_dist, 2),
            "eta_minutes": 0,
            "status": "Arriving Now",
            "display_time": "Arriving Now",
            "detail": "Bus is at stop platform (<120m)",
            "badge_color": "#166534",
            "badge_bg": "#DCFCE7",
            "badge_border": "#86EFAC"
        }

    # Calculate remaining route distance using route waypoints if available
    total_dist = direct_dist * 1.15  # Baseline road curvature

    if remaining_waypoints:
        # Extract (lat, lon) coordinates regardless of dict or tuple structure
        pts = []
        for p in remaining_waypoints:
            if isinstance(p, (tuple, list)) and len(p) >= 2:
                pts.append((float(p[0]), float(p[1])))
            elif isinstance(p, dict):
                lat = p.get("latitude", p.get("lat"))
                lon = p.get("longitude", p.get("lon", p.get("lng")))
                if lat is not None and lon is not None:
                    pts.append((float(lat), float(lon)))

        if pts:
            # Find waypoint closest to target stop
            closest_idx = 0
            min_d = float('inf')
            for i, pt in enumerate(pts):
                d = calculate_distance_km(pt[0], pt[1], stop_lat, stop_lon)
                if d < min_d:
                    min_d = d
                    closest_idx = i

            # If closest waypoint is reasonably near the stop (<1.2km), stop is ahead on remaining corridor
            if min_d <= 1.2:
                accum = calculate_distance_km(current_lat, current_lon, pts[0][0], pts[0][1])
                for k in range(closest_idx):
                    accum += calculate_distance_km(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1])
                accum += calculate_distance_km(pts[closest_idx][0], pts[closest_idx][1], stop_lat, stop_lon)
                total_dist = max(direct_dist, accum)
            else:
                # Stop is behind or on circular return loop
                total_dist = direct_dist * 1.25

    # Realistic effective speed (min 18.0 km/h, max 50.0 km/h, fallback 28.0 km/h if stationary)
    effective_speed = max(18.0, min(50.0, float(speed_kmh) if speed_kmh and float(speed_kmh) > 5.0 else 28.0))
    travel_time_hours = total_dist / effective_speed
    eta_mins = max(1, round(travel_time_hours * 60.0))
    status_text = f"{eta_mins} min" if eta_mins == 1 else f"{eta_mins} mins"

    return {
        "distance_km": round(total_dist, 1),
        "eta_minutes": eta_mins,
        "status": status_text,
        "display_time": status_text,
        "detail": f"{round(total_dist, 1)} km remaining • {round(effective_speed)} km/h avg",
        "badge_color": "#0F766E",
        "badge_bg": "#CCFBF1",
        "badge_border": "#5EEAD4"
    }

def step_simulation_tick(bus_id: Optional[int] = None, dropped_bus_ids: List[int] = None) -> int:
    """
    Advances buses along their route waypoints by 1 step.
    If bus_id is passed, ensures that specific bus is stepped.
    Skips any bus present in dropped_bus_ids to preserve last known coordinates.
    Returns count of updated buses.
    """
    if dropped_bus_ids is None:
        dropped_bus_ids = []

    conn = get_connection()
    cursor = conn.cursor()

    if bus_id is not None:
        target_buses = cursor.execute("""
            SELECT b.id, b.bus_number, b.current_route_id, b.status
            FROM buses b
            WHERE b.id = ? AND b.current_route_id IS NOT NULL
        """, (bus_id,)).fetchall()
    else:
        target_buses = cursor.execute("""
            SELECT b.id, b.bus_number, b.current_route_id, b.status
            FROM buses b
            WHERE b.current_route_id IS NOT NULL 
              AND b.status != 'maintenance'
        """).fetchall()

    updated_count = 0
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    for b in target_buses:
        b_id = b["id"]
        route_id = b["current_route_id"]

        # If bus has simulated GPS loss, stop updates and preserve last known coordinates!
        if b_id in dropped_bus_ids:
            continue

        waypoints = cursor.execute("""
            SELECT latitude, longitude, sequence
            FROM route_waypoints
            WHERE route_id = ?
            ORDER BY sequence ASC
        """, (route_id,)).fetchall()

        if not waypoints:
            continue

        latest_gps = cursor.execute("""
            SELECT waypoint_index, latitude, longitude
            FROM gps_updates
            WHERE bus_id = ?
            ORDER BY timestamp DESC, id DESC
            LIMIT 1
        """, (b_id,)).fetchone()

        next_idx = 0
        if latest_gps and latest_gps["waypoint_index"] is not None:
            next_idx = (latest_gps["waypoint_index"] + 1) % len(waypoints)

        curr_wpt = waypoints[next_idx]
        prev_wpt = waypoints[(next_idx - 1 + len(waypoints)) % len(waypoints)]

        heading = calculate_bearing(
            prev_wpt["latitude"], prev_wpt["longitude"],
            curr_wpt["latitude"], curr_wpt["longitude"]
        )

        # Realistic speed oscillation (24-42 km/h)
        speed = max(20.0, round(28.0 + (math.sin(next_idx) * 10.0), 1))

        # Check nearest & next stop
        stops = cursor.execute("""
            SELECT s.id, s.name, s.latitude, s.longitude, rs.stop_order
            FROM route_stops rs
            JOIN stops s ON rs.stop_id = s.id
            WHERE rs.route_id = ?
            ORDER BY rs.stop_order ASC
        """, (route_id,)).fetchall()

        nearest_stop_id = None
        next_stop_id = None
        min_dist = float('inf')

        for s in stops:
            d = calculate_distance_km(curr_wpt["latitude"], curr_wpt["longitude"], s["latitude"], s["longitude"])
            if d < min_dist:
                min_dist = d
                nearest_stop_id = s["id"]

        if stops:
            curr_stop_idx = next((i for i, s in enumerate(stops) if s["id"] == nearest_stop_id), 0)
            next_stop_id = stops[(curr_stop_idx + 1) % len(stops)]["id"]

        nearest_stop_name = next((s["name"] for s in stops if s["id"] == nearest_stop_id), "Stop")
        next_stop_name = next((s["name"] for s in stops if s["id"] == next_stop_id), "Next Stop")

        status_msg = (
            f"Arrived at: {nearest_stop_name}"
            if min_dist <= 0.12 else
            f"En route to: {next_stop_name}"
        )

        cursor.execute("""
            INSERT INTO gps_updates (
                bus_id, latitude, longitude, speed_kmh, heading,
                current_stop_id, next_stop_id, waypoint_index, is_simulated, status_message, timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
        """, (
            b_id,
            curr_wpt["latitude"],
            curr_wpt["longitude"],
            speed,
            heading,
            nearest_stop_id,
            next_stop_id,
            next_idx,
            status_msg,
            now_str
        ))

        # Ensure bus status is active/in_transit
        cursor.execute("UPDATE buses SET status = 'in_transit' WHERE id = ? AND status != 'in_transit'", (b_id,))
        updated_count += 1

    conn.commit()
    conn.close()
    return updated_count

def reset_all_buses_to_route_start():
    """Restores all buses to their original starting positions and updates timestamp to now."""
    conn = get_connection()
    cursor = conn.cursor()
    buses = cursor.execute("SELECT id, bus_number, current_route_id FROM buses WHERE current_route_id IS NOT NULL").fetchall()
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # Map of bus_number -> initial starting position from seed_data
    initial_positions = {
        'BUS-01': (12.9515, 77.5385, 34.5, 195.0, 8, 'En route along Mysore Road Corridor', 'in_transit'),
        'BUS-02': (12.9379, 77.5802, 28.0, 260.0, 7, 'Crossing South End Circle signal', 'in_transit'),
        'BUS-03': (12.9265, 77.5480, 22.0, 310.0, 4, 'Passing BDA Complex', 'active'),
        'BUS-04': (12.9344, 77.5345, 0.0, 0.0, 0, 'Standing by at Central Terminal', 'idle'),
    }

    for b in buses:
        b_num = b['bus_number']
        if b_num in initial_positions:
            lat, lon, spd, head, wpt_idx, msg, status = initial_positions[b_num]
            cursor.execute("""
                INSERT INTO gps_updates (
                    bus_id, latitude, longitude, speed_kmh, heading,
                    waypoint_index, is_simulated, status_message, timestamp
                )
                VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)
            """, (b["id"], lat, lon, spd, head, wpt_idx, msg, now_str))
            cursor.execute("UPDATE buses SET status = ? WHERE id = ?", (status, b["id"]))
        else:
            first_wpt = cursor.execute("""
                SELECT latitude, longitude FROM route_waypoints
                WHERE route_id = ? ORDER BY sequence ASC LIMIT 1
            """, (b["current_route_id"],)).fetchone()
            if first_wpt:
                cursor.execute("""
                    INSERT INTO gps_updates (
                        bus_id, latitude, longitude, speed_kmh, heading,
                        waypoint_index, is_simulated, status_message, timestamp
                    )
                    VALUES (?, ?, ?, 25.0, 0.0, 0, 1, 'Initial route position', ?)
                """, (b["id"], first_wpt["latitude"], first_wpt["longitude"], now_str))
                cursor.execute("UPDATE buses SET status = 'in_transit' WHERE id = ?", (b["id"],))

    conn.commit()
    conn.close()

def ensure_initial_gps_fresh():
    """
    Refreshes latest GPS update timestamps to now so demo starts in a clean live state.
    """
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        UPDATE gps_updates 
        SET timestamp = ?
        WHERE id IN (
            SELECT MAX(id) FROM gps_updates GROUP BY bus_id
        )
    """, (now_str,))
    conn.commit()
    conn.close()

def is_gps_stale(timestamp_str: Optional[str], dropped: bool = False, max_age_seconds: int = 180) -> bool:
    """
    Returns True if the GPS signal is manually dropped, missing, or older than max_age_seconds.
    """
    if dropped:
        return True
    if not timestamp_str:
        return True
    try:
        dt = datetime.strptime(timestamp_str.split('.')[0], "%Y-%m-%d %H:%M:%S")
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        elapsed = (now - dt).total_seconds()
        return elapsed > max_age_seconds
    except Exception:
        return False
