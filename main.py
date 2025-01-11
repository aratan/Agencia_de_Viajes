import gradio as gr
import ollama

# Inicializar el cliente Ollama
client = ollama.Client(host='http://localhost:11434')

class Agent:
    def __init__(self, role, goal, backstory, data_file=None, verbose=False, temperature=0.7):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.data_file = data_file
        self.verbose = verbose
        self.temperature = temperature  # Añadido parámetro de temperatura

    def execute_task(self, task_description, shared_info=None):
        print(f"[{self.role}] Ejecutando tarea: {task_description}")
        data = self._read_data()
        if data:
            print(f"[{self.role}] Datos leídos desde {self.data_file}: {data}")

        prompt_parts = []
        if data:
            prompt_parts.append(f"Basado en la siguiente información: {data}.")
        if shared_info:
            prompt_parts.append(f"Información compartida: {shared_info}.")
        prompt_parts.append(task_description)
        prompt = " ".join(prompt_parts)

        # Añadida la temperatura al generar el texto usando 'options'
        response = client.generate(model="falcon3:10b", prompt=prompt, options={'temperature': self.temperature})
        return response['response'].strip()

    def _read_data(self):
        print(f"[{self.role}] Intentando leer datos desde: {self.data_file}")
        if self.data_file:
            try:
                with open(self.data_file, "r") as f:
                    data = f.read()
                    print(f"[{self.role}] Lectura exitosa de {self.data_file}.")
                    return data
            except FileNotFoundError:
                print(f"[{self.role}] Error: No se encontró el archivo {self.data_file}.")
                return None
            except Exception as e:
                print(f"[{self.role}] Error al leer {self.data_file}: {e}")
                return None
        else:
            print(f"[{self.role}] No se especificó archivo de datos.")
            return None

class Task:
    def __init__(self, description, agent):
        self.description = description
        self.agent = agent

# Definir los agentes con temperatura personalizada
agente_vuelos = Agent(
    role="Agente de Búsqueda de Vuelos",
    goal="Encontrar el vuelo más barato disponible y notificar la mejor opción: vuelo, precio.",
    backstory="Especialista en precios de vuelos económicos.",
    data_file="vuelos.txt",
    verbose=False,
    temperature=0.2  # Ejemplo: menos creativo, más preciso
)

agente_hoteles = Agent(
    role="Agente de Búsqueda de Hoteles",
    goal="Encontrar el hotel más barato disponible y notificar la mejor opcion: Hotel, precio.",
    backstory="Especialista en precios de hoteles económicos.",
    data_file="hoteles.txt",
    verbose=False,
    temperature=0.8  # Ejemplo: más creativo, menos predecible
)

# Nuevo agente para generar el informe
agente_informes = Agent(
    role="Agente de Informes de Viaje",
    goal="Generar un informe conciso con la mejor oferta de vuelo y hotel.",
    backstory="Especialista en consolidar información de viajes.",
    verbose=True,
    temperature=0.5  # Temperatura para el informe
)

agentes = [agente_vuelos, agente_hoteles, agente_informes]

