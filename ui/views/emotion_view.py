import flet as ft


def build_emotion_view(arboles: list, on_select_emotion) -> ft.Control:
    """
    Pantalla inicial: selección de emoción principal.
    Lee los JSONs disponibles en utils/arboles y los presenta como tarjetas.
    """
    cards = []

    for arbol in arboles:
        icon = arbol.get("icon", "🎵")
        titulo = arbol.get("valor", "Sin nombre")
        descripcion = arbol.get("descripcion", "")

        card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(icon, size=48),
                    ft.Text(
                        titulo,
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        descripcion,
                        size=13,
                        color=ft.Colors.GREY_700,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(vertical=28, horizontal=20),
            border_radius=20,
            bgcolor=ft.Colors.INDIGO_50,
            border=ft.border.all(1.5, ft.Colors.INDIGO_100),
            ink=True,
            on_click=lambda e, a=arbol: on_select_emotion(a),
            width=260,
        )
        cards.append(ft.Container(content=card, col={"xs": 12, "sm": 6, "md": 4}))

    return ft.Column(
        controls=[
            ft.Container(height=12),
            ft.Text(
                "Selecciona la emoción principal que quieres transmitir",
                size=22,
                italic=True,
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.INDIGO_800,
            ),
            ft.Container(height=8),
            ft.ResponsiveRow(
                controls=cards,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=16,
    )
