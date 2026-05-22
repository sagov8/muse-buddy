


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
    on_open_chords,
) -> ft.Control:

    texto = current_node.get("valor", "")
    subtipo = current_node.get("subtipo", "frase")

    contexto = " · ".join(
        [n.get("valor", "") for n in path[:-1] if n.get("valor")]
    )

    emocion_principal = (
        path[0].get("valor", "").lower()
        if path
        else ""
    )

    # =========================
    # THEMES
    # =========================

    theme_map = {
        "amor": {
            "accent": "#EC4899",
            "soft": "#4A102A",
        },
        "tristeza": {
            "accent": "#60A5FA",
            "soft": "#172554",
        },
        "ira": {
            "accent": "#EF4444",
            "soft": "#450A0A",
        },
        "felicidad": {
            "accent": "#F59E0B",
            "soft": "#451A03",
        },
    }

    theme = theme_map.get(
        emocion_principal,
        {
            "accent": "#8B5CF6",
            "soft": "#2E1065",
        },
    )

    accent = theme["accent"]
    soft = theme["soft"]

    # =========================
    # COLORS
    # =========================

    page_bg = "#09090B"

    card_bg = "#111827"
    secondary_bg = "#1E293B"

    border_color = "#334155"

    text_primary = "#F8FAFC"
    text_secondary = "#CBD5E1"

    # =========================
    # HELPERS
    # =========================

    def section_title(text):
        return ft.Text(
            text,
            size=18,
            weight=ft.FontWeight.BOLD,
            color=text_primary,
        )

    def action_button(text, icon, mode):

        return ft.ElevatedButton(
            text,
            icon=icon,
            width=260,
            disabled=is_generating,

            on_click=lambda e, t=texto:
            on_generate_ai(mode, t),

            style=ft.ButtonStyle(
                bgcolor=accent,
                color="white",
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=16),
            ),
        )

    def lyric_line(chord, lyric):

        return ft.Container(
            padding=ft.padding.symmetric(vertical=12),

            content=ft.Column(
                spacing=4,

                controls=[

                    ft.Text(
                        chord,
                        color=accent,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),

                    ft.Text(
                        lyric,
                        color=text_primary,
                        size=15,
                    ),
                ],
            ),
        )

    # =========================
    # LEFT PANEL
    # =========================

    left_panel = ft.Container(
        bgcolor=card_bg,

        border=ft.border.all(
            1,
            border_color,
        ),

        border_radius=28,

        padding=24,

        shadow=[
            ft.BoxShadow(
                blur_radius=20,
                color="#00000025",
                offset=ft.Offset(0, 8),
            )
        ],

        content=ft.Column(
            spacing=22,

            controls=[

                ft.Text(
                    "Frase semilla",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=text_primary,
                ),

                ft.Text(
                    contexto,
                    size=13,
                    color=text_secondary,
                ),

                ft.Container(
                    bgcolor=secondary_bg,
                    border_radius=20,
                    padding=20,

                    content=ft.Text(
                        texto,
                        size=16,
                        italic=True,
                        color=text_primary,
                    ),
                ),

                ft.Container(
                    bgcolor=soft,
                    border_radius=999,
                    padding=ft.padding.symmetric(
                        horizontal=14,
                        vertical=8,
                    ),

                    content=ft.Text(
                        subtipo.upper(),
                        size=11,
                        color=accent,
                        weight=ft.FontWeight.BOLD,
                    ),
                ),

                ft.OutlinedButton(
                    "Copiar frase",
                    icon=ft.Icons.COPY,
                    disabled=is_generating,
                    on_click=lambda e, t=texto: on_copy_seed(t),
                ),

                ft.Divider(color=border_color),

                section_title("Generar contenido"),

                action_button(
                    "Explicar emoción",
                    ft.Icons.PSYCHOLOGY,
                    "explicacion",
                ),

                action_button(
                    "Generar versos",
                    ft.Icons.EDIT_NOTE,
                    "versos",
                ),

                action_button(
                    "Generar coro",
                    ft.Icons.MUSIC_NOTE,
                    "coro",
                ),

                action_button(
                    "Generar títulos",
                    ft.Icons.TITLE,
                    "titulos",
                ),

                ft.Divider(color=border_color),

                section_title("Reescritura"),

                style_dropdown,

                ft.ElevatedButton(
                    "Reescribir letra",
                    icon=ft.Icons.AUTO_FIX_HIGH,
                    width=260,
                    disabled=is_generating,

                    on_click=lambda e, t=texto:
                    on_generate_ai(
                        "reescritura",
                        t,
                        style_dropdown.value or "poético"
                    ),

                    style=ft.ButtonStyle(
                        bgcolor="#27272A",
                        color="white",
                        padding=18,
                        shape=ft.RoundedRectangleBorder(radius=16),
                    ),
                ),
            ],
        ),
    )

    # =========================
    # RIGHT PANEL
    # =========================

    right_panel = ft.Container(
        bgcolor=card_bg,

        border=ft.border.all(
            1,
            border_color,
        ),

        border_radius=28,

        padding=26,

        expand=True,

        shadow=[
            ft.BoxShadow(
                blur_radius=25,
                color="#00000035",
                offset=ft.Offset(0, 10),
            )
        ],

        content=ft.Column(
            spacing=24,

            controls=[

                # HEADER
                ft.Column(
                    spacing=6,

                    controls=[

                        ft.Text(
                            "Muse Buddy Studio",
                            size=34,
                            weight=ft.FontWeight.BOLD,
                            color=text_primary,
                        ),

                        ft.Text(
                            "Editor inteligente de composición musical",
                            size=14,
                            color=text_secondary,
                        ),
                    ],
                ),

                # RESULTADO IA
                ft.Container(
                    bgcolor=secondary_bg,
                    border_radius=24,
                    padding=20,

                    content=ft.Column(
                        spacing=14,

                        controls=[

                            result_title,

                            ft.Row(
                                spacing=10,

                                controls=[
                                    loading_ring,
                                    status_text,
                                ],
                            ),

                            ai_output,

                            ft.Row(
                                wrap=True,
                                spacing=10,

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
                            ),
                        ],
                    ),
                ),

                # =========================
                # EDITOR
                # =========================

                section_title("Editor creativo"),

                ft.Container(
                    expand=True,

                    bgcolor="#0F172A",

                    border_radius=24,

                    padding=20,

                    border=ft.border.all(
                        1,
                        border_color,
                    ),

                    shadow=[
                        ft.BoxShadow(
                            blur_radius=25,
                            color="#00000055",
                            offset=ft.Offset(0, 8),
                        )
                    ],

                    content=lyrics_editor,
                ),

                ft.Row(
                    wrap=True,
                    spacing=12,

                    controls=[

                        ft.ElevatedButton(
                            "Mejorar letra",
                            icon=ft.Icons.AUTO_AWESOME,
                            disabled=is_generating,
                            on_click=on_improve_lyrics,

                            style=ft.ButtonStyle(
                                bgcolor=accent,
                                color="white",
                            ),
                        ),

                        ft.ElevatedButton(
                            "Continuar letra",
                            icon=ft.Icons.LIBRARY_MUSIC,
                            disabled=is_generating,
                            on_click=on_continue_lyrics,

                            style=ft.ButtonStyle(
                                bgcolor="#27272A",
                                color="white",
                            ),
                        ),

                        ft.OutlinedButton(
                            "Copiar",
                            icon=ft.Icons.COPY_ALL,
                            disabled=is_generating,
                            on_click=on_copy_lyrics,
                        ),

                        ft.TextButton(
                            "Limpiar",
                            disabled=is_generating,
                            on_click=on_clear_editor,
                        ),
                    ],
                ),

                # =========================
                # ACORDES
                # =========================

                ft.Divider(color=border_color),

                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                    controls=[

                        section_title("Progresión armónica"),

                        ft.ElevatedButton(
                            "Generar acordes",
                            icon=ft.Icons.GRAPHIC_EQ,
                            on_click=on_open_chords,

                            style=ft.ButtonStyle(
                                bgcolor=accent,
                                color="white",
                                padding=18,
                                shape=ft.RoundedRectangleBorder(radius=16),
                            ),
                        ),
                    ],
                ),

                # VISTA ARMÓNICA
                ft.Container(
                    bgcolor=secondary_bg,

                    border_radius=24,

                    padding=24,

                    border=ft.border.all(
                        1,
                        border_color,
                    ),

                    content=ft.Column(
                        spacing=18,

                        controls=[

                            ft.Text(
                                "Vista armónica",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=text_primary,
                            ),

                            lyric_line(
                                "Am",
                                "Tus ojos caen sobre mí",
                            ),

                            lyric_line(
                                "F",
                                "La noche vuelve a hablar",
                            ),

                            lyric_line(
                                "C",
                                "Aunque el silencio siga aquí",
                            ),

                            lyric_line(
                                "G",
                                "Todo vuelve a comenzar",
                            ),
                        ],
                    ),
                ),

                # =========================
                # PROGRESIÓN FINAL
                # =========================

                ft.Container(
                    bgcolor=soft,

                    border_radius=24,

                    padding=24,

                    shadow=[
                        ft.BoxShadow(
                            blur_radius=25,
                            color=accent + "55",
                            offset=ft.Offset(0, 0),
                        )
                    ],

                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                        controls=[

                            ft.Column(
                                spacing=4,

                                controls=[

                                    ft.Text(
                                        "Progresión sugerida",
                                        color="#E5E7EB",
                                        size=13,
                                    ),

                                    ft.Text(
                                        "Am - F - C - G",
                                        size=30,
                                        weight=ft.FontWeight.BOLD,
                                        color="white",
                                    ),
                                ],
                            ),

                            ft.Icon(
                                ft.Icons.MUSIC_NOTE,
                                color="white",
                                size=42,
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )

    return ft.Container(
        bgcolor=page_bg,
        padding=14,

        content=ft.ResponsiveRow(
            columns=12,
            spacing=22,
            run_spacing=22,

            controls=[

                ft.Container(
                    col={"xs": 12, "md": 4},
                    content=left_panel,
                ),

                ft.Container(
                    col={"xs": 12, "md": 8},
                    content=right_panel,
                ),
            ],
        ),
    )

