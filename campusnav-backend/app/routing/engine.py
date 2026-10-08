"""
A* Routing Engine for CampusNav
Implements A* algorithm with fallback to Dijkstra for campus navigation.
"""
import heapq
import math
from typing import Optional


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two geographic coordinates in meters."""
    R = 6371000  # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def euclidean_distance(x1, y1, x2, y2):
    """Euclidean distance for SVG/pixel coordinates."""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def heuristic(node_a, node_b, nodes_map):
    """Heuristic for A* — straight-line distance between nodes."""
    a = nodes_map[node_a]
    b = nodes_map[node_b]

    # Use geographic coordinates if available
    if a.get("latitude") and a.get("longitude") and b.get("latitude") and b.get("longitude"):
        return haversine_distance(
            a["latitude"], a["longitude"],
            b["latitude"], b["longitude"]
        )
    # Fall back to pixel/map coordinates
    if a.get("map_x") is not None and a.get("map_y") is not None:
        scale = 0.5  # rough meters-per-pixel scale
        return euclidean_distance(
            a["map_x"], a["map_y"],
            b["map_x"], b["map_y"]
        ) * scale

    return 0


def astar(graph, start, goal, nodes_map, mode="fastest"):
    """
    A* pathfinding algorithm.
    graph: dict of {node_id: [(neighbor_id, distance, edge_data), ...]}
    nodes_map: dict of {node_id: checkpoint_data}
    mode: 'fastest' | 'shortest' | 'accessible'
    Returns: (path_list, total_distance, total_time) or (None, None, None)
    """
    open_heap = []
    heapq.heappush(open_heap, (0, start))

    came_from = {}
    g_score = {node: float("inf") for node in graph}
    g_score[start] = 0

    f_score = {node: float("inf") for node in graph}
    f_score[start] = heuristic(start, goal, nodes_map)

    edge_data_map = {}  # track edge data for each traversal

    while open_heap:
        _, current = heapq.heappop(open_heap)

        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            total_dist = g_score[goal]
            # Calculate total time
            total_time = 0
            for i in range(len(path) - 1):
                key = (path[i], path[i+1])
                if key in edge_data_map:
                    total_time += edge_data_map[key].get("walking_time", 0)
            return path, round(total_dist, 1), round(total_time, 1)

        for neighbor, dist, edge_data in graph.get(current, []):
            # Skip inaccessible edges in accessible mode
            if mode == "accessible" and edge_data.get("stairs", False):
                continue
            # Skip blocked edges
            if not edge_data.get("is_active", True):
                continue

            # Weight modifier for mode
            weight = dist
            if mode == "accessible":
                if edge_data.get("stairs"):
                    weight *= 10  # heavy penalty for stairs
                if edge_data.get("ramp") or edge_data.get("elevator"):
                    weight *= 0.8  # prefer accessible
            elif mode == "shortest":
                weight = dist  # pure distance

            tentative_g = g_score[current] + weight

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal, nodes_map)
                edge_data_map[(current, neighbor)] = edge_data
                heapq.heappush(open_heap, (f_score[neighbor], neighbor))

    return None, None, None


def dijkstra(graph, start, goal, mode="fastest"):
    """
    Dijkstra fallback algorithm.
    Returns: (path_list, total_distance, total_time) or (None, None, None)
    """
    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    came_from = {}
    edge_data_map = {}

    heap = [(0, start)]

    while heap:
        current_dist, current = heapq.heappop(heap)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            total_time = 0
            for i in range(len(path) - 1):
                key = (path[i], path[i+1])
                if key in edge_data_map:
                    total_time += edge_data_map[key].get("walking_time", 0)
            return path, round(distances[goal], 1), round(total_time, 1)

        if current_dist > distances[current]:
            continue

        for neighbor, dist, edge_data in graph.get(current, []):
            if mode == "accessible" and edge_data.get("stairs", False):
                continue
            if not edge_data.get("is_active", True):
                continue

            weight = dist
            new_dist = distances[current] + weight

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                came_from[neighbor] = current
                edge_data_map[(current, neighbor)] = edge_data
                heapq.heappush(heap, (new_dist, neighbor))

    return None, None, None


def build_graph(checkpoints, connections):
    """Build adjacency list graph from DB data."""
    graph = {cp["checkpoint_id"]: [] for cp in checkpoints}
    nodes_map = {cp["checkpoint_id"]: cp for cp in checkpoints}

    for conn in connections:
        if not conn.get("is_active", True):
            continue
        frm = conn["from_checkpoint"]
        to = conn["to_checkpoint"]
        dist = conn.get("distance", 50)
        time = conn.get("walking_time", dist / 1.4)  # ~1.4 m/s walking speed

        edge_data = {
            "distance": dist,
            "walking_time": time,
            "accessible": conn.get("accessible", True),
            "stairs": conn.get("stairs", False),
            "ramp": conn.get("ramp", False),
            "elevator": conn.get("elevator", False),
            "is_active": conn.get("is_active", True),
            "connection_id": conn.get("connection_id", ""),
        }

        if frm in graph:
            graph[frm].append((to, dist, edge_data))
        if to in graph:
            # Bidirectional edge
            graph[to].append((frm, dist, edge_data))

    return graph, nodes_map


def generate_instructions(path, nodes_map, connections_map):
    """
    Convert path into human-readable turn-by-turn instructions.
    """
    if not path or len(path) < 2:
        return []

    instructions = []

    def get_direction(p1, p2, p3=None):
        """Simple direction hint based on coordinate bearing."""
        if p2.get("map_x") is None:
            return ""
        dx = p2.get("map_x", 0) - p1.get("map_x", 0)
        dy = p2.get("map_y", 0) - p1.get("map_y", 0)

        if abs(dx) > abs(dy):
            return "east" if dx > 0 else "west"
        else:
            return "south" if dy > 0 else "north"

    for i, node_id in enumerate(path):
        node = nodes_map.get(node_id, {})
        name = node.get("name", node_id)

        if i == 0:
            instructions.append({
                "step": i + 1,
                "checkpoint_id": node_id,
                "instruction": f"Start at {name}.",
                "type": "start",
                "distance": 0,
            })
        elif i == len(path) - 1:
            # Get connection from previous
            prev_node_id = path[i - 1]
            conn_key = (prev_node_id, node_id)
            conn = connections_map.get(conn_key) or connections_map.get((node_id, prev_node_id), {})
            dist = conn.get("distance", 0)

            instruction_text = f"You have arrived at {name}."
            instructions.append({
                "step": i + 1,
                "checkpoint_id": node_id,
                "instruction": instruction_text,
                "type": "arrive",
                "distance": dist,
            })
        else:
            prev_node_id = path[i - 1]
            next_node_id = path[i + 1]
            conn_key = (prev_node_id, node_id)
            conn = connections_map.get(conn_key) or connections_map.get((node_id, prev_node_id), {})
            dist = conn.get("distance", 0)

            # Detect special path features
            if conn.get("stairs"):
                inst_type = "stairs"
                action = "Take the stairs"
            elif conn.get("elevator"):
                inst_type = "elevator"
                action = "Take the elevator"
            elif conn.get("ramp"):
                inst_type = "ramp"
                action = "Use the ramp"
            else:
                inst_type = "walk"
                action = f"Walk {int(dist)}m"

            instruction_text = f"{action} towards {name}."
            instructions.append({
                "step": i + 1,
                "checkpoint_id": node_id,
                "instruction": instruction_text,
                "type": inst_type,
                "distance": dist,
            })

    return instructions


def find_route(checkpoints, connections, from_id, to_id, mode="fastest"):
    """
    Main routing function. Tries A* first, falls back to Dijkstra.
    Returns dict with path, geometry, distance, time, instructions.
    """
    graph, nodes_map = build_graph(checkpoints, connections)

    # Build connections lookup
    connections_map = {}
    for c in connections:
        key = (c["from_checkpoint"], c["to_checkpoint"])
        connections_map[key] = c

    # Validate endpoints
    if from_id not in graph:
        return {"error": f"Start checkpoint '{from_id}' not found in graph"}
    if to_id not in graph:
        return {"error": f"Destination checkpoint '{to_id}' not found in graph"}

    # Try A* first
    path, distance, walking_time = astar(graph, from_id, to_id, nodes_map, mode)

    algorithm_used = "A*"
    if path is None:
        # Fallback to Dijkstra
        path, distance, walking_time = dijkstra(graph, from_id, to_id, mode)
        algorithm_used = "Dijkstra"

    if path is None:
        return {"error": "No route found between these locations"}

    # Build geometry (ordered coordinates for map drawing)
    geometry = []
    for node_id in path:
        node = nodes_map.get(node_id, {})
        point = {"checkpoint_id": node_id, "name": node.get("name", node_id)}
        if node.get("latitude") and node.get("longitude"):
            point["lat"] = node["latitude"]
            point["lng"] = node["longitude"]
        if node.get("map_x") is not None:
            point["map_x"] = node["map_x"]
            point["map_y"] = node["map_y"]
        geometry.append(point)

    # Generate human-readable instructions
    instructions = generate_instructions(path, nodes_map, connections_map)

    # Estimated walking time in minutes
    if walking_time is None or walking_time == 0:
        walking_time = round(distance / 84, 1)  # ~84m/min (5km/h walking)

    return {
        "path": path,
        "geometry": geometry,
        "distance": distance,
        "walking_time_minutes": round(walking_time / 60, 1) if walking_time > 60 else round(walking_time, 1),
        "walking_time_seconds": walking_time,
        "mode": mode,
        "algorithm": algorithm_used,
        "instructions": instructions,
        "checkpoints_count": len(path),
    }
