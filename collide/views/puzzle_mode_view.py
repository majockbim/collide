import flet as ft
import random
import asyncio
from collide.components.back_button import back_button
from collide.models.ball import Ball
from collide.models.physics_engine import PhysicsEngine

def puzzle_view(page: ft.Page):
    page.title = "Puzzle Mode"
    page.controls.clear()
    
    # Set fixed window size (mobile-like aspect ratio)
    page.window.width = 400
    page.window.height = 700
    page.window.resizable = False
    page.padding = 0
    page.spacing = 0
    
    # Get full screen dimensions
    canvas_width = 400
    canvas_height = 700
    
    # Game state
    lines = []
    drawing = {"start": None}
    is_drawing_enabled = True
    game_running = False
    
    # Ball setup
    ball_radius = 10
    ball_start_x = canvas_width // 2
    ball_start_y = 50
    
    # Physics engine
    physics_ball = Ball(ball_start_x, ball_start_y, ball_radius)
    physics_engine = PhysicsEngine(canvas_width, canvas_height)
    physics_engine.set_ball(physics_ball)
    
    # Target setup
    target_x = random.randint(50, canvas_width - 50)
    target_y = random.randint(canvas_height - 150, canvas_height - 100)
    physics_engine.set_target(target_x, target_y)
    
    # Visual elements
    ball_container = ft.Container(
        width=ball_radius * 2,
        height=ball_radius * 2,
        bgcolor="#e52c34",
        border_radius=ball_radius,
        left=ball_start_x - ball_radius,
        top=ball_start_y - ball_radius
    )
    
    target_container = ft.Container(
        content=ft.Text("X", size=30, color="#e52c34", weight=ft.FontWeight.BOLD),
        left=target_x - 15,
        top=target_y - 20
    )
    
    # Status text
    status_text = ft.Text(
        "Draw lines to guide the ball to X, then tap START!",
        size=14,
        color="white",
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.W_500
    )
    
    # Control buttons
    start_button = ft.Container(
        content=ft.Text("START", color="white", size=16, weight=ft.FontWeight.BOLD),
        bgcolor="#e52c34",
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        border_radius=20,
        alignment=ft.alignment.center,
    )
    
    reset_button = ft.Container(
        content=ft.Text("RESET", color="white", size=16, weight=ft.FontWeight.BOLD),
        bgcolor="#2b2d2e",
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        border_radius=20,
        alignment=ft.alignment.center,
    )
    
    # Stack for game elements
    game_stack = ft.Stack(
        width=canvas_width,
        height=canvas_height,
        controls=[ball_container, target_container],
    )
    
    # Control panel at bottom
    control_panel = ft.Container(
        content=ft.Column([
            status_text,
            ft.Row([
                start_button,
                reset_button,
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="rgba(0,0,0,0.8)",
        padding=15,
        height=100,
        width=canvas_width,
    )
    
    # Add control panel to stack
    game_stack.controls.append(ft.Container(
        content=control_panel,
        bottom=0,
        left=0,
    ))
    
    # Back button overlay
    back_btn = ft.Container(
        content=ft.Container(
            content=ft.Icon(ft.Icons.ARROW_BACK, color="white", size=24),
            bgcolor="rgba(0,0,0,0.6)",
            padding=10,
            border_radius=20,
        ),
        top=40,
        left=20,
    )
    
    game_stack.controls.append(back_btn)
    
    def create_line_visual(x1, y1, x2, y2):
        """Create visual representation of a line"""
        import math
        
        # Calculate line properties
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        
        if length < 5:  # Skip very short lines
            return None
            
        angle = math.atan2(dy, dx)
        
        line_container = ft.Container(
            width=length,
            height=3,
            bgcolor="#2b2d2e",
            border_radius=1.5,
            left=x1,
            top=y1 - 1.5,
            rotate=ft.transform.Rotate(angle),
        )
        
        return line_container
    
    def on_pointer_down(e):
        nonlocal is_drawing_enabled
        if not is_drawing_enabled or game_running:
            return
        drawing["start"] = (e.local_x, e.local_y)
    
    def on_pointer_up(e):
        nonlocal is_drawing_enabled
        if not is_drawing_enabled or not drawing["start"] or game_running:
            return
        
        x1, y1 = drawing["start"]
        x2, y2 = e.local_x, e.local_y
        
        # Create line visual
        line_visual = create_line_visual(x1, y1, x2, y2)
        if line_visual:
            game_stack.controls.insert(-3, line_visual)  # Insert before control panel and back button
            lines.append(((x1, y1), (x2, y2)))
        
        drawing["start"] = None
        page.update()
    
    async def game_loop():
        """Main game animation loop"""
        nonlocal game_running
        
        while game_running:
            # Update physics
            result = physics_engine.update()
            
            # Update ball visual position
            ball_container.left = physics_ball.x - ball_radius
            ball_container.top = physics_ball.y - ball_radius
            
            # Check game state
            if result == "win":
                status_text.value = "🎉 You won! Ball hit the target!"
                status_text.color = "#4CAF50"
                game_running = False
                is_drawing_enabled = False
            elif result == "lose":
                status_text.value = "😞 Ball missed! Try again!"
                status_text.color = "#FF5722"
                game_running = False
                is_drawing_enabled = True
            elif result == "stopped":
                status_text.value = "😞 Ball stopped! Try again!"
                status_text.color = "#FF5722"
                game_running = False
                is_drawing_enabled = True
            
            page.update()
            await asyncio.sleep(1/60)  # 60 FPS
    
    async def start_game(e):
        nonlocal game_running, is_drawing_enabled
        
        if game_running:
            return
            
        game_running = True
        is_drawing_enabled = False
        
        # Set up physics
        physics_engine.add_lines(lines)
        physics_ball.start_moving()
        
        status_text.value = "Ball is moving..."
        status_text.color = "white"
        page.update()
        
        # Start game loop
        await game_loop()
    
    def reset_game(e):
        nonlocal game_running, is_drawing_enabled, lines
        
        game_running = False
        is_drawing_enabled = True
        
        # Reset physics
        physics_ball.reset(ball_start_x, ball_start_y)
        physics_engine.add_lines([])
        
        # Reset visuals
        ball_container.left = ball_start_x - ball_radius
        ball_container.top = ball_start_y - ball_radius
        
        # Clear lines
        lines.clear()
        # Remove line visuals (keep ball, target, control panel, back button)
        game_stack.controls = [ball_container, target_container, 
                              ft.Container(content=control_panel, bottom=0, left=0),
                              back_btn]
        
        # Generate new target
        nonlocal target_x, target_y
        target_x = random.randint(50, canvas_width - 50)
        target_y = random.randint(canvas_height - 150, canvas_height - 100)
        physics_engine.set_target(target_x, target_y)
        target_container.left = target_x - 15
        target_container.top = target_y - 20
        
        status_text.value = "Draw lines to guide the ball to X, then tap START!"
        status_text.color = "white"
        page.update()
    
    def go_back(e):
        page.go("/menu")
    
    # Set up event handlers
    game_stack.on_pointer_down = on_pointer_down
    game_stack.on_pointer_up = on_pointer_up
    start_button.on_click = lambda e: page.run_task(start_game(e))
    reset_button.on_click = reset_game
    back_btn.on_click = go_back
    
    # Main container with full screen game
    main_container = ft.Container(
        content=game_stack,
        width=canvas_width,
        height=canvas_height,
        bgcolor="#87CEEB",  # Sky blue background
        padding=0,
        margin=0,
    )
    
    page.controls.append(main_container)
    page.update()