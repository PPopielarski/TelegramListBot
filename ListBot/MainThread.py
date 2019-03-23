from BotAPI import InlineKeyboard

ik = InlineKeyboard.InlineKeyboard()
ik.add_button("text", "cdm00")
ik.add_button("text2", "cdm22")
x = ik.get_keyboard_markup()
ik2 = InlineKeyboard.InlineKeyboard(json_data = x)
print(ik2.get_keyboard_markup())
ik2.move_button(0,0,2,2)

print(ik2.get_keyboard_markup())

ik2.move_button(2, 2, new_row=0, new_column=0)

print(ik2.get_keyboard_markup())