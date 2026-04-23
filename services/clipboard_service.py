import pyperclip
import flet as ft

def copiar_texto(page: ft.Page, texto: str, ok_msg="Texto copiado al portapapeles"):
    try:
        pyperclip.copy(texto)
        page.snack_bar = ft.SnackBar(ft.Text(ok_msg))
    except Exception as e:
        page.snack_bar = ft.SnackBar(ft.Text(f"No se pudo copiar: {e}"))

    page.snack_bar.open = True
    page.update()