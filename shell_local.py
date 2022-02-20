import time
import os
from rich import print
from rich.console import Console
from rich.table import Table
import pathlib
from pathlib import Path
import socket
import config

dir_path = pathlib.Path.cwd()
path_adb = Path(dir_path, 'prog', 'adb.exe')
path_scrcpy = Path(dir_path, 'prog', 'scrcpy.exe')
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)


def reboot_adb():
    print('[bold magenta]Закрываю все подключения[/bold magenta]')
    os.system(str(path_adb) + ' kill-server')
    time.sleep(3)
    print('[bold green]Запускаю ADB сервер[/bold green]')
    os.system(str(path_adb) + ' start-server')
    time.sleep(3)


def conn_scrcpy(ip, port):
    os.system(str(path_adb) + ' connect ' + ip + ':' + port)
    t = 0
    while t < 3:
        time.sleep(1)
        print('Старт через', 3 - t)
        t += 1
    print('[bold green]Создаю подключение к [/bold green]' + ip)
    os.system(str(path_scrcpy) + ' -s ' + ip + ':' + port + f' -Sw --max-fps 20')



list_vm_l = []
def list_vm(query):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Num", width=3)
    table.add_column("Device ip", width=18)
    for x in query:
        ind = query.index(x)
        list_vm_l.append(x)
        table.add_row(
            str(ind), x
        )
    console.print(table)

def main():
    console = Console()
    console.print('###############  [bold red]Будьте Внимательны[/bold red] ##############\n', '\n',
                  '[bold green]Выберите действия:[/bold green] \n', '\n',
                  '# [ 1 ] Локальное подключение к виртуалке\n',
                  '# [ 2 ] Перезапустить ADB сервер\n'
                  )
    do = input('# => Ведите номер действия(число): ')
    if int(do) == 1:
        console.print('Получаю список возможных подключений', style="white on blue")
        time.sleep(1)
        list_vm(config.list_ip)
        do = input('Ведите номер виртуалки(Number): ')
        # print(list_ip[int(do)])
        conn_scrcpy(config.list_ip[int(do)], '5555')
        time.sleep(5)
    elif int(do) == 2:
        time.sleep(1)
        reboot_adb()


if __name__ == '__main__':
    while True:
        time.sleep(1)
        main()