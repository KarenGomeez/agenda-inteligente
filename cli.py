from database import create_tables, add_task, get_tasks, complete_task, delete_task
from colorama import Fore, Style, init

init(autoreset=True)


def header():
    print(Fore.CYAN + "\n" + "=" * 30)
    print("   🧠 AGENDA INTELIGENTE")
    print("=" * 30 + "\n")


def menu():
    print("1. ➕ Agregar tarea")
    print("2. 📋 Ver tareas")
    print("3. ✅ Completar tarea")
    print("4. 🗑️ Eliminar tarea")
    print("5. 🚪 Salir\n")


def format_task(task):
    id, title, desc, cat, type_, priority, due, status, created = task

    if status == "completada":
        status_icon = "✔"
        color = Fore.GREEN
    else:
        status_icon = "⏳"
        color = Fore.WHITE

    priority_icon = {
        "urgente": "🔥",
        "alta": "⚡",
        "media": "📌",
        "baja": "🌱"
    }.get(priority, "•")

    return (
        color +
        f"[{id}] {status_icon} {title} | {cat} | {priority_icon} {priority} | {status}"
    )


def show_tasks():
    tasks = get_tasks()

    print(Fore.MAGENTA + "\n📋 TAREAS:\n")

    if not tasks:
        print("No hay tareas aún.")
        return

    for t in tasks:
        print(format_task(t))


def add_task_ui():
    print(Fore.CYAN + "\n➕ NUEVA TAREA\n")

    title = input("Título: ")
    category = input("Categoría: ")
    priority = input("Prioridad (urgente, alta, media, baja): ")

    add_task(title, "", category, "task", priority)

    print(Fore.GREEN + "\n✔ Tarea agregada!\n")


def complete_task_ui():
    print(Fore.CYAN + "\n✅ COMPLETAR TAREA\n")

    task_id = input("ID de la tarea: ")

    if not task_id.isdigit():
        print(Fore.RED + "❌ ID inválido")
        return

    complete_task(int(task_id))

    print(Fore.GREEN + "✔ Tarea completada!\n")


def delete_task_ui():
    print(Fore.RED + "\n🗑️ ELIMINAR TAREA\n")

    task_id = input("ID de la tarea: ")

    if not task_id.isdigit():
        print(Fore.RED + "❌ ID inválido")
        return

    confirm = input("⚠️ ¿Seguro? (s/n): ")

    if confirm.lower() != "s":
        print(Fore.YELLOW + "❌ Cancelado")
        return

    delete_task(int(task_id))

    print(Fore.GREEN + "✔ Eliminada!\n")


def main():
    create_tables()

    while True:
        header()
        menu()

        option = input("👉 Elegí una opción: ")

        if option == "1":
            add_task_ui()

        elif option == "2":
            show_tasks()
            input("\nEnter para volver...")

        elif option == "3":
            complete_task_ui()
            input("\nEnter para volver...")

        elif option == "4":
            delete_task_ui()
            input("\nEnter para volver...")

        elif option == "5":
            print("👋 Chau!")
            break

        else:
            print(Fore.RED + "❌ Opción inválida")


if __name__ == "__main__":
    main()