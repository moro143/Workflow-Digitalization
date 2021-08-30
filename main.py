import tkinter as tk

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

        self.message = Message(self)
        self.frame = Workspace(self)
              
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
        self._root.employeeId = employeeid
        self._root.show_orderId()

class OrderId(tk.Frame):

    def __init__(self, root, *args, **kwargs):
        self._root = root

        tk.Frame.__init__(self, root, *args, **kwargs)
        self.pack(fill="both")

        self.orderIdLabel = tk.Label(self, text="Order Id")
        self.orderIdLabel.pack(side=tk.LEFT)

        self.orderIdEntry = tk.Entry(self)
        self.orderIdEntry.pack(side=tk.LEFT)

        self.orderIdButton = tk.Button(self, text="OK", command=self.orderIdButtonPress)
        self.orderIdButton.pack(side=tk.LEFT)
    
    def orderIdButtonPress(self):
        orderid = self.orderIdEntry.get()
        self._root.orderid = orderid
        self._root.show_affirmation()

class Affirmation(tk.Frame):

    def __init__(self, root, *args, **kwargs):
        self._root = root
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.pack(fill="both")

        self.employeeIdLabel = tk.Label(self, text="EmployeeId: "+self._root.employeeId)
        self.employeeIdLabel.pack(side=tk.TOP)

        self.orderIdButton = tk.Button(self, text="Yes", command=self.agreed)
        self.orderIdButton.pack(side=tk.LEFT)
        self.orderIdButton = tk.Button(self, text="No", command=self.denied)
        self.orderIdButton.pack(side=tk.LEFT)
    
    def denied(self):
        self._root._root.message.error("Rejected by user")
        self._root.show_employeeId()
    
    def agreed(self):
        self._root._root.message.done("Done")
        self._root.show_employeeId()

if __name__ == "__main__":
    root = Root()
    root.mainloop()