import flet as ft
import random
from collide.components.back_button import back_button

def puzzle_view(page: ft.Page):
    page.title = "Puzzle Mode"
    page.controls.clear()

    page.controls.append(back_button(page))

    canvas_width = 600
    canvas_height = 400

    lines = []
    drawing = {"start": None}
    is_drawing_enabled = True

    # Ball and target
    ball_radius = 10
    ball = ft.Container(
        width=ball_radius*2,
        height=ball_radius*2,
        bgcolor="red",
        border_radius=ball_radius,
        left=canvas_width // 2,
        top=0
    )

    target_x = random.randint(100, canvas_width - 100)
    target = ft.Text("X", size=30, color="blue", left=target_x, top=canvas_height - 40)

    # Stack where lines and objects are drawn
    stack = ft.Stack(
        width=canvas_width,
        height=canvas_height,
        controls=[ball, target],
    )

    stack_container = ft.Container(
        content=stack,
        width=canvas_width,
        height=canvas_height,
        bgcolor="#f5f5f5",
        border_radius=10,
        border=ft.border.all(1, ft.Colors.GREY_500),
    )


    def on_pointer_down(e):
        if not is_drawing_enabled:
            return
        drawing["start"] = (e.local_x, e.local_y)

    def on_pointer_up(e):
        if not is_drawing_enabled or not drawing["start"]:
            return

        x1, y1 = drawing["start"]
        x2, y2 = e.local_x, e.local_y

        line = ft.Container(
            left=min(x1, x2),
            top=min(y1, y2),
            content=ft.Line(
                x1=0,
                y1=0,
                x2=x2 - x1,
                y2=y2 - y1,
                color="black",
                width=2
            )
        )
        stack.controls.append(line)
        lines.append(((x1, y1), (x2, y2)))
        drawing["start"] = None
        page.update()

    def start_game(e):
        nonlocal is_drawing_enabled
        is_drawing_enabled = False
        # TODO: implement ball falling & physics
        print("Start clicked")

    stack.on_pointer_down = on_pointer_down
    stack.on_pointer_up = on_pointer_up

    # Add everything to page
    page.controls.append(
    ft.Column(
        [
            stack_container,
            ft.ElevatedButton("Start", on_click=start_game),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
)

    page.update()
