import os
import random
import threading
import time
import mariadb
from threading import Thread
from aiogram import Bot,  Dispatcher, executor, types

TOKEN = 'telegramToken'
bot = Bot(token=TOKEN)


def poweroff_vm(name):
    threading.Thread(target=os.system, args=('poweroff_vm.bat ' + name,)).start()
    print(f'[bolt green]Выключение {name} завершено [/bolt green]')


def power_off():
    i = 0
    while i <= 6*3600:
        time.sleep(1)
        i += 1
        #print('Прошло ', i, ' секунд')
    print('Пора выключить виртуалки')
    i = 0
    for x in query:
        time.sleep(0.1)
        # print(x[4])
        poweroff_vm(x[4])
        time.sleep(5)
    th = Thread(target=power_off)
    th.start()


def reboot_vm(name):
    threading.Thread(target=os.system, args=('reboot_vm.bat ' + name,)).start()
    print(f'[bolt green]Презагрузка {name} завершена [/bolt green]')


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
dp = Dispatcher(bot)
th = Thread(target=power_off)
th.start()

def keyboard(kb_config):
    _keyboard = types.InlineKeyboardMarkup()

    for rows in kb_config:
        btn = types.InlineKeyboardButton(
            callback_data=rows[0],
            text=rows[1]
        )
        _keyboard.insert(btn)

    return _keyboard


@dp.callback_query_handler()
async def callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, text=callback_query.data)
    print(callback_query.message)
    await bot.send_message(callback_query.from_user.id, text=f"Перезапускаю {query[int(callback_query.data)][4]}")
    reboot_vm(query[int(callback_query.data)][4])


@dp.message_handler(commands=['start'])
async def process_admin_command(message: types.Message):
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo="https://www.dverimariam.ru/userfiles/images/states/2017/06/refresh-double-flat.png",
        reply_markup=keyboard([
            ["0", "0", "текст сообщения", None],
            ["1", "1", "текст сообщения", None],
            ["2", "2", "текст сообщения", None],
            ["3", "3", "текст сообщения", None],
            ["4", "4", "текст сообщения", None],
            ["5", "5", "текст сообщения", None],
            ["6", "6", "текст сообщения", None],
            ["7", "7", "текст сообщения", None],
            ["8", "8", "текст сообщения", None],
            ["9", "9", "текст сообщения", None],
            ["10", "10", "текст сообщения", None],
            ["11", "11", "текст сообщения", None],
            ["12", "12", "текст сообщения", None],
            ["13", "13", "текст сообщения", None],
            ["14", "14", "текст сообщения", None],
            ["15", "15", "текст сообщения", None],
            ["16", "16", "текст сообщения", None],
            ["17", "17", "текст сообщения", None],
            ["18", "18", "текст сообщения", None],
            ["19", "19", "текст сообщения", None],
            ["20", "20", "текст сообщения", None],
            ["21", "21", "текст сообщения", None],
            ["22", "22", "текст сообщения", None],
            ["23", "23", "текст сообщения", None],
            ["24", "24", "текст сообщения", None],
            ["25", "25", "текст сообщения", None],
            ["26", "26", "текст сообщения", None],
            ["27", "27", "текст сообщения", None]
        ]),
        caption="Перезапуск виртуалки"
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)