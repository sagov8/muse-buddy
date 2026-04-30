import flet as ft


def build_header(tree: dict) -> ft.Control:
    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Herramienta para compositores", size=12, color=ft.Colors.GREY_600),
            ft.Text(tree.get("valor", "Árbol Creativo"), size=32, weight=ft.FontWeight.BOLD),
            #ft.Text(
            #    tree.get("descripcion", "Explora emociones y genera ideas para tus canciones"),
            #    size=14,
            #    color=ft.Colors.GREY_600,
            #    text_align=ft.TextAlign.CENTER,
            #),
        ],
    )