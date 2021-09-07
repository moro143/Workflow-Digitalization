import pymssql
import secrets

DATABASE_NAME = secrets.DATABASE_NAME
SERVER = secrets.SERVER

ORDER_ID_NAME = secrets.ORDER_ID_NAME
ORDERS_TABLE_NAME = secrets.ORDERS_TABLE_NAME
EMPLOYEE_TABLE_NAME = secrets.EMPLOYEE_TABLE_NAME
BARCODE_NAME = secrets.BARCODE_NAME
EMPLOYEEID_NAME = secrets.EMPLOYEEID_NAME
EMPLOYEE_FIRST_NAME_NAME = secrets.EMPLOYEE_FIRST_NAME_NAME
EMPLOYEE_LAST_NAME_NAME = secrets.EMPLOYEE_LAST_NAME_NAME
TIME_FINISHING_ORDER_NAME = secrets.TIME_FINISHING_ORDER_NAME
TIME_STARTING_ORDER_NAME = secrets.TIME_STARTING_ORDER_NAME
ORDER_ID_PART_NAME = secrets.ORDER_ID_PART_NAME
USER = secrets.USER
PASSWORD = secrets.PASSWORD

ORDERS_DONE_TABLE = secrets.ORDERS_DONE_TABLE
STAGE_NAME = secrets.STAGE_NAME

def get_orderIds(barCode):
    conn = pymssql.connect(server=SERVER, database=DATABASE_NAME)
    cursor = conn.cursor()
    command =  "SELECT "+ORDER_ID_NAME+" FROM "+ORDERS_TABLE_NAME+" WHERE "+BARCODE_NAME+"="+str(barCode)
    cursor.execute(command)
    orderIds = []
    while True:
        tmp = cursor.fetchone()
        if tmp == None:
            break
        orderIds.append(tmp[0])
    conn.commit()
    return orderIds

def get_employee_name_from_employeeId(employeeId):
    conn = pymssql.connect(server=SERVER, database=DATABASE_NAME, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    command = "SELECT "+EMPLOYEE_FIRST_NAME_NAME+", " +EMPLOYEE_LAST_NAME_NAME+ " FROM "+EMPLOYEE_TABLE_NAME+" WHERE "+EMPLOYEEID_NAME+"="+str(employeeId)
    cursor.execute(command)
    name = cursor.fetchone()
    conn.commit()
    return name

def order_already_done_on_stage(orderId, stage):
    conn = pymssql.connect(server=SERVER, database=DATABASE_NAME, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    command = "SELECT {} FROM {} WHERE {}={} AND {}='{}'".format(TIME_FINISHING_ORDER_NAME, ORDERS_DONE_TABLE, ORDER_ID_NAME, orderId, STAGE_NAME, stage)
    print(command)
    #command = "SELECT " + TIME_FINISHING_ORDER_NAME + " FROM " + stage + " WHERE " + ORDER_ID_NAME + "=" + str(orderId)
    cursor.execute(command)
    response = cursor.fetchone()
    conn.commit()
    if response == None or response[0] == None:
        return False
    return True

def order_already_started_on_stage(orderId, stage):
    conn = pymssql.connect(server=SERVER, database=DATABASE_NAME, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    command = "SELECT {} FROM {} WHERE {}={} AND {}='{}'".format(TIME_STARTING_ORDER_NAME, ORDERS_DONE_TABLE, ORDER_ID_NAME, orderId, STAGE_NAME, stage)
    print(command)
    #command = "SELECT " + TIME_STARTING_ORDER_NAME + " FROM " + stage + " WHERE " + ORDER_ID_NAME + "=" + str(orderId)
    cursor.execute(command)
    response = cursor.fetchone()
    conn.commit()
    if response == None or response[0] == None:
        return False
    return True

def start_order(orderids, stage, employeeId):
    conn = pymssql.connect(server=SERVER, database=DATABASE_NAME, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    for id in orderids:
        command = "INSERT INTO {} ({}, {}, {}, {}) VALUES ({}, {}, GETDATE(), '{}')".format(ORDERS_DONE_TABLE, ORDER_ID_NAME, EMPLOYEEID_NAME, TIME_STARTING_ORDER_NAME, STAGE_NAME, id, employeeId, stage)
        #command = "INSERT INTO " + stage + " ("+ ORDER_ID_NAME +", "+ EMPLOYEEID_NAME +", "+ TIME_STARTING_ORDER_NAME +", "+ ORDER_ID_PART_NAME +") VALUES ("+ str(id) + " , " + str(employeeId) +", GETDATE(), '" + str(id) + "-" + str(1) + "')"
        cursor.execute(command)
    conn.commit()

def end_order(orderids, stage, employyeId):
    conn = pymssql.connect(server=SERVER, database=DATABASE_NAME, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    for id in orderids:
        command = "UPDATE {} SET {}=GETDATE() WHERE {}={}".format(ORDERS_DONE_TABLE, TIME_FINISHING_ORDER_NAME, ORDER_ID_NAME, id)
        print(command)
        #command = "UPDATE " + stage + " SET " + TIME_FINISHING_ORDER_NAME +"=GETDATE() WHERE " + ORDER_ID_NAME +"="+ str(id)
        cursor.execute(command)
    conn.commit()
#