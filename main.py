from database import create_tables, add_task, get_tasks, tasks_exist

if __name__ == "__main__":

    print("🚀 Iniciando Agenda Inteligente...\n")

    create_tables()

    if not tasks_exist():

        add_task("Estudiar Python", "SQLite base", "estudio", "task", "alta")
        add_task("Pagar internet", "Factura mensual", "casa", "task", "urgente")
        add_task("Idea app", "agenda inteligente", "desarrollo", "idea", "baja")

    tasks = get_tasks()

    print("\n📋 LISTA DE TAREAS:\n")

    for t in tasks:
        print(t)
        