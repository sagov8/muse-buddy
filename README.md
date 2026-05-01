# 🎵 Muse Buddy

*Herramienta de apoyo creativo para compositores.*  
Guía al usuario desde una emoción hasta una frase semilla, y usa IA para generar versos, coros y títulos que sirvan de punto de partida para una canción.

---

## ¿Cómo funciona?

El flujo tiene cuatro pasos:

1. *Emoción* — Elige la emoción principal que quieres transmitir (ej. Amor, Tristeza).
2. *Aspecto* — Selecciona qué tipo o aspecto de esa emoción quieres explorar (ej. Romántico, Platónico).
3. *Tono* — Define el matiz o tono emocional (ej. Apasionado, Tierno, Tormentoso).
4. *Frase semilla* — Elige la frase que más se acerca a lo que sientes. Desde ahí, la IA genera contenido creativo.

---

## Funcionalidades de IA

Desde la frase semilla seleccionada puedes:

- Explicar la emoción detrás de la frase
- Generar versos, coro o títulos
- Reescribir en distintos estilos (poético, íntimo, comercial, melancólico, minimalista)
- Mejorar o continuar una letra en el editor integrado

---

## Estructura del proyecto


muse-buddy/
├── main.py                        # Entrada principal de la app (Flet)
├── models/
│   └── app_state.py               # Estado de navegación del árbol
├── services/
│   ├── ai_service.py              # Prompts y llamadas a la IA
│   └── clipboard_service.py       # Copiar texto al portapapeles
├── ui/
│   ├── components/
│   │   ├── header.py              # Encabezado de la app
│   │   └── breadcrumb.py          # Navegación de migas de pan
│   └── views/
│       ├── emotion_view.py        # Pantalla de selección de emoción
│       ├── node_view.py           # Pantalla de categorías, tonos y semillas
│       └── leaf_view.py           # Pantalla de trabajo con la frase semilla
└── utils/
    ├── data_loader.py             # Carga y listado de árboles JSON
    └── arboles/
        ├── amor_tree.json         # Árbol de emociones: Amor
        └── tristeza_tree.json     # Árbol de emociones: Tristeza


---

## Agregar nuevas emociones

Basta con crear un nuevo archivo JSON en utils/arboles/ siguiendo la misma estructura de los existentes. La app lo detecta automáticamente al iniciar.

Estructura básica:

json
{
  "valor": "Alegría",
  "tipo": "tema",
  "descripcion": "Descripción de la emoción",
  "icon": "☀️",
  "hijos": [
    {
      "valor": "Categoría",
      "tipo": "categoria",
      "descripcion": "...",
      "icon": "◆",
      "hijos": [
        {
          "valor": "Tono",
          "tipo": "mood",
          "descripcion": "...",
          "icon": "◇",
          "hijos": [
            { "valor": "Frase semilla aquí", "tipo": "seed", "subtipo": "metáfora" }
          ]
        }
      ]
    }
  ]
}


---

## Requisitos

- Python 3.10+
- [Flet](https://flet.dev/) — pip install flet
- Acceso a la API de IA configurada en services/ai_service.py

## Ejecutar

bash
python main.py