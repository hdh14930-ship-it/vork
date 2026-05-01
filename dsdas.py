import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
import json
import os

FAV_FILE = "favorites.json"

def search_users():
    query = entry.get().strip()
    if not query:
        messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым.")
        return

    listbox_results.delete(0, tk.END)
    label_status.config(text="Поиск...")
    try:
        response = requests.get(f"https://api.github.com/search/users?q={query}")
        response.raise_for_status()
        users = response.json()["items"]
        if not users:
            label_status.config(text="Пользователи не найдены.")
            return

        for user in users:
            listbox_results.insert(tk.END, user["login"])
        label_status.config(text=f"Найдено: {len(users)}")
    except Exception as e:
        label_status.config(text="Ошибка при поиске")
        messagebox.showerror("Ошибка", str(e))

def add_to_favorites():
    selected = listbox_results.curselection()
    if not selected:
        messagebox.showinfo("Нет выбора", "Выберите пользователя из списка.")
        return

    user = listbox_results.get(selected[0])
    favorites = load_favorites()
    if user in favorites:
        messagebox.showinfo("Уже в избранном", "Пользователь уже добавлен.")
        return

    favorites.append(user)
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(favorites, f, ensure_ascii=False, indent=2)
    listbox_favorites.insert(tk.END, user)
    label_status.config(text=f"Добавлен: {user}")

def load_favorites():
    if os.path.isfile(FAV_FILE):
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def update_fav_listbox():
    listbox_favorites.delete(0, tk.END)
    for user in load_favorites():
        listbox_favorites.insert(tk.END, user)

root = tk.Tk()
root.title("GitHub User Finder")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

entry = tk.Entry(frame, width=30)
entry.grid(row=0, column=0, padx=5)
btn_search = tk.Button(frame, text="Найти", command=search_users)
btn_search.grid(row=0, column=1, padx=5)

listbox_results = tk.Listbox(frame, height=10, width=30)
listbox_results.grid(row=1, column=0, columnspan=2, pady=5)

btn_add_fav = tk.Button(frame, text="Добавить в избранное", command=add_to_favorites)
btn_add_fav.grid(row=2, column=0, columnspan=2, pady=5)

label_favs = tk.Label(frame, text="Избранные пользователи:")
label_favs.grid(row=3, column=0, columnspan=2, pady=(10,0))

listbox_favorites = tk.Listbox(frame, height=7, width=30)
listbox_favorites.grid(row=4, column=0, columnspan=2, pady=5)

label_status = tk.Label(frame, text="")
label_status.grid(row=5, column=0, columnspan=2)

update_fav_listbox()
root.mainloop()
