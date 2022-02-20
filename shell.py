import random
import time
import os
import mariadb
from rich import print
from rich.console import Console
from rich.table import Table
import pathlib
from pathlib import Path
import socket

dir_path = pathlib.Path.cwd()
path_adb = Path(dir_path, 'prog', 'adb.exe')
path_scrcpy = Path(dir_path, 'prog', 'scrcpy.exe')
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)


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
        print('Запрос ', random.randint(1, 5))
        conn.close()
        return result
    except conn.Error as error:
        print("Error: {}".format(error))


list_vm_l = []


def list_vm(query):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Num", width=3)
    table.add_column("Port", justify="right")
    table.add_column("Device Name", width=18)
    for x in query:
        ind = query.index(x)
        list_vm_l.append(x[4])
        table.add_row(
            str(ind), x[0], x[4]
        )
    console.print(table)


def reboot_adb():
    print('[bold magenta]Закрываю все подключения[/bold magenta]')
    os.system(str(path_adb) + ' kill-server')
    print('[bold green]Запускаю ADB сервер[/bold green]')
    os.system(str(path_adb) + ' start-server')


def conn_scrcpy(ip, port, name):
    os.system(str(path_adb) + ' connect ' + ip + ':' + port)
    t = 0
    while t < 3:
        time.sleep(1)
        print('Старт через', 3 - t)
        t += 1
    print('[bold green]Создаю подключение к [/bold green]' + ip)
    os.system(str(path_scrcpy) + ' -s ' + ip + ':' + port + f' -Sw --max-fps 15' + f' --window-title "{name}"')


query = get_data()


def main():
    console = Console()
    console.print('###############  [bold red]Будьте Внимательны[/bold red] ##############\n', '\n',
                  '[bold green]Выберите действия:[/bold green] \n', '\n',
                  '# [ 1 ] Удаленное подключение к виртуалке\n', '# [ 2 ] Локальное подключение\n',
                  '# [ 3 ] Перезапустить ADB сервер\n', '# [ 4 ] Перезапустить удаленную виртуалку\n',
                  '# [ 5 ] Выключить виртуалку\n',
                  '# [ 6 ] Установка/Переустановка всех APK\n', '\n',
                  '# [ 8 ] *** WinShell Проброс портов ( только для админа )\n',
                  '# [ 7 ] *** Только для отладки (не использовать)\n'
                  )
    do = input('# => Ведите номер действия(число): ')
    if int(do) == 1:
        console.print('Получаю список возможных подключений', style="white on blue")
        time.sleep(1)
        list_vm(query)
        do = input('Ведите номер виртуалки(Number): ')
        print(query[int(do)][1], query[int(do)][0], query[int(do)][4])
        conn_scrcpy(query[int(do)][1], query[int(do)][0], query[int(do)][4])
        time.sleep(5)
    elif int(do) == 2:
        console.print('Запускаю локальное подключение', style="bold blue")
        time.sleep(1)
        list_vm(query)
        do = input('Ведите номер виртуалки(Number): ')
        conn_scrcpy(query[int(do)][2], query[int(do)][0], query[int(do)][4])
        time.sleep(5)
    elif int(do) == 3:
        console.print('Перезапускаю ADB Сервер', style="bold blue")
        time.sleep(1)
        reboot_adb()
    elif int(do) == 4:
        console.print('Перезапуск виртуалки', style="bold blue")
        time.sleep(1)
        list_vm(query)
        do = input('Ведите номер виртуалки(Number): ')
        print('Перезапускаю виртуалку', query[int(do)][4])
        client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        client.connect(('your_ip', 9090))
        data = client.recv(2048)
        print(data.decode("utf-8"))
        client.send(f'reboot;{query[int(do)][4]}'.encode("utf-8"))
    elif int(do) == 5:
        console.print('Выключить виртуалку', style="bold blue")
        time.sleep(1)
        list_vm(query)
        do = input('Ведите номер виртуалки(Number): ')
        print('Выключаю виртуалку', query[int(do)][4])
        client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        client.connect(('your_ip', 9090))
        data = client.recv(2048)
        print(data.decode("utf-8"))
        client.send(f'off;{query[int(do)][4]}'.encode("utf-8"))
    elif int(do) == 6:
        print('Приступаю к уставке APK')
        list_vm(query)
        do = input('Ведите номер виртуалки(Number): ')
        print('Виртуалка для установки', query[int(do)][4])
        do1 = input('Уверены что всё верно? [y или n]')
        if do1 == 'y':
            client = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
            )
            client.connect(('your_ip', 9090))
            data = client.recv(2048)
            print(data.decode("utf-8"))
            client.send(f'install;{query[int(do)][3]}'.encode("utf-8"))
            console.print('Проверьте результат через 2-3 минуты', style="bold green")
            time.sleep(5)
        elif do1 == 'n':
            console.print('Отмена установки', style="bold red")
            time.sleep(2)
    elif int(do) == 7:
        print('[DEV] Локальноя отладка подключение')
        time.sleep(1)
        list_vm(query)
        do = input('Ведите номер виртуалки(Number): ')
        conn_scrcpy(query[int(do)][3], query[int(do)][0], query[int(do)][4])
        time.sleep(5)
    elif int(do) == 8:
        print('Создать проброс портов')
        print('Мой локальный IP: ', local_ip)
        ip1 = input('Локальный ip ПК: ')
        port1 = input('Локальный порт ПК: ')
        ip2 = input('IP локальной виртуалки: ')
        do = input('Подтвердите выполнение [y или n]')
        if do == 'y':
            os.system(
                f'netsh interface portproxy add v4tov4 listenaddress={ip1} listenport={port1} connectaddress={ip2} connectport=5555')
            time.sleep(2)
        elif do == 'n':
            print('Отмена изменений')
        do1 = input('Посмотреть список проброса портов [y или n]')
        if do1 == 'y':
            os.system('netsh interface portproxy show all')
            time.sleep(2)
        elif do1 == 'n':
            print('Отмена проверки')


if __name__ == '__main__':
    while True:
        time.sleep(1)
        main()