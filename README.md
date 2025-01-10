# Agencia_de_Viajes

Esto es un ejemplo de como usar tres agentes de IA, en una agencia de viajes, esta aplicación al cual no es profesional, solo un toy un juguete.

![image](https://github.com/user-attachments/assets/d2127594-af57-4965-b748-4af76b9be0ac)


# Multi-Agent Framework for Automated Task Execution with LLMs

This project demonstrates a multi-agent framework for utilizing LLMs to solve real-world problems in an orchestrated manner. The example provided focuses on travel planning, where agents search for the best flight and hotel deals, and generate a consolidated report. Each agent operates independently or can share information collaboratively to achieve better outcomes.

## Features

- **Modular Agent Design**: Each agent has a defined role, goal, and backstory, making it highly customizable.
- **LLM Integration**: Uses `ollama.Client` to interact with LLM models, allowing flexible and creative responses.
- **Temperature Tuning**: Each agent's response creativity is controlled by a `temperature` parameter.
- **Data-Driven**: Agents can read from external data files to enhance their outputs.
- **Information Sharing**: Agents can work collaboratively, sharing insights to optimize results.
- **Error Handling**: Includes robust exception handling for file operations and API calls.

## Prerequisites

1. **Ollama Client**: Install the Ollama client and ensure it is running locally.
   - [Ollama Installation Guide](https://ollama.com)
2. **Python**: Requires Python 3.7 or higher.
3. **Dependencies**: Install dependencies via pip:
   ```bash
   pip install ollama
   ```



# Project Structure

Agents: Encapsulate logic for specific tasks, e.g., searching for flights or hotels.
Tasks: Define descriptions and assign them to appropriate agents.
Data Files: Optional external data (vuelos.txt, hoteles.txt) for enhancing agent operations.

## How It Works

### Initialization

Agents are instantiated with unique roles, goals, and configurations:

```python

agente_vuelos = Agent(
    role="Agente de Búsqueda de Vuelos",
    goal="Encontrar el vuelo más barato disponible y notificar la mejor opción: vuelo, precio.",
    backstory="Especialista en precios de vuelos económicos.",
    data_file="vuelos.txt",
    temperature=0.2
)
Task Execution
Tasks are defined with a description and assigned to agents:
```

```python
tarea_vuelo = Task(
    description="Busca vuelo más barato a Madrid - Paris para 2024-12-15/2024-12-20.",
    agent=agente_vuelos
)
```

The agent executes the task using the LLM, optionally incorporating shared information:

```python
resultado = tarea.agent.execute_task(tarea.description, shared_info)
```

Collaborative Workflow
Agents share results to improve subsequent outputs:

```python
shared_info[agente_vuelos.role] = resultado
```

Output
Results are displayed at the end of execution:

```python
print("\n--- Resultados Compartidos ---")
for role, resultado in resultados.items():
    print(f"{role}: {resultado}")
```

# Example Use Case: Travel Planning
## This example simulates planning a trip from Madrid to Paris:

Flight Search: Finds the cheapest flight for the given dates.
Hotel Search: Finds the cheapest hotel for the stay.
Report Generation: Combines the best options into a concise travel report

