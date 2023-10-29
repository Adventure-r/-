import tkinter as tk
from tkinter import ttk
import sqlite3

#Основное окно
class Main(tk.Frame):
    #Функция вызывающаяся при создании сущности
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    #Структура окна
    def init_main(self):
        #Добавление виджетов
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='.\итоговый проект\img\\add.png')
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='.\итоговый проект\img\\update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.update_img, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='.\итоговый проект\img\\delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.delete_img, command=self.delete_record)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='.\итоговый проект\img\\search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.search_img, command=self.open_seach_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='.\итоговый проект\img\\refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        #Расположение виджетов
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email'), height=45, show='headings')
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)

        #Отображение более приятных наименований для колонок
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='E-mail')

        #Прижато к левой стенке окна
        self.tree.pack(side=tk.LEFT)

    #Открытия дочернего окна
    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_seach_dialog(self):
        Search()

    def search_records(self, name):
        name = '%' + name + '%'
        self.db.c.execute('SELECT * FROM db WHERE name LIKE ?', (name,))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    #Добавление записи
    def records(self, name, tel, email):
        self.db.insert_data(name, tel, email)
        self.view_records()

    #Просмотр всех записей
    def view_records(self):
        self.db.c.execute('SELECT * FROM db')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end',  values=row) for row in self.db.c.fetchall()]
    
    def update_record(self, name, tel, email):
        self.db.c.execute('UPDATE db SET name=?, tel =?, email=? WHERE id=?', (name, tel, email, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def delete_record(self):
        for select_item in self.tree.selection():
            self.db.c.execute('DELETE FROM db WHERE id=?', self.tree.set(select_item, '#1'))
        
        self.db.conn.commit()
        self.view_records()

#Дочернее окно, добавление контакта
class Child(tk.Toplevel):
    #Функция вызывающаяся при создании сущности
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
    
    #Создание окна
    def init_child(self):
        #Свойства окна
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        #Добавление виджетов
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Телефон:')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='E-mail:')
        label_sum.place(x=50, y=110)

        #Расположение виджетов
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        #Кнопка "Закрыть"
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        #Кнопка "Добавить"
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event:
            self.view.records(self.entry_name.get(), self.entry_email.get(), self.entry_tel.get()))
        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Ркдактировать контакт')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=180, y=170)
        btn_edit.bind('<Button-1>', lambda event:
            self.view.update_record(self.entry_name.get(), 
                              self.entry_email.get(), 
                              self.entry_tel.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('SELECT * FROM db WHERE id=?', (self.view.tree.set(self.view.tree.selection()[0], '#1')))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app
    
    def init_search(self):
        self.title('Поиск контакта')
        self.geometry('300x300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Имя:')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=185, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=185, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')



#Класс для работы базой данных
class DB:
    def __init__(self):
        #Подключение бд
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()
        
        #Создание таблицы
        self.c.execute('''CREATE TABLE IF NOT EXISTS db (
                       id INTEGER PRIMARY KEY,
                       name TEXT,
                       tel TEXT,
                       email TEXT

        );''')
        self.conn.commit()

    #Добавление данный в таблицу
    def insert_data(self, name, tel, email):
        self.c.execute('INSERT INTO db(name, tel, email) VALUES (?, ?, ?);', (name, tel, email))
        self.conn.commit()
    

#Запуск программы если был открыт этот файл
if __name__ == '__main__':
    #Создание приложения  
    root = tk.Tk()
    #Создание бд
    db = DB()
    #Открытие основного окна
    app = Main(root)
    app.pack()
    #Свойства этого окна
    root.title('Телефонная книга')
    root.geometry('665x450')
    root.resizable(False, False)
    #Необхадимая функция обеспечивающая работу приложения
    root.mainloop()
