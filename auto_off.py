import os
import random
import threading
import time
import mariadb
from aiogram import Bot,  Dispatcher, executor, types
from threading import Thread

def poweroff_vm(name):
    threading.Thread(target=os.system, args=('poweroff_vm.bat ' + name,)).start()
    print(f'[bolt green]Выключение {name} завершено [/bolt green]')


def get_data():
    conn = mariadb.connect(
        user="root",
        password="your_db_password",
        host="your_db_ip",
        port=3336,
        database="red_vm"
    )
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT wide_port, wide_ip, local_ip, vm_ip, device_name FROM vms_info")
        result = cur.fetchall()
        print('Запрос ', random.randint(1, 5))
        conn.close()
        return result
    except conn.Error as error:
        print("Error: {}".format(error))

query = get_data()


def power_off():
    i = 0
    while i <= 6:
        time.sleep(1)
        i += 1
        print('Прошло ', i, ' секунд')
    print('Пора выключить виртуалки')
    for x in query:
        time.sleep(1)
        # print(x[4])
        poweroff_vm(x[4])
        time.sleep(5)


thread_off = Thread(target=power_off())
thread_off.start()
print('dddd')
