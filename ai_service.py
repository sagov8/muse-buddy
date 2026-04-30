from __future__ import annotations

from typing import Callable

import ollama


MODEL_NAME = "gemma2"
OLLAMA_HOST = "http://localhost:11434"

_client = ollama.Client(host=OLLAMA_HOST)


def generar_texto(prompt: str) -> str:
    try:
        result = _client.generate(
            model=MODEL_NAME,
            prompt=prompt,
            stream=False,
            options={
                "temperature": 1.05,
                "top_p": 0.95,
                "top_k": 60,
                "repeat_penalty": 1.15,
                "num_predict": 900,
            },
        )
        return result.get("response", "No se recibió respuesta del modelo.").strip()
    except ollama.ResponseError as e:
        return f"Error de Ollama: {e.error}"
    except Exception as e:
        return f"Error conectando con Ollama: {e}"


def instrucciones_base() -> str:
    return """
Actúa como un coautor musical experto en letras en español.
Tu objetivo es ayudar a crear canciones originales, emocionales y cantables.

Reglas creativas:
- Usa imágenes concretas, sensoriales y cinematográficas.
- Evita clichés como "corazón roto", "sin ti no soy nada", "lágrimas de amor", "alma perdida".
- No imites artistas reales ni copies canciones existentes.
- Prioriza frases que puedan cantarse con naturalidad.
- Mezcla emoción directa con metáforas frescas.
- Evita sonar genérico, robótico o demasiado explicativo.
- Mantén coherencia entre tema, emoción, tono y frase semilla.
""".strip()


def construir_contexto(tema: str, categoria: str, mood: str, frase_semilla: str) -> str:
    return f"""
Tema principal: {tema}
Categoría emocional: {categoria}
Matiz o tono: {mood}
Frase semilla: "{frase_semilla}"
""".strip()


def prompt_explicacion(tema: str, categoria: str, mood: str, frase_semilla: str) -> str:
    contexto = construir_contexto(tema, categoria, mood, frase_semilla)
    return f"""
{instrucciones_base()}

{contexto}

Tarea:
Analiza esta idea como punto de partida para una canción.

Incluye:
1. Emoción central.
2. Conflicto interno o narrativo.
3. Posible historia detrás de la canción.
4. Imágenes, símbolos o metáforas que podrían desarrollarse.
5. Dirección musical sugerida en términos emocionales, no técnicos.

Responde en español con secciones breves y útiles para componer.
""".strip()


def prompt_ideas_letra(tema: str, categoria: str, mood: str, frase_semilla: str) -> str:
    contexto = construir_contexto(tema, categoria, mood, frase_semilla)
    return f"""
{instrucciones_base()}

{contexto}

Tarea:
Genera un banco creativo de ideas para escribir una letra completa.

Incluye:
1. Concepto central de la canción.
2. Punto de vista narrativo.
3. Escena inicial sugerida.
4. Conflicto emocional.
5. 6 imágenes concretas para versos.
6. 4 frases gancho originales.
7. Posible estructura: verso, pre-coro, coro y puente.

Responde con ideas breves, potentes y listas para usar.
""".strip()


def prompt_versos(tema: str, categoria: str, mood: str, frase_semilla: str) -> str:
    contexto = construir_contexto(tema, categoria, mood, frase_semilla)
    return f"""
{instrucciones_base()}

{contexto}

Tarea:
Escribe 8 versos originales inspirados en la frase semilla.

Condiciones:
- No repitas exactamente la frase semilla.
- Cada verso debe tener una imagen clara.
- Deben sonar naturales, emocionales y cantables.
- Evita rimas forzadas.
- Mantén una progresión emocional entre los versos.

Responde solo con los versos, uno por línea.
""".strip()


def prompt_coro(tema: str, categoria: str, mood: str, frase_semilla: str) -> str:
    contexto = construir_contexto(tema, categoria, mood, frase_semilla)
    return f"""
{instrucciones_base()}

{contexto}

Tarea:
Escribe un coro corto y memorable para una canción.

Condiciones:
- Máximo 4 líneas.
- Debe tener una frase gancho fuerte.
- Debe ser emocional, directo y cantable.
- Puede usar repetición, pero sin volverse plano.
- Debe sentirse como el centro de la canción.

Responde solo con el coro.
""".strip()


def prompt_titulos(tema: str, categoria: str, mood: str, frase_semilla: str) -> str:
    contexto = construir_contexto(tema, categoria, mood, frase_semilla)
    return f"""
{instrucciones_base()}

{contexto}

Tarea:
Genera 12 posibles títulos de canción en español.

Condiciones:
- Mezcla títulos directos, poéticos y misteriosos.
- Deben ser memorables y fáciles de recordar.
- Evita títulos demasiado largos.
- No uses títulos genéricos.

Responde solo con la lista de títulos.
""".strip()


