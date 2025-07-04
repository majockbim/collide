import flet as ft

def menu_view(page: ft.Page):
    page.title = "Collide - Select Mode"

    def go_to_puzzle(e):
        page.go("/puzzle")

    def go_to_simulation(e):
        page.go("/simulation")
    
    def go_back(e):
        page.go("/")

    page.controls.clear()
    
    # Add back button at the top
    back_btn = ft.Container(
        content=ft.Image(
            src="assets/images/back_red.png",
            width=40,
            height=40,
        ),
        margin=ft.margin.only(top=40, left=20),
        on_click=go_back,
    )
    
    page.controls.append(back_btn)
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
                            ft.Text("More Gamemodes Coming Soon..", size=20, weight=ft.FontWeight.W_600, color="#e52c34"),
                            
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