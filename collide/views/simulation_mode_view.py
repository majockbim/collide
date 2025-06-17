import flet as ft
from collide.components.back_button import back_button

def simulation_view(page: ft.Page):
    page.title = "Simulation Mode"
    page.controls.clear()
    page.controls.append(back_button(page))
    page.controls.append(ft.Text("Simulation mode coming soon!", text_align=ft.TextAlign.CENTER, size=24, color="#e52c34"))
    page.update()