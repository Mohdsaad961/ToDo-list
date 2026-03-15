# from pathlib import Path
# import json


# class ToDo:
#     database = Path("data.json")

#     def __init__(self):
#         if self.database.exists():
#             with self.database.open("r") as f:
#                 self.data = json.load(f)
#         else:
#             self.data = []

#     def _save(self):
#         with self.database.open("w") as f:
#             json.dump(self.data, f, indent=4)

#     def add_task(self):
#         while True:
#             task = input("Enter task (press Enter to stop): \n").strip()

#             if task == "":
#                 break

#             task_data = {
#                 "task": task,
#                 "completed": False
#             }

#             self.data.append(task_data)
#             self._save()
#             print("✔ Task added successfully\n")

        
#     def show_tasks(self):
#         if not self.data:
#             print("No tasks found\n")
#             return
#         else:
#             for i, task in enumerate(self.data, start=1):
#                 status = "✔" if task["completed"] else "❌"
#                 print(i,":",task["task"], status)

#     def delete_task(self):
#         self.show_tasks()
#         try:
#             num = int(input("Enter task number to delete: "))
#             self.data.pop(num - 1)
#             self._save()
#             print("🗑 Task deleted\n")

#         except:
#             print("Invalid choice\n")

#     def complete_task(self):
#         self.show_tasks()
#         try:
#             num = int(input("Enter task number to mark completed: "))
#             if self.data[num - 1]["completed"] == False:
#                 self.data[num - 1]["completed"] = True
#                 print("✔ Task marked as completed\n")

#             elif self.data[num - 1]["completed"] == True:
#                 print("✔ Task already marked as completed\n")
            
#             self._save()

#         except:
#             print("Invalid choice\n")

# todo = ToDo()

# def menu():
#     print("====== DAILY TASK MANAGER ======")
#     print("1. Add Task")
#     print("2. Delete Task")
#     print("3. Mark Task Completed")
#     print("4. Show Tasks")
#     print("5. Exit")
#     print("================================")


# def main():
#     while True:
#         menu()
#         choice = input("Select option: ")

#         if choice == "1":
#             todo.add_task()

#         elif choice == "2":
#             todo.delete_task()

#         elif choice == "3":
#             todo.complete_task()

#         elif choice == "4":
#             todo.show_tasks()

#         elif choice == "5":
#             print("Goodbye 👋")
#             break

#         else:
#             print("Invalid option\n")


# if __name__ == "__main__":
#     main()










# from pathlib import Path
# import json


# class ToDo:
#     database = Path("data.json")

#     def __init__(self):
#         self.data = self._load()

#     def _load(self):
#         if self.database.exists():
#             with self.database.open("r") as f:
#                 return json.load(f)
#         return []

#     def _save(self):
#         with self.database.open("w") as f:
#             json.dump(self.data, f, indent=4)

#     def add_task(self):
#         while True:
#             task = input("Enter task (press Enter to stop): ").strip()
#             if not task:
#                 break

#             self.data.append({
#                 "task": task,
#                 "completed": False
#             })

#             self._save()
#             print("✔ Task added\n")

#     def show_tasks(self):
#         if not self.data:
#             print("No tasks found\n")
#             return

#         print("\n------ TASK LIST ------")
#         for i, task in enumerate(self.data, 1):
#             status = "✔" if task["completed"] else "❌"
#             print(f"{i}. {task['task']} {status}")
#         print()

#     def _get_index(self, message):
#         try:
#             num = int(input(message))
#             if 1 <= num <= len(self.data):
#                 return num - 1
#         except ValueError:
#             pass

#         print("Invalid choice\n")
#         return None

#     def delete_task(self):
#         self.show_tasks()
#         idx = self._get_index("Enter task number to delete: ")

#         if idx is not None:
#             self.data.pop(idx)
#             self._save()
#             print("🗑 Task deleted\n")

#     def complete_task(self):
#         self.show_tasks()
#         idx = self._get_index("Enter task number to mark completed: ")

#         if idx is not None:
#             if not self.data[idx]["completed"]:
#                 self.data[idx]["completed"] = True
#                 print("✔ Task marked as completed\n")
#             else:
#                 print("✔ Task already completed\n")

