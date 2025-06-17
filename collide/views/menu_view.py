import flet as ft
from collide.components.back_button import back_button

def menu_view(page: ft.Page):

    page.title = "Collide - Select Mode"

    def go_to_puzzle(e):
        page.go("/puzzle")

    def go_to_simulation(e):
        page.go("/simulation")

    page.controls.clear()
    page.controls.append(back_button(page))
    page.controls.append(
        ft.Container(
        alignment=ft.alignment.center,
        expand=True,
        content=ft.Column(
            [
                ft.Text("Select Mode", size=32, weight=ft.FontWeight.BOLD, color="#e52c34"),
                ft.Column(
                    [
                        ft.Text("Puzzle Game", size=20, weight=ft.FontWeight.W_600, color="#e52c34"),
                        ft.Container(
                            content=ft.Text(
                                "Use your knowledge of physics to solve puzzles to draw strategic lines that guide a falling ball to a target. "
                                "Bounce off surfaces, avoid missing, and challenge your problem-solving skills.", color="#2b2d2e",
                                text_align=ft.TextAlign.CENTER
                            ),
                            alignment=ft.alignment.center,
                            width=500,
                            padding=15,
                            bgcolor="#e9e8e0",
                            border_radius=10,
                            on_click=go_to_puzzle,
                        ),
                        ft.Text("Simulation Mode", size=20, weight=ft.FontWeight.W_600, color="#e52c34"),
                        ft.Container(
                            content=ft.Text(
                                "Create and simulate your own physics experiments. "
                                "Draw lines, set parameters, and watch the physics engine bring your ideas to life.", color="#2b2d2e",
                                text_align=ft.TextAlign.CENTER
                            ),
                            alignment=ft.alignment.center,
                            width=500,
                            padding=15,
                            bgcolor="#eae9e2",
                            border_radius=10,
                            on_click=go_to_simulation,
                        ),
                    ],
                    spacing=25,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            spacing=30,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
)
    page.update()