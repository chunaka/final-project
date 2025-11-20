from models.process_manager import ProcessManager

class ConsoleUI:
    def __init__(self, scheduler_cls):
        self.scheduler_cls = scheduler_cls
        self.pm = ProcessManager()
        self.scheduler = None


    def show_menu(self):
        print("OS SIMULATOR")
        print("1. Cargar procesos desde archivo")
        print("2. Ejecutar Scheduler")
        print("3. Mostrar resultados")
        print("4. Mostrar métricas")
        print("5. Salir")
        return input("Opción: ").strip()

    def load_processes(self, path):
        try:
            self.pm.load_from_file(path)
            print(f"[OK] Procesos cargados: {len(self.pm.ready_queue)}")
        except Exception as e:
            print(f"[ERROR] No se pudieron cargar procesos: {e}")

    
    def run_scheduler(self):
        if not self.pm.ready_queue:
            print(f"[ERROR] No hay procesos cargados")
            return
        
        self.scheduler = self.scheduler_cls()

        for process in self.pm.ready_queue:
            self.scheduler.add_process(process.pcb)
        
        self.scheduler.run()
        print(f"[OK] Scheduler ejecutado")

    
    def show_results(self):
        if not self.scheduler or not self.scheduler.timeline:
            print(f"[ERROR] No hay resultados.")
            return
        
        print(f"\nTIMELINE")
        for pid, start, end in self.scheduler.timeline:
            bar = "="*(end-start)
            print(f"P{pid}|{bar}|{start}->{end}")
    
    def show_metrics(self):
        if not self.scheduler or not self.scheduler.timeline:
            print(f"[ERROR] No se ha ejecutado ningún algoritmo.")
            return
        
        m = self.scheduler.compute_metrics()
        print(f"\nMETRICS")
        for k, v in m.items():
            print(f"{k}: {v:.3f}")


