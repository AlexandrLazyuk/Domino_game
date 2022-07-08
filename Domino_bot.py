import random
import telebot
from telebot import types
import logging
from random import shuffle
from itertools import combinations_with_replacement, chain
from collections import Counter

API_TOKEN = '5485680314:AAFIDI5l5sDD_VQOExyeRfeXxmZU4Qj0YuA'

bot = telebot.TeleBot(API_TOKEN)
telebot.logger.setLevel(logging.INFO)

storage = dict()


def init_storage(user_id):
    storage[user_id] = dict(attempt=None, random_digit=None)


def set_data_storage(user_id, key, value):
    storage[user_id][key] = value


def get_data_storage(user_id):
    return storage[user_id]


@bot.message_handler(func=lambda message: message.text.lower() == "Привет")
def command_text_hi(m):
    bot.send_message(m.chat.id, "Хай, бро!!! :)")


@bot.message_handler(func=lambda message: message.text.lower() == "Как дела")
def command_text_dela(m):
    bot.send_message(m.chat.id, "Шикардос")


@bot.message_handler(func=lambda message: message.text.lower() == "Игра")
def digitgames(message):
    init_storage(message.chat.id)  ### Инициализирую хранилище

    # определяем функцию поворота кости
    def turn_func(func_input, func_pieces):
        # стоп если нет кости
        if int(func_input) == 0 and len(stock_pieces) == 0:
            return None


        # дать ход игроку
        elif int(func_input) == 0 and len(stock_pieces) > 0:
            func_pieces.append(stock_pieces[-1])
            stock_pieces.remove(stock_pieces[-1])
            return None

        # расположить кость справа от змейки
        if int(func_input) > 0:
            # получить кость от игрока или компьютера
            piece_to_end = func_pieces[int(func_input) - 1]
            # повернуть кость
            if piece_to_end[1] == snake[-1][-1]:
                piece_to_end.reverse()
            # положить на место
            snake.append(piece_to_end)
            # удалить кость
            func_pieces.remove(func_pieces[int(func_input) - 1])

        # расположить кость слева от змейки
        else:
            # получить кость от игрока или компьютера
            piece_to_start = func_pieces[-int(func_input) - 1]
            # реверс кости
            if piece_to_start[0] == snake[0][0]:
                piece_to_start.reverse()
            # положить кость
            snake.insert(0, piece_to_start)
            # удалить кость
            func_pieces.remove(func_pieces[-int(func_input) - 1])

    # проверяем, выигрывает ли эта змейка
    def win_snake(func_snake):
        if func_snake[0][0] == func_snake[-1][-1] and sum(x.count(func_snake[0][0]) for x in func_snake) == 8:
            return True

    # определяем список костяшек
    dominoes = list(combinations_with_replacement(range(0, 7), 2))

    # преобразовать список кортежей в список списков
    dominoes = [list(x) for x in dominoes]

    # тосуем колоду
    shuffle(dominoes)

    # определяем коэффициент равный половине числа костяшек домино
    coefficient = len(dominoes) // 2

    # получить первую половину домино
    stock_pieces = dominoes[:coefficient]

    # получить части компьютера и игрока
    computer_pieces = dominoes[coefficient:int(coefficient * 1.5)]
    player_pieces = dominoes[int(coefficient * 1.5):]

    # найти змейку
    snake = [max([[x, y] for x, y in computer_pieces + player_pieces if x == y])]

    # удалить змею из фигур компьютера или игрока
    computer_pieces.remove(snake[0]) if snake[0] in computer_pieces else player_pieces.remove(snake[0])

    # кто ходит первый
    turn_num = 0 if len(player_pieces) > len(computer_pieces) else 1

    # старт игры
    while True:

        # показать стоковые, игровые и компьютерные фишки
        print('=' * 70)
        print('Stock size:', len(stock_pieces))
        print('Computer pieces:', len(computer_pieces), '\n')
        print(*snake, '\n', sep='') if len(snake) <= 6 else print(*snake[:3], '...', *snake[-3:], '\n', sep='')
        print("Your pieces:")

        for num, piece in enumerate(player_pieces):
            print(f"{num + 1}: {piece}")

        # условие победы игрока
        if len(player_pieces) == 0 or win_snake(snake) and turn_num == 0:
            print("\nStatus: The game is over. You won!")
            break

        # условие победы компьютера
        if len(computer_pieces) == 0 or win_snake(snake) and turn_num == 1:
            print("\nStatus: The game is over. The computer won!")
            break

        # определить концы змеи
        connection_keys = [snake[0][0], snake[-1][-1]]
        # условие розыгрыша
        if len(stock_pieces) == 0 and \
                not any(item in connection_keys for item in list(chain(*(player_pieces + computer_pieces)))):
            print("\nStatus: The game is over. It's a draw!")
            break

        # ход игрока
        if turn_num % 2 == 0:
            # считаем номер хода
            turn_num += 1
            # сообщение
            print("\nStatus: It's your turn to make a move. Enter your command.")
            # ввод игрока
            user_input = input()
            # проверка валидности комманды игрока
            if user_input.lstrip("-").isdigit() and int(user_input) in range(-len(player_pieces),
                                                                             len(player_pieces) + 1):
                # предоставить кость игроку
                if int(user_input) == 0:
                    turn_func(user_input, player_pieces)
                    continue

                # определить текущую часть
                current_piece = player_pieces[int(user_input) - 1] if int(user_input) > 0 \
                    else player_pieces[-int(user_input) - 1]

                # проверяем часть кости на валидность
                if connection_keys[-1] in current_piece and int(user_input) > 0 or \
                        connection_keys[0] in current_piece and int(user_input) < 0:
                    turn_func(user_input, player_pieces)
                else:
                    print("Illegal move. Please try again.")
                    turn_num -= 1
                    continue
            else:
                print("Invalid input. Please try again.")
                turn_num -= 1
                continue
        # ход компьютера
        else:
            # считаем номер хода компьютера
            turn_num += 1
            # сообщение
            print("\nStatus: Computer is about to make a move. Press Enter to continue...")
            # комманда компьютера
            input()
            # считать количество частей в змейке и в частях компьютера
            count_nums = Counter(chain(*(computer_pieces + snake)))
            # определить баллы
            scores = list()
            # перебрать все части, чтобы получить очки
            for piece in computer_pieces:
                score = count_nums[piece[0]] + count_nums[piece[1]]
                scores.append(score)
            # сортировать произведения по баллам
            computer_pieces = [x for _, x in sorted(zip(scores, computer_pieces), reverse=True)]
            # заставить компьютер двигаться
            for piece in computer_pieces:
                # проверить, как подключить змейку
                if connection_keys[-1] in piece:
                    turn_func(str(computer_pieces.index(piece) + 1), computer_pieces)
                    break
                elif connection_keys[0] in piece:
                    turn_func(str(-computer_pieces.index(piece) - 1), computer_pieces)
                    break
            # предоставить кость компьютеру
            else:
                turn_func('0', computer_pieces)


if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling()