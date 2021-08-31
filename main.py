import tkinter as tk
import sql_commands
import secrets

STAGES = secrets.STAGES
FONT = secrets.FONT
FONT_SIZE = secrets.FONT_SIZE
BUTTON_HEIGHT = 5
BUTTON_WIDTH = 10
BUTTON_COLOR = 'white'
BUTTON_COLOR_GOOD = 'green'
BUTTON_COLOR_BAD = 'red'

class Root(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Title")
        self.geometry("600x600+50+50")
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
    
        self.message = tk.Label(self, text="", width=300)
        self.message.config(font=(FONT, FONT_SIZE))
        self.message.pack()
    
    def done(self, message):
        self.message.destroy()
        self.message = tk.Label(self, text = message, bg="green", width=300)
        self.message.config(font=(FONT, FONT_SIZE))
        self.message.pack()
    
    def error(self, message):
        self.message.destroy()
        self.message = tk.Label(self, text = message, bg="red", width=300)
        self.message.config(font=(FONT, FONT_SIZE))
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
        self.employeeIdLabel.config(font=(FONT, FONT_SIZE))
        self.employeeIdLabel.pack(side=tk.LEFT)

        self.employeeIdEntry = tk.Entry(self)
        self.employeeIdEntry.pack(side=tk.LEFT)
        self.employeeIdEntry.focus()
        self.employeeIdEntry.config(font=(FONT, FONT_SIZE))
        
        self.employeeIdEntry.bind('<Return>', self.employeeIdButtonPress)

        self.employeeIdButton = tk.Button(self, text="OK", command=self.employeeIdButtonPress, height=BUTTON_HEIGHT, width=BUTTON_WIDTH, bg=BUTTON_COLOR)
        self.employeeIdButton.config(font=(FONT, FONT_SIZE))        
        self.employeeIdButton.pack(side=tk.LEFT)
    
    def employeeIdButtonPress(self, event=None):
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
        self.orderIdLabel.config(font=(FONT, FONT_SIZE))
        self.orderIdLabel.pack(side=tk.LEFT)

        self.orderIdEntry = tk.Entry(self)
        self.orderIdEntry.config(font=(FONT, FONT_SIZE))
        self.orderIdEntry.pack(side=tk.LEFT)
        self.orderIdEntry.focus()
        self.orderIdEntry.bind('<Return>', self.orderIdButtonPress)

        self.orderIdButton = tk.Button(self, text="OK", command=self.orderIdButtonPress, height=BUTTON_HEIGHT, width=BUTTON_WIDTH, bg=BUTTON_COLOR)
        self.orderIdButton.config(font=(FONT, FONT_SIZE))
        self.orderIdButton.pack(side=tk.LEFT)
    
    def orderIdButtonPress(self, event=None):
        barCode = self.orderIdEntry.get()[4:]
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
        self.employeeIdLabel.config(font=(FONT, FONT_SIZE))
        self.employeeIdLabel.pack(side=tk.TOP)

        self.orderIdLabel = tk.Label(self, text="Order Id: "+str(self._root.orderId))
        self.orderIdLabel.config(font=(FONT, FONT_SIZE))
        self.orderIdLabel.pack(side=tk.TOP)

        if sql_commands.order_alreadey_started_on_stage(str(self._root.orderId[0]), self._root._root.stage.clicked.get()):
            self.orderIdButton = tk.Button(self, text="End the order", command=self.endOrder, height=BUTTON_HEIGHT, width=BUTTON_WIDTH, bg=BUTTON_COLOR)
        else:
            self.orderIdButton = tk.Button(self, text="Start the order", command=self.startOrder, height=BUTTON_HEIGHT, width=BUTTON_WIDTH, bg=BUTTON_COLOR_GOOD)
        
        self.orderIdButton.config(font=(FONT, FONT_SIZE))
        self.orderIdButton.pack(side=tk.LEFT)

        self.orderIdButtonCancel = tk.Button(self, text="Cancel", command=self.denied, height=BUTTON_HEIGHT, width=BUTTON_WIDTH, bg=BUTTON_COLOR_BAD)
        self.orderIdButtonCancel.config(font=(FONT, FONT_SIZE))
        self.orderIdButtonCancel.pack(side=tk.LEFT)
    
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