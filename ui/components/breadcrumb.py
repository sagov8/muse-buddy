import flet as ft


def build_breadcrumb(path: list[dict], on_click_path) -> ft.Row:
    items = []

    for i, nodo in enumerate(path):
        if i > 0:
            items.append(ft.Text("›", color=ft.Colors.GREY_600))

        es_actual = i == len(path) - 1

        if es_actual:
            items.append(
                ft.Text(
                    nodo.get("valor", "Nodo"),
                    weight=ft.FontWeight.BOLD,
                )
            )
        else:
            items.append(
                ft.TextButton(
                    nodo.get("valor", "Nodo"),
                    on_click=lambda e, idx=i: on_click_path(idx),
                )
            )

    return ft.Row(wrap=True, spacing=8, controls=items)