from functions import *
import pandas as pd
import socket
import time


args = args_parser()
# SERVER = args.server
SERVER = '192.168.0.6'
PORT = args.port

ADDR = (SERVER, PORT)
CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT.connect(ADDR)

file_name = 'AGR-567 TC temperature Hourly September20.xlsx'
Excel_file = pd.ExcelFile(file_name)

col_name = ['Standard_Date_Time', 'EffPower', 'TC1', 'TC2', 'TC3', 'TC4']
content = pd.read_excel(Excel_file, nrows=10, usecols=col_name)

com_time = 0
while True:
    if com_time == 0:
        print('send message: ', '\n', content)
    send_msg(CLIENT, ['MSG_CLIENT_TO_SERVER', content])

    if True:
        recv = recv_msg(CLIENT, 'MSG_SERVER_TO_CLIENT')
        print(recv[1])
        com_time += 1
        if com_time == 10:
            break
        time.sleep(3)
