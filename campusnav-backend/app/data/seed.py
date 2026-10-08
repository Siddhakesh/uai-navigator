"""
UAI Campus Seed Data
Real-world campus layout for Universal AI University (UAI), Karjat.
Map coordinates are based on the campus image dimensions (approx 800x600 pixel canvas).
These map_x/map_y values position checkpoints on the Leaflet image overlay.
"""


def get_seed_data():
    """Return complete UAI campus navigation seed data."""

    buildings = [
        {
            "building_id": "B001",
            "name": "Main Building (Academic Block)",
            "description": "Central academic block with all departments",
            "floors": 4,
            "color": "#3B82F6",
            "polygon": [
                [250, 180], [450, 180], [450, 360], [250, 360]
            ],
        },
        {
            "building_id": "B002",
            "name": "Administration Block",
            "description": "College administration, principal office, admissions",
            "floors": 2,
            "color": "#8B5CF6",
            "polygon": [
                [100, 150], [240, 150], [240, 280], [100, 280]
            ],
        },
        {
            "building_id": "B003",
            "name": "Library Block",
            "description": "Central library and reading rooms",
            "floors": 2,
            "color": "#10B981",
            "polygon": [
                [460, 150], [580, 150], [580, 280], [460, 280]
            ],
        },
        {
            "building_id": "B004",
            "name": "Hostel Block",
            "description": "Student residential quarters",
            "floors": 5,
            "color": "#F59E0B",
            "polygon": [
                [600, 100], [750, 100], [750, 320], [600, 320]
            ],
        },
        {
            "building_id": "B005",
            "name": "Sports Complex",
            "description": "Indoor and outdoor sports facilities",
            "floors": 1,
            "color": "#EF4444",
            "polygon": [
                [50, 380], [250, 380], [250, 520], [50, 520]
            ],
        },
        {
            "building_id": "B006",
            "name": "Canteen & Cafeteria",
            "description": "Student cafeteria and food court",
            "floors": 1,
            "color": "#F97316",
            "polygon": [
                [260, 380], [420, 380], [420, 460], [260, 460]
            ],
        },
    ]

    checkpoints = [
        # ── Gates & Entry ──────────────────────────────────────────────────
        {
            "checkpoint_id": "CP001",
            "name": "Main Gate",
            "description": "Main entrance gate of UAI campus",
            "map_x": 400, "map_y": 560,
            "building_id": None, "floor": 0,
            "type": "gate", "is_active": True, "icon": "gate",
        },
        {
            "checkpoint_id": "CP002",
            "name": "Security Cabin",
            "description": "Security check post at main gate",
            "map_x": 400, "map_y": 530,
            "building_id": None, "floor": 0,
            "type": "security", "is_active": True, "icon": "security",
        },
        {
            "checkpoint_id": "CP003",
            "name": "Main Road Junction",
            "description": "T-junction on the main campus road",
            "map_x": 400, "map_y": 480,
            "building_id": None, "floor": 0,
            "type": "junction", "is_active": True, "icon": "junction",
        },
        # ── Parking ────────────────────────────────────────────────────────
        {
            "checkpoint_id": "CP004",
            "name": "Parking Zone",
            "description": "Student and staff vehicle parking",
            "map_x": 200, "map_y": 500,
            "building_id": None, "floor": 0,
            "type": "parking", "is_active": True, "icon": "parking",
        },
        # ── Admin Block ────────────────────────────────────────────────────
        {
            "checkpoint_id": "CP005",
            "name": "Admin Block Entrance",
            "description": "Entrance to Administration Block",
            "map_x": 170, "map_y": 380,
            "building_id": "B002", "floor": 0,
            "type": "entrance", "is_active": True, "icon": "building",
        },
        {
            "checkpoint_id": "CP006",
            "name": "Reception",
            "description": "College reception and information desk",
            "map_x": 170, "map_y": 330,
            "building_id": "B002", "floor": 0,
            "type": "checkpoint", "is_active": True, "icon": "reception",
        },
        {
            "checkpoint_id": "CP007",
            "name": "Principal Office",
            "description": "Office of the Principal / Director",
            "map_x": 130, "map_y": 270,
            "building_id": "B002", "floor": 1,
            "type": "office", "is_active": True, "icon": "office",
        },
        {
            "checkpoint_id": "CP008",
            "name": "Admissions Office",
            "description": "Admissions and student registrar office",
            "map_x": 200, "map_y": 270,
            "building_id": "B002", "floor": 1,
            "type": "office", "is_active": True, "icon": "office",
        },
        # ── Main Academic Block ────────────────────────────────────────────
        {
            "checkpoint_id": "CP009",
            "name": "Academic Block Entrance",
            "description": "Main entrance of the Academic Building",
            "map_x": 350, "map_y": 380,
            "building_id": "B001", "floor": 0,
            "type": "entrance", "is_active": True, "icon": "building",
        },
        {
            "checkpoint_id": "CP010",
            "name": "Ground Floor Corridor",
            "description": "Ground floor main corridor of Academic Block",
            "map_x": 350, "map_y": 330,
            "building_id": "B001", "floor": 0,
            "type": "corridor", "is_active": True, "icon": "corridor",
        },
        {
            "checkpoint_id": "CP011",
            "name": "Staircase A (Academic Block)",
            "description": "Main staircase in Academic Block",
            "map_x": 280, "map_y": 300,
            "building_id": "B001", "floor": 0,
            "type": "stairs", "is_active": True, "icon": "stairs",
        },
        {
            "checkpoint_id": "CP012",
            "name": "Elevator (Academic Block)",
            "description": "Elevator in Academic Block",
            "map_x": 310, "map_y": 300,
            "building_id": "B001", "floor": 0,
            "type": "elevator", "is_active": True, "icon": "elevator",
        },
        {
            "checkpoint_id": "CP013",
            "name": "Computer Science Dept",
            "description": "Computer Science & Engineering Department, Floor 1",
            "map_x": 390, "map_y": 270,
            "building_id": "B001", "floor": 1,
            "type": "department", "is_active": True, "icon": "department",
        },
        {
            "checkpoint_id": "CP014",
            "name": "AI & ML Department",
            "description": "Artificial Intelligence & Machine Learning Department, Floor 2",
            "map_x": 390, "map_y": 230,
            "building_id": "B001", "floor": 2,
            "type": "department", "is_active": True, "icon": "department",
        },
        {
            "checkpoint_id": "CP015",
            "name": "Data Science Lab",
            "description": "Data Science and Analytics Lab, Floor 2",
            "map_x": 430, "map_y": 230,
            "building_id": "B001", "floor": 2,
            "type": "lab", "is_active": True, "icon": "lab",
        },
        {
            "checkpoint_id": "CP016",
            "name": "Research Lab",
            "description": "Research & Innovation Lab, Floor 3",
            "map_x": 390, "map_y": 195,
            "building_id": "B001", "floor": 3,
            "type": "lab", "is_active": True, "icon": "lab",
        },
        {
            "checkpoint_id": "CP017",
            "name": "Seminar Hall",
            "description": "Main seminar hall and conference room, Floor 1",
            "map_x": 320, "map_y": 265,
            "building_id": "B001", "floor": 1,
            "type": "hall", "is_active": True, "icon": "hall",
        },
        {
            "checkpoint_id": "CP018",
            "name": "Faculty Offices (Floor 1)",
            "description": "Faculty cabins and staff room, Floor 1",
            "map_x": 430, "map_y": 265,
            "building_id": "B001", "floor": 1,
            "type": "office", "is_active": True, "icon": "office",
        },
        # ── Library ────────────────────────────────────────────────────────
        {
            "checkpoint_id": "CP019",
            "name": "Library Entrance",
            "description": "Main entrance to the library",
            "map_x": 500, "map_y": 300,
            "building_id": "B003", "floor": 0,
            "type": "entrance", "is_active": True, "icon": "library",
        },
        {
            "checkpoint_id": "CP020",
            "name": "Library Reading Room",
            "description": "Main reading hall of the library",
            "map_x": 520, "map_y": 220,
            "building_id": "B003", "floor": 1,
            "type": "library", "is_active": True, "icon": "library",
        },
        # ── Cafeteria ──────────────────────────────────────────────────────
        {
            "checkpoint_id": "CP021",
            "name": "Cafeteria",
            "description": "Student cafeteria and food court",
            "map_x": 340, "map_y": 430,
            "building_id": "B006", "floor": 0,
            "type": "cafeteria", "is_active": True, "icon": "cafeteria",
        },
        # ── Sports ─────────────────────────────────────────────────────────
        {
            "checkpoint_id": "CP022",
            "name": "Sports Complex",
            "description": "Main sports complex and ground",
            "map_x": 150, "map_y": 450,
            "building_id": "B005", "floor": 0,
            "type": "sports", "is_active": True, "icon": "sports",
        },
        # ── Hostel ─────────────────────────────────────────────────────────
        {
            "checkpoint_id": "CP023",
            "name": "Hostel Entrance",
            "description": "Entrance to student hostel block",
            "map_x": 640, "map_y": 350,
            "building_id": "B004", "floor": 0,
            "type": "entrance", "is_active": True, "icon": "hostel",
        },
        {
            "checkpoint_id": "CP024",
            "name": "Hostel Common Room",
            "description": "Hostel common room and TV lounge",
            "map_x": 680, "map_y": 250,
            "building_id": "B004", "floor": 1,
            "type": "checkpoint", "is_active": True, "icon": "hostel",
        },
        # ── Central Plaza / Fountain ───────────────────────────────────────
        {
            "checkpoint_id": "CP025",
            "name": "Central Courtyard / Fountain",
            "description": "UAI central campus fountain plaza",
            "map_x": 400, "map_y": 420,
            "building_id": None, "floor": 0,
            "type": "plaza", "is_active": True, "icon": "fountain",
        },
    ]

    connections = [
        # Gate to road junction
        {
            "connection_id": "CN001", "from_checkpoint": "CP001", "to_checkpoint": "CP002",
            "distance": 20, "walking_time": 15, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        {
            "connection_id": "CN002", "from_checkpoint": "CP002", "to_checkpoint": "CP003",
            "distance": 50, "walking_time": 36, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        # Junction to Parking
        {
            "connection_id": "CN003", "from_checkpoint": "CP003", "to_checkpoint": "CP004",
            "distance": 100, "walking_time": 72, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        # Junction to Admin Block
        {
            "connection_id": "CN004", "from_checkpoint": "CP003", "to_checkpoint": "CP005",
            "distance": 120, "walking_time": 86, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        # Junction to Academic Block
        {
            "connection_id": "CN005", "from_checkpoint": "CP003", "to_checkpoint": "CP009",
            "distance": 80, "walking_time": 58, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        # Junction to Cafeteria
        {
            "connection_id": "CN006", "from_checkpoint": "CP003", "to_checkpoint": "CP025",
            "distance": 60, "walking_time": 43, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        # Central courtyard connections
        {
            "connection_id": "CN007", "from_checkpoint": "CP025", "to_checkpoint": "CP021",
            "distance": 30, "walking_time": 22, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        {
            "connection_id": "CN008", "from_checkpoint": "CP025", "to_checkpoint": "CP022",
            "distance": 100, "walking_time": 72, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        {
            "connection_id": "CN009", "from_checkpoint": "CP025", "to_checkpoint": "CP009",
            "distance": 50, "walking_time": 36, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        # Admin Block internal
        {
            "connection_id": "CN010", "from_checkpoint": "CP005", "to_checkpoint": "CP006",
            "distance": 30, "walking_time": 22, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        {
            "connection_id": "CN011", "from_checkpoint": "CP006", "to_checkpoint": "CP007",
            "distance": 40, "walking_time": 29, "accessible": False, "stairs": True,
            "ramp": False, "elevator": False, "is_active": True,
        },
        {
            "connection_id": "CN012", "from_checkpoint": "CP006", "to_checkpoint": "CP008",
            "distance": 35, "walking_time": 25, "accessible": False, "stairs": True,
            "ramp": False, "elevator": False, "is_active": True,
        },
        # Academic Block internal
        {
            "connection_id": "CN013", "from_checkpoint": "CP009", "to_checkpoint": "CP010",
            "distance": 30, "walking_time": 22, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        {
            "connection_id": "CN014", "from_checkpoint": "CP010", "to_checkpoint": "CP011",
            "distance": 25, "walking_time": 18, "accessible": False, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        {
            "connection_id": "CN015", "from_checkpoint": "CP010", "to_checkpoint": "CP012",
            "distance": 20, "walking_time": 15, "accessible": True, "stairs": False,
            "ramp": False, "elevator": True, "is_active": True,
        },
        # Ground floor to Floor 1
        {
            "connection_id": "CN016", "from_checkpoint": "CP011", "to_checkpoint": "CP017",
            "distance": 30, "walking_time": 60, "accessible": False, "stairs": True,
            "ramp": False, "elevator": False, "is_active": True,
        },
        {
            "connection_id": "CN017", "from_checkpoint": "CP012", "to_checkpoint": "CP017",
            "distance": 25, "walking_time": 45, "accessible": True, "stairs": False,
            "ramp": False, "elevator": True, "is_active": True,
        },
        {
            "connection_id": "CN018", "from_checkpoint": "CP017", "to_checkpoint": "CP013",
            "distance": 30, "walking_time": 22, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        {
            "connection_id": "CN019", "from_checkpoint": "CP017", "to_checkpoint": "CP018",
            "distance": 40, "walking_time": 29, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        # Floor 1 to Floor 2
        {
            "connection_id": "CN020", "from_checkpoint": "CP013", "to_checkpoint": "CP014",
            "distance": 30, "walking_time": 60, "accessible": False, "stairs": True,
            "ramp": False, "elevator": False, "is_active": True,
        },
        {
            "connection_id": "CN021", "from_checkpoint": "CP012", "to_checkpoint": "CP014",
            "distance": 30, "walking_time": 60, "accessible": True, "stairs": False,
            "ramp": False, "elevator": True, "is_active": True,
        },
        {
            "connection_id": "CN022", "from_checkpoint": "CP014", "to_checkpoint": "CP015",
            "distance": 20, "walking_time": 15, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        # Floor 2 to Floor 3
        {
            "connection_id": "CN023", "from_checkpoint": "CP014", "to_checkpoint": "CP016",
            "distance": 30, "walking_time": 60, "accessible": False, "stairs": True,
            "ramp": False, "elevator": False, "is_active": True,
        },
        {
            "connection_id": "CN024", "from_checkpoint": "CP012", "to_checkpoint": "CP016",
            "distance": 35, "walking_time": 75, "accessible": True, "stairs": False,
            "ramp": False, "elevator": True, "is_active": True,
        },
        # Library path
        {
            "connection_id": "CN025", "from_checkpoint": "CP003", "to_checkpoint": "CP019",
            "distance": 150, "walking_time": 108, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        {
            "connection_id": "CN026", "from_checkpoint": "CP009", "to_checkpoint": "CP019",
            "distance": 80, "walking_time": 58, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        {
            "connection_id": "CN027", "from_checkpoint": "CP019", "to_checkpoint": "CP020",
            "distance": 40, "walking_time": 60, "accessible": False, "stairs": True,
            "ramp": False, "elevator": False, "is_active": True,
        },
        # Hostel path
        {
            "connection_id": "CN028", "from_checkpoint": "CP003", "to_checkpoint": "CP023",
            "distance": 250, "walking_time": 180, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
        {
            "connection_id": "CN029", "from_checkpoint": "CP023", "to_checkpoint": "CP024",
            "distance": 50, "walking_time": 60, "accessible": False, "stairs": True,
            "ramp": False, "elevator": False, "is_active": True,
        },
        # Sports to main road
        {
            "connection_id": "CN030", "from_checkpoint": "CP004", "to_checkpoint": "CP022",
            "distance": 80, "walking_time": 58, "accessible": True, "stairs": False,
            "ramp": False, "elevator": False, "is_active": True,
        },
    ]

    destinations = [
        # Administrative
        {
            "destination_id": "D001", "name": "Principal Office",
            "aliases": ["director office", "principal", "HOD office"],
            "checkpoint_id": "CP007", "building_id": "B002", "floor": 1,
            "category": "administration", "description": "Office of the Principal / Director",
            "icon": "🏛️", "is_active": True,
        },
        {
            "destination_id": "D002", "name": "Admissions Office",
            "aliases": ["admission", "registrar", "student office"],
            "checkpoint_id": "CP008", "building_id": "B002", "floor": 1,
            "category": "administration", "description": "Student admissions and registrar office",
            "icon": "📋", "is_active": True,
        },
        {
            "destination_id": "D003", "name": "Reception",
            "aliases": ["front desk", "info desk", "information"],
            "checkpoint_id": "CP006", "building_id": "B002", "floor": 0,
            "category": "administration", "description": "College reception and information desk",
            "icon": "ℹ️", "is_active": True,
        },
        # Academic
        {
            "destination_id": "D004", "name": "AI & ML Department",
            "aliases": ["artificial intelligence", "machine learning", "AI dept", "ML dept", "AIML"],
            "checkpoint_id": "CP014", "building_id": "B001", "floor": 2,
            "category": "department", "description": "AI and Machine Learning Department",
            "icon": "🤖", "is_active": True,
        },
        {
            "destination_id": "D005", "name": "Computer Science Department",
            "aliases": ["CSE", "CS dept", "computer science", "IT department"],
            "checkpoint_id": "CP013", "building_id": "B001", "floor": 1,
            "category": "department", "description": "Computer Science & Engineering Department",
            "icon": "💻", "is_active": True,
        },
        {
            "destination_id": "D006", "name": "Data Science Lab",
            "aliases": ["DS lab", "analytics lab", "data lab"],
            "checkpoint_id": "CP015", "building_id": "B001", "floor": 2,
            "category": "lab", "description": "Data Science and Analytics Laboratory",
            "icon": "📊", "is_active": True,
        },
        {
            "destination_id": "D007", "name": "Research Lab",
            "aliases": ["innovation lab", "R&D", "research center"],
            "checkpoint_id": "CP016", "building_id": "B001", "floor": 3,
            "category": "lab", "description": "Research and Innovation Laboratory",
            "icon": "🔬", "is_active": True,
        },
        {
            "destination_id": "D008", "name": "Seminar Hall",
            "aliases": ["conference room", "seminar", "auditorium", "hall"],
            "checkpoint_id": "CP017", "building_id": "B001", "floor": 1,
            "category": "hall", "description": "Main seminar and conference hall",
            "icon": "🎓", "is_active": True,
        },
        # Library
        {
            "destination_id": "D009", "name": "Library",
            "aliases": ["reading room", "book library", "central library", "books"],
            "checkpoint_id": "CP019", "building_id": "B003", "floor": 0,
            "category": "library", "description": "Central Library and Reading Room",
            "icon": "📚", "is_active": True,
        },
        # Facilities
        {
            "destination_id": "D010", "name": "Cafeteria",
            "aliases": ["canteen", "food court", "mess", "eat", "lunch", "food"],
            "checkpoint_id": "CP021", "building_id": "B006", "floor": 0,
            "category": "facility", "description": "Student cafeteria and food court",
            "icon": "🍽️", "is_active": True,
        },
        {
            "destination_id": "D011", "name": "Sports Complex",
            "aliases": ["sports", "ground", "basketball", "cricket", "gym"],
            "checkpoint_id": "CP022", "building_id": "B005", "floor": 0,
            "category": "sports", "description": "Sports complex and grounds",
            "icon": "⚽", "is_active": True,
        },
        {
            "destination_id": "D012", "name": "Hostel",
            "aliases": ["residence", "dorm", "dormitory", "boys hostel"],
            "checkpoint_id": "CP023", "building_id": "B004", "floor": 0,
            "category": "residential", "description": "Student hostel and residential block",
            "icon": "🏠", "is_active": True,
        },
        {
            "destination_id": "D013", "name": "Parking",
            "aliases": ["parking lot", "car park", "bike parking", "vehicle"],
            "checkpoint_id": "CP004", "building_id": None, "floor": 0,
            "category": "facility", "description": "Student and staff vehicle parking",
            "icon": "🅿️", "is_active": True,
        },
        {
            "destination_id": "D014", "name": "Main Gate",
            "aliases": ["entrance", "exit", "gate 1", "entry gate"],
            "checkpoint_id": "CP001", "building_id": None, "floor": 0,
            "category": "gate", "description": "Main entrance gate of UAI campus",
            "icon": "🚪", "is_active": True,
        },
    ]

    return {
        "buildings": buildings,
        "checkpoints": checkpoints,
        "connections": connections,
        "destinations": destinations,
    }
