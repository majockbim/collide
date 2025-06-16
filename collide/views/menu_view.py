import flet as ft

def menu_view(page: ft.Page):
    page.title = "Collide - Select Mode"

    def go_to_puzzle(e):
        page.go("/puzzle")

    def go_to_simulation(e):
        page.go("/simulation")

    page.controls.clear()
    page.controls.append(
        ft.Column(
            [
                ft.Text("Select Mode", size=32, weight=ft.FontWeight.BOLD),
                ft.Column(
                    [
                        ft.Text("Puzzle Game", size=20, weight=ft.FontWeight.W_600),
                        ft.Container(
                            content=ft.Text(
                                "Use your knowledge of physics to solve puzzles to draw strategic lines that guide a falling ball to a target."
                                "Bounce off surfaces, avoid missing, and challenge your problem-solving skills."
                            ),
                            width=500,
                            padding=15,
                            bgcolor=ft.colors.BLUE_50,
                            border_radius=10,
                            on_click=go_to_puzzle
                        ),
                        ft.Text("Simulation Mode", size=20, weight=ft.FontWeight.W_600),
                        ft.Container(
                            content=ft.Text(
                                "Create and simulate your own physics experiments. "
                                "Draw lines, set parameters, and watch the physics engine bring your ideas to life."
                            ),
                            width=500,
                            padding=15,
                            bgcolor=ft.colors.GREEN_100,
                            border_radius=10,
                            on_click=go_to_simulation
                        )
                    ],
                    spacing=25
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )
    page.update()