def prompt_reescritura(
    tema: str, categoria: str, mood: str, frase_semilla: str, estilo: str
) -> str:
    contexto = construir_contexto(tema, categoria, mood, frase_semilla)
    return f"""
{instrucciones_base()}

{contexto}

Estilo deseado: {estilo}

Tarea:
Reescribe la frase semilla en 7 variaciones distintas.

Condiciones:
- Conserva la emoción principal.
- Cada variación debe sentirse diferente.
- Que suenen como líneas reales de canción.
- Incluye opciones simples, poéticas, intensas y sutiles.
- No expliques las opciones.

Responde solo con las 7 variaciones, una por línea.
""".strip()


def prompt_mejorar_letra(letra: str, tema: str, categoria: str, mood: str) -> str:
    return f"""
{instrucciones_base()}

Tema principal: {tema}
Categoría emocional: {categoria}
Matiz o tono: {mood}

Letra actual:
\"\"\"
{letra}
\"\"\"

Tarea:
Mejora esta letra manteniendo su intención emocional.

Condiciones:
- Hazla más fluida, poética y cantable.
- Mejora imágenes, ritmo y fuerza expresiva.
- Conserva la idea principal.
- Evita clichés y frases demasiado comunes.
- No expliques los cambios.

Devuelve solo la letra mejorada.
""".strip()


def prompt_continuar_letra(letra: str, tema: str, categoria: str, mood: str) -> str:
    return f"""
{instrucciones_base()}

Tema principal: {tema}
Categoría emocional: {categoria}
Matiz o tono: {mood}

Letra actual:
\"\"\"
{letra}
\"\"\"

Tarea:
Continúa esta canción con 8 líneas nuevas.

Condiciones:
- Mantén coherencia emocional y estilística.
- No repitas lo ya escrito.
- Haz que funcione como siguiente estrofa, pre-coro o desarrollo.
- Usa imágenes nuevas.
- Mantén un lenguaje cantable.

Devuelve solo las nuevas líneas.
""".strip()


def prompt_letra_completa(
    tema: str,
    categoria: str,
    mood: str,
    frase_semilla: str,
    estilo: str = "poético",
) -> str:
    contexto = construir_contexto(tema, categoria, mood, frase_semilla)
    return f"""
{instrucciones_base()}

{contexto}
Estilo deseado: {estilo}

Tarea:
Escribe una letra completa de canción en español.

Estructura:
[Verso 1]
[Pre-Coro]
[Coro]
[Verso 2]
[Puente]
[Coro Final]

Condiciones:
- La letra debe ser original.
- Debe tener una evolución emocional clara.
- El coro debe sentirse memorable.
- Evita clichés.
- Usa lenguaje natural, poético y cantable.
- No expliques nada fuera de la letra.

Devuelve solo la letra con sus secciones.
""".strip()


def generar_prompt_creativo(
    modo: str,
    tema: str,
    tipo_amor: str,
    mood: str,
    frase_semilla: str,
    estilo: str = "poético",
) -> str:
    modo = modo.lower().strip()

    prompts: dict[str, Callable[[], str]] = {
        "explicacion": lambda: prompt_explicacion(
            tema, tipo_amor, mood, frase_semilla
        ),
        "ideas": lambda: prompt_ideas_letra(
            tema, tipo_amor, mood, frase_semilla
        ),
        "ideas_letra": lambda: prompt_ideas_letra(
            tema, tipo_amor, mood, frase_semilla
        ),
        "versos": lambda: prompt_versos(
            tema, tipo_amor, mood, frase_semilla
        ),
        "coro": lambda: prompt_coro(
            tema, tipo_amor, mood, frase_semilla
        ),
        "titulos": lambda: prompt_titulos(
            tema, tipo_amor, mood, frase_semilla
        ),
        "reescritura": lambda: prompt_reescritura(
            tema, tipo_amor, mood, frase_semilla, estilo
        ),
        "letra_completa": lambda: prompt_letra_completa(
            tema, tipo_amor, mood, frase_semilla, estilo
        ),
        "cancion": lambda: prompt_letra_completa(
            tema, tipo_amor, mood, frase_semilla, estilo
        ),
    }

    return prompts.get(
        modo,
        lambda: prompt_explicacion(tema, tipo_amor, mood, frase_semilla),
    )()