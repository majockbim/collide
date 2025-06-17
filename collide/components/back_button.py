import flet as ft

def back_button(page: ft.Page):
    def go_back(e):
        # Define the proper back navigation
        current_route = page.route
        
        if current_route == "/menu":
            page.go("/")
        elif current_route == "/puzzle":
            page.go("/menu")
        elif current_route == "/simulation":
            page.go("/menu")
        else:
            page.go("/")
    
    return ft.Container(
        content=ft.Image(
            src="assets/images/back_red.png",
            width=40,
            height=40,
        ),
        top=40,
        left=20,
        on_click=go_back,
    )