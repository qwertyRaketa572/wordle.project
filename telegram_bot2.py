from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
Token = '5943360499:AAGflXYTuqKK6-8l57YDc2-Ninu5YrqyxNI'
sania = Bot(token=Token)
dp = Dispatcher(sania)
g5 = []
g4 = []
g3 = []
g2 = []

@dp.message_handler(commands=['start', 'help'])
async def start(so: types.Message):
    kl = InlineKeyboardMarkup()
    button = InlineKeyboardButton('помощь', callback_data='first')
    button1 = InlineKeyboardButton('я дурачок', callback_data='second')
    kl.add(button, button1)
    await so.answer('Это оригинальный бот нашей игры, выберите кнопку из нескольких вариантов, а мы попытаемся вам помочь', reply_markup=kl)
    print(so)
@dp.message_handler(commands=['mark'])
async def start(so: types.Message):
    kr = InlineKeyboardMarkup()
    m = InlineKeyboardButton('2', callback_data='sixth')
    m1 = InlineKeyboardButton('3', callback_data='seventh')
    m2 = InlineKeyboardButton('4', callback_data='eighth')
    m3 = InlineKeyboardButton('5', callback_data='ninth')
    kr.add(m, m1, m2, m3)
    await so.answer('Пожалуйста оцените выполненную мной работу', reply_markup=kr)
@dp.message_handler(commands=['I_love_big_black_dicks'])
async def start(so: types.Message):
    br = InlineKeyboardMarkup()
    but = InlineKeyboardButton('Не нажимай!', callback_data='third')
    br.add(but)
    await so.answer('Боже, если я сейчас стою на защите и реально всем это показываю, то я прям супер маленький мозг имею', reply_markup=br)
@dp.message_handler(commands=['bumer_jokes'])
async def start(so: types.Message):
    br1 = InlineKeyboardMarkup()
    but2 = InlineKeyboardButton('Это вам', callback_data='fourth')
    br1.add(but2)
    await so.answer('Илья Сергеевич, я просто на 99,99% уверен, что вы не повелись на эти глупейшие разводки, этот 0,01 процент говорит лишь о человеческом факторе, мало ли вы не выспались', reply_markup=br1)
@dp.message_handler(commands=['real_help'])
async def start(so: types.Message):
    br2 = InlineKeyboardMarkup()
    but3 = InlineKeyboardButton('Подарочек', callback_data='fifth')
    br2.add(but3)
    await so.answer('Итак, нужно вводить слова, количество букв в которых равно количеству синих квадратов в строчке. Твоя задача отгадать слово, загаданное компьютером. Если ты вводишь несуществующее слово, оно окрашивается красным. '
                    'Попытайся обойтись без нецензурных слов, хотя иногда только такие на ум и приходят). Давай не грусти и возвращайся в игру.', reply_markup=br2)
@dp.callback_query_handler()
async def first_button(data: types.CallbackQuery):
    five = 0
    four = 0
    three = 0
    two = 0
    if data.data == 'first':
        await sania.send_message(chat_id=data.from_user.id, text='братан, ты че угараешь, какая помощь от бота в тг? Перейди на соседнюю кнопку, может что-нибудь получится')
    if data.data == 'second':
        await sania.send_message(chat_id=data.from_user.id,
                                 text='если ты это признаешь, значит не все так плохо. Крепись! Нас много!)')
    if data.data == 'third':
        await sania.send_message(chat_id=data.from_user.id,
                                 text='Конечно, я еще и на кнопку нажал, с каждым днем все больше и больше убеждаюсь, что я приемный')
    if data.data == 'fourth':
        await sania.send_message(chat_id=data.from_user.id,
                                 text='🌷')
    if data.data == 'fifth':
        await sania.send_message(chat_id=data.from_user.id,
                                 text='🗿')
    if data.data == 'ninth':
        five += 1
        await sania.send_message(chat_id=data.from_user.id,
                                 text='сердечно благодарю)')
    if data.data == 'eighth':
        four += 1
        await sania.send_message(chat_id=data.from_user.id,
                                 text='спасибо)')
    if data.data == 'seventh':
        three += 1
        await sania.send_message(chat_id=data.from_user.id,
                                 text='мда, прям так себе?')
    if data.data == 'sixth':
        two += 1
        await sania.send_message(chat_id=data.from_user.id,
                                 text='ну не на столько же...')
    if five != 0:
        g5.append(five)
    if four != 0:
        g4.append(four)
    if three != 0:
        g3.append(three)
    if two != 0:
        g2.append(two)


if __name__ == "__main__":
    executor.start_polling(dp)
    print(len(g5), 'пять')
    print(len(g4), 'четыре')
    print(len(g3), 'три')
    print(len(g2), 'два')

