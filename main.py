import ollama

# Inicializar el cliente Ollama. Victor Arbiol Martinez
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
        response = client.generate(model="llama3", prompt=prompt, options={'temperature': self.temperature})
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

# Definir la información de la búsqueda (esto en un escenario real vendría del usuario)
destino = "Madrid - Paris"
fecha_ida = "2024-12-15"
fecha_vuelta = "2024-12-20"

# Definir las tareas
tarea_vuelo = Task(
    description=f"Busca vuelo más barato a {destino} para {fecha_ida}/{fecha_vuelta}.",
    agent=agente_vuelos
)

tarea_hotel = Task(
    description=f"Busca hotel más barato para {fecha_ida}/{fecha_vuelta}.",
    agent=agente_hoteles
)

tarea_informe = Task(
    description="Genera un informe con la mejor opción de vuelo y hotel.",
    agent=agente_informes
)

tareas = [tarea_vuelo, tarea_hotel, tarea_informe]

# Simular la ejecución del equipo
resultados = {}
shared_info = {}  # Usaremos un diccionario para almacenar los resultados de cada agente
compartir = True  # Cambia a False para que los agentes trabajen de manera independiente

for tarea in tareas:
    resultado = tarea.agent.execute_task(tarea.description, shared_info)
    resultados[tarea.agent.role] = resultado
    if compartir:
        shared_info[tarea.agent.role] = resultado

# Mostrar los resultados
if compartir:
    print("\n--- Resultados Compartidos ---")
    for role, resultado in resultados.items():
        print(f"{role}: {resultado}")
else:
    print("\n--- Resultados Independientes ---")
    for role, resultado in resultados.items():
        print(f"{role}: {resultado}")