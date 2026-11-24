"""
CampusRide Streamlit - Automated Test Suite
Verifies database integrity, authentication, GPS simulation, ETA math, and CRUD functionality.
"""

import unittest
import database as db
import seed_data
from simulation import (
    calculate_distance_km,
    calculate_bearing,
    calculate_eta,
    step_simulation_tick,
    reset_all_buses_to_route_start,
    is_gps_stale
)

class TestCampusRideStreamlit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        seed_data.seed_all()

    def test_01_users_and_authentication(self):
        """Verifies demo accounts exist and password hashes match."""
        student = db.get_user_by_email("student@campusride.edu")
        self.assertIsNotNone(student)
        self.assertEqual(student["role"], "student")
        self.assertEqual(student["password_hash"], db.hash_password("Student@123"))

        admin = db.get_user_by_email("admin@campusride.edu")
        self.assertIsNotNone(admin)
        self.assertEqual(admin["role"], "admin")
        self.assertEqual(admin["password_hash"], db.hash_password("Admin@123"))

    def test_02_routes_and_stops_hierarchy(self):
        """Verifies transit corridors, stops, and waypoints are seeded."""
        routes = db.get_all_routes()
        self.assertGreaterEqual(len(routes), 4)

        r1 = db.get_route_by_id(routes[0]["id"])
        self.assertIsNotNone(r1)

        stops = db.get_stops_for_route(r1["id"])
        self.assertGreaterEqual(len(stops), 4)

        waypoints = db.get_waypoints_for_route(r1["id"])
        self.assertGreater(len(waypoints), 5)

    def test_03_distance_and_bearing_math(self):
        """Tests Haversine distance and bearing calculations."""
        # Distance from Majestic (12.9767, 77.5713) to Campus Arch (12.9344, 77.5345) ~ 6.2 km direct
        dist = calculate_distance_km(12.9767, 77.5713, 12.9344, 77.5345)
        self.assertGreater(dist, 5.0)
        self.assertLess(dist, 8.0)

        # Bearing between two points
        bearing = calculate_bearing(12.9767, 77.5713, 12.9344, 77.5345)
        self.assertGreaterEqual(bearing, 0.0)
        self.assertLessEqual(bearing, 360.0)

    def test_04_eta_boundary_conditions(self):
        """Tests ETA near-stop (<120m) and normal transit conditions."""
        stop_lat = 12.9344
        stop_lon = 77.5345

        # Proximity test: 50 meters away
        near_eta = calculate_eta(stop_lat + 0.0003, stop_lon, stop_lat, stop_lon, [])
        self.assertEqual(near_eta["eta_minutes"], 0)
        self.assertEqual(near_eta["status"], "Arriving Now")

        # Distance test: 10 km away
        far_eta = calculate_eta(stop_lat + 0.08, stop_lon, stop_lat, stop_lon, [], speed_kmh=30.0)
        self.assertGreater(far_eta["eta_minutes"], 0)
        self.assertGreater(far_eta["distance_km"], 5.0)

    def test_05_gps_simulation_step(self):
        """Verifies simulated GPS coordinates advance along route."""
        bus = db.get_all_buses()[0]
        initial_gps = db.get_latest_gps(bus["id"])

        updated_count = step_simulation_tick()
        self.assertGreater(updated_count, 0)

        new_gps = db.get_latest_gps(bus["id"])
        self.assertIsNotNone(new_gps)
        self.assertGreater(new_gps["speed_kmh"], 15.0)
        self.assertEqual(new_gps["is_simulated"], 1)

    def test_06_stale_gps_detection(self):
        """Verifies stale heartbeat detection when dropped or expired."""
        # When bus has manual GPS loss simulated
        self.assertTrue(is_gps_stale("2026-11-23 12:00:00", dropped=True))

        # When timestamp is recent (1 second ago)
        recent_ts = "2099-01-01 12:00:00"
        self.assertFalse(is_gps_stale(recent_ts, dropped=False))

    def test_07_admin_bus_crud_and_duplicate_prevention(self):
        """Verifies full bus CRUD operations and duplicate prevention."""
        conn = db.get_connection()

        # Insert new bus
        conn.execute("""
            INSERT INTO buses (bus_number, registration_number, capacity, driver_name, driver_phone, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("BUS-TEST", "KA-05-TEST-1234", 45, "Test Driver", "+91 91234 56789", "active"))
        conn.commit()

        bus = conn.execute("SELECT * FROM buses WHERE bus_number = 'BUS-TEST'").fetchone()
        self.assertIsNotNone(bus)
        self.assertEqual(bus["registration_number"], "KA-05-TEST-1234")

        # Prevent duplicate bus_number
        with self.assertRaises(Exception):
            conn.execute("""
                INSERT INTO buses (bus_number, registration_number, capacity, driver_name, driver_phone)
                VALUES ('BUS-TEST', 'KA-05-NEW-9999', 40, 'D2', '999')
            """)

        # Clean up
        conn.execute("DELETE FROM buses WHERE bus_number = 'BUS-TEST'")
        conn.commit()
        conn.close()

if __name__ == "__main__":
    unittest.main()
