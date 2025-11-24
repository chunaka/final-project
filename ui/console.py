import os
from models.process_manager import ProcessManager

class ConsoleUI:
    def __init__(self, scheduler_cls):
        self.scheduler_cls = scheduler_cls
        self.pm = ProcessManager()
        self.scheduler = None

    def clear_screen(self):
        """Limpia la pantalla de la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self, title):
        """Imprime un encabezado formateado"""
        self.clear_screen()
        print("=" * 60)
        print(f" {title.center(58)} ")
        print("=" * 60)
        print()

    def print_separator(self):
        """Imprime un separador"""
        print("-" * 60)

    def wait_for_user(self):
        """Espera a que el usuario presione Enter"""
        input("\nPresiona Enter para continuar...")

    def show_menu(self):
        self.print_header("OS SIMULATOR - MENÚ PRINCIPAL")
        print("  1. Cargar procesos desde archivo")
        print("  2. Ejecutar Scheduler")
        print("  3. Mostrar resultados")
        print("  4. Mostrar métricas")
        print("  5. Volver al menú principal")
        self.print_separator()
        return input("Seleccione una opción: ").strip()

    def load_processes(self, path):
        try:
            self.pm.load_from_file(path)
            print(f"\n[OK] Procesos cargados exitosamente: {len(self.pm.ready_queue)}")
            self.print_separator()
            
            # Mostrar procesos cargados
            print("\nProcesos en memoria:")
            for process in self.pm.ready_queue:
                pcb = process.pcb
                print(f"  • PID {pcb.pid}: Burst={pcb.burst_time}, "
                      f"Arrival={pcb.arrival_time}, Priority={pcb.priority}, "
                      f"User={process.user}")
            
            self.wait_for_user()
        except Exception as e:
            print(f"\n[ERROR] Al cargar procesos: {e}")
            self.wait_for_user()

    def run_scheduler(self):
        if not self.pm.ready_queue:
            print(f"\n[ERROR] No hay procesos cargados")
            self.wait_for_user()
            return
        
        self.print_header("EJECUTANDO SCHEDULER")
        
        # Pass ProcessManager to scheduler
        self.scheduler = self.scheduler_cls(process_manager=self.pm)
        self.scheduler.run()
        
        print("[OK] Scheduler ejecutado exitosamente")
        print(f"[INFO] Context switches realizados: {self.pm.context_switch_count()}")
        
        self.wait_for_user()

    def show_results(self):
        if not self.scheduler or not self.scheduler.timeline:
            print(f"\n[ERROR] No hay resultados. Ejecuta el scheduler primero.")
            self.wait_for_user()
            return
        
        self.print_header("TIMELINE DE EJECUCIÓN")
        
        print("Diagrama de Gantt:")
        print()
        for pid, start, end in self.scheduler.timeline:
            duration = end - start
            bar = "█" * duration
            print(f"  P{pid} │{bar}│ [{start:2d} → {end:2d}] ({duration} unidades)")
        
        print()
        self.print_separator()
        print(f"Total de eventos: {len(self.scheduler.timeline)}")
        
        self.wait_for_user()
    
    def show_metrics(self):
        if not self.scheduler or not self.scheduler.timeline:
            print(f"\n[ERROR] No se ha ejecutado ningún algoritmo.")
            self.wait_for_user()
            return
        
        self.print_header("MÉTRICAS DEL SCHEDULER")
        
        m = self.scheduler.compute_metrics()
        
        print("Resultados de rendimiento:")
        print()
        print(f"  • Tiempo de espera promedio:    {m['avg_waiting']:.3f} unidades")
        print(f"  • Tiempo de retorno promedio:   {m['avg_turnaround']:.3f} unidades")
        print(f"  • Throughput:                    {m['throughput']:.3f} procesos/unidad")
        print()
        self.print_separator()
        
        # Información adicional por proceso
        print("\nDetalle por proceso:")
        for process in self.pm.terminated_list:
            pcb = process.pcb
            waiting = pcb.start_time - pcb.arrival_time
            turnaround = pcb.completion_time - pcb.arrival_time
            print(f"  P{pcb.pid}: Espera={waiting}, Retorno={turnaround}, "
                  f"Completado en t={pcb.completion_time}")
        
        self.wait_for_user()

