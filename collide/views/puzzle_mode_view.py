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
    drawing = {"start": None, "current_line": None}
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
    
    # Target setup - positioned in bottom 3/4 of screen as requested
    def generate_new_target():
        # Bottom 3/4 of screen means from y = canvas_height * 0.25 to canvas_height - 100
        min_y = int(canvas_height * 0.25)
        max_y = canvas_height - 100
        target_x = random.randint(50, canvas_width - 50)
        target_y = random.randint(min_y, max_y)
        return target_x, target_y
    
    target_x, target_y = generate_new_target()
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
    
    # Control panel at bottom - moved up to be more visible
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
        height=120,
        width=canvas_width,
    )
    
    # Add control panel to stack - positioned higher up
    game_stack.controls.append(ft.Container(
        content=control_panel,
        bottom=20,  # Changed from 0 to 20 to move it up
        left=0,
    ))
    
    # Back button overlay - using the fixed back_button component
    back_btn = back_button(page)
    game_stack.controls.append(back_btn)
    
    def create_line_visual(x1, y1, x2, y2):
        import math

        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx * dx + dy * dy)

        # Allow shorter lines for testing
        if length < 2:  # instead of 5
            return None

        angle = math.atan2(dy, dx)
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        return ft.Container(
            width=length,
            height=3,
            bgcolor="#2b2d2e",
            border_radius=1.5,
            left=center_x - length / 2,
            top=center_y - 1.5,
            rotate=ft.transform.Rotate(angle),
        )
    
    def on_pointer_down(e):
        nonlocal is_drawing_enabled
        if not is_drawing_enabled or game_running:
            return

        drawing["start"] = (e.local_x, e.local_y)
        print(f"[DEBUG] Pointer down at {drawing['start']}")

    
    def on_pointer_move(e):
        if not is_drawing_enabled or not drawing["start"] or game_running:
            return

        # Remove previous preview line
        if drawing["current_line"]:
            try:
                game_stack.controls.remove(drawing["current_line"])
            except:
                pass

        x1, y1 = drawing["start"]
        x2, y2 = e.local_x, e.local_y

        preview_line = create_line_visual(x1, y1, x2, y2)
        if preview_line:
            preview_line.bgcolor = "rgba(43, 45, 46, 0.5)"  # optional: show ghost preview
            game_stack.controls.append(preview_line)  # use append to avoid bad stacking
            drawing["current_line"] = preview_line
            page.update()

    
    def on_pointer_up(e):
        nonlocal is_drawing_enabled
        if not is_drawing_enabled or not drawing["start"] or game_running:
            return

        # Remove preview
        if drawing["current_line"]:
            try:
                game_stack.controls.remove(drawing["current_line"])
            except:
                pass
            drawing["current_line"] = None

        x1, y1 = drawing["start"]
        x2, y2 = e.local_x, e.local_y
        print(f"[DEBUG] Pointer up at {(x2, y2)}")

        final_line = create_line_visual(x1, y1, x2, y2)
        if final_line:
            game_stack.controls.append(final_line)
            lines.append(((x1, y1), (x2, y2)))
            print(f"[DEBUG] Line added: {(x1, y1)} -> {(x2, y2)}")

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
    
    def start_game_handler(e):
        async def _start_game():
            nonlocal game_running, is_drawing_enabled

            if game_running:
                return

            game_running = True
            is_drawing_enabled = False

            print(f"Starting game with {len(lines)} lines")

            # Set up physics
            physics_engine.add_lines(lines)
            physics_ball.start_moving()

            status_text.value = "Ball is moving..."
            status_text.color = "white"
            page.update()

            await game_loop()

        page.run_task(_start_game)

    
    def reset_game(e):
        nonlocal game_running, is_drawing_enabled, lines, target_x, target_y
        
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
                              ft.Container(content=control_panel, bottom=20, left=0),
                              back_btn]
        
        # Generate new target
        target_x, target_y = generate_new_target()
        physics_engine.set_target(target_x, target_y)
        target_container.left = target_x - 15
        target_container.top = target_y - 20
        
        status_text.value = "Draw lines to guide the ball to X, then tap START!"
        status_text.color = "white"
        
        # Clear any preview line
        drawing["start"] = None
        drawing["current_line"] = None
        
        page.update()
    
    # Set up event handlers
    game_stack.on_pointer_down = on_pointer_down
    game_stack.on_pointer_move = on_pointer_move  # Added for live preview
    game_stack.on_pointer_up = on_pointer_up
    start_button.on_click = start_game_handler
    reset_button.on_click = reset_game
    
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