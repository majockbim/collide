import math

class Ball:
    def __init__(self, x, y, radius=10):
        self.x = x
        self.y = y
        self.vx = 0  # velocity x
        self.vy = 0  # velocity y
        self.radius = radius
        self.gravity = 0.3
        self.bounce_damping = 0.7
        self.friction = 0.99
        self.is_moving = False
        self.min_velocity = 0.1
        
    def update(self):
        """Update ball position and velocity"""
        if not self.is_moving:
            return
            
        # Apply gravity
        self.vy += self.gravity
        
        # Apply friction
        self.vx *= self.friction
        self.vy *= self.friction
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Stop if velocity is very small
        if abs(self.vx) < self.min_velocity and abs(self.vy) < self.min_velocity:
            self.is_moving = False
    
    def start_moving(self):
        """Start the ball moving"""
        self.is_moving = True
        if self.vy == 0:
            self.vy = 1  # Small initial velocity
    
    def bounce_off_line(self, line_start, line_end):
        """Bounce off a line using reflection physics"""
        x1, y1 = line_start
        x2, y2 = line_end
        
        # Calculate line normal
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        
        if length == 0:
            return
            
        # Normalize line direction
        dx /= length
        dy /= length
        
        # Normal vector (perpendicular to line)
        nx = -dy
        ny = dx
        
        # Velocity dot normal
        dot = self.vx * nx + self.vy * ny
        
        # Reflect velocity
        self.vx -= 2 * dot * nx
        self.vy -= 2 * dot * ny
        
        # Apply damping
        self.vx *= self.bounce_damping
        self.vy *= self.bounce_damping
    
    def bounce_off_wall(self, wall_type):
        """Bounce off screen walls"""
        if wall_type == "left" or wall_type == "right":
            self.vx = -self.vx * self.bounce_damping
        elif wall_type == "top" or wall_type == "bottom":
            self.vy = -self.vy * self.bounce_damping
    
    def reset(self, x, y):
        """Reset ball to starting position"""
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.is_moving = False
    
    def distance_to_point(self, x, y):
        """Calculate distance from ball center to a point"""
        dx = self.x - x
        dy = self.y - y
        return math.sqrt(dx*dx + dy*dy)
    
    def distance_to_line(self, line_start, line_end):
        """Calculate distance from ball center to line segment"""
        x1, y1 = line_start
        x2, y2 = line_end
        
        # Vector from line start to ball
        dx = self.x - x1
        dy = self.y - y1
        
        # Vector along line
        lx = x2 - x1
        ly = y2 - y1
        
        # Line length squared
        length_sq = lx*lx + ly*ly
        
        if length_sq == 0:
            # Line is a point
            return math.sqrt(dx*dx + dy*dy)
        
        # Project ball onto line
        t = max(0, min(1, (dx*lx + dy*ly) / length_sq))
        
        # Closest point on line
        closest_x = x1 + t * lx
        closest_y = y1 + t * ly
        
        # Distance to closest point
        dx = self.x - closest_x
        dy = self.y - closest_y
        return math.sqrt(dx*dx + dy*dy)