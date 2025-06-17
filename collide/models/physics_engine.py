import math
from .ball import Ball

class PhysicsEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ball = None
        self.lines = []
        self.target_x = 0
        self.target_y = 0
        self.target_radius = 20
        
    def set_ball(self, ball):
        """Set the ball for physics simulation"""
        self.ball = ball
    
    def add_lines(self, lines):
        """Add lines to the physics world"""
        self.lines = lines
    
    def set_target(self, x, y):
        """Set target position"""
        self.target_x = x
        self.target_y = y
    
    def update(self):
        """Update physics simulation"""
        if not self.ball or not self.ball.is_moving:
            return "stopped"
        
        # Store old position
        old_x = self.ball.x
        old_y = self.ball.y
        
        # Update ball physics
        self.ball.update()
        
        # Check wall collisions
        self._check_wall_collisions()
        
        # Check line collisions
        self._check_line_collisions()
        
        # Check target collision
        if self._check_target_collision():
            return "win"
            
        # Check if ball stopped
        if not self.ball.is_moving:
            return "lose"
            
        return "playing"
    
    def _check_wall_collisions(self):
        """Check and handle wall collisions"""
        if not self.ball:
            return
            
        # Left wall
        if self.ball.x - self.ball.radius <= 0:
            self.ball.x = self.ball.radius
            self.ball.bounce_off_wall("left")
        
        # Right wall
        if self.ball.x + self.ball.radius >= self.width:
            self.ball.x = self.width - self.ball.radius
            self.ball.bounce_off_wall("right")
        
        # Top wall
        if self.ball.y - self.ball.radius <= 0:
            self.ball.y = self.ball.radius
            self.ball.bounce_off_wall("top")
        
        # Bottom wall - stop the ball
        if self.ball.y + self.ball.radius >= self.height:
            self.ball.y = self.height - self.ball.radius
            self.ball.is_moving = False
    
    def _check_line_collisions(self):
        """Check and handle line collisions"""
        if not self.ball:
            return
            
        for line_start, line_end in self.lines:
            distance = self.ball.distance_to_line(line_start, line_end)
            
            if distance <= self.ball.radius + 2:  # collision threshold
                # Push ball away from line
                self._push_ball_from_line(line_start, line_end)
                # Bounce off line
                self.ball.bounce_off_line(line_start, line_end)
                break
    
    def _push_ball_from_line(self, line_start, line_end):
        """Push ball away from line to prevent overlap"""
        x1, y1 = line_start
        x2, y2 = line_end
        
        # Find closest point on line
        dx = self.ball.x - x1
        dy = self.ball.y - y1
        lx = x2 - x1
        ly = y2 - y1
        length_sq = lx*lx + ly*ly
        
        if length_sq == 0:
            return
            
        t = max(0, min(1, (dx*lx + dy*ly) / length_sq))
        closest_x = x1 + t * lx
        closest_y = y1 + t * ly
        
        # Push ball away
        push_dx = self.ball.x - closest_x
        push_dy = self.ball.y - closest_y
        push_distance = math.sqrt(push_dx*push_dx + push_dy*push_dy)
        
        if push_distance > 0:
            push_dx /= push_distance
            push_dy /= push_distance
            self.ball.x = closest_x + push_dx * (self.ball.radius + 2)
            self.ball.y = closest_y + push_dy * (self.ball.radius + 2)
    
    def _check_target_collision(self):
        """Check if ball hits target"""
        if not self.ball:
            return False
            
        distance = self.ball.distance_to_point(self.target_x, self.target_y)
        return distance <= (self.ball.radius + self.target_radius)
    
    def reset(self, start_x, start_y):
        """Reset physics simulation"""
        if self.ball:
            self.ball.reset(start_x, start_y)