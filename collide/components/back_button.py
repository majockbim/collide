import flet as ft

def back_button(page: ft.Page):
    def go_back(e):
        route_stack = page.session.get("route_stack")

        if route_stack and len(route_stack) > 1:
            route_stack.pop()  # Remove current
            prev_route = route_stack[-1]  # Peek previous
            page.session.set("route_stack", route_stack)
            page.go(prev_route)
        else:
            page.go("/")  # If no history, go home

    return ft.Container(
        content=ft.Image(
            src="assets/images/back_red.png",
            width=40,
            height=40,
            fit=ft.ImageFit.CONTAIN
        ),
        alignment=ft.alignment.top_left,
        padding=10,
        on_click=go_back
    )