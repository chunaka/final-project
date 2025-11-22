# 🧩 OS-Simulator

Simulador modular de un sistema operativo en Python. Modela procesos, planificación, gestión de recursos y sistema de archivos con una arquitectura extensible.

## 🎯 Características Destacadas

- ✅ **Context Switching**: Implementación completa del cambio de contexto entre procesos
- ✅ **Tres Schedulers**: FCFS, SJF y Round Robin completamente funcionales
- ✅ **Interfaz Mejorada**: UI de consola con navegación clara y limpieza de pantalla
- ✅ **Métricas Detalladas**: Seguimiento de context switches, tiempos de espera y throughput
- ✅ **Sistema de Archivos**: Gestión completa de archivos con permisos y usuarios

## 🧱 Estructura actual del proyecto

```
os-simulator/
├── models/
│   ├── __init__.py
│   ├── pcb.py                # Process Control Block
│   ├── process.py            # High-level process wrapper
│   └── process_manager.py    # Process lifecycle management + context_switch
│
├── schedulers/
│   ├── __init__.py
│   ├── scheduler_base.py     # Base scheduler con ProcessManager
│   ├── fcfs.py               # First Come First Served
│   ├── sjf.py                # Shortest Job First
│   └── round_robin.py        # Round Robin (preemptive)
│
├── ui/
│   ├── __init__.py
│   ├── console.py            # Enhanced console interface
│   └── gui.py                # Interfaz gráfica (Pendiente)
│
├── filesystem/
│   ├── __init__.py
│   ├── node.py               # Nodos del sistema de archivos
│   ├── file_system.py        # Sistema de archivos
│   ├── permissions.py        # Gestión de permisos
│   ├── user.py               # Gestión de usuarios
│   └── commands.py           # Comandos del sistema
│
├── utils/
├── tests/
│   ├── test_processes.py
│   └── processes_example.txt # Archivo de prueba
│
├── main.py
├── requirements.txt
└── README.md
```

## ⚙️ Estado del desarrollo

### Gestión de procesos y scheduling

| Módulo | Estado | Características |
|--------|--------|----------------|
| PCB | ✅ | Control block completo con métricas |
| Process | ✅ | Wrapper de alto nivel con estados |
| ProcessManager | ✅ | **Con context_switch y tracking** |
| SchedulerBase | ✅ | Integración con ProcessManager |
| FCFS | ✅ | No preemptivo, usa context_switch |
| SJF | ✅ | No preemptivo, selección por burst time |
| Round Robin | ✅ | **Preemptivo con quantum configurable** |

### Sistema de archivos

| Módulo | Estado |
|--------|--------|
| Node | ✅ |
| FileSystem | ✅ |
| Permissions | ✅ |
| User | ✅ |
| Commands | ✅ |

### Interfaz de usuario

| Elemento | Estado | Características |
|----------|--------|----------------|
| `main.py` | ✅ | Selección de scheduler con validación |
| `ui/console.py` | ✅ | **UI mejorada con headers y limpieza** |
| `ui/gui.py` | ⚙️ | Interfaz gráfica (Pendiente) |
| Carga desde archivo | ✅ | Formato CSV con validación |
| Timeline visual | ✅ | Diagrama de Gantt con barras Unicode |
| Métricas | ✅ | **Incluye contador de context switches** |

## 📘 Módulos principales

### 📌 ProcessManager

**Gestión centralizada de procesos con context switching:**

```python
# Métodos principales
- create_process(pid, burst_time, arrival_time, priority, user)
- context_switch()              # ⭐ Cambio de contexto entre procesos
- execute_current(time_units)   # Ejecuta proceso actual
- terminate_current_process(current_time)
- has_ready_processes()         # Verifica ready_queue
- context_switch_count()        # ⭐ Contador de switches
- load_from_file(filepath)      # Carga desde archivo
```

**Características clave:**
- Gestión de colas (ready, blocked, terminated)
- Tracking automático de context switches
- Manejo de estados de procesos

### 📌 FCFS Scheduler

**First Come First Served - No preemptivo:**

- Ordena procesos por tiempo de llegada
- **Usa `context_switch()` para cada proceso**
- Maneja períodos de inactividad (idle time)
- Calcula métricas: waiting time, turnaround time, throughput

**Context switches esperados:** 1 por proceso (N procesos = N switches)

### 📌 SJF Scheduler

**Shortest Job First - No preemptivo:**

- Selecciona el proceso con menor burst time disponible
- **Usa `context_switch()` para cada proceso**
- Reordena ready_queue por burst time dinámicamente
- Optimiza tiempo promedio de espera

