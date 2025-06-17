import flet as ft
from collide.views.start_view import start_view
from collide.views.menu_view import menu_view
from collide.views.puzzle_mode_view import puzzle_view
from collide.views.simulation_mode_view import simulation_view

def main(page: ft.Page):
    page.bgcolor = "#ebece7"

    routes = {
        "/": start_view,
        "/menu": menu_view,
        "/puzzle": puzzle_view,
        "/simulation": simulation_view,
    }

    page.fonts = {
        "VanillaCaramel": "assets/fonts/Vanilla Caramel.otf",
    }

    page.theme = ft.Theme(font_family="VanillaCaramel")

    # Initialize history stack
    if not page.session.contains_key("route_stack"):
        page.session.set("route_stack", ["/"]) # Start at "/"

    def route_change(e):
        route_stack = page.session.get("route_stack")

        # Only add to stack if this is a forward navigation
        if not route_stack or route_stack[-1] != page.route:
            route_stack.append(page.route)
            page.session.set("route_stack", route_stack)
        
        # Call the correct view
        routes.get(page.route, start_view)(page)

    page.on_route_change = route_change
    page.go(page.route or "/")

ft.app(target=main)