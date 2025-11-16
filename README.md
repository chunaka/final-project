# 🧩 OS-Simulator

Simulador modular de un sistema operativo en Python.  
El proyecto modela componentes reales de un SO: procesos, planificación y gestión de recursos, con un enfoque modular y extensible

## 🧱 Estructura actual del proyecto

```
os-simulator/
├── models/
│   ├── pcb.py                # Process Control Block
│   ├── process.py            # Lógica de procesos
│   ├── process_manager.py    # Gestor de colas y estados
│
├── schedulers/
│   ├── scheduler_base.py     # Clase base para planificadores
│   ├── fcfs.py               # First-Come, First-Served
│   ├── round_robin.py        # (Pendiente)
│   ├── sjf.py                # (Pendiente)
│
├── filesystem/               # (Pendiente)
├── ui/                       # (Pendiente)
├── utils/                    # Utilidades
├── tests/                    # Pruebas unitarias
└── README.md
```

## ⚙️ Estado del desarrollo


### Sprint 1 — Gestión básica de procesos

| Módulo | Estado | Resumen |
|--------|--------|---------|
| PCB | ✅ Completado | Información de control del proceso (PID, estado, tiempos, prioridad). |
| Process | ✅ Completado | Lógica de ejecución, cambios de estado y métricas. |
| ProcessManager | ⚙️ MVP Listo | Maneja colas READY/BLOCKED/TERMINATED y cambio de contexto básico. |
| SchedulerBase | ✅ Completado | Plantilla para algoritmos de planificación. |
| FCFSScheduler | ✅ Completado | Implementa FCFS, timeline y métricas. |

## 📘 Módulos implementados

### 📌 PCB (models/pcb.py)

Estructura que almacena:

- PID
- Estado del proceso
- Program counter
- Arrival / Burst / Remaining time
- Prioridad
- Métricas: turnaround, waiting, response


### 📌 Process (models/process.py)

Capa lógica sobre el PCB:

- Cambio de estado
- Ejecución simulada (`execute()`)
- Actualización de tiempos
- Detección de finalización


### 📌 ProcessManager (models/process_manager.py)

MVP funcional con:

- READY queue
- BLOCKED queue
- TERMINATED list
- Proceso en CPU
- Creación de procesos
- Cambio de contexto simple
- Bloqueo/desbloqueo


### 📌 Scheduler Base (schedulers/scheduler_base.py)

Define la interfaz estándar:

- `add_process()`
- `run()`
- `compute_metrics()`
- Registro de timeline
- Lista de procesos


### 📌 FCFS Scheduler (schedulers/fcfs.py)

Implementación completa de **First-Come, First-Served**:

- Ordena por arrival time
- Ejecuta sin interrupciones
- Registra (inicio, fin) de cada proceso

**Métricas:**
- Average waiting time
- Average turnaround time
- Throughput

## 🧪 Pruebas disponibles

**Ubicación:** `tests/test_processes.py`

```python
procesos_test1 = [
    {"pid": 1, "llegada": 0, "rafaga": 5, "usuario": "usuario1"},
    {"pid": 2, "llegada": 1, "rafaga": 3, "usuario": "usuario2"}
]
```

Pruebas iniciales para validar creación y transición básica de procesos.