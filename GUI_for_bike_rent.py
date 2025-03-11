import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import pymysql as sql
import random
import string
from tkinter import ttk

# Database Connection
def connect_db():
    return sql.connect(host='localhost', user='root', password='Rath@1234', db='bike_rental')


# Generate Unique Transaction ID
def generate_transaction_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


class BikeRentalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bike Rental System")
        self.root.geometry("600x400")
        self.stock = 1000  # Initial Stock
        self.price_per_unit = 100
        self.bike_img = PhotoImage(file="/Users/shantanudwivedi/Downloads/icons8-bike-64.png")
        self.password = "Admin123"

        # Bike Display
        self.image_label = tk.Label(self.root, image=self.bike_img, bg='#f0f0f0')
        self.image_label.pack()

        # UI Components
        tk.Label(root, text='Bike Rental System', font=('Arial', 20, 'bold')).pack(pady=10)
        tk.Button(root, text='Rent a Bike', command=self.rent_bike, font=('Arial', 12)).pack(pady=5)
        tk.Button(root, text='Admin Panel', command=self.admin_panel, font=('Arial', 12)).pack(pady=5)
        tk.Button(root, text='Exit', command=root.quit, font=('Arial', 12)).pack(pady=5)



    def rent_bike(self):
        rent_window = tk.Toplevel(self.root)
        rent_window.title("Rent a Bike")
        rent_window.geometry("400x300")

        tk.Label(rent_window, text="Customer Name:").pack()
        name_entry = tk.Entry(rent_window)
        name_entry.pack()

        tk.Label(rent_window, text="Contact Number:").pack()
        contact_entry = tk.Entry(rent_window)
        contact_entry.pack()

        tk.Label(rent_window, text="Number of Bikes:").pack()
        quantity_entry = tk.Entry(rent_window)
        quantity_entry.pack()



        def process_rental():
            name = name_entry.get()
            contact = contact_entry.get()
            quantity = int(quantity_entry.get())
            if not name or not contact or not quantity:
                messagebox.showerror("Error", "All fields are required.")
                return

            if quantity <= 0 or quantity > self.stock:
                messagebox.showerror("Error", "Invalid Quantity")
                return

            price = quantity * self.price_per_unit
            transaction_id = generate_transaction_id()

            # Store in Database
            db = connect_db()
            cur = db.cursor()
            cur.execute(
                "INSERT INTO rentals (transaction_id, customer_name, contact, bikes_rented, total_price) VALUES (%s, %s, %s, %s, %s)",
                (transaction_id, name, contact, quantity, price))
            db.commit()
            db.close()

            self.stock -= quantity
            messagebox.showinfo("Success", f"Transaction ID: {transaction_id}\nTotal Price: ₹{price}")
            rent_window.destroy()

        tk.Button(rent_window, text="Confirm Rental", command=process_rental).pack(pady=10)

    def admin_panel(self):

        admin_window = tk.Toplevel(self.root)
        admin_window.title("Admin Panel")
        admin_window.geometry("300x200")
        tk.Label(admin_window, text="Enter Password:").pack()
        password_entry = tk.Entry(admin_window, show='*')
        password_entry.pack()



        def login():
            if password_entry.get() == self.password:
                self.update_stock()
            else:
                messagebox.showerror("Error", "Wrong Password")
                admin_window.destroy()

        tk.Button(admin_window, text="Login", command=login).pack(pady=10)

    def update_stock(self):
        stock_window = tk.Toplevel(self.root)
        stock_window.title("Update Stock and all records")
        stock_window.geometry("600x300")
        bg_image = tk.PhotoImage(file="/Users/shantanudwivedi/Downloads/Untitled design (1).png")  # Use PNG/GIF format
        # Create a Label to hold the image
        bg_label = tk.Label(stock_window, image=bg_image)
        bg_label.place(x=0,y=0)  # Stretch image to window size

        # Keep a reference to avoid garbage collection
        stock_window.bg_image = bg_image
        l1 = tk.Label(stock_window, text="Add Bikes to Stock:")
        l1.place(x=10,y=10)
        e1 = stock_entry = tk.Entry(stock_window)
        e1.place(x=150,y=10)
        l2 = tk.Label(stock_window,text="update price per unit:")
        l2.place(x=10,y=50)
        l3 = tk.Label(stock_window,text="update password")
        l3.place(x=10,y=100)
        e2=price_entry = tk.Entry(stock_window)
        e2.place(x=150,y=50)
        e3=price_entry = tk.Entry(stock_window)
        e3.place(x=150,y=100)


        def update():
            add_stock = int(stock_entry.get())
            self.stock += add_stock
            messagebox.showinfo("Success", f"Stock Updated! Total Bikes: {self.stock}")
            stock_window.destroy()

        b1=tk.Button(stock_window, text="Update", command=update)
        b1.place(x=300,y=10)

        def allrecords():

            import pymysql as sql
            g = sql.connect(host='localhost', user='root', password='Rath@1234', db='bike_rental')
            cur = g.cursor()
            n = "select * from rentals"
            cur.execute(n)
            result = cur.fetchall()

            allwindow = tk.Toplevel(self.root)
            allwindow.title("all transaction record")
            tree = ttk.Treeview(allwindow,columns=("id","transaction id","customer name","contact","bike rented","total price","rental date"),show="headings")
            tree.heading("id", text="id")
            tree.heading("transaction id", text="transaction id")
            tree.heading("customer name", text="customer name")
            tree.heading("contact", text="contact")
            tree.heading("bike rented",text="bike rented")
            tree.heading("total price",text="total price")
            tree.heading("rental date",text="rental date")

            for row in result:
                tree.insert("", "end", values=row)

            tree.pack(expand=True, fill="both")


        b3=tk.Button(stock_window,text="show all transactions",command=allrecords,width=60)
        b3.place(x=10,y=150)

        b5 = tk.Button(stock_window,text="exit",command=stock_window.destroy,width=60)
        b5.place(x=10,y=200)

        def priceupdate():
            c = int(e2.get())
            self.price_per_unit = c
            messagebox.showinfo("success",f'price per unit updated to{c}')
        b2=tk.Button(stock_window,text="update price per uint",command=priceupdate)
        b2.place(x=300,y=50)

        def password():
            c = e3.get()
            self.password = c
            messagebox.showinfo("success","password reset success")
        b4 = tk.Button(stock_window,text="update password",command=password)
        b4.place(x=300,y=100)

        def report():
            import datetime
            k= datetime.datetime.now()
            db = connect_db()
            cur = db.cursor()
            doublequot = '"'
            cur.execute(f"(SELECT 'id', 'transaction_id', 'customer_name', 'contact', 'bikes_rented', 'total_price', 'rental_date')UNION select * into outfile '/Users/shantanudwivedi/Downloads/exportdata {k}.csv' fields terminated by ','enclosed by '{doublequot}' lines terminated by '\n' from bike_rental.rentals")
            db.commit()
            db.close()
            messagebox.showinfo('success',"file exported to default location : /Users/shantanudwivedi/Downloads")

        b5 = tk.Button(stock_window,text="export transction file",command=report,width=60)
        b5.place(x=10,y=250)

        bike_models = ["Honda CB 350", "Royal Enfield Classic", "Yamaha R15", "KTM Duke 250", "Bajaj Pulsar NS200"]

        b6=ttk.Combobox(stock_window,values=bike_models,state="readonly")
        b6.place(x=400,y=10)

        s = b6.get()
        print(s)
if __name__ == "__main__":
    root = tk.Tk()
    app = BikeRentalApp(root)
    root.mainloop()

