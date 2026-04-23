import flet as ft


def build_node_view(current_node: dict, on_select_node) -> ft.Control:
    hijos = current_node.get("hijos", [])
    cards = []

    for hijo in hijos:
        icon = hijo.get("icon", "•")
        titulo = hijo.get("valor", "Sin nombre")
        descripcion = hijo.get("descripcion", "")

        card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(icon, size=24),
                    ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(descripcion, size=12, color=ft.Colors.GREY_600),
                ],
                spacing=8,
            ),
            padding=16,
            border_radius=16,
            bgcolor=ft.Colors.BLUE_50,
            border=ft.border.all(1, ft.Colors.BLUE_100),
            ink=True,
            on_click=lambda e, n=hijo: on_select_node(n),
            width=220,
        )
        cards.append(ft.Container(content=card, col={"sm": 6, "md": 4}))

    descripcion_actual = current_node.get("descripcion", "Selecciona una opción")

    return ft.Column(
        controls=[
            ft.Text(descripcion_actual, size=20, italic=True),
            ft.ResponsiveRow(cards),
        ]
    )