**Context switches esperados:** 1 por proceso (N procesos = N switches)

### 📌 Round Robin Scheduler

**Round Robin - Preemptivo con quantum:**

- **Caso de uso ideal para context_switch**
- Quantum configurable (default: 2)
- Reencolación automática de procesos no completados
- **Múltiples context switches por proceso**

**Context switches esperados:** Significativamente > N (depende del quantum)

**Ejemplo con quantum=2:**
```
P1 (burst=5): ejecuta 2 → switch → ejecuta 2 → switch → ejecuta 1 ✓
P2 (burst=3): ejecuta 2 → switch → ejecuta 1 ✓
P3 (burst=8): ejecuta 2 → switch → ejecuta 2 → switch → ...
```

### 📌 Console UI (`ui/console.py`)

**Interfaz mejorada con:**

- ✅ Limpieza de pantalla entre operaciones
- ✅ Headers formateados para cada sección
- ✅ Separadores visuales claros
- ✅ Pausas para revisar resultados
- ✅ Mensajes con formato `[OK]`, `[ERROR]`, `[INFO]`

**Funcionalidades:**

1. **Cargar procesos**: Desde archivo con vista previa
2. **Ejecutar scheduler**: Con reporte de context switches
3. **Timeline visual**: Diagrama de Gantt con Unicode
4. **Métricas detalladas**: Por proceso y promedio global

**Ejemplo de Timeline:**
```
Diagrama de Gantt:

  P1 │█████│ [ 0 → 5] (5 unidades)
  P2 │███│ [ 5 → 8] (3 unidades)
  P3 │████████│ [ 8 → 16] (8 unidades)
```

**Ejemplo de ejecución:**
```
[OK] Scheduler ejecutado exitosamente
[INFO] Context switches realizados: 9
```

### 📌 Sistema de Archivos (`filesystem/`)

Implementación completa de sistema de archivos:

- **Node**: Estructura de archivo/directorio con metadatos
- **FileSystem**: Operaciones CRUD sobre archivos y directorios
- **Permissions**: Sistema de permisos (lectura, escritura, ejecución)
- **User**: Gestión de usuarios y propietarios
- **Commands**: Comandos del sistema (ls, cd, mkdir, etc.)

## 🧪 Pruebas

### Archivo de prueba

`tests/processes_example.txt`:
```
# pid,arrival,burst,priority,user
1,0,5,0,alice
2,1,3,1,bob
3,2,8,0,root
```

### Resultados esperados

| Scheduler | Context Switches | Observación |
|-----------|------------------|-------------|
| FCFS | 3 | 1 por proceso |
| SJF | 3 | 1 por proceso |
| Round Robin (q=2) | 9 | Múltiples por preemption |

## 🚀 Uso

```bash
# Activar entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar simulador
python main.py
```

**Flujo de uso:**
1. Seleccionar scheduler (FCFS, SJF o Round Robin)
2. Si es Round Robin, especificar quantum
3. Cargar procesos desde archivo
4. Ejecutar scheduler
5. Ver timeline y métricas

## 📊 Métricas Calculadas

- **Waiting Time**: Tiempo desde llegada hasta primera ejecución
- **Turnaround Time**: Tiempo total desde llegada hasta finalización
- **Throughput**: Procesos completados por unidad de tiempo
- **Context Switches**: ⭐ Número total de cambios de contexto

## 🔄 Arquitectura de Context Switching

```
ProcessManager
    ├── context_switch()
    │   ├── Guarda proceso actual → ready_queue (si no terminado)
    │   ├── Toma siguiente de ready_queue
    │   ├── Cambia estados (READY → RUNNING)
    │   └── Incrementa contador
    │
    └── Usado por todos los schedulers:
        ├── FCFS: 1 switch por proceso
        ├── SJF: 1 switch por proceso
        └── Round Robin: múltiples switches (preemptivo)
```

## 🎓 Características Educativas

Este simulador demuestra:

- **Diferencia entre schedulers no preemptivos y preemptivos**
- **Impacto del quantum en Round Robin**
- **Costo del context switching** (visible en el contador)
- **Métricas de rendimiento** de diferentes algoritmos
- **Arquitectura modular** para sistemas operativos

## 📝 Próximos pasos

- [ ] Interfaz gráfica (GUI)
- [ ] Scheduler de prioridad con preemption
- [ ] Multilevel feedback queue
- [ ] Gestión de memoria
- [ ] Simulación de I/O blocking