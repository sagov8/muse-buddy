import json
import urllib.request
import urllib.error


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:mini"


def generar_texto(prompt: str) -> str:
    data = json.dumps(
        {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("response", "No se recibió respuesta del modelo.")
    except urllib.error.URLError as e:
        return f"Error conectando con Ollama: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"


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
Eres un asistente creativo para compositores en español.

{contexto}

Tarea:
1. Explica la emoción central de esta idea en 1 o 2 párrafos.
2. Describe qué tipo de canción podría nacer de esta frase.
3. Señala imágenes, símbolos o metáforas que podrían desarrollarse.

Responde en español, de forma clara, poética y útil.
""".strip()


def prompt_versos(tema: str, categoria: str, mood: str, frase_semilla: str) -> str:
    contexto = construir_contexto(tema, categoria, mood, frase_semilla)
    return f"""
Eres un compositor asistente.

{contexto}

Tarea:
Escribe 6 versos originales inspirados en la frase semilla.
Condiciones:
- Deben sonar naturales y poéticos
- No repitas exactamente la frase semilla
- Mantén coherencia emocional con la categoría y el tono
- Evita clichés muy obvios

Responde solo con los 6 versos, uno por línea.
""".strip()


def prompt_coro(tema: str, categoria: str, mood: str, frase_semilla: str) -> str:
    contexto = construir_contexto(tema, categoria, mood, frase_semilla)
    return f"""
Eres un compositor asistente.

{contexto}

Tarea:
Escribe 1 coro corto para una canción.
Condiciones:
- Máximo 4 líneas
- Debe ser memorable
- Debe tener lenguaje emocional y cantable
- Inspirado en la frase semilla

Responde solo con el coro.
""".strip()


def prompt_titulos(tema: str, categoria: str, mood: str, frase_semilla: str) -> str:
    contexto = construir_contexto(tema, categoria, mood, frase_semilla)
    return f"""
Eres un asistente creativo para canciones.

{contexto}

Tarea:
Genera 10 posibles títulos de canción en español.
Condiciones:
- Deben sonar artísticos y memorables
- Mezcla opciones directas y metafóricas
- No uses numeración excesiva ni explicación larga

Responde con una lista simple de 10 títulos.
""".strip()


def prompt_reescritura(
    tema: str, categoria: str, mood: str, frase_semilla: str, estilo: str
) -> str:
    contexto = construir_contexto(tema, categoria, mood, frase_semilla)
    return f"""
Eres un asistente creativo para compositores.

{contexto}

Tarea:
Reescribe la frase semilla en estilo "{estilo}".
Genera 5 variaciones.

Condiciones:
- Conserva la emoción principal
- Cada variación debe sentirse distinta
- Que suenen como posibles líneas de canción

Responde con 5 opciones, una por línea.
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

    if modo == "explicacion":
        return prompt_explicacion(tema, tipo_amor, mood, frase_semilla)
    if modo == "versos":
        return prompt_versos(tema, tipo_amor, mood, frase_semilla)
    if modo == "coro":
        return prompt_coro(tema, tipo_amor, mood, frase_semilla)
    if modo == "titulos":
        return prompt_titulos(tema, tipo_amor, mood, frase_semilla)
    if modo == "reescritura":
        return prompt_reescritura(tema, tipo_amor, mood, frase_semilla, estilo)

    return prompt_explicacion(tema, tipo_amor, mood, frase_semilla)

def prompt_mejorar_letra(letra: str, tema: str, categoria: str, mood: str) -> str:
    return f"""
Eres un asistente experto en composición de canciones en español.

Tema principal: {tema}
Categoría emocional: {categoria}
Matiz o tono: {mood}

Letra actual:
\"\"\"
{letra}
\"\"\"

Tarea:
1. Mejora esta letra manteniendo su intención emocional.
2. Hazla más fluida, poética y cantable.
3. Conserva la idea principal, pero mejora imágenes, ritmo y fuerza expresiva.
4. No expliques cambios: devuelve solo la letra mejorada.

Responde en español.
""".strip()


def prompt_continuar_letra(letra: str, tema: str, categoria: str, mood: str) -> str:
    return f"""
Eres un asistente experto en composición de canciones en español.

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
- Mantén coherencia emocional y estilística
- No repitas lo ya escrito
- Haz que pueda servir como siguiente estrofa o desarrollo

Devuelve solo las nuevas líneas.
""".strip()