#             self._save()


# todo = ToDo()


# def menu():
#     print("====== DAILY TASK MANAGER ======")
#     print("1. Add Task")
#     print("2. Delete Task")
#     print("3. Mark Task Completed")
#     print("4. Show Tasks")
#     print("5. Exit")
#     print("================================")


# def main():
#     actions = {
#         "1": todo.add_task,
#         "2": todo.delete_task,
#         "3": todo.complete_task,
#         "4": todo.show_tasks
#     }

#     while True:
#         menu()
#         choice = input("Select option: ")

#         if choice == "5":
#             print("Goodbye 👋")
#             break

#         action = actions.get(choice)
#         if action:
#             action()
#         else:
#             print("Invalid option\n")


# if __name__ == "__main__":
#     main()













# from pathlib import Path
# import json
# import os
# from colorama import Fore, Style, init

# init(autoreset=True)


# class ToDo:
#     database = Path("data.json")

#     def __init__(self):
#         self.data = self._load()

#     def _load(self):
#         if self.database.exists():
#             with self.database.open("r") as f:
#                 return json.load(f)
#         return []

#     def _save(self):
#         with self.database.open("w") as f:
#             json.dump(self.data, f, indent=4)

#     def add_task(self):
#         print(Fore.CYAN + "\nAdd Tasks (Press Enter to stop)\n")

#         while True:
#             task = input(Fore.YELLOW + "➤ Enter task: ").strip()

#             if not task:
#                 break

#             self.data.append({
#                 "task": task,
#                 "completed": False
#             })

#             self._save()
#             print(Fore.GREEN + "✔ Task added\n")

#     def show_tasks(self):
#         if not self.data:
#             print(Fore.RED + "\nNo tasks found\n")
#             return

#         print(Fore.CYAN + "\n========== TASK LIST ==========\n")

#         for i, task in enumerate(self.data, 1):
#             if task["completed"]:
#                 status = Fore.GREEN + "✔ Completed"
#             else:
#                 status = Fore.RED + "✘ Pending"

#             print(Fore.YELLOW + f"{i}. {task['task']}  " + status)

#         print()

#     def _get_index(self, message):
#         try:
#             num = int(input(Fore.YELLOW + message))
#             if 1 <= num <= len(self.data):
#                 return num - 1
#         except ValueError:
#             pass

#         print(Fore.RED + "Invalid choice\n")
#         return None

#     def delete_task(self):
#         self.show_tasks()
#         idx = self._get_index("Enter task number to delete: ")

#         if idx is not None:
#             removed = self.data.pop(idx)
#             self._save()
#             print(Fore.GREEN + f"🗑 Deleted: {removed['task']}\n")

#     def complete_task(self):
#         self.show_tasks()
#         idx = self._get_index("Enter task number to mark completed: ")

#         if idx is not None:
#             if not self.data[idx]["completed"]:
#                 self.data[idx]["completed"] = True
#                 print(Fore.GREEN + "✔ Task marked as completed\n")
#             else:
#                 print(Fore.BLUE + "Task already completed\n")

#             self._save()


# todo = ToDo()


# def clear():
#     os.system("cls" if os.name == "nt" else "clear")


# def menu():
#     clear()

#     print(Fore.MAGENTA + Style.BRIGHT)
#     print("╔══════════════════════════════╗")
#     print("║      DAILY TASK MANAGER      ║")
#     print("╚══════════════════════════════╝\n")

#     print(Fore.CYAN + "1." + Style.RESET_ALL + " Add Task")
#     print(Fore.CYAN + "2." + Style.RESET_ALL + " Delete Task")
#     print(Fore.CYAN + "3." + Style.RESET_ALL + " Mark Task Completed")
#     print(Fore.CYAN + "4." + Style.RESET_ALL + " Show Tasks")
#     print(Fore.CYAN + "5." + Style.RESET_ALL + " Exit\n")


# def main():
#     actions = {
#         "1": todo.add_task,
#         "2": todo.delete_task,
#         "3": todo.complete_task,
#         "4": todo.show_tasks
#     }

#     while True:
#         menu()

#         choice = input(Fore.YELLOW + "Select option: ")

