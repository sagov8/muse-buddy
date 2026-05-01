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
    page.title = "Muse Buddy"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window_width = 1000
    page.window_height = 780
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Cargar lista de emociones disponibles desde utils/arboles/
    try:
        arboles_disponibles = listar_arboles()
    except Exception as e:
        page.add(ft.Text(f"Error listando árboles: {e}", color=ft.Colors.RED))
        return

    if not arboles_disponibles:
        page.add(ft.Text("No se encontraron árboles en utils/arboles/", color=ft.Colors.RED))
        return

    # Estado de emoción seleccionada (None = pantalla de selección)
    emocion_seleccionada = {"valor": None}  # dict para mutabilidad en closures
    state = {"obj": None}  # AppState se crea al elegir emoción

    content = ft.Column(spacing=16, expand=True)

    ai_output = ft.TextField(
        label="Resultado IA",
        multiline=True,
        min_lines=10,
        max_lines=18,
        read_only=True,
        expand=True,
    )

    lyrics_editor = ft.TextField(
        label="Editor de letra",
        multiline=True,
        min_lines=12,
        max_lines=24,
        expand=True,
        hint_text="Aquí puedes mezclar versos, escribir ideas y construir tu canción...",
    )

    loading_ring = ft.ProgressRing(visible=False, width=28, height=28, stroke_width=3)
    status_text = ft.Text("", color=ft.Colors.BLUE_700, italic=True)
    result_title = ft.Text("Salida creativa", size=18, weight=ft.FontWeight.BOLD)

    style_dropdown = ft.Dropdown(
        label="Estilo de reescritura",
        value="poético",
        width=220,
        options=[
            ft.dropdown.Option("poético"),
            ft.dropdown.Option("íntimo"),
            ft.dropdown.Option("comercial"),
            ft.dropdown.Option("melancólico"),
            ft.dropdown.Option("minimalista"),
        ],
    )

    def limpiar_resultado_ia():
        if state["obj"]:
            state["obj"].ai_result = ""
        ai_output.value = ""
        result_title.value = "Salida creativa"

    def build_page_header():
        """Header dinámico: muestra 'Muse Buddy' en selección, o el nombre de la emoción en navegación."""
        if emocion_seleccionada["valor"] is None:
            return ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Herramienta para compositores", size=12, color=ft.Colors.GREY_600),
                    ft.Text("Muse Buddy", size=32, weight=ft.FontWeight.BOLD),
                ],
            )
        else:
            tree = state["obj"].root
            return build_header(tree)

    def render():
        content.controls.clear()

        # ── Pantalla 1: selección de emoción ──
        if emocion_seleccionada["valor"] is None:
            content.controls.append(
                build_emotion_view(
                    arboles=arboles_disponibles,
                    on_select_emotion=seleccionar_emocion,
                )
            )
            page.controls.clear()
            page.add(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            build_page_header(),
                            ft.Divider(),
                            content,
                        ],
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    width=900,
                )
            )
            page.update()
            return

        # ── Pantallas 2+: navegación dentro del árbol ──
        s = state["obj"]
        breadcrumb = build_breadcrumb(s.path, on_click_path=ir_a_path_index)

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
                )
            )
        else:
            content.controls.append(
                build_node_view(
                    current_node=s.current_node,
                    on_select_node=ir_a_nodo,
                )
            )

        # Botón volver: si estamos en la raíz del árbol, vuelve a selección de emoción
        if len(s.path) > 1:
            content.controls.append(ft.TextButton("← Volver", on_click=volver_atras))
        else:
            content.controls.append(
                ft.TextButton("← Cambiar emoción", on_click=volver_a_emociones)
            )

        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        build_page_header(),
                        ft.Divider(),
                        breadcrumb,
                        content,
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=900,
            )
        )
        page.update()

    # ── Handlers ──

    def seleccionar_emocion(arbol: dict):
        """Carga el árbol de la emoción elegida e inicia la navegación."""
        try:
            tree = cargar_datos(arbol["archivo"])
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error cargando árbol: {e}"))
            page.snack_bar.open = True
            page.update()
            return

        emocion_seleccionada["valor"] = arbol["valor"]
        state["obj"] = AppState(tree)
        limpiar_resultado_ia()
        render()

    def volver_a_emociones(e=None):
        emocion_seleccionada["valor"] = None
        state["obj"] = None
        limpiar_resultado_ia()
        lyrics_editor.value = ""
        render()

    def ir_a_nodo(nodo: dict):
        state["obj"].go_to_node(nodo)
        limpiar_resultado_ia()
        render()

    def volver_atras(e=None):
        state["obj"].go_back()
        limpiar_resultado_ia()
        render()

    def ir_a_path_index(index: int):
        state["obj"].go_to_path_index(index)
        limpiar_resultado_ia()
        render()

    def copy_seed(seed_text: str):
        copiar_texto(page, seed_text, "Frase copiada al portapapeles")

    def copiar_letra(e=None):
        copiar_texto(page, lyrics_editor.value or "", "Letra copiada al portapapeles")

    async def ejecutar_ia(modo: str, seed_text: str, estilo: str = "poético"):
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
            mensaje=f"Generando contenido con IA ({modo})...",
            titulo=f"Salida IA: {modo.capitalize()}",
        )

        try:
            respuesta = await asyncio.to_thread(generar_texto, prompt)
        except Exception as e:
            respuesta = f"Error generando contenido: {e}"

        finalizar_carga(respuesta)

    def generar_con_ia(modo: str, seed_text: str, estilo: str = "poético"):
        if state["obj"].is_generating:
            return
        page.run_task(ejecutar_ia, modo, seed_text, estilo)

    def reemplazar_editor_con_resultado(e=None):
        if ai_output.value and ai_output.value.strip():
            lyrics_editor.value = ai_output.value.strip()
            page.update()

    def agregar_resultado_al_editor(e=None):
        if ai_output.value and ai_output.value.strip():
            texto_actual = lyrics_editor.value.strip() if lyrics_editor.value else ""
            nuevo_bloque = ai_output.value.strip()
            lyrics_editor.value = (
                f"{texto_actual}\n\n{nuevo_bloque}" if texto_actual else nuevo_bloque
            )
            page.update()

    def limpiar_editor(e=None):
        lyrics_editor.value = ""
        page.update()

    async def ejecutar_mejora_letra():
        letra_actual = (lyrics_editor.value or "").strip()
        if not letra_actual:
            page.snack_bar = ft.SnackBar(ft.Text("Primero escribe o agrega algo al editor"))
            page.snack_bar.open = True
            page.update()
            return

        tema, categoria, mood = state["obj"].get_context()
        prompt = prompt_mejorar_letra(letra_actual, tema, categoria, mood)

        iniciar_carga(mensaje="Mejorando letra con IA...", titulo="Salida IA: Letra mejorada")

        try:
            respuesta = await asyncio.to_thread(generar_texto, prompt)
        except Exception as ex:
            respuesta = f"Error generando contenido: {ex}"

        finalizar_carga(respuesta)

    def mejorar_letra_con_ia(e=None):
        if state["obj"].is_generating:
            return
        page.run_task(ejecutar_mejora_letra)

    async def ejecutar_continuacion_letra():
        letra_actual = (lyrics_editor.value or "").strip()
        if not letra_actual:
            page.snack_bar = ft.SnackBar(ft.Text("Primero escribe o agrega algo al editor"))
            page.snack_bar.open = True
            page.update()
            return

        tema, categoria, mood = state["obj"].get_context()
        prompt = prompt_continuar_letra(letra_actual, tema, categoria, mood)

        iniciar_carga(mensaje="Generando continuación...", titulo="Salida IA: Continuación")

        try:
            respuesta = await asyncio.to_thread(generar_texto, prompt)
        except Exception as ex:
            respuesta = f"Error generando contenido: {ex}"

        finalizar_carga(respuesta)

    def continuar_letra_con_ia(e=None):
        if state["obj"].is_generating:
            return
        page.run_task(ejecutar_continuacion_letra)

    def iniciar_carga(mensaje: str, titulo: str):
        s = state["obj"]
        s.is_generating = True
        loading_ring.visible = True
        status_text.value = "Procesando..."
        result_title.value = titulo
        ai_output.value = mensaje
        style_dropdown.disabled = True
        page.update()

    def finalizar_carga(respuesta: str):
        s = state["obj"]
        s.is_generating = False
        loading_ring.visible = False
        status_text.value = "Listo"
        s.ai_result = respuesta
        ai_output.value = respuesta
        style_dropdown.disabled = False
        page.update()

    render()


if __name__ == "__main__":
    ft.app(target=main)
