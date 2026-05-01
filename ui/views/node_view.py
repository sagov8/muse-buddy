import flet as ft


def build_node_view(current_node: dict, on_select_node) -> ft.Control:
    hijos = current_node.get("hijos", [])
    cards = []

    # Detectar el tipo de los hijos para saber en qué nivel estamos
    tipo_hijos = hijos[0].get("tipo", "") if hijos else ""
    hijos_son_semillas = tipo_hijos == "seed"
    hijos_son_categorias = tipo_hijos == "categoria"
    hijos_son_moods = tipo_hijos == "mood"

    for hijo in hijos:
        icon = hijo.get("icon", "•")
        titulo = hijo.get("valor", "Sin nombre")
        descripcion = hijo.get("descripcion", "")
        subtipo = hijo.get("subtipo", "")

        if hijos_son_semillas:
            card = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            titulo,
                            size=15,
                            italic=True,
                            weight=ft.FontWeight.W_500,
                        ),
                        ft.Text(
                            subtipo.upper(),
                            size=10,
                            color=ft.Colors.PURPLE_400,
                        ) if subtipo else ft.Container(height=0),
                    ],
                    spacing=6,
                ),
                padding=16,
                border_radius=12,
                bgcolor=ft.Colors.PURPLE_50,
                border=ft.border.all(1, ft.Colors.PURPLE_100),
                ink=True,
                on_click=lambda e, n=hijo: on_select_node(n),
                width=280,
            )
        else:
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

    # Texto guía según el nivel del árbol
    if hijos_son_semillas:
        texto_guia = (
            "Elige una frase semilla que consideres es la que más se acerca "
            "a lo que sientes para empezar a construir tu canción"
        )
        texto_color = ft.Colors.PURPLE_800

    elif hijos_son_categorias:
        emocion = current_node.get("valor", "esta emoción")
        texto_guia = f"¿Qué aspecto o tipo de {emocion.lower()} quieres explorar en tu canción?"
        texto_color = ft.Colors.INDIGO_700

    elif hijos_son_moods:
        texto_guia = "¿En qué tono o matiz quieres expresar tu canción?"
        texto_color = ft.Colors.TEAL_700

    else:
        texto_guia = current_node.get("descripcion", "Selecciona una opción")
        texto_color = ft.Colors.BLACK87

    return ft.Column(
        controls=[
            ft.Text(
                texto_guia,
                size=20,
                italic=True,
                color=texto_color,
            ),
            ft.ResponsiveRow(cards),
        ]
    )
