import flet as ft


def build_leaf_view(
    current_node: dict,
    path: list[dict],
    style_dropdown: ft.Dropdown,
    ai_output: ft.TextField,
    lyrics_editor: ft.TextField,
    loading_ring: ft.ProgressRing,
    result_title: ft.Text,
    status_text: ft.Text,
    is_generating: bool,
    on_copy_seed,
    on_generate_ai,
    on_replace_editor,
    on_append_editor,
    on_improve_lyrics,
    on_continue_lyrics,
    on_copy_lyrics,
    on_clear_editor,
) -> ft.Control:
    texto = current_node.get("valor", "")
    subtipo = current_node.get("subtipo", "frase")
    contexto = " · ".join([n.get("valor", "") for n in path[:-1] if n.get("valor")])

    return ft.Column(
        controls=[
            ft.Text("Frase semilla", size=22, weight=ft.FontWeight.BOLD),
            ft.Text(contexto, size=14, color=ft.Colors.GREY_600),
            ft.TextField(
                value=texto,
                multiline=True,
                min_lines=3,
                read_only=True,
                border_radius=12,
            ),
            ft.Text(subtipo.upper(), size=11, color=ft.Colors.GREY_600),
            ft.Row(
                controls=[
                    ft.OutlinedButton(
                        "Copiar",
                        icon=ft.Icons.COPY,
                        disabled=is_generating,
                        on_click=lambda e, t=texto: on_copy_seed(t),
                    ),
                ],
                wrap=True,
            ),
            ft.Divider(),
            ft.Text("Acciones creativas con IA", size=18, weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Explicar emoción",
                        icon=ft.Icons.PSYCHOLOGY,
                        disabled=is_generating,
                        on_click=lambda e, t=texto: on_generate_ai("explicacion", t),
                    ),
                    ft.ElevatedButton(
                        "Generar versos",
                        icon=ft.Icons.EDIT_NOTE,
                        disabled=is_generating,
                        on_click=lambda e, t=texto: on_generate_ai("versos", t),
                    ),
                    ft.ElevatedButton(
                        "Generar coro",
                        icon=ft.Icons.MUSIC_NOTE,
                        disabled=is_generating,
                        on_click=lambda e, t=texto: on_generate_ai("coro", t),
                    ),
                ],
                wrap=True,
            ),
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Generar títulos",
                        icon=ft.Icons.TITLE,
                        disabled=is_generating,
                        on_click=lambda e, t=texto: on_generate_ai("titulos", t),
                    ),
                    style_dropdown,
                    ft.ElevatedButton(
                        "Reescribir",
                        icon=ft.Icons.AUTO_FIX_HIGH,
                        disabled=is_generating,
                        on_click=lambda e, t=texto: on_generate_ai(
                            "reescritura", t, style_dropdown.value or "poético"
                        ),
                    ),
                ],
                wrap=True,
            ),
            ft.Divider(),
            result_title,
            ft.Row(
                controls=[loading_ring, status_text],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ai_output,
            ft.Row(
                controls=[
                    ft.OutlinedButton(
                        "Reemplazar editor",
                        icon=ft.Icons.VERTICAL_ALIGN_CENTER,
                        disabled=is_generating,
                        on_click=on_replace_editor,
                    ),
                    ft.OutlinedButton(
                        "Agregar al editor",
                        icon=ft.Icons.ADD,
                        disabled=is_generating,
                        on_click=on_append_editor,
                    ),
                ],
                wrap=True,
            ),
            lyrics_editor,
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Mejorar letra",
                        icon=ft.Icons.AUTO_AWESOME,
                        disabled=is_generating,
                        on_click=on_improve_lyrics,
                    ),
                    ft.ElevatedButton(
                        "Continuar letra",
                        icon=ft.Icons.LIBRARY_MUSIC,
                        disabled=is_generating,
                        on_click=on_continue_lyrics,
                    ),
                    ft.OutlinedButton(
                        "Copiar letra",
                        icon=ft.Icons.COPY_ALL,
                        disabled=is_generating,
                        on_click=on_copy_lyrics,
                    ),
                    ft.TextButton(
                        "Limpiar editor",
                        icon=ft.Icons.DELETE_OUTLINE,
                        disabled=is_generating,
                        on_click=on_clear_editor,
                    ),
                ],
                wrap=True,
            ),
        ]
    )