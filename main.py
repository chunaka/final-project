import os
from ui.console import ConsoleUI
from schedulers.fcfs import FCFSScheduler
from schedulers.sjf import SJFScheduler
from schedulers.round_robin import RoundRobinScheduler

def clear_screen():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Imprime el encabezado principal"""
    clear_screen()
    print("=" * 60)
    print(" SIMULADOR DE PLANIFICACIÓN DE PROCESOS ".center(60, "="))
    print("=" * 60)

def main():
    schedulers = {
        "1": FCFSScheduler,
        "2": SJFScheduler,
        "3": RoundRobinScheduler
    }
    
    scheduler_names = {
        "1": "FCFS (First Come First Served)",
        "2": "SJF (Shortest Job First)",
        "3": "Round Robin"
    }
    
    # Solicitar selección del usuario
    while True:
        print_header()
        print("\nSeleccione el algoritmo de planificación:")
        print()
        print("  1. FCFS (First Come First Served)")
        print("  2. SJF (Shortest Job First)")
        print("  3. Round Robin")
        print()
        print("-" * 60)
        
        choice = input("\nIngrese su opción (1-3): ").strip()
        
        if choice in schedulers:
            selected_scheduler_class = schedulers[choice]
            scheduler_name = scheduler_names[choice]
            
            # Si es Round Robin, solicitar quantum
            if choice == "3":
                while True:
                    try:
                        print()
                        quantum = int(input("Ingrese el quantum de tiempo (default: 2): ").strip() or "2")
                        if quantum > 0:
                            # Create a wrapper that accepts process_manager as keyword argument
                            selected_scheduler = lambda process_manager: selected_scheduler_class(process_manager=process_manager, quantum=quantum)
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
            print(f"\n[ERROR] Opción inválida: {choice}")
            input("\nPresiona Enter para intentar nuevamente...")
    
    ui = ConsoleUI(selected_scheduler)

    while True:
        option = ui.show_menu()
        
        if option == "1":
            clear_screen()
            print("=" * 60)
            print(" CARGAR PROCESOS ".center(60, "="))
            print("=" * 60)
            print()
            path = input("Ruta del archivo: ")
            ui.load_processes(path)

        elif option == "2":
            ui.run_scheduler()
            
        elif option == "3":
            ui.show_results()

        elif option == "4":
            ui.show_metrics()

        elif option == "5":
            clear_screen()
            break

        else:
            print(f"\n[ERROR] Opción inválida: {option}")
            input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()