import numpy as np
import heapq
import math
from enum import Enum
from wpimath.geometry import Pose2d, Rotation2d, Translation2d


class ObstacleType(Enum):
    CIRCLE = 1
    RECTANGLE = 2
    HEXAGON = 3  # New obstacle type for the reef


class Obstacle:
    """
    Represents an obstacle on the field that the robot must avoid.
    """

    def __init__(self, obstacle_type, params):
        """
        Initialize an obstacle.

        Args:
            obstacle_type: ObstacleType.CIRCLE, ObstacleType.RECTANGLE, or ObstacleType.HEXAGON
            params: For CIRCLE: (center_x, center_y, radius)
                   For RECTANGLE: (min_x, min_y, max_x, max_y)
                   For HEXAGON: (center_x, center_y, radius, rotation_rad)
                                radius is distance from center to vertices,
                                rotation_rad is the rotation in radians
        """
        self.type = obstacle_type
        self.params = params

        # Pre-compute hexagon vertices if needed
        if self.type == ObstacleType.HEXAGON:
            center_x, center_y, radius, rotation = self.params
            self.vertices = self._calculate_hexagon_vertices(center_x, center_y, radius, rotation)

    def _calculate_hexagon_vertices(self, center_x, center_y, radius, rotation):
        """Calculate the six vertices of a hexagon"""
        vertices = []
        for i in range(6):
            angle = rotation + i * (2 * math.pi / 6)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            vertices.append((x, y))
        return vertices

    def _is_point_in_polygon(self, x, y, vertices):
        """
        Check if a point is inside a polygon using ray casting algorithm.
        """
        inside = False
        j = len(vertices) - 1

        for i in range(len(vertices)):
            xi, yi = vertices[i]
            xj, yj = vertices[j]

            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside

            j = i

        return inside

    def is_point_inside(self, x, y, safety_margin=0.0):
        """Check if a point is inside the obstacle (including safety margin)"""
        if self.type == ObstacleType.CIRCLE:
            center_x, center_y, radius = self.params
            distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            return distance <= (radius + safety_margin)

        elif self.type == ObstacleType.RECTANGLE:
            min_x, min_y, max_x, max_y = self.params
            return (min_x - safety_margin <= x <= max_x + safety_margin and
                    min_y - safety_margin <= y <= max_y + safety_margin)

        elif self.type == ObstacleType.HEXAGON:
            # For safety margin with hexagon, we first check if point is in the original hexagon
            if self._is_point_in_polygon(x, y, self.vertices):
                return True

            # If safety margin is specified, check if the point is within that distance of any edge
            if safety_margin > 0:
                center_x, center_y = self.params[0], self.params[1]
                # Quick check if the point is outside a circle that encompasses the hexagon + margin
                max_possible_distance = self.params[2] + safety_margin
                if math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2) > max_possible_distance:
                    return False

                # Check distance to each edge
                for i in range(len(self.vertices)):
                    v1 = self.vertices[i]
                    v2 = self.vertices[(i + 1) % len(self.vertices)]

                    # Distance from point to line segment
                    dist = self._point_to_line_segment_distance(x, y, v1[0], v1[1], v2[0], v2[1])
                    if dist <= safety_margin:
                        return True

            return False

        return False

    def _point_to_line_segment_distance(self, x, y, x1, y1, x2, y2):
        """Calculate the minimum distance from a point to a line segment"""
        # Vector from (x1,y1) to (x2,y2)
        dx = x2 - x1
        dy = y2 - y1

        # If the line segment is just a point
        if dx == 0 and dy == 0:
            return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)

        # Calculate projection of point onto line
        t = ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)

        # If projection is outside segment, use distance to closest endpoint
        if t < 0:
            return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)
        elif t > 1:
            return math.sqrt((x - x2) ** 2 + (y - y2) ** 2)

        # Distance to the projection point on the line
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy
        return math.sqrt((x - proj_x) ** 2 + (y - proj_y) ** 2)


