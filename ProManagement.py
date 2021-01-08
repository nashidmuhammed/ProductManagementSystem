from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox

root = Tk()
root.geometry("1200x700+0+0")
root.title("NFOUR ProductManagementSystem|Version 1.0")
#root.iconbitmap('D:\PROJECTS\ProManagementSystem/nfour.png')
p1 = PhotoImage(file = 'nfour.png')
root.iconphoto(False, p1)

title = Label(root,text="Product Management System", font=("Segoe UI",30,"bold"),bg="#86D5D0")
title.pack(side=TOP,fill=X)



'''All Variables'''
id_var = StringVar()
category_var = StringVar()
name_var = StringVar()
price_var = StringVar()
qty_var = StringVar()
search_by = StringVar()
search_txt = StringVar()


def add_product():
    if name_var.get() == "" or qty_var.get() == "" or category_var.get() == "":
        messagebox.showwarning("Error","All fields are required!")
    else:
        conn = sqlite3.connect('products.db')
        c = conn.cursor()
        try:
            print("enter try")
            c.execute("SELECT rowid, * FROM products WHERE category LIKE '" + category_var.get() + "'")
            ct = c.fetchone()[1]
            print("Typed =", category_var.get(), "name = ", ct)
            c.execute("SELECT rowid, * FROM products WHERE name LIKE '"+name_var.get()+"'")
            nm = c.fetchone()[2]
            print("Typed =", name_var.get(), "name = ", nm)


            if nm.casefold() == str(name_var.get()).casefold() and ct.casefold() == str(category_var.get()).casefold():
                print("if completed")
                messagebox.showerror("Error","Product already exist in this Category")
            else:
                print("enter else")
                c.execute("INSERT INTO products VALUES (?,?,?,?)",
                          (category_var.get(), name_var.get(), price_var.get(), qty_var.get()))
                conn.commit()
                show_product()
                clear()
                conn.close()
                messagebox.showinfo("Success", "Record has been inserted")
        except:
            print("enter except")
            c.execute("INSERT INTO products VALUES (?,?,?,?)", (category_var.get(),name_var.get(),price_var.get(),qty_var.get()))
            conn.commit()
            show_product()
            clear()
            conn.close()
            messagebox.showinfo("Success","Record has been inserted")

#fetch data
def show_product():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM PRODUCTS")
    # print(c.fetchall())
    rows = c.fetchall()
    if len(rows)!=0:
        print("show if enter")
        Product_table.delete(*Product_table.get_children())
        for row in rows:
            Product_table.insert('',END,values=row)
            conn.commit()
    conn.close()

def clear():
    id_var.set("")
    category_var.set("")
    name_var.set("")
    price_var.set("")
    qty_var.set("")

def get_product(ev):
    pro_row=Product_table.focus()
    contents=Product_table.item(pro_row)
    row=contents['values']
    id_var.set(row[0])
    category_var.set(row[1])
    name_var.set(row[2])
    price_var.set(row[3])
    qty_var.set(row[4])


def update_product():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("UPDATE products SET category=?,name=?,price=?,qty=? WHERE rowid=?",
              (category_var.get(), name_var.get(), price_var.get(), qty_var.get(),id_var.get()))

    # c.execute("SELECT * FROM PRODUCTS")
    # print(c.fetchall())

    conn.commit()
    print("successfully updated...")
    show_product()
    clear()
    conn.close()
    messagebox.showinfo("Updated","Successfully updated!")


def delete_product():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE rowid = "+id_var.get())
    conn.commit()
    conn.close()
    show_product()
    clear()
    messagebox.showinfo("Deleted","Successfully deleted!")


def search_data():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    print("serchby=",search_by.get())
    print("serchTXT=",search_txt.get())
    if search_by.get() == 'All':
        c.execute("SELECT rowid, * FROM products WHERE name LIKE '%"+str(search_txt.get())+"%'")
    else:
        c.execute("SELECT rowid, * FROM products WHERE category LIKE '"+str(search_by.get())+"' AND name LIKE '%"+str(search_txt.get())+"%'")
    # print(c.fetchall())
    rows = c.fetchall()
    if len(rows) != 0:
        Product_table.delete(*Product_table.get_children())
        for row in rows:
            Product_table.insert('', END, values=row)
            conn.commit()
    else:
        print("No product fount")
        messagebox.showerror("Not Found","No item found")
    print("successfully searched...")
    conn.close()


def about_us():
    messagebox.showinfo('About Us','This is the base level Product/Goods management system.\nIt helps to Add thousands of products to the Database and also to get data via searching or filtering\nThank you for supporting.\nFor more info Contact: nfourgroupn4@gmail.com')


"""################################################################################################################"""
menubar = Menu(root)
root.config(menu=menubar)
#submenu
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label="New Database")
subMenu.add_command(label="Shop Name")
subMenu.add_command(label="Exit",command=root.destroy)

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help",menu=subMenu)
subMenu.add_command(label="About Us",command=about_us)


Manage_Frame = Frame(root,bd=4,relief=RIDGE,bg="dark cyan")
Manage_Frame.place(x=30,y=100,width=500,height=650)

m_title = Label(Manage_Frame,text="Manage Product",font=("Segoe UI",20,"bold"),bg="dark cyan",fg="white")
m_title.grid(row=0,columnspan=2,pady=20)

lbl_id=Label(Manage_Frame,text="Id",font=("Segoe UI",15,"bold"),bg="dark cyan",fg="white")
lbl_id.grid(row=1,column=0,pady=10,padx=20,sticky="w")

