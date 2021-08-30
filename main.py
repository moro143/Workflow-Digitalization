import tkinter as tk
import sql_commands
import secrets

STAGES = secrets.STAGES

class Root(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Title")
        self.geometry("300x300+50+50")
        self._container = None
        self.show_main()
    
    def show_main(self):
        if self._container != None:
            self._container.destroy()
        self._container = Main(self)

class Main(tk.Frame):

    def __init__(self, root, *args, **kwargs):
        self._root = root

        tk.Frame.__init__(self, root, *args, **kwargs)
        self.pack()

        self.stage = Stage(self)
        self.message = Message(self)
        self.frame = Workspace(self)        

class Stage(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.pack(side = tk.TOP)

        self.clicked = tk.StringVar()
        self.clicked.set(STAGES[0])
        drop = tk.OptionMenu(root, self.clicked, *STAGES)
        drop.pack()


class Message(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.pack(side = tk.TOP)

        self._container = None
    
        self.message = tk.Label(self, text="")
        self.message.pack()
    
    def done(self, message):
        self.message.destroy()
        self.message = tk.Label(self, text = message, bg="green")
        self.message.pack()
    
    def error(self, message):
        self.message.destroy()
        self.message = tk.Label(self, text = message, bg="red")
        self.message.pack()

class Workspace(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root
        self.employeeId = None
        self.orderId = None

        tk.Frame.__init__(self, root, *args, **kwargs)
        self.pack(side = tk.BOTTOM)
        
        self._container = None
        self.show_employeeId()
    
    def show_employeeId(self):
        if self._container != None:
            self._container.destroy()
        self._container = EmployeeId(self)

    def show_orderId(self):
        if self._container != None:
            self._container.destroy()
        self._container = OrderId(self)
    
    def show_affirmation(self):
        if self._container != None:
            self._container.destroy()
        self._container = Affirmation(self)

class EmployeeId(tk.Frame):

    def __init__(self, root, *args, **kwargs):
        self._root = root

        tk.Frame.__init__(self, root, *args, **kwargs)
        self.pack(fill="both")

        self.employeeIdLabel = tk.Label(self, text="Employee Id")
        self.employeeIdLabel.pack(side=tk.LEFT)

        self.employeeIdEntry = tk.Entry(self)
        self.employeeIdEntry.pack(side=tk.LEFT)

        self.employeeIdButton = tk.Button(self, text="OK", command=self.employeeIdButtonPress)
        self.employeeIdButton.pack(side=tk.LEFT)
    
    def employeeIdButtonPress(self):
        employeeid = self.employeeIdEntry.get()
        if not employeeid.isnumeric():
            self._root._root.message.error("Error, employeeId have to be numeric")
            self._root.show_employeeId()
        elif sql_commands.get_employee_name_from_employeeId(employeeid)==None:
            self._root._root.message.error("Error, no employeeId in database")
            self._root.show_employeeId()
        else:
            self._root.employeeId = employeeid
            self._root.show_orderId()
            self._root._root.message.done("")

class OrderId(tk.Frame):

    def __init__(self, root, *args, **kwargs):
        self._root = root

        tk.Frame.__init__(self, root, *args, **kwargs)
        self.pack(fill="both")

        self.orderIdLabel = tk.Label(self, text="Order Bar Code: ")
        self.orderIdLabel.pack(side=tk.LEFT)

        self.orderIdEntry = tk.Entry(self)
        self.orderIdEntry.pack(side=tk.LEFT)

        self.orderIdButton = tk.Button(self, text="OK", command=self.orderIdButtonPress)
        self.orderIdButton.pack(side=tk.LEFT)
    
    def orderIdButtonPress(self):
        barCode = self.orderIdEntry.get()
        if not barCode.isnumeric():
            self._root._root.message.error("Error, Bar Code have to be numeric")
            self._root.show_orderId()
        elif len(orderids:=sql_commands.get_orderIds(barCode))==0:
            self._root._root.message.error("Error, Order not in database")
            self._root.show_orderId()
        elif sql_commands.order_already_done_on_stage(orderids[0], self._root._root.stage.clicked.get()):
            self._root._root.message.error("Error, Order already done on this stage")
            self._root.show_orderId()
        else:
            self._root.orderId = orderids
            self._root.show_affirmation()
            self._root._root.message.done("")

class Affirmation(tk.Frame):

    def __init__(self, root, *args, **kwargs):
        self._root = root
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.pack(fill="both")
        employeeNameTable = sql_commands.get_employee_name_from_employeeId(self._root.employeeId)
        name0 = "".join(employeeNameTable[0].split())
        name1 = "".join(employeeNameTable[1].split())
        self.employeeIdLabel = tk.Label(self, text="Employee Id: "+name0+" "+ name1)
        self.employeeIdLabel.pack(side=tk.TOP)
        self.orderIdLabel = tk.Label(self, text="Order Id: "+str(self._root.orderId))
        self.orderIdLabel.pack(side=tk.TOP)

        if sql_commands.order_alreadey_started_on_stage(str(self._root.orderId[0]), self._root._root.stage.clicked.get()):
            self.orderIdButton = tk.Button(self, text="End the order", command=self.endOrder)
        else:
            self.orderIdButton = tk.Button(self, text="Start the order", command=self.startOrder)
        self.orderIdButton.pack(side=tk.LEFT)
        self.orderIdButton = tk.Button(self, text="Cancel", command=self.denied)
        self.orderIdButton.pack(side=tk.LEFT)
    
    def denied(self):
        self._root._root.message.error("Rejected by user")
        self._root.show_employeeId()
    
    def endOrder(self):
        sql_commands.end_order(self._root.orderId, self._root._root.stage.clicked.get(), self._root.employeeId)
        self._root._root.message.done("Done")
        self._root.show_employeeId()
    
    def startOrder(self):
        sql_commands.start_order(self._root.orderId, self._root._root.stage.clicked.get(), self._root.employeeId)
        self._root._root.message.done("Done")
        self._root.show_employeeId()

if __name__ == "__main__":
    root = Root()
    root.mainloop()