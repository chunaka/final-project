import os
from ui.console import ConsoleUI
from schedulers.fcfs import FCFSScheduler
from schedulers.sjf import SJFScheduler
from schedulers.round_robin import RoundRobinScheduler
from filesystem.commands import FileSystemCLI, create_demo_filesystem

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_main_header():
    clear_screen()
    print("=" * 60)
    print(" SIMULADOR DE SISTEMA OPERATIVO ".center(60, "="))
    print("=" * 60)

def show_main_menu():
    print_main_header()
    print("\nSELECCIONE UN MÓDULO:")
    print()
    print("  1. Planificación de Procesos (Schedulers)")
    print("  2. Sistema de Archivos")
    print("  3. Salir")
    print()
    print("-" * 60)
    return input("\nIngrese su opción (1-3): ").strip()

def run_scheduler_module():
    clear_screen()
    print("=" * 60)
    print(" PLANIFICACIÓN DE PROCESOS ".center(60, "="))
    print("=" * 60)
    
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
    
    while True:
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
            
            if choice == "3":
                while True:
                    try:
                        print()
                        quantum = int(input("Ingrese el quantum de tiempo (default: 2): ").strip() or "2")
                        if quantum > 0:
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
            print("\n[INFO] Volviendo al menú principal...\n")
            break

        else:
            print(f"\n[ERROR] Opción inválida: {option}")
            input("\nPresiona Enter para continuar...")

def run_filesystem_module():
    """Ejecuta el módulo de sistema de archivos"""
    clear_screen()
    print("=" * 60)
    print(" SISTEMA DE ARCHIVOS ".center(60, "="))
    print("=" * 60)
    print()
    print("¿Cómo desea inicializar el sistema de archivos?")
    print()
    print("  1. Cargar desde archivo de configuración")
    print("  2. Usar estructura de demostración")
    print()
    print("-" * 60)
    
    choice = input("\nIngrese su opción (1-2): ").strip()
    
    if choice == "1":
        # Cargar desde archivo
        from filesystem.loader import load_filesystem_from_file
        
        print()
        path = input("Ruta del archivo de configuración: ").strip()
        
        try:
            print(f"\n[INFO] Cargando sistema de archivos desde {path}...\n")
            fs = load_filesystem_from_file(path)
            print("\n[OK] Sistema de archivos cargado exitosamente\n")
        except Exception as e:
            print(f"\n[ERROR] No se pudo cargar el archivo: {e}")
            print("[INFO] Usando estructura de demostración...\n")
            fs = create_demo_filesystem()
    else:
        # Usar demo
        print()
        print("[INFO] Creando sistema de archivos con usuarios demo...")
        print()
        fs = create_demo_filesystem()
    
    # Ejecutar CLI del filesystem
    cli = FileSystemCLI(fs)
    cli.run()
    
    clear_screen()
    print("\n[INFO] Volviendo al menú principal...\n")

def main():
    while True:
        choice = show_main_menu()
        
        if choice == "1":
            run_scheduler_module()
        
        elif choice == "2":
            run_filesystem_module()
        
        elif choice == "3":
            clear_screen()
            break
        
        else:
            print(f"\n[ERROR] Opción inválida: {choice}")
            input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()