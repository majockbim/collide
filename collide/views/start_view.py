import flet as ft

def start_view(page: ft.Page):
    page.title = "Collide - Start"

    def go_to_menu(e):
        page.go("/menu")

    page.controls.clear()
    page.controls.append(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("collide", size=48, weight=ft.FontWeight.BOLD, color="#e52c34"),
                    ft.Text("press to start", size=16, italic=True, color="#2b2d2e"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            alignment=ft.alignment.center,
            expand=True,
            on_click=go_to_menu,
        )
    )
    page.update()