#         if choice == "5":
#             print(Fore.GREEN + "\nGoodbye 👋")
#             break

#         action = actions.get(choice)

#         if action:
#             action()
#             input(Fore.BLUE + "\nPress Enter to continue...")
#         else:
#             print(Fore.RED + "Invalid option\n")
#             input("Press Enter to continue...")


# if __name__ == "__main__":
#     main()







# import tkinter as tk
# from tkinter import messagebox
# from pathlib import Path
# import json


# class ToDo:
#     database = Path("data.json")

#     def __init__(self):
#         self.data = self.load()

#     def load(self):
#         if self.database.exists():
#             with open(self.database, "r") as f:
#                 return json.load(f)
#         return []

#     def save(self):
#         with open(self.database, "w") as f:
#             json.dump(self.data, f, indent=4)

#     def add(self, task):
#         self.data.append({"task": task, "completed": False})
#         self.save()

#     def delete(self, index):
#         self.data.pop(index)
#         self.save()

#     def complete(self, index):
#         self.data[index]["completed"] = True
#         self.save()


# class ToDoApp:

#     def __init__(self, root):
#         self.todo = ToDo()

#         self.root = root
#         self.root.title("Advanced To-Do Manager")
#         self.root.geometry("450x500")
#         self.root.config(bg="#2c3e50")

#         title = tk.Label(root, text="Daily Task Manager",
#                          font=("Arial", 18, "bold"),
#                          bg="#2c3e50", fg="white")
#         title.pack(pady=10)

#         frame = tk.Frame(root, bg="#2c3e50")
#         frame.pack()

#         self.entry = tk.Entry(frame, width=30, font=("Arial", 12))
#         self.entry.grid(row=0, column=0, padx=5)

#         add_btn = tk.Button(frame, text="Add",
#                             bg="#27ae60", fg="white",
#                             command=self.add_task)
#         add_btn.grid(row=0, column=1)

#         list_frame = tk.Frame(root)
#         list_frame.pack(pady=15)

#         scrollbar = tk.Scrollbar(list_frame)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#         self.listbox = tk.Listbox(
#             list_frame,
#             width=40,
#             height=15,
#             font=("Arial", 11),
#             yscrollcommand=scrollbar.set
#         )

#         self.listbox.pack()
#         scrollbar.config(command=self.listbox.yview)

#         btn_frame = tk.Frame(root, bg="#2c3e50")
#         btn_frame.pack()

#         complete_btn = tk.Button(
#             btn_frame,
#             text="Mark Completed",
#             bg="#3498db",
#             fg="white",
#             command=self.complete_task
#         )
#         complete_btn.grid(row=0, column=0, padx=10)

#         delete_btn = tk.Button(
#             btn_frame,
#             text="Delete Task",
#             bg="#e74c3c",
#             fg="white",
#             command=self.delete_task
#         )
#         delete_btn.grid(row=0, column=1)

#         self.counter = tk.Label(root,
#                                 text="",
#                                 bg="#2c3e50",
#                                 fg="white",
#                                 font=("Arial", 10))
#         self.counter.pack(pady=10)

#         self.refresh()

#     def refresh(self):
#         self.listbox.delete(0, tk.END)

#         for task in self.todo.data:
#             status = "✔" if task["completed"] else "❌"
#             self.listbox.insert(tk.END, f"{task['task']} {status}")

#         self.counter.config(text=f"Total Tasks: {len(self.todo.data)}")

#     def add_task(self):
#         task = self.entry.get().strip()

#         if not task:
#             messagebox.showwarning("Warning", "Task cannot be empty")
#             return

#         self.todo.add(task)
#         self.entry.delete(0, tk.END)
#         self.refresh()

#     def delete_task(self):
#         try:
#             index = self.listbox.curselection()[0]
#             self.todo.delete(index)
#             self.refresh()
#         except:
#             messagebox.showwarning("Warning", "Select a task first")

#     def complete_task(self):
#         try:
#             index = self.listbox.curselection()[0]
#             self.todo.complete(index)
#             self.refresh()
#         except:
#             messagebox.showwarning("Warning", "Select a task first")


# root = tk.Tk()
# app = ToDoApp(root)
# root.mainloop()