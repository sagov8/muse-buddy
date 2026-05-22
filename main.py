
import flet as ft
import asyncio

from utils.data_loader import cargar_datos, listar_arboles
from services.ai_service import (
    generar_texto,
    generar_prompt_creativo,
    prompt_mejorar_letra,
    prompt_continuar_letra,
)
from models.app_state import AppState
from services.clipboard_service import copiar_texto

from ui.components.header import build_header
from ui.components.breadcrumb import build_breadcrumb
from ui.views.emotion_view import build_emotion_view
from ui.views.node_view import build_node_view
from ui.views.leaf_view import build_leaf_view


def main(page: ft.Page):

    # =========================================================
    # PAGE CONFIG
    # =========================================================

    page.title = "Muse Buddy"

    page.theme_mode = ft.ThemeMode.LIGHT

    page.bgcolor = "#0F0F13"

    page.padding = 24

    page.window_width = 1440
    page.window_height = 920

    page.scroll = ft.ScrollMode.AUTO

    # =========================================================
    # LOAD DATA
    # =========================================================

    try:
        arboles_disponibles = listar_arboles()

    except Exception as e:

        page.add(
            ft.Text(
                f"Error listando árboles: {e}",
                color="white",
            )
        )

        return

    if not arboles_disponibles:

        page.add(
            ft.Text(
                "No se encontraron árboles",
                color="red",
            )
        )

        return

    # =========================================================
    # STATE
    # =========================================================

    emocion_seleccionada = {
        "valor": None
    }

    state = {
        "obj": None
    }

    content = ft.Column(
        spacing=16,
        expand=True,
    )

    # =========================================================
    # INPUTS
    # =========================================================

    ai_output = ft.TextField(
        label="Resultado IA",

        multiline=True,

        min_lines=10,
        max_lines=18,

        read_only=True,

        bgcolor="#23232C",

        border_color="#3F3F46",

        color="#F8FAFC",

        border_radius=18,
        
    )

    lyrics_editor = ft.TextField(
        label="Editor de letra",

        multiline=True,

        min_lines=14,
        max_lines=26,

        bgcolor="#23232C",

        border_color="#3F3F46",

        color="#F8FAFC",

        border_radius=18,

        hint_text="Escribe tu canción aquí...",
    )

    loading_ring = ft.ProgressRing(
        visible=False,
        width=26,
        height=26,
    )

    status_text = ft.Text(
        "",
        color="#C084FC",
    )

    result_title = ft.Text(
        "Salida creativa",
        size=20,
        weight=ft.FontWeight.BOLD,
        color="white",
    )

    style_dropdown = ft.Dropdown(
        label="Estilo",

        value="poético",

        width=220,

        bgcolor="#23232C",

        border_color="#3F3F46",

        color="#F8FAFC",

        options=[
            ft.dropdown.Option("poético"),
            ft.dropdown.Option("íntimo"),
            ft.dropdown.Option("comercial"),
            ft.dropdown.Option("melancólico"),
            ft.dropdown.Option("minimalista"),
        ],
    )

    # =========================================================
    # MODAL ACORDES
    # =========================================================

    def abrir_modal_acordes(e=None):

        print("ABRIENDO MODAL")

        accent = "#8B5CF6"

        dialog = ft.AlertDialog(
            modal=True,

            bgcolor="#18181B",

            title=ft.Text(
                "Constructor armónico",
                color="white",
                weight=ft.FontWeight.BOLD,
            ),

            content=ft.Container(
                width=700,

                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,

                    spacing=24,

                    controls=[

                        # GRAFO
                        ft.Container(
                            bgcolor="#23232A",

                            border_radius=20,

                            padding=20,

                            content=ft.Column(
                                spacing=20,

                                controls=[

                                    ft.Text(
                                        "Grafo de acordes",
                                        color="white",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                    ),

                                    ft.Column(
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                                        controls=[

                                            ft.Container(
                                                width=70,
                                                height=70,

                                                border_radius=999,

                                                bgcolor=accent,

                                                alignment=ft.Alignment(0, 0),

                                                content=ft.Text(
                                                    "Am",
                                                    color="white",
                                                    size=20,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                            ),

                                            ft.Text(
                                                "╱      ╲",
                                                color="#71717A",
                                                size=20,
                                            ),

                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.CENTER,

                                                spacing=80,

                                                controls=[

                                                    ft.Container(
                                                        width=70,
                                                        height=70,

                                                        border_radius=999,

                                                        bgcolor="#27272A",

                                                        alignment=ft.Alignment(0, 0),

                                                        content=ft.Text(
                                                            "F",
                                                            color="white",
                                                            size=20,
                                                            weight=ft.FontWeight.BOLD,
                                                        ),
                                                    ),

                                                    ft.Container(
                                                        width=70,
                                                        height=70,

                                                        border_radius=999,

                                                        bgcolor="#27272A",

                                                        alignment=ft.Alignment(0, 0),

                                                        content=ft.Text(
                                                            "C",
                                                            color="white",
                                                            size=20,
                                                            weight=ft.FontWeight.BOLD,
                                                        ),
                                                    ),
                                                ],
                                            ),

                                            ft.Text(
                                                "╲      ╱",
                                                color="#71717A",
                                                size=20,
                                            ),

                                            ft.Container(
                                                width=70,
                                                height=70,

                                                border_radius=999,

                                                bgcolor="#27272A",

                                                alignment=ft.Alignment(0, 0),

                                                content=ft.Text(
                                                    "G",
                                                    color="white",
                                                    size=20,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ),

                        # PALETA
                        ft.Container(
                            bgcolor="#23232A",

                            border_radius=20,

                            padding=20,

                            content=ft.Column(
                                spacing=16,

                                controls=[

                                    ft.Text(
                                        "Paleta de acordes",
                                        color="white",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                    ),

                                    ft.Row(
                                        wrap=True,

                                        spacing=10,

                                        controls=[

                                            ft.Chip(
                                                label=ft.Text("Am"),
                                                bgcolor="#27272A",
                                            ),

                                            ft.Chip(
                                                label=ft.Text("F"),
                                                bgcolor="#27272A",
                                            ),

                                            ft.Chip(
                                                label=ft.Text("C"),
                                                bgcolor="#27272A",
                                            ),

                                            ft.Chip(
                                                label=ft.Text("G"),
                                                bgcolor="#27272A",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ),

                        # PREVIEW
                        ft.Container(
                            bgcolor="#23232A",

                            border_radius=20,

                            padding=20,

                            content=ft.Column(
                                spacing=16,

                                controls=[

                                    ft.Text(
                                        "Vista armónica",
                                        color="white",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                    ),

                                    ft.Column(
                                        spacing=14,

                                        controls=[

                                            ft.Column(
                                                spacing=4,

                                                controls=[

                                                    ft.Text(
                                                        "Am",
                                                        color=accent,
                                                        size=18,
                                                        weight=ft.FontWeight.BOLD,
                                                    ),

                                                    ft.Text(
                                                        "Tus ojos vuelven a mí",
                                                        color="white",
                                                        size=15,
                                                    ),
                                                ],
                                            ),

                                            ft.Column(
                                                spacing=4,

                                                controls=[

                                                    ft.Text(
                                                        "F",
                                                        color=accent,
                                                        size=18,
                                                        weight=ft.FontWeight.BOLD,
                                                    ),

                                                    ft.Text(
                                                        "Y el silencio empieza a hablar",
                                                        color="white",
                                                        size=15,
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ),

                        # FINAL
                        ft.Container(
                            bgcolor="#23232A",

                            border_radius=20,

                            padding=20,

                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                                controls=[

                                    ft.Column(
                                        spacing=4,

                                        controls=[

                                            ft.Text(
                                                "Resolución sugerida",
                                                color="#A1A1AA",
                                                size=12,
                                            ),

                                            ft.Text(
                                                "Am",
                                                size=32,
                                                weight=ft.FontWeight.BOLD,
                                                color="white",
                                            ),
                                        ],
                                    ),

                                    ft.Icon(
                                        ft.Icons.MUSIC_NOTE,
                                        color=accent,
                                        size=40,
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),

            actions_alignment=ft.MainAxisAlignment.END,

            actions=[
                ft.TextButton(
                    "Cerrar",

                    on_click=lambda e: cerrar_modal(dialog),
                )
            ],
        )

        page.overlay.append(dialog)

        dialog.open = True

        page.update()

    def cerrar_modal(dialog):

        dialog.open = False

        page.update()

    # =========================================================
    # HELPERS
    # =========================================================

    def limpiar_resultado_ia():

        if state["obj"]:
            state["obj"].ai_result = ""

        ai_output.value = ""

        result_title.value = "Salida creativa"

    # =========================================================
    # HEADER
    # =========================================================

    def build_page_header():

        if emocion_seleccionada["valor"] is None:

            return ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[

                    ft.Text(
                        "Herramienta para compositores",
                        size=12,
                        color="#A1A1AA",
                    ),

                    ft.Text(
                        "Muse Buddy",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color="white",
                    ),
                ],
            )

        else:

            tree = state["obj"].root

            return build_header(tree)

    # =========================================================
    # RENDER
    # =========================================================

    def render():

        content.controls.clear()

        if emocion_seleccionada["valor"] is None:

            content.controls.append(

                build_emotion_view(
                    arboles=arboles_disponibles,
                    on_select_emotion=seleccionar_emocion,
                )
            )

            page.clean()

            page.add(

                ft.Container(
                    width=1280,

                    content=ft.Column(

                        spacing=20,

                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                        controls=[

                            build_page_header(),

                            ft.Divider(),

                            content,
                        ],
                    ),
                )
            )

            page.update()

            return

        s = state["obj"]

        breadcrumb = build_breadcrumb(
            s.path,
            on_click_path=ir_a_path_index,
        )

        if s.is_leaf():

            content.controls.append(

                build_leaf_view(
                    current_node=s.current_node,

                    path=s.path,

                    style_dropdown=style_dropdown,

                    ai_output=ai_output,

                    lyrics_editor=lyrics_editor,

                    loading_ring=loading_ring,

                    result_title=result_title,

                    status_text=status_text,

                    is_generating=s.is_generating,

                    on_copy_seed=copy_seed,

                    on_generate_ai=generar_con_ia,

                    on_replace_editor=reemplazar_editor_con_resultado,

                    on_append_editor=agregar_resultado_al_editor,

                    on_improve_lyrics=mejorar_letra_con_ia,

                    on_continue_lyrics=continuar_letra_con_ia,

                    on_copy_lyrics=copiar_letra,

                    on_clear_editor=limpiar_editor,

                    on_open_chords=abrir_modal_acordes,
                )
            )

        else:

            content.controls.append(

                build_node_view(
                    current_node=s.current_node,
                    on_select_node=ir_a_nodo,
                )
            )

        page.clean()

        page.add(

            ft.Container(
                width=1280,

                content=ft.Column(

                    spacing=20,

                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                    controls=[

                        build_page_header(),

                        ft.Divider(),

                        breadcrumb,

                        content,
                    ],
                ),
            )
        )

        page.update()

    # =========================================================
    # NAVIGATION
    # =========================================================

    def seleccionar_emocion(arbol):

        tree = cargar_datos(arbol["archivo"])

        emocion_seleccionada["valor"] = arbol["valor"]

        state["obj"] = AppState(tree)

        limpiar_resultado_ia()

        render()

    def volver_a_emociones(e=None):

        emocion_seleccionada["valor"] = None

        state["obj"] = None

        render()

    def ir_a_nodo(nodo):

        state["obj"].go_to_node(nodo)

        render()

    def volver_atras(e=None):

        state["obj"].go_back()

        render()

    def ir_a_path_index(index):

        state["obj"].go_to_path_index(index)

        render()

    # =========================================================
    # COPY
    # =========================================================

    def copy_seed(seed_text):

        copiar_texto(
            page,
            seed_text,
            "Frase copiada",
        )

    def copiar_letra(e=None):

        copiar_texto(
            page,
            lyrics_editor.value or "",
            "Letra copiada",
        )

    # =========================================================
    # IA
    # =========================================================

    async def ejecutar_ia(modo, seed_text, estilo="poético"):

        tema, categoria, mood = state["obj"].get_context()

        prompt = generar_prompt_creativo(
            modo=modo,
            tema=tema,
            tipo_amor=categoria,
            mood=mood,
            frase_semilla=seed_text,
            estilo=estilo,
        )

        iniciar_carga(
            "Generando contenido...",
            f"Salida IA: {modo}",
        )

        try:

            respuesta = await asyncio.to_thread(
                generar_texto,
                prompt,
            )

        except Exception as e:

            respuesta = f"Error: {e}"

        finalizar_carga(respuesta)

    def generar_con_ia(modo, seed_text, estilo="poético"):

        if state["obj"].is_generating:
            return

        page.run_task(
            ejecutar_ia,
            modo,
            seed_text,
            estilo,
        )

    # =========================================================
    # EDITOR
    # =========================================================

    def reemplazar_editor_con_resultado(e=None):

        lyrics_editor.value = ai_output.value

        page.update()

    def agregar_resultado_al_editor(e=None):

        lyrics_editor.value += "\n\n" + ai_output.value

        page.update()

    def limpiar_editor(e=None):

        lyrics_editor.value = ""

        page.update()

    # =========================================================
    # MEJORAR
    # =========================================================

    async def ejecutar_mejora_letra():

        letra_actual = lyrics_editor.value.strip()

        if not letra_actual:
            return

        tema, categoria, mood = state["obj"].get_context()

        prompt = prompt_mejorar_letra(
            letra_actual,
            tema,
            categoria,
            mood,
        )

        iniciar_carga(
            "Mejorando letra...",
            "Letra mejorada",
        )

        respuesta = await asyncio.to_thread(
            generar_texto,
            prompt,
        )

        finalizar_carga(respuesta)

    def mejorar_letra_con_ia(e=None):

        page.run_task(
            ejecutar_mejora_letra
        )

    # =========================================================
    # CONTINUAR
    # =========================================================

    async def ejecutar_continuacion_letra():

        letra_actual = lyrics_editor.value.strip()

        if not letra_actual:
            return

        tema, categoria, mood = state["obj"].get_context()

        prompt = prompt_continuar_letra(
            letra_actual,
            tema,
            categoria,
            mood,
        )

        iniciar_carga(
            "Continuando letra...",
            "Continuación",
        )

        respuesta = await asyncio.to_thread(
            generar_texto,
            prompt,
        )

        finalizar_carga(respuesta)

    def continuar_letra_con_ia(e=None):

        page.run_task(
            ejecutar_continuacion_letra
        )

    # =========================================================
    # LOADING
    # =========================================================

    def iniciar_carga(mensaje, titulo):

        s = state["obj"]

        s.is_generating = True

        loading_ring.visible = True

        status_text.value = "Procesando..."

        result_title.value = titulo

        ai_output.value = mensaje

        page.update()

    def finalizar_carga(respuesta):

        s = state["obj"]

        s.is_generating = False

        loading_ring.visible = False

        status_text.value = "Listo"

        ai_output.value = respuesta

        page.update()

    # =========================================================
    # START
    # =========================================================

    render()


if __name__ == "__main__":
    ft.app(target=main)

