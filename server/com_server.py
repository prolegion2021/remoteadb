import socket
import time
import os
from rich import print
import pathlib
from pathlib import Path
import threading

dir_path = pathlib.Path.cwd()
path_adb = Path(dir_path, 'prog', 'adb.exe')
path_scrcpy = Path(dir_path, 'prog', 'scrcpy.exe')


def reboot_vm(name):
    threading.Thread(target=os.system, args=('reboot_vm.bat ' + name,)).start()
    print(f'[bolt green]Презагрузка {name} завершена [/bolt green]')


def main_server():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )
    server.bind(
        ('', 9090)
    )
    server.listen(5)
    while True:
        time.sleep(1)
        print('[bolt orange]Получение пакетов[/bolt orange]')
        user_socket, adress = server.accept()
        user_socket.send("Подключение к серверу - Успех ".encode("utf-8"))
        data = user_socket.recv(2048)
        a = data.decode("utf-8")
        print('[bolt green]Перезагрузка виртуалки: [/bolt green]', a)
        reboot_vm(a)
        user_socket.close()
        break


if __name__ == '__main__':
    while True:
        main_server()