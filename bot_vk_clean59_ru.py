from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json
import logging
import requests

# https://vk.com/cleaning.perm
# https://vk.com/im?media=&sel=-38391278
# 8c578ab634482f4d1d81e55e4fc8678e5b74aba4157a54003951824050eeba1ab6be4c3d92abb02856bc0
# 38391278

# описание try и что он делает
# https://pythonworld.ru/tipy-dannyx-v-python/isklyucheniya-v-python-konstrukciya-try-except-dlya-obrabotki-isklyuchenij.html

# В блоке try мы выполняем инструкцию, которая может породить исключение, а в блоке внизу except мы перехватываем их.
try:

    group_id = '38391278'
    group_token = '8c578ab634482f4d1d81e55e4fc8678e5b74aba4157a54003951824050eeba1ab6be4c3d92abb02856bc0'
    api_version = '5.120'

    # виды callback-кнопок
    callback_types = ('show_snackbar')

    # запускаем бот
    vk_session = VkApi(token=group_token, api_version=api_version)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=group_id)

    # настройки для обоих клавиатур
    settings = dict(one_time=False, inline=True)

    # # # # # # # #
    # Клавиатура [1]
    # # # # # # # #

    keyboard_1 = VkKeyboard(**settings)

    # [ add_callback_button ] and [ add_button ]

    keyboard_1.add_button(label='Уборка (картиры, офисы, дома)',
                          color=VkKeyboardColor.POSITIVE,
                          payload={"type": "button-1"}
                          )

    keyboard_1.add_line()


    keyboard_1.add_button(label='Мойка окон и балконов',
                          color=VkKeyboardColor.POSITIVE,
                          payload={"type": "button-1"}
                          )

    keyboard_1.add_line()

    keyboard_1.add_button(label='Химчистка',
                          color=VkKeyboardColor.PRIMARY,
                          payload={"type": "button-1"}
                          )

    keyboard_1.add_button(label='Наши цены',
                          color=VkKeyboardColor.SECONDARY,
                          payload={"type": "button-1"}
                          )

    # # # # # # # #
    # Клавиатура [2]
    # # # # # # # #

    keyboard_2 = VkKeyboard(**settings)

    keyboard_2.add_button(label='Квартира',
                          color=VkKeyboardColor.POSITIVE,
                          payload={"type": "button-1"}
                          )

    keyboard_2.add_button(label='Офис',
                          color=VkKeyboardColor.POSITIVE,
                          payload={"type": "button-1"}
                          )

    keyboard_2.add_line()

    keyboard_2.add_button(label='Коттедж или дом',
                          color=VkKeyboardColor.POSITIVE,
                          payload={"type": "button-1"}
                          )

    keyboard_2.add_line()

    keyboard_2.add_button(label='Уборка территории',
                          color=VkKeyboardColor.PRIMARY,
                          payload={"type": "button-1"}
                          )

    # # # # # # # #
    # Клавиатура [3]
    # # # # # # # #

    keyboard_3 = VkKeyboard(**settings)

    keyboard_3.add_button(label='Влажная',
                          color=VkKeyboardColor.POSITIVE,
                          payload={"type": "button-1"}
                          )

    keyboard_3.add_button(label='Генеральная',
                          color=VkKeyboardColor.POSITIVE,
                          payload={"type": "button-1"}
                          )

    keyboard_3.add_line()

    keyboard_3.add_button(label='После ремонта',
                          color=VkKeyboardColor.POSITIVE,
                          payload={"type": "button-1"}
                          )

    keyboard_3.add_button(label='Другое',
                          color=VkKeyboardColor.SECONDARY,
                          payload={"type": "button-1"}
                          )

    # # # # # # # #
    # Клавиатура [4]
    # # # # # # # #

    keyboard_4 = VkKeyboard(**settings)

    keyboard_4.add_button(label='до 30 м2',
                          color=VkKeyboardColor.PRIMARY,
                          payload={"type": "button-1"}
                          )

    keyboard_4.add_button(label='от 30 до 50 м2',
                          color=VkKeyboardColor.PRIMARY,
                          payload={"type": "button-1"}
                          )

    keyboard_4.add_line()

    keyboard_4.add_button(label='от 50 до 100 м2',
                          color=VkKeyboardColor.PRIMARY,
                          payload={"type": "button-1"}
                          )

    keyboard_4.add_button(label='больше 100 м2',
                          color=VkKeyboardColor.PRIMARY,
                          payload={"type": "button-1"}
                          )

    f_toggle: bool = False

    for event in longpoll.listen():

        # отправляем меню на сообщение от пользователя
        if event.type == VkBotEventType.MESSAGE_NEW:

            # # # #
            # show [ user name ] first_name and last_name
            # START

            user_id = event.obj['message']['from_id']
            vk = vk_session.get_api()
            id = user_id
            user_get = vk.users.get(user_ids=(id))
            user_get = user_get[0]
            first_name = user_get['first_name']
            last_name = user_get['last_name']
            full_name = first_name + " " + last_name

            # print(first_name)

            # # # #
            # show [ user name ] first_name and last_name
            # END

            if event.obj.message['text'] == '+':
                if event.from_user:

                    # тут будет сообщение, которое мы передаем в первом запросе после [ + ]
                    event.obj.message['text'] = first_name + ', здравствуйте! Нажмите на интересующую услугу. ' \
                                                             '\r\n' \
                                                             '\r\nНе нашли нужную? Просто напишите сообщение.👇🏻'

                    # если клиент пользователя не поддерживает callback-кнопки,
                    # нажатие на них будет отправлять текстовые
                    # сообщения. т.е. они будут работать как обычные inline кнопки.

                    if 'callback' not in event.obj.client_info['button_actions']:
                        print('клиент {event.obj.message["from_id"]} не поддерживает callback')

                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        keyboard=keyboard_1.get_keyboard(),
                        message=event.obj.message['text'])

            x = event.obj.message['text']
            # print(x)

            if (x in 'Уборка (картиры, офисы, дома)'):
                # print("проверка прошла " + x)
                vk.messages.send(
                    user_id=event.obj.message['from_id'],
                    random_id=get_random_id(),
                    peer_id=event.obj.message['from_id'],
                    keyboard=keyboard_2.get_keyboard(),
                    message='✅Где выполнить уборку?')

            if (x in 'Квартира' or x in 'Офис' or x in 'Коттедж или дом (частный)'):
                # print("проверка прошла " + x)
                vk.messages.send(
                    user_id=event.obj.message['from_id'],
                    random_id=get_random_id(),
                    peer_id=event.obj.message['from_id'],
                    keyboard=keyboard_3.get_keyboard(),
                    message='✅Какой нужен тип уборки?')

            if (x in 'Уборка территории'):
                # print("проверка прошла " + x)
                vk.messages.send(
                    user_id=event.obj.message['from_id'],
                    random_id=get_random_id(),
                    peer_id=event.obj.message['from_id'],
                    message='Спасибо!🙂 Теперь напишите:\r\n'
                            '\r\n- адрес (где надо сделать уборку)'
                            '\r\n- дату и время'
                            '\r\n- точную площадь территории'
                            '\r\n- номер телефона.'
                            '\r\n'
                            '\r\nПосле этого, мы свяжемся с вами.')

            if (x in 'Наши цены'):
                # print("проверка прошла " + x)
                vk.messages.send(
                    user_id=event.obj.message['from_id'],
                    random_id=get_random_id(),
                    peer_id=event.obj.message['from_id'],
                    message='\r\n [ ссылки на Яндекс Диск ]'
                            '\r\n\r\n > Химчистка диванов: https://yadi.sk/i/QCFhf-_xdbmu3Q'
                            '\r\n'
                            '\r\n > Мойка окон: https://yadi.sk/i/VXTcW6RgPzw31g'
                            '\r\n'
                            '\r\n > Уборка коттеджей и загородных домов: https://yadi.sk/i/bgnlGZrx1yN9XA')

            if (x in 'Влажная' or x in 'Генеральная' or x in 'После ремонта' or x in 'Другое'):
                # print("проверка прошла " + x)
                vk.messages.send(
                    user_id=event.obj.message['from_id'],
                    random_id=get_random_id(),
                    peer_id=event.obj.message['from_id'],
                    keyboard=keyboard_4.get_keyboard(),
                    message='✅Какая площадь?')

            if (x in 'до 30 м2' or x in 'от 30 до 50 м2' or x in 'от 50 до 100 м2' or x in 'больше 100 м2'):
                # print("проверка прошла " + x)
                vk.messages.send(
                    user_id=event.obj.message['from_id'],
                    random_id=get_random_id(),
                    peer_id=event.obj.message['from_id'],
                    message='Спасибо!🙂 Теперь напишите:\r\n'
                            '\r\n- адрес (где надо сделать уборку)'
                            '\r\n- дату и время'
                            '\r\n- точную площадь помещения'
                            '\r\n- санузлы'
                            '\r\n- нужна ли мойка окон (сколько окон)'
                            '\r\n- номер телефона.'
                            '\r\n'
                            '\r\nПосле этого, мы свяжемся с вами.')

            if (x in 'Мойка окон и балконов'):
                # print("проверка прошла " + x)
                vk.messages.send(
                    user_id=event.obj.message['from_id'],
                    random_id=get_random_id(),
                    peer_id=event.obj.message['from_id'],
                    message='Спасибо!🙂 Теперь напишите:\r\n'
                            '\r\n- адрес (где сделать мойку)'
                            '\r\n- дату и время'
                            '\r\n- количество окон/лоджий (их площадь)'
                            '\r\n- номер телефона.'
                            '\r\n'
                            '\r\nПосле этого, мы свяжемся с вами.')

            if (x in 'Химчистка'):
                # print("проверка прошла " + x)
                vk.messages.send(
                    user_id=event.obj.message['from_id'],
                    random_id=get_random_id(),
                    peer_id=event.obj.message['from_id'],
                    message='Спасибо!🙂 Теперь напишите\r\n:'
                            '\r\n- адрес (где сделать химчистку)'
                            '\r\n- дату и время'
                            '\r\n- что нужно почистить'
                            '\r\n- номер телефона. '
                            '\r\n'
                            '\r\nПосле этого, мы свяжемся с вами.')

    if __name__ == '__main__':
        print()

# Переподключение к серверам ВК
except requests.exceptions.ReadTimeout:

        print("\n Переподключение к серверам ВК \n")
        time.sleep(3)