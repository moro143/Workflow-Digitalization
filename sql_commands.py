import pymssql
import secrets

DATABASE_NAME = secrets.DATABASE_NAME
ORDER_ID_NAME = secrets.ORDER_ID_NAME
ORDERS_TABLE_NAME = secrets.ORDERS_TABLE_NAME
EMPLOYEE_TABLE_NAME = secrets.EMPLOYEE_TABLE_NAME
BARCODE_NAME = secrets.BARCODE_NAME
EMPLOYEEID_NAME = secrets.EMPLOYEEID_NAME
EMPLOYEE_FIRST_NAME_NAME = secrets.EMPLOYEE_FIRST_NAME_NAME
EMPLOYEE_LAST_NAME_NAME = secrets.EMPLOYEE_LAST_NAME_NAME
SERVER = secrets.SERVER

def get_orderIds(barCode):
    conn = pymssql.connect(server=SERVER, database=DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT "+ORDER_ID_NAME+" FROM "+ORDERS_TABLE_NAME+" WHERE "+BARCODE_NAME+"="+str(barCode))
    orderIds = []
    while True:
        tmp = cursor.fetchone()
        if tmp == None:
            break
        orderIds.append(tmp[0])
    conn.commit()
    return orderIds

def get_employee_name_from_employeeId(employeeId):
    conn = pymssql.connect(server=SERVER, database=DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT "+EMPLOYEE_FIRST_NAME_NAME+", " +EMPLOYEE_LAST_NAME_NAME+ " FROM "+EMPLOYEE_TABLE_NAME+" WHERE "+EMPLOYEEID_NAME+"="+str(employeeId))
    name = cursor.fetchone()
    conn.commit()
    return name

print(get_employee_name_from_employeeId(13))