def ejecutar_busqueda(pregunta, fecha_ida_str, fecha_vuelta_str):
    resultados = {}
    shared_info = {}
    compartir = True

    # Definir las tareas utilizando la información del usuario
    tarea_vuelo = Task(
        description=f"Basado en la pregunta: '{pregunta}'. Busca vuelo más barato para el destino en la pregunta para {fecha_ida_str}/{fecha_vuelta_str}.",
        agent=agente_vuelos
    )

    tarea_hotel = Task(
        description=f"Basado en la pregunta: '{pregunta}'. Busca hotel más barato para las fechas {fecha_ida_str}/{fecha_vuelta_str}.",
        agent=agente_hoteles
    )

    tarea_informe = Task(
        description=f"Basado en la pregunta: '{pregunta}'. Genera un informe con la mejor opción de vuelo y hotel para las fechas {fecha_ida_str}/{fecha_vuelta_str}.",
        agent=agente_informes
    )

    tareas = [tarea_vuelo, tarea_hotel, tarea_informe]

    for tarea in tareas:
        resultado = tarea.agent.execute_task(tarea.description, shared_info)
        resultados[tarea.agent.role] = resultado
        if compartir:
            shared_info[tarea.agent.role] = resultado

    # Formatear los resultados para la interfaz de Gradio en Markdown con estilos
    output_text = """
    <div style='font-family: Arial, sans-serif; color: #333; line-height: 1.6;'>
        <h2 style='color: #0056b3; border-bottom: 2px solid #0056b3; padding-bottom: 5px; margin-bottom: 20px;'>
            Resumen de tu Viaje
        </h2>
        <p style='margin-bottom: 10px;'>A continuación, encontrarás las mejores opciones encontradas para tu viaje:</p>
        <div style='background-color: #f9f9f9; padding: 15px; border-left: 5px solid #007bff; margin-bottom: 15px;'>
            <h3 style='color: #007bff; margin-top: 0;'>
                <i class="fas fa-plane" style='margin-right: 5px;'></i> Mejor Opción de Vuelo
            </h3>
            <p><strong>Información:</strong> <span style='color: #555;'>{agente_vuelos_resultado}</span></p>
        </div>
        <div style='background-color: #f9f9f9; padding: 15px; border-left: 5px solid #28a745; margin-bottom: 15px;'>
            <h3 style='color: #28a745; margin-top: 0;'>
                <i class="fas fa-hotel" style='margin-right: 5px;'></i> Mejor Opción de Hotel
            </h3>
            <p><strong>Información:</strong> <span style='color: #555;'>{agente_hoteles_resultado}</span></p>
        </div>
        <div style='margin-top: 20px; padding: 15px; background-color: #e8f0fe; border-radius: 5px;'>
            <h4 style='color: #0056b3;'>Informe Adicional</h4>
            <p style='color: #555;'>{agente_informes_resultado}</p>
        </div>
        <p style='font-size: 0.9em; color: #777; margin-top: 20px;'>
            ¡Esperamos que esta información te sea útil para planificar tu viaje!
        </p>
    </div>
    """.format(
        agente_vuelos_resultado=resultados.get("Agente de Búsqueda de Vuelos", "No se encontraron resultados."),
        agente_hoteles_resultado=resultados.get("Agente de Búsqueda de Hoteles", "No se encontraron resultados."),
        agente_informes_resultado=resultados.get("Agente de Informes de Viaje", "No se generó informe.")
    )

    return output_text

if __name__ == "__main__":
    custom_css = """
    body,
    .gradio-container {
        background-color: white !important;
        color: black !important;
    }
    .sidebar {
        background-color: white !important;
    }
    .form,
    .output {
        background-color: #f0f0f0 !important; /* Gris claro */
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }
    """
    iface = gr.Interface(
        fn=ejecutar_busqueda,
        inputs=[
            gr.Textbox(label="Pregunta sobre tu viaje (ej. Quiero viajar de Madrid a Paris)", lines=2),
            gr.Textbox(label="Fecha de ida (YYYY-MM-DD)", placeholder="YYYY-MM-DD"),
            gr.Textbox(label="Fecha de vuelta (YYYY-MM-DD)", placeholder="YYYY-MM-DD")
        ],
        outputs=gr.Markdown(label="Resultados de la búsqueda"),
        title="<h1 style='color: #007bff; text-align: center;'>Tu Asistente de Viajes Personalizado</h1>",
        description="""
        <div style='text-align: center;'>
            <img src="https://tse2.mm.bing.net/th?id=OIP.KySxO7qdx-aFE-IZ8hBgSQHaE-&rs=1&pid=ImgDetMain" style="display: block; margin-left: auto; margin-right: auto; width: 25%; height: 25%;">
        </div>
        <div style='text-align: center;'>
            Bienvenido a tu agente de búsqueda de viajes. Introduce tu destino y fechas de viaje para encontrar las mejores ofertas en vuelos y hoteles.
        </div>
        """,
        head=f"<style>{custom_css}</style>"
    )
    iface.launch()