txt_id = Entry(Manage_Frame,textvariable=id_var,font=("Segoe UI",15,"bold"),bd=5,relief=GROOVE,state="readonly")
txt_id.grid(row=1,column=1,pady=10,padx=20,sticky="w")

lbl_cat=Label(Manage_Frame,text="Category",font=("Segoe UI",15,"bold"),bg="dark cyan",fg="white")
lbl_cat.grid(row=2,column=0,pady=10,padx=20,sticky="w")

combo_cat=ttk.Combobox(Manage_Frame,textvariable=category_var,width=19,font=("Segoe UI",15,"bold"),state="readonly")
combo_cat['values'] = ("Mobile","Cover","Accessories","Screen","Other")
combo_cat.grid(row=2,column=1,pady=10,padx=20,sticky="w")

lbl_name=Label(Manage_Frame,text="Product Name",font=("Segoe UI",15,"bold"),bg="dark cyan",fg="white")
lbl_name.grid(row=3,column=0,pady=10,padx=20,sticky="w")

txt_name = Entry(Manage_Frame,textvariable=name_var,font=("Segoe UI",15,"bold"),bd=5,relief=GROOVE)
txt_name.grid(row=3,column=1,pady=10,padx=20,sticky="w")

lbl_price=Label(Manage_Frame,text="Product Price",font=("Segoe UI",15,"bold"),bg="dark cyan",fg="white")
lbl_price.grid(row=4,column=0,pady=10,padx=20,sticky="w")

txt_price = Entry(Manage_Frame,textvariable=price_var,font=("Segoe UI",15,"bold"),bd=5,relief=GROOVE)
txt_price.grid(row=4,column=1,pady=10,padx=20,sticky="w")

lbl_qty=Label(Manage_Frame,text="Available QTY",font=("Segoe UI",15,"bold"),bg="dark cyan",fg="white")
lbl_qty.grid(row=5,column=0,pady=10,padx=20,sticky="w")

txt_qty = Entry(Manage_Frame,textvariable=qty_var,font=("Segoe UI",15,"bold"),bd=5,relief=GROOVE)
txt_qty.grid(row=5,column=1,pady=10,padx=20,sticky="w")
'''button'''
btn_Frame = Frame(Manage_Frame,bd=4,relief=RIDGE,bg="dark cyan")
btn_Frame.place(x=30,y=500,width=450)

Addbtn = Button(btn_Frame,text="Add",command=add_product,width=10).grid(row=0,column=0,padx=10,pady=10)
updatebtn = Button(btn_Frame,text="Update",command=update_product,width=10).grid(row=0,column=1,padx=10,pady=10)
deletebtn = Button(btn_Frame,text="Delete",command=delete_product,width=10).grid(row=0,column=2,padx=10,pady=10)
clearbtn = Button(btn_Frame,text="Clear",command=clear,width=10).grid(row=0,column=3,padx=10,pady=10)


'''Datail'''

Detail_Frame=Frame(root,bd=4,relief=RIDGE,bg="sky blue")
Detail_Frame.place(x=550,y=100,width=900,height=650)

lbl_search=Label(Detail_Frame,text="Search By",font=("Segoe UI",15,"bold"),bg="sky blue",fg="black")
lbl_search.grid(row=0,column=0,pady=10,padx=20,sticky="w")

'''tttttttttttest combo'''
#clicked = StringVar()
search_by.set("All")

drop = OptionMenu(Detail_Frame, search_by, "All", "Mobile", "Cover", "Accessories", "Other")
drop.grid(row=0,column=1,pady=10,padx=20,sticky="ew")
drop.configure(width=10)


'''combo_search=ttk.Combobox(Detail_Frame,textvariable=search_by,width=10,font=("Segoe UI",13,"bold"),state="readonly")
combo_search['values']=("Mobile","Cover","Accessories","Screen","Other")
combo_search.grid(row=0,column=1,pady=10,padx=20,sticky="w")'''

txt_search = Entry(Detail_Frame,textvariable=search_txt,width=30,font=("Segoe UI",12,"bold"),bd=5,relief=GROOVE)
txt_search.grid(row=0,column=2,pady=10,padx=20,sticky="w")

search_btn = Button(Detail_Frame,command=search_data,text="Search",width=10,pady=5).grid(row=0,column=3,padx=10,pady=10)
showall_btn = Button(Detail_Frame,command=show_product,text="Show All",width=10,pady=5).grid(row=0,column=4,padx=10,pady=10)

'''Table Frame'''
Table_Frame=Frame(Detail_Frame,bd=4,relief=RIDGE,bg="sky blue")
Table_Frame.place(x=25,y=70,width=850,height=550)

scroll_x=Scrollbar(Table_Frame,orient=HORIZONTAL)
scroll_y=Scrollbar(Table_Frame,orient=VERTICAL)
Product_table = ttk.Treeview(Table_Frame,columns=("Product Id","Category","Product Name","Product Price","Available Qty"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
scroll_x.pack(side=BOTTOM,fill=X)
scroll_y.pack(side=RIGHT,fill=Y)
scroll_x.config(command=Product_table.xview)
scroll_y.config(command=Product_table.yview)
Product_table.heading("Product Id",text="Product Id")
Product_table.heading("Category",text="Category")
Product_table.heading("Product Name",text="Product Name")
Product_table.heading("Product Price",text="Product Price")
Product_table.heading("Available Qty",text="Available Qty")
Product_table['show']='headings'
Product_table.column("Product Id",width=70)
Product_table.column("Product Price",width=100)
Product_table.pack(fill=BOTH,expand=1)
Product_table.bind("<ButtonRelease-1>",get_product)

show_product()


root.mainloop()