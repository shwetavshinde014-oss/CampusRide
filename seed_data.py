"""
CampusRide Streamlit - Seed Data Module
Initializes database with realistic academic transit corridors, stops, waypoints, fleet and schedules.
"""

from database import get_connection, init_db, hash_password

def seed_all():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing data in correct FK order
    cursor.executescript("""
        DELETE FROM gps_updates;
        DELETE FROM schedules;
        DELETE FROM route_stops;
        DELETE FROM route_waypoints;
        DELETE FROM buses;
        DELETE FROM stops;
        DELETE FROM routes;
        DELETE FROM users;
    """)

    print("Seeding CampusRide Streamlit database...")

    # 1. Users
    student_hash = hash_password("Student@123")
    admin_hash = hash_password("Admin@123")

    cursor.executemany("""
        INSERT INTO users (name, email, password_hash, role, department, phone)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        ('Aditi Rao', 'student@campusride.edu', student_hash, 'student', 'Computer Science & Engineering', '+91 98765 12345'),
        ('Arjun Nair', 'arjun@campusride.edu', student_hash, 'student', 'Electronics & Comm. Engineering', '+91 98765 23456'),
        ('Prof. K. Venkatesh', 'admin@campusride.edu', admin_hash, 'admin', 'Campus Transportation Management', '+91 94480 99887')
    ])

    # 2. Stops (Bangalore Academic & Urban Belt: Lat 12.91 - 12.98, Lng 77.53 - 77.63)
    stops_data = [
        ('Main University Arch', 'Gate 1, Academic Boulevard', 12.9344, 77.5345),
        ('Dr. APJ Abdul Kalam Tech Block', 'Near CS & AI Research Labs', 12.9362, 77.5358),
        ('Cauvery & Krishna Hostels', 'Block C Dining Hall & Quad', 12.9380, 77.5332),
        ('University Sports Complex', 'Olympic Pool & Pavilion', 12.9320, 77.5380),
        ('Deepanjali Nagar Metro', 'Exit B, Mysore Road', 12.9515, 77.5385),
        ('Vijayanagar Bus Terminal', 'Near Pipeline Water Tank', 12.9698, 77.5348),
        ('Toll Gate Magadi Road', 'Opposite Reliance Mart', 12.9735, 77.5450),
        ('Majestic Transit Interchange', 'Platform 18 Extension', 12.9767, 77.5713),
        ('South End Circle Metro', 'Lalbagh West Gate Road', 12.9379, 77.5802),
        ('Jayanagar 4th Block Complex', 'Bus Terminus Bay 3', 12.9298, 77.5835),
        ('Central Silk Board Junction', 'Flyover Ramp Entry', 12.9176, 77.6238),
        ('Koramangala Water Tank', '80 Feet Road Junction', 12.9340, 77.6225),
        ('Banashankari TTMC', 'Bus Station Bay 6', 12.9155, 77.5736),
        ('Padmanabhanagar Devegowda Park', 'Carmel Convent Corner', 12.9185, 77.5560),
        ('Kathriguppe Big Bazaar Circle', 'Near BDA Complex', 12.9265, 77.5480),
        ('Outer Ring Road Flyover Junction', 'BSK 3rd Stage Entry', 12.9310, 77.5420)
    ]
    cursor.executemany("INSERT INTO stops (name, landmark, latitude, longitude) VALUES (?, ?, ?, ?)", stops_data)

    # Stop IDs map
    s_rows = cursor.execute("SELECT id, name FROM stops").fetchall()
    s_map = {r["name"]: r["id"] for r in s_rows}

    # 3. Routes
    routes_data = [
        ('R-101', 'North Metro Corridor Express', 'Direct high-capacity line linking Majestic Interchange, Vijayanagar, and Deepanjali Metro to Main Campus Arch.', '#0D9488', 14.2, 45, 1),
        ('R-102', 'East Tech Corridor & Jayanagar', 'Connects Koramangala, Silk Board hub, and Jayanagar commercial district to University Academic Blocks.', '#2563EB', 18.5, 55, 1),
        ('R-203', 'South Ring Road & TTMC Shuttle', 'Feeder route serving Banashankari TTMC, Padmanabhanagar, and Ring Road residential colonies.', '#D97706', 9.8, 30, 1),
        ('R-305', 'Hostel & Sports Campus Loop', 'Intra-campus circular shuttle connecting all student residential quads, library, sports arena, and academic departments.', '#7C3AED', 4.5, 15, 1)
    ]
    cursor.executemany("""
        INSERT INTO routes (route_code, name, description, color, total_distance_km, estimated_duration_mins, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, routes_data)

    r_rows = cursor.execute("SELECT id, route_code FROM routes").fetchall()
    r_map = {r["route_code"]: r["id"] for r in r_rows}

    # 4. Route Stops Mapping
    r_stops_data = [
        # Route 101: Majestic -> Magadi -> Vijayanagar -> Deepanjali -> Campus Arch
        (r_map['R-101'], s_map['Majestic Transit Interchange'], 1, 0),
        (r_map['R-101'], s_map['Toll Gate Magadi Road'], 2, 12),
        (r_map['R-101'], s_map['Vijayanagar Bus Terminal'], 3, 22),
        (r_map['R-101'], s_map['Deepanjali Nagar Metro'], 4, 32),
        (r_map['R-101'], s_map['Main University Arch'], 5, 45),

        # Route 102: Silk Board -> Koramangala -> Jayanagar -> South End -> Tech Block
        (r_map['R-102'], s_map['Central Silk Board Junction'], 1, 0),
        (r_map['R-102'], s_map['Koramangala Water Tank'], 2, 14),
        (r_map['R-102'], s_map['Jayanagar 4th Block Complex'], 3, 28),
        (r_map['R-102'], s_map['South End Circle Metro'], 4, 38),
        (r_map['R-102'], s_map['Dr. APJ Abdul Kalam Tech Block'], 5, 55),

        # Route 203: Banashankari -> Padmanabhanagar -> Kathriguppe -> ORR -> Campus Arch
        (r_map['R-203'], s_map['Banashankari TTMC'], 1, 0),
        (r_map['R-203'], s_map['Padmanabhanagar Devegowda Park'], 2, 8),
        (r_map['R-203'], s_map['Kathriguppe Big Bazaar Circle'], 3, 16),
        (r_map['R-203'], s_map['Outer Ring Road Flyover Junction'], 4, 23),
        (r_map['R-203'], s_map['Main University Arch'], 5, 30),

        # Route 305: Campus Arch -> Tech Block -> Hostels -> Sports Arena -> Campus Arch
        (r_map['R-305'], s_map['Main University Arch'], 1, 0),
        (r_map['R-305'], s_map['Dr. APJ Abdul Kalam Tech Block'], 2, 4),
        (r_map['R-305'], s_map['Cauvery & Krishna Hostels'], 3, 8),
        (r_map['R-305'], s_map['University Sports Complex'], 4, 12)
    ]
    cursor.executemany("INSERT INTO route_stops (route_id, stop_id, stop_order, time_offset_mins) VALUES (?, ?, ?, ?)", r_stops_data)

    # 5. Route Waypoints (Dense GPS paths for realistic smooth Leaflet/Folium drawing)
    r1_points = [
        (12.9767, 77.5713), (12.9755, 77.5620), (12.9742, 77.5530),
        (12.9735, 77.5450), (12.9715, 77.5395), (12.9698, 77.5348),
        (12.9640, 77.5360), (12.9580, 77.5372), (12.9515, 77.5385),
        (12.9460, 77.5375), (12.9405, 77.5360), (12.9370, 77.5350),
        (12.9344, 77.5345)
    ]
    for i, pt in enumerate(r1_points):
        cursor.execute("INSERT INTO route_waypoints (route_id, sequence, latitude, longitude) VALUES (?, ?, ?, ?)",
                       (r_map['R-101'], i + 1, pt[0], pt[1]))

    r2_points = [
        (12.9176, 77.6238), (12.9245, 77.6230), (12.9340, 77.6225),
        (12.9325, 77.6080), (12.9310, 77.5950), (12.9298, 77.5835),
        (12.9345, 77.5815), (12.9379, 77.5802), (12.9370, 77.5640),
        (12.9360, 77.5480), (12.9362, 77.5358)
    ]
    for i, pt in enumerate(r2_points):
        cursor.execute("INSERT INTO route_waypoints (route_id, sequence, latitude, longitude) VALUES (?, ?, ?, ?)",
                       (r_map['R-102'], i + 1, pt[0], pt[1]))

    r3_points = [
        (12.9155, 77.5736), (12.9168, 77.5640), (12.9185, 77.5560),
        (12.9220, 77.5520), (12.9265, 77.5480), (12.9285, 77.5450),
        (12.9310, 77.5420), (12.9330, 77.5380), (12.9344, 77.5345)
    ]
    for i, pt in enumerate(r3_points):
        cursor.execute("INSERT INTO route_waypoints (route_id, sequence, latitude, longitude) VALUES (?, ?, ?, ?)",
                       (r_map['R-203'], i + 1, pt[0], pt[1]))

    r4_points = [
        (12.9344, 77.5345), (12.9355, 77.5350), (12.9362, 77.5358),
        (12.9372, 77.5345), (12.9380, 77.5332), (12.9360, 77.5320),
        (12.9335, 77.5340), (12.9320, 77.5380), (12.9332, 77.5365),
        (12.9344, 77.5345)
    ]
    for i, pt in enumerate(r4_points):
        cursor.execute("INSERT INTO route_waypoints (route_id, sequence, latitude, longitude) VALUES (?, ?, ?, ?)",
                       (r_map['R-305'], i + 1, pt[0], pt[1]))

    # 6. Buses
    buses_data = [
        ('BUS-01', 'KA-05-MB-1024', 52, 'Ramesh Kumar', '+91 98765 43210', 'in_transit', r_map['R-101']),
        ('BUS-02', 'KA-05-MB-2048', 48, 'Suresh Hegde', '+91 98450 11223', 'in_transit', r_map['R-102']),
        ('BUS-03', 'KA-05-MB-3072', 54, 'Anand Patil', '+91 97412 88990', 'active', r_map['R-203']),
        ('BUS-04', 'KA-05-MB-4096', 36, 'Vijay Gowda', '+91 99001 77665', 'idle', r_map['R-305']),
        ('BUS-05', 'KA-05-MB-5120', 50, 'Mohammed Rafiq', '+91 98860 33445', 'maintenance', None)
    ]
    cursor.executemany("""
        INSERT INTO buses (bus_number, registration_number, capacity, driver_name, driver_phone, status, current_route_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, buses_data)

    b_rows = cursor.execute("SELECT id, bus_number FROM buses").fetchall()
    b_map = {r["bus_number"]: r["id"] for r in b_rows}

    # 7. Schedules
    schedules_data = [
        (b_map['BUS-01'], r_map['R-101'], 'morning', '07:30', '08:15', 'Mon-Sat'),
        (b_map['BUS-02'], r_map['R-102'], 'morning', '07:15', '08:10', 'Mon-Sat'),
        (b_map['BUS-03'], r_map['R-203'], 'morning', '07:45', '08:20', 'Mon-Sat'),
        (b_map['BUS-04'], r_map['R-305'], 'shuttle', '08:30', '08:45', 'Mon-Fri'),
        (b_map['BUS-01'], r_map['R-101'], 'evening', '17:15', '18:05', 'Mon-Fri'),
        (b_map['BUS-02'], r_map['R-102'], 'evening', '17:30', '18:25', 'Mon-Fri'),
        (b_map['BUS-03'], r_map['R-203'], 'evening', '17:00', '17:40', 'Mon-Fri'),
        (b_map['BUS-04'], r_map['R-305'], 'shuttle', '16:45', '17:00', 'Mon-Fri')
    ]
    cursor.executemany("""
        INSERT INTO schedules (bus_id, route_id, trip_type, departure_time, arrival_time, days_of_week)
        VALUES (?, ?, ?, ?, ?, ?)
    """, schedules_data)

    # 8. Initial GPS updates
    from datetime import datetime, timezone
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    gps_data = [
        (b_map['BUS-01'], 12.9515, 77.5385, 34.5, 195.0, s_map['Deepanjali Nagar Metro'], s_map['Main University Arch'], 8, 'En route along Mysore Road Corridor', now_str),
        (b_map['BUS-02'], 12.9379, 77.5802, 28.0, 260.0, s_map['South End Circle Metro'], s_map['Dr. APJ Abdul Kalam Tech Block'], 7, 'Crossing South End Circle signal', now_str),
        (b_map['BUS-03'], 12.9265, 77.5480, 22.0, 310.0, s_map['Kathriguppe Big Bazaar Circle'], s_map['Outer Ring Road Flyover Junction'], 4, 'Passing BDA Complex', now_str),
        (b_map['BUS-04'], 12.9344, 77.5345, 0.0, 0.0, s_map['Main University Arch'], s_map['Dr. APJ Abdul Kalam Tech Block'], 0, 'Standing by at Central Terminal', now_str)
    ]
    cursor.executemany("""
        INSERT INTO gps_updates (bus_id, latitude, longitude, speed_kmh, heading, current_stop_id, next_stop_id, waypoint_index, is_simulated, status_message, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
    """, gps_data)

    conn.commit()
    conn.close()
    print("Database seeded successfully with 3 users, 16 stops, 4 routes, 5 buses, 8 schedules and GPS updates.")

if __name__ == "__main__":
    seed_all()
