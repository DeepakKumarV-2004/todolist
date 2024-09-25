from tkinter import *
from tkinter .ttk import *
import mysql.connector
from tkinter import messagebox
def add_task():
    tas = taskentry.get()
    if len(tas) == 0:
        messagebox.showinfo('error','Please fill the task!')
    else:
        tasks.append(tas)
        cursor.execute('insert into tasks(title) values(%s)',(tas,))
        mydb.commit()
        list_update()
        taskentry.delete(0,'end')
def list_update():
    task_listbox.delete(0,'end')
    for tk in tasks:
        task_listbox.insert('end',tk)

def delete_task():
    try:
        val = task_listbox.get(task_listbox.curselection())
        if val in tasks:
            tasks.remove(val)
            cursor.execute("DELETE FROM tasks WHERE title = %s",(val,))
            mydb.commit()
            list_update()
    except:
        messagebox.showinfo('error','no tasks selected.Cannot Delete.')
def delete_all():
    mes  = messagebox.askyesno('Delete All','Are you sure?')
    if mes == True:
        while (len(tasks)!=0):
            tasks.pop()
        cursor.execute('delete from tasks')
        mydb.commit()
        list_update()
def close():
    print(tasks)
    window.destroy()
def retrive_database():
    while(len(tasks)!=0):
        tasks.pop()
    cursor.execute('SELECT title FROM tasks')
    task_listbox.delete(0,'end')
    result = cursor.fetchall()
    for row in result:
        tasks.append(row[0])

if __name__  == "__main__":
    mydb = mysql.connector.connect(host = "localhost",user = "Debug",password = "Deepak@9245710194",database="my_first_database")
    cursor = mydb.cursor()
    cursor.execute('create table if not exists tasks (title varchar(255))')
    tasks = []
    window =Tk()
    window.title("TO-DO LIST")
    window.geometry('400x675+600+20')
    window.resizable(0,0)
    window.configure(bg="lightblue")
    #header
    headerlabel = Label(text = "the To-Do List",font=("Brush script MT","30"),background="lightblue",foreground="black")
    headerlabel.pack(pady=15)
    #listbox
    task_listbox = Listbox(width=50,height=15,selectmode="SINGLE",selectbackground="yellow",selectforeground="blue")
    task_listbox.pack(pady=15)
    #label
    tasklabel = Label(text = "Enter the task:",font=("consolas","11","bold"),background="lightblue",foreground="brown")
    tasklabel.pack(pady=10)
    #entry
    taskentry = Entry(font = ("Consolas","12"),width= 32,foreground="black",background="#FFFFFF")
    taskentry.pack(pady=10)
    #button-add
    addbut = Button(text = "Add Task",width = 40,command=add_task)
    addbut.pack(pady=10)
    #button-del
    delbut = Button(text = "Delete Task",width = 40,command=delete_task)
    delbut.pack(pady = 10)
    #delallbut
    delallbut = Button(text = "Delete All Task",width = 40,command=delete_all)
    delallbut.pack(pady = 10)
    #exit
    exit = Button(text = "Exit",width = 40,command=close)
    exit.pack(pady = 10)
    retrive_database()
    list_update()
    window.mainloop()
    mydb.commit()
    cursor.close()
