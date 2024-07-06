import os
import random
import time
import logging

from dotenv import load_dotenv

from fingercounter.imgmodule import get_fingers

load_dotenv()

DATA_PLAYERS = []
ROLES = ['innocent', 'innocent', 'mafia', 'doctor', 'commissar']


def win():
    n_m = 0
    n_i = 0
    for i in DATA_PLAYERS:
        if i.role == 'mafia' and i.is_alive:
            n_m += 1
        elif i.is_alive:
            n_i += 1
    if n_m >= n_i:
        return 'mafia'
    elif n_m == 0:
        return 'innocent'
    else:
        return 'noone'


def get_sums():
    n_m = 0
    n_i = 0
    for i in DATA_PLAYERS:
        if i.role == 'mafia' and i.is_alive:
            n_m += 1
        elif i.is_alive:
            n_i += 1
    return n_m, n_i


class Player:
    def __init__(self, role: str, is_alive: bool, player_id: int):
        self.role = role
        self.is_alive = is_alive
        self.player_id = player_id

    def get_role(self):
        return self.role

    def kill(self):
        if self.is_alive:
            if self.role == 'mafia':
                raise ZeroDivisionError
            self.is_alive = False
            return self.player_id
        else:
            raise ValueError

    def kick(self):
        if self.is_alive:
            self.is_alive = False
        else:
            raise ValueError


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    n = int(os.getenv("NUM_PLAYERS"))
    speak_time = int(os.getenv("SPEAK_TIME"))
    os.system('say игра начинается пидоры')
    print('the game begins\n')
    random.shuffle(ROLES)
    for i in range(1, n + 1):
        DATA_PLAYERS.append(Player(role=ROLES[i - 1], is_alive=True, player_id=i))

    os.system('say сейчас буду раздавать вам роли выколите свои ебаные глазки у вас 10 секунд')
    time.sleep(1)
    for i in range(1, n + 1):
        print(f'\rигрок номер {i} твоя роль {DATA_PLAYERS[i - 1].get_role().upper()} закрой глаза как прочитаешь это',
              end='')
        os.system(f'say игрок номер {i} открывает глаза и смотрит свою жалку роль в обществе пидорасов')
        if random.random() > 0.7:
            os.system('say ахахахахаххаха мирный долбоеб его пиздить первым')
        time.sleep(1)
    print(f'\rвсе получили свои роли\n', end='')
    os.system(f'say теперь все знают что вы пидоры аххаахвазрзварзва')

    lap = 1

    # day
    while win() == 'noone':
        os.system(f'say {lap}ой день начинается')
        for i in range(n):
            os.system(f'say игрок номер {(i + lap) % (n + 1)} начинает свою речь')
            time.sleep(speak_time + speak_time * 0.5 * (lap - 1))
            os.system(f'say заебал пиздеть')
        # voting
        if lap != 1:
            os.system(f'say ГОЛОСОВАНИЕ')
            idx = int(input('\nвведите номер игрока которого кикнули нахуй'))
            if idx != -1:
                try:
                    DATA_PLAYERS[idx - 1].kick()
                    os.system(f'say вы исключили игрока номер {idx}')
                except ValueError:
                    os.system('say тайлер дерден был убит')
        if win() != 'noone':
            break
        if get_sums()[0] == 1 and get_sums()[1] == 2:
            os.system('say ебать вы мирные лохи среди вас троих мафия так что ищите его псы')
        else:
            # night
            os.system(f'say заебали все пиздеть начинается ночь вам пизда закрывайте ебаные глаза у вас 10 секунд')
            time.sleep(10)
            # mafia
            os.system(f'say мафия открывает глаза но не пиздак и показывает в камеру номер игрока котого хочет кокнуть')
            time.sleep(3)
            os.system(f'say мафия целится в игрока номер {random.randint(1, n)}')
            cnt = get_fingers()
            try:
                DATA_PLAYERS[cnt - 1].kill()
                os.system('say мафия сделала килл')
            except ValueError:
                os.system(f'say мафия вообще долбоеб стреляет по тайлеру дёрдену')
            except ZeroDivisionError:
                os.system(f'say АХПХВАРХВАРХАХР МАФИЯ ЗАСТРЕЛИЛАСЬ')
                break
            os.system(f'say мафия закрывает глаза')
            time.sleep(10)
            # doctor
            os.system('say врач открывает глаза')
            time.sleep(3)
            cnt = get_fingers()
            DATA_PLAYERS[cnt - 1].is_alive = True
            os.system('say врач сейвит бедолагу и засыпает нахуй')
            time.sleep(10)
            # commissar
            os.system(f'say мусор открывает глаза')
            time.sleep(3)
            cnt = get_fingers()
            if DATA_PLAYERS[cnt - 1].role == 'mafia':
                print('ОН ЕБАНАЯ МАФИЯ', end='')
            else:
                print('дефолтный нефор', end='')
            print('\r', end='')
            time.sleep(5)
            os.system('say мусор засыпает')
            time.sleep(10)
            # status
            os.system('say ночь кончилась просыпайтесь нахуй')
            time.sleep(5)
            for i in range(n):
                os.system(f'say игрок номер {i + 1} {'живой' if DATA_PLAYERS[i].is_alive else 'нафидил'}')
                time.sleep(1)
            os.system('say минута молчания в честь умерших')
            time.sleep(10)

        lap += 1
