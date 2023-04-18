from vkbottle import Keyboard, Text, KeyboardButtonColor

main_keyboard = Keyboard(one_time=True)
main_keyboard.add(Text("Бронь"), color=KeyboardButtonColor.PRIMARY)
main_keyboard.row()
main_keyboard.add(Text("Задать вопрос"), color=KeyboardButtonColor.PRIMARY)
