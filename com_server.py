import socket
import time
import os
from rich import print
import mariadb
import pathlib
from pathlib import Path
import socket
import threading

dir_path = pathlib.Path.cwd()
path_adb = Path(dir_path, 'prog', 'adb.exe')
path_scrcpy = Path(dir_path, 'prog', 'scrcpy.exe')
apk1 = Path(dir_path, 'apk', 'boost.apk')
apk2 = Path(dir_path, 'apk', 'duck.apk')
apk3 = Path(dir_path, 'apk', 'firefox.apk')
apk4 = Path(dir_path, 'apk', 'myip.apk')
apk5 = Path(dir_path, 'apk', 'myst.apk')


def get_data():
    conn = mariadb.connect(
        user="root",
        password="your_password",
        host="your_ip",
        port=3336,
        database="red_vm"
    )
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT wide_port, wide_ip, local_ip, vm_ip, device_name FROM vms_info")
        result = cur.fetchall()
        conn.close()
        return result
    except conn.Error as error:
        print("Error: {}".format(error))


def reboot_vm(name):
    threading.Thread(target=os.system, args=('reboot_vm.bat ' + name,)).start()
    print(f'[bolt green]Презагрузка {name} завершена [/bolt green]')


def off_vm(name):
    threading.Thread(target=os.system, args=('poweroff_vm.bat ' + name,)).start()
    print(f'[bolt green]Завершение работы {name} выполнено [/bolt green]')


def main_server():
    while True:
        try:
            server = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
            )
            server.bind(
                ('', 9090)
            )
            server.listen(5)
            time.sleep(1)
            print('[bolt orange]Получение пакетов[/bolt orange]')
            user_socket, adress = server.accept()
            user_socket.send("Подключение к серверу - Успех ".encode("utf-8"))
            data = user_socket.recv(2048)
            a = data.decode("utf-8")
            vars = a.split(";")
            if vars[0] == 'reboot':
                print('Делаю перезагрузку', vars[1])
                reboot_vm(vars[1])
            if vars[0] == 'off':
                print('Выключаю устройство', vars[1])
                off_vm(vars[1])
            if vars[0] == 'install':
                print('Установка APK', vars[1])
                os.system(str(path_adb) + ' -s ' + vars[1] + ' install ' + str(apk1))
                os.system(str(path_adb) + ' -s ' + vars[1] + ' install ' + str(apk2))
                os.system(str(path_adb) + ' -s ' + vars[1] + ' install ' + str(apk3))
                os.system(str(path_adb) + ' -s ' + vars[1] + ' install ' + str(apk4))
                os.system(str(path_adb) + ' -s ' + vars[1] + ' install ' + str(apk5))
            user_socket.close()
            break
        except Exception as ex:
            print('Сбой выполнения сервера ', ex)


if __name__ == '__main__':
    while True:
        main_server()