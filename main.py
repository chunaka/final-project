from ui.console import ConsoleUI
from schedulers.fcfs import FCFSScheduler
from schedulers.sjf import SJFScheduler
from schedulers.round_robin import RoundRobinScheduler

def main():
    # Mostrar menú de selección de scheduler
    print("=" * 50)
    print("SIMULADOR DE PLANIFICACIÓN DE PROCESOS")
    print("=" * 50)
    print("\nSeleccione el algoritmo de planificación:")
    print("1. FCFS (First Come First Served)")
    print("2. SJF (Shortest Job First)")
    print("3. Round Robin")
    print("=" * 50)
    
    schedulers = {
        "1": FCFSScheduler,
        "2": SJFScheduler,
        "3": RoundRobinScheduler
    }
    
    scheduler_names = {
        "1": "FCFS",
        "2": "SJF",
        "3": "Round Robin"
    }
    
    # Solicitar selección del usuario
    while True:
        choice = input("\nIngrese su opción (1-3): ").strip()
        if choice in schedulers:
            selected_scheduler_class = schedulers[choice]
            scheduler_name = scheduler_names[choice]
            
            # Si es Round Robin, solicitar quantum
            if choice == "3":
                while True:
                    try:
                        quantum = int(input("Ingrese el quantum de tiempo (default: 2): ").strip() or "2")
                        if quantum > 0:
                            selected_scheduler = lambda: selected_scheduler_class(quantum=quantum)
                            break
                        else:
                            print("[ERROR] El quantum debe ser mayor a 0")
                    except ValueError:
                        print("[ERROR] Ingrese un número entero válido")
            else:
                selected_scheduler = selected_scheduler_class
            
            print(f"\n[OK] Scheduler seleccionado: {scheduler_name}\n")
            break
        else:
            print(f"[ERROR] Opción inválida: {choice}")
    
    ui = ConsoleUI(selected_scheduler)

    while True:
        option = ui.show_menu()
        
        if option == "1":
            path = input("Ruta del archivo: ")
            ui.load_processes(path)

        elif option == "2":
            ui.run_scheduler()
            
        elif option == "3":
            ui.show_results()

        elif option == "4":
            ui.show_metrics()

        elif option == "5":
            print("Saliendo...")
            break

        else:
            print(f"[ERROR] Opción inválida: {option}")

if __name__ == "__main__":
    main()