class Pathfinder:
    """
    Pathfinding class for FRC robots that can avoid obstacles and generate
    a path from the robot's current position to a goal position.

    Uses wpimath.geometry.Pose2d for representing poses.
    """

    def __init__(self, start_pose, goal_pose, field_width=17.3736, field_height=7.9248, grid_size=0.1):
        """
        Initialize the pathfinder.

        Args:
            start_pose: Pose2d object representing robot's starting position
            goal_pose: Pose2d object representing goal position
            field_width: Width of the field in meters (default: FRC 2023 field)
            field_height: Height of the field in meters (default: FRC 2023 field)
            grid_size: Size of grid cells for pathfinding in meters
        """
        self.start_pose = start_pose
        self.goal_pose = goal_pose
        self.field_width = field_width
        self.field_height = field_height
        self.grid_size = grid_size
        self.obstacles = []

        # Calculate grid dimensions
        self.grid_width = int(field_width / grid_size)
        self.grid_height = int(field_height / grid_size)

        # Movement directions (8-connected grid)
        self.directions = [
            (1, 0), (1, 1), (0, 1), (-1, 1),
            (-1, 0), (-1, -1), (0, -1), (1, -1)
        ]

    def add_obstacle(self, obstacle):
        """Add an obstacle to the field"""
        self.obstacles.append(obstacle)

    def is_valid_position(self, x, y, robot_radius=0.5):
        """
        Check if a position is valid (in bounds and not in collision with obstacles).

        Args:
            x, y: Position coordinates
            robot_radius: Robot radius to use for collision checking

        Returns:
            True if position is valid, False otherwise
        """
        # Check field boundaries
        if x < 0 or x >= self.field_width or y < 0 or y >= self.field_height:
            return False

        # Check obstacles
        for obstacle in self.obstacles:
            if obstacle.is_point_inside(x, y, robot_radius):
                return False

        return True

    def _grid_to_world(self, grid_x, grid_y):
        """Convert grid coordinates to world coordinates"""
        return grid_x * self.grid_size, grid_y * self.grid_size

    def _world_to_grid(self, world_x, world_y):
        """Convert world coordinates to grid coordinates"""
        return int(world_x / self.grid_size), int(world_y / self.grid_size)

    def _distance_between_poses(self, pose1, pose2):
        """Calculate distance between two wpimath.geometry.Pose2d objects"""
        # Get the x and y coordinates of each pose
        x1 = pose1.X()
        y1 = pose1.Y()
        x2 = pose2.X()
        y2 = pose2.Y()

        # Calculate Euclidean distance
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def _angle_between_poses(self, pose1, pose2):
        """Calculate angle from pose1 to pose2 in radians"""
        # Get the x and y coordinates of each pose
        x1 = pose1.X()
        y1 = pose1.Y()
        x2 = pose2.X()
        y2 = pose2.Y()

        # Calculate angle
        return math.atan2(y2 - y1, x2 - x1)

    def find_path(self, robot_radius=0.5, smoothing=True):
        """
        Find a path from start to goal using A* algorithm.

        Args:
            robot_radius: Robot radius to use for collision checking
            smoothing: Whether to smooth the resulting path

        Returns:
            List of wpimath.geometry.Pose2d objects representing the path
        """
        # Convert start and goal to grid coordinates
        start_grid_x, start_grid_y = self._world_to_grid(self.start_pose.X(), self.start_pose.Y())
        goal_grid_x, goal_grid_y = self._world_to_grid(self.goal_pose.X(), self.goal_pose.Y())

        # Check if start or goal are invalid
        start_world_x, start_world_y = self._grid_to_world(start_grid_x, start_grid_y)
        goal_world_x, goal_world_y = self._grid_to_world(goal_grid_x, goal_grid_y)

        if not self.is_valid_position(start_world_x, start_world_y, robot_radius):
            raise ValueError("Start position is invalid (collision or out of bounds)")

        if not self.is_valid_position(goal_world_x, goal_world_y, robot_radius):
            raise ValueError("Goal position is invalid (collision or out of bounds)")

        # A* algorithm implementation
        open_set = []
        heapq.heappush(open_set, (0, (start_grid_x, start_grid_y)))

        came_from = {}
        g_score = {(start_grid_x, start_grid_y): 0}
        f_score = {(start_grid_x, start_grid_y): self._heuristic(start_grid_x, start_grid_y, goal_grid_x, goal_grid_y)}

        open_set_hash = {(start_grid_x, start_grid_y)}

        while open_set:
            _, current = heapq.heappop(open_set)
            open_set_hash.remove(current)

            current_x, current_y = current

            # Check if we reached the goal
            if current == (goal_grid_x, goal_grid_y):
                # Reconstruct path
                grid_path = self._reconstruct_path(came_from, current)

                # Convert to world coordinates
                world_path = [self._grid_to_world(x, y) for x, y in grid_path]

                # Create path of Pose2d objects
                pose_path = self._create_pose_path(world_path)

                # Apply path smoothing if requested
                if smoothing and len(pose_path) > 2:
                    pose_path = self._smooth_path(pose_path, robot_radius)

                return pose_path

            # Explore neighbors
            for dx, dy in self.directions:
                neighbor_x, neighbor_y = current_x + dx, current_y + dy
                neighbor = (neighbor_x, neighbor_y)

                # Check if neighbor is valid
                neighbor_world_x, neighbor_world_y = self._grid_to_world(neighbor_x, neighbor_y)
                if not self.is_valid_position(neighbor_world_x, neighbor_world_y, robot_radius):
                    continue

                # Calculate distance (use Euclidean for diagonals)
                move_cost = math.sqrt(dx * dx + dy * dy)
                tentative_g_score = g_score[current] + move_cost

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # This path to neighbor is better than any previous one
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score_value = tentative_g_score + self._heuristic(neighbor_x, neighbor_y, goal_grid_x,
                                                                        goal_grid_y)
                    f_score[neighbor] = f_score_value

                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score_value, neighbor))
                        open_set_hash.add(neighbor)

        # No path found
        return []

    def _heuristic(self, x1, y1, x2, y2):
        """Heuristic function for A* (Euclidean distance)"""
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def _reconstruct_path(self, came_from, current):
        """Reconstruct path from came_from dictionary"""
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)

        total_path.reverse()
        return total_path

    def _create_pose_path(self, world_path):
        """Create a path of wpimath.geometry.Pose2d objects with proper orientations"""
        pose_path = []

        for i in range(len(world_path)):
            x, y = world_path[i]

            # Calculate orientation
            if i < len(world_path) - 1:
                next_x, next_y = world_path[i + 1]
                angle = math.atan2(next_y - y, next_x - x)
            else:
                # Use goal orientation for the last point
                angle = self.goal_pose.rotation().radians()

            # Create wpimath.geometry.Pose2d object
            rotation = Rotation2d(angle)
            pose = Pose2d(x, y, rotation)
            pose_path.append(pose)

        # Make sure the final pose has the desired orientation
        if pose_path:
            pose_path[-1] = Pose2d(
                pose_path[-1].X(),
                pose_path[-1].Y(),
                self.goal_pose.rotation()
            )

        return pose_path

    def _smooth_path(self, pose_path, robot_radius):
        """Apply path smoothing to reduce zigzagging"""
        if len(pose_path) <= 2:
            return pose_path

        # Path simplification - remove unnecessary waypoints
        # If we can go directly from i to i+2 without collision, skip i+1
        i = 0
        simplified_path = [pose_path[0]]

        while i < len(pose_path) - 1:
            # Find furthest visible point
            furthest = i + 1
            for j in range(i + 2, len(pose_path)):
                if self._is_line_collision_free(pose_path[i], pose_path[j], robot_radius):
                    furthest = j
                else:
                    break

            simplified_path.append(pose_path[furthest])
            i = furthest

        # Adjust orientations for the simplified path
        for i in range(len(simplified_path) - 1):
            angle = self._angle_between_poses(simplified_path[i], simplified_path[i + 1])
            rotation = Rotation2d(angle)

            # Create new Pose2d with updated rotation
            simplified_path[i] = Pose2d(
                simplified_path[i].X(),
                simplified_path[i].Y(),
                rotation
            )

        # Keep goal orientation for last pose
        if simplified_path:
            simplified_path[-1] = Pose2d(
                simplified_path[-1].X(),
                simplified_path[-1].Y(),
                self.goal_pose.rotation()
            )

        return simplified_path

    def _is_line_collision_free(self, pose1, pose2, robot_radius):
        """Check if a line between two poses is collision-free"""
        step_count = max(int(self._distance_between_poses(pose1, pose2) / (self.grid_size * 0.5)), 10)

        for i in range(1, step_count):
            t = i / step_count
            x = pose1.X() + t * (pose2.X() - pose1.X())
            y = pose1.Y() + t * (pose2.Y() - pose1.Y())

            if not self.is_valid_position(x, y, robot_radius):
                return False

        return True

    def visualize_path(self, path=None, show_grid=True):
        """
        Visualize the field, obstacles, and path using matplotlib.

        Args:
            path: List of Pose2d objects. If None, call find_path().
            show_grid: Whether to show the grid
        """
        try:
            import matplotlib.pyplot as plt
            from matplotlib.patches import Circle, Rectangle, Arrow, Polygon
        except ImportError:
            print("Matplotlib is required for visualization")
            return

        if path is None:
            path = self.find_path()

        plt.figure(figsize=(10, 6))
        ax = plt.gca()

        # Draw field boundary
        plt.plot([0, self.field_width, self.field_width, 0, 0],
                 [0, 0, self.field_height, self.field_height, 0], 'k-', linewidth=2)

        # Draw grid
        if show_grid:
            for i in range(0, self.grid_width + 1):
                plt.plot([i * self.grid_size, i * self.grid_size],
                         [0, self.field_height], 'k-', alpha=0.2)
            for i in range(0, self.grid_height + 1):
                plt.plot([0, self.field_width],
                         [i * self.grid_size, i * self.grid_size], 'k-', alpha=0.2)

        # Draw obstacles
        for obstacle in self.obstacles:
            if obstacle.type == ObstacleType.CIRCLE:
                center_x, center_y, radius = obstacle.params
                circle = Circle((center_x, center_y), radius, fill=True, color='red', alpha=0.5)
                ax.add_patch(circle)
            elif obstacle.type == ObstacleType.RECTANGLE:
                min_x, min_y, max_x, max_y = obstacle.params
                width, height = max_x - min_x, max_y - min_y
                rect = Rectangle((min_x, min_y), width, height, fill=True, color='red', alpha=0.5)
                ax.add_patch(rect)
            elif obstacle.type == ObstacleType.HEXAGON:
                # Create a polygon patch from vertices
                poly = Polygon(obstacle.vertices, fill=True, color='blue', alpha=0.5)
                ax.add_patch(poly)

        # Draw path
        if path:
            path_x = [pose.X() for pose in path]
            path_y = [pose.Y() for pose in path]
            plt.plot(path_x, path_y, 'b-', linewidth=2, label='Path')

            # Draw orientation arrows
            for pose in path:
                arrow_length = 0.3
                angle = pose.rotation().radians()
                dx = arrow_length * math.cos(angle)
                dy = arrow_length * math.sin(angle)
                arrow = Arrow(pose.X(), pose.Y(), dx, dy, width=0.2, color='blue')
                ax.add_patch(arrow)

        # Draw start and goal
        plt.plot(self.start_pose.X(), self.start_pose.Y(), 'go', markersize=10, label='Start')
        plt.plot(self.goal_pose.X(), self.goal_pose.Y(), 'ro', markersize=10, label='Goal')

        plt.legend()
        plt.grid(True)
        plt.axis('equal')
        plt.title('FRC Robot Path Planning')
        plt.xlabel('X (meters)')
        plt.ylabel('Y (meters)')
        plt.show()
