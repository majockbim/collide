import flet as ft
from collide.views.start_view import start_view
from collide.views.menu_view import menu_view
from collide.views.puzzle_mode_view import puzzle_view

def main(page: ft.Page):
    # Set fixed window size and properties
    page.window.width = 400
    page.window.height = 700
    page.window.resizable = False
    page.window.maximizable = False
    page.bgcolor = "#ebece7"
    page.padding = 0
    page.spacing = 0

    routes = {
        "/": start_view,
        "/menu": menu_view,
        "/puzzle": puzzle_view,
    }

    page.fonts = {
        "VanillaCaramel": "assets/fonts/Vanilla Caramel.otf",
    }

    page.theme = ft.Theme(font_family="VanillaCaramel")

    # Initialize history stack
    if not page.session.contains_key("route_stack"):
        page.session.set("route_stack", ["/"])

    def route_change(e):
        # Call the correct view
        routes.get(page.route, start_view)(page)

    page.on_route_change = route_change
    page.go(page.route or "/")

ft.app(target=main)