import os
import json
import urllib.request

# Obtener la API Key desde las variables de entorno de GitHub
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("Error: No se encontró la GEMINI_API_KEY en las variables de entorno.")
    exit(1)

# Archivo de base de datos
FILE_PATH = "proyectos.json"

def cargar_proyectos():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def guardar_proyectos(proyectos):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(proyectos, f, ensure_ascii=False, indent=2)

def generar_nuevo_proyecto():
    # URL oficial de la API de Gemini usando REST
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    prompt = """
    Genera un nuevo proyecto o recurso útil en español para una comunidad web.
    Debe pertenecer a una de estas 4 categorías exactamente: 'finanzas', 'tecnologia', 'autoayuda', 'recursos'.
    
    Responde ÚNICAMENTE con un objeto JSON válido con la siguiente estructura (sin bloques markdown de código ```json, solo texto llano):
    {
      "titulo": "Título atractivo del recurso",
      "descripcion": "Una breve descripción explicativa de 2 a 3 oraciones.",
      "categoria": "tecnologia",
      "tipo": "gratis",
      "precio": 0,
      "bloqueado": "",
      "link": "[https://github.com](https://github.com)"
    }
    """

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            text_response = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
            
            # Limpiar posible formato Markdown si Gemini lo incluye
            if text_response.startswith("```"):
                lines = text_response.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                text_response = "\n".join(lines).strip()

            nuevo_item = json.loads(text_response)
            return nuevo_item
    except Exception as e:
        print(f"Error al llamar a Gemini API: {e}")
        return None

def main():
    proyectos = cargar_proyectos()
    print(f"Proyectos actuales: {len(proyectos)}")
    
    nuevo_proyecto = generar_nuevo_proyecto()
    if nuevo_proyecto:
        # Agregar el nuevo proyecto al principio de la lista
        proyectos.insert(0, nuevo_proyecto)
        # Mantener solo los últimos 20 proyectos para no sobrecargar el archivo
        proyectos = proyectos[:20]
        guardar_proyectos(proyectos)
        print("¡Nuevo proyecto generado e insertado con éxito!")
    else:
        print("No se pudo generar un nuevo proyecto.")

if __name__ == "__main__":
    main()
