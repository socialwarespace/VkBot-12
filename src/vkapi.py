import traceback
import vk_api
import os
import json
from src import logger
from random import randint
import re

vk_session = vk_api.VkApi(token=os.environ.get("VK_TOKEN"))
vk = vk_session.get_api()

sub_menu_button_color = "default"
action_button_color = "primary"

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def convert(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def get_buttons(keyboard_state):
    return {
        "main_menu": main_menu_button(),
        "schedule_menu": schedule_menu_button(),
        "replacements_menu": replacements_menu_button(),
        "settings_menu": settings_menu_button(),
    }.get(convert(keyboard_state))


def get_translation(keyboard_state):
    return {
        "main_menu": "Главное меню",
        "schedule_menu": "Меню Расписание",
        "replacements_menu": "Меню Замены",
        "settings_menu": "Меню Настройки",
    }.get(convert(keyboard_state))


'''
------------------------------------------------------------------------------------------
КНОПКИ ГЛАВНОГО МЕНЮ
------------------------------------------------------------------------------------------
'''


def main_menu_button():
    schedule_button = [{
        "action": {
            "type": "text",
            "payload": "{\"button\": \"schedule_menu\"}",
            "label": "Расписание"
        },
        "color": sub_menu_button_color
    }]

    replacements_button = [{
        "action": {
            "type": "text",
            "payload": "{\"button\":\"replacements_menu\"}",
            "label": "Замены"
        },
        "color": sub_menu_button_color
    }]

    bells_button = [{
        "action": {
            "type": "text",
            "payload": "{\"button\":\"bells_button\"}",
            "label": "Звонки на сегодня"
        },
        "color": action_button_color
    }]

    settings_button = [{
        "action": {
            "type": "text",
            "payload": "{\"button\":\"settings_menu\"}",
            "label": "Настройки"
        },
        "color": sub_menu_button_color
    }]

    return [
        schedule_button, replacements_button, bells_button, settings_button
    ]


'''
-----------------------------------------------------------------------------------------
КНОПКИ МЕНЮ РАСПИСАНИЯ
-----------------------------------------------------------------------------------------
'''


def schedule_menu_button():
    tomorrow_hyb_button = [{
        "action": {
            "type": "text",
            "payload": "{\"button\":\"tomorrow_hyb_button\"}",
            "label": "Расписание с заменами на завтра"
        },
        "color": action_button_color
    }]
    today_hyb_button = [{
        "action": {
            "type": "text",
            "payload": "{\"button\":\"today_hyb_button\"}",
            "label": "Расписание с заменами на сегодня"
        },
        "color": action_button_color
    }]

    tomorrow_sch_button = [{
        "action": {
            "type": "text",
            "payload": "{\"button\":\"tomorrow_sch_button\"}",
            "label": "Расписание без замен на завтра"
        },
        "color": action_button_color
    }]
    today_sch_button = [{
        "action": {
            "type": "text",
            "payload": "{\"button\":\"today_sch_button\"}",
            "label": "Расписание без замен на сегодня"
        },
        "color": action_button_color
    }]

    back_button = [{
        "action": {
            "type": "text",
            "payload": "{\"button\":\"main_menu\"}",
            "label": "Назад"
        },
        "color": sub_menu_button_color
    }]

    return [
        tomorrow_hyb_button, today_hyb_button, tomorrow_sch_button,
        today_sch_button, back_button
    ]


'''
------------------------------------------------------------------------------------------
КНОПКИ МЕНЮ ЗАМЕН
------------------------------------------------------------------------------------------
'''


def replacements_menu_button():
    tomorrow_rep_button = [{
        "action": {
            "type": "text",
            "payload": "{\"button\":\"tomorrow_rep_button\"}",
            "label": "Замены на завтра"
        },
        "color": action_button_color
    }]

    today_rep_button = [{
        "action": {
            "type": "text",
            "payload": "{\"button\":\"today_rep_button\"}",
            "label": "Замены на сегодня"
        },
        "color": action_button_color
    }]

    back_button = [{
        "action": {
            "type": "text",
            "payload": "{\"button\":\"main_menu\"}",
            "label": "Назад"
        },
        "color": sub_menu_button_color
    }]

    return [tomorrow_rep_button, today_rep_button, back_button]


'''
-------------------------------------------------------------------------------------------
КНОПКИ МЕНЮ НАСТРОЕК
-------------------------------------------------------------------------------------------
'''


def settings_menu_button():
    about_button = [{
        "action": {
            "type": "text",
            "payload": "{\"button\":\"about_button\"}",
            "label": "Информация"
        },
        "color": action_button_color
    }]

    change_group_button = [{
        "action": {
            "type": "text",
            "payload": "{\"button\":\"change_group_button\"}",
            "label": "Сменить группу"
        },
        "color": action_button_color
    }]

    set_timer_button = [{
        "action": {
            "type": "text",
            "payload": "{\"button\":\"set_timer_button\"}",
            "label": "Установить таймер"
        },
        "color": action_button_color
    }]

    unset_timer_button = [{
        "action": {
            "type": "text",
            "payload": "{\"button\":\"unset_timer_button\"}",
            "label": "Убрать таймер"
        },
        "color": action_button_color
    }]

    back_button = [{
        "action": {
            "type": "text",
            "payload": "{\"button\":\"main_menu\"}",
            "label": "Назад"
        },
        "color": sub_menu_button_color
    }]

    return [
        about_button, change_group_button, set_timer_button,
        unset_timer_button, back_button
    ]


_RAND_MAX = 2147483647


def _get_random_id():
    return randint(1, _RAND_MAX)


def send_message_decorator(function_to_decorate):
    def try_to_send(*args, **kwargs):
        try:
            function_to_decorate(*args, **kwargs)
        except Exception:
            logger.error(
                "Send message function failed: {function}",
                function=function_to_decorate.__name__,
                exception=traceback.format_exc())

    return try_to_send


@send_message_decorator
def send_message_with_keyboard(user_id, message, keyboard_state):
    if keyboard_state is not None:
        buttons = get_buttons(keyboard_state)
        if buttons is None:
            vk.messages.send(
                user_id=user_id, message=message, random_id=_get_random_id())
        else:
            vk.messages.send(
                user_id=user_id,
                message=get_translation(keyboard_state),
                random_id=_get_random_id(),
                keyboard=json.dumps({
                    "one_time": False,
                    "buttons": buttons
                },
                                    ensure_ascii=False).encode("utf-8"))
    else:
        vk.messages.send(
            user_id=user_id, message=message, random_id=_get_random_id())


@send_message_decorator
def send_message_with_keyboard_to_many(user_ids, message, keyboard_state):
    if keyboard_state is not None:
        buttons = get_buttons(keyboard_state)
        if buttons is None:
            vk.messages.send(
                user_ids=user_ids, message=message, random_id=_get_random_id())
        else:
            vk.messages.send(
                user_ids=user_ids,
                message=get_translation(keyboard_state),
                random_id=_get_random_id(),
                keyboard=json.dumps({
                    "one_time": False,
                    "buttons": buttons
                },
                                    ensure_ascii=False).encode("utf-8"))
    else:
        vk.messages.send(
            user_ids=user_ids, message=message, random_id=_get_random_id())


@send_message_decorator
def send_message_to_all(user_id, message, keyboard_state):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=_get_random_id(),
        keyboard=json.dumps({
            "one_time": False,
            "buttons": get_buttons(keyboard_state)
        },
                            ensure_ascii=False).encode("utf-8"))


@send_message_decorator
def send_message_without_keyboard(user_id, message):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=_get_random_id(),
        keyboard=json.dumps({
            "one_time": False,
            "buttons": []
        }),
        ensure_ascii=False)


@send_message_decorator
def send(peer_id, message):
    vk.messages.send(
        peer_id=peer_id, message=message, random_id=_get_random_id())
