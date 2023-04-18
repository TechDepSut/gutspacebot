from vkbottle import Keyboard, Text, KeyboardButtonColor

main_keyboard = Keyboard(one_time=True)
main_keyboard.add(Text("Бронь"), color=KeyboardButtonColor.PRIMARY)
main_keyboard.row()
main_keyboard.add(Text("Задать вопрос"), color=KeyboardButtonColor.PRIMARY)

error_keyboard = Keyboard(one_time=True)
error_keyboard.add(Text("Отменить бронь"), color=KeyboardButtonColor.PRIMARY)
error_keyboard.row()
error_keyboard.add(Text("Назад"), color=KeyboardButtonColor.PRIMARY)
