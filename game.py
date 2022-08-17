from random import randint, choice

f = open('start.txt', 'r', encoding='utf8')
text = f.read()
f.close()

def print_mas(mas):
    '''Преобразовывает массив, сотоящий из кодов, в символы.'''
    for row in mas:
        for i in row:
            print(chr(i), end='\t')
        print()

def realize_field(mas):
    '''Ставит коды ограждений в массиве.'''
    for j in range(len(mas)):
        for i in range(len(mas[0])):
            if j==0 and 0<i<9 or j==9 and 0<i<9:
                mas[j][i]=9552                          #Растановка горизонтальных палок
            if 0<j<9 and i==0 or 0<j<9 and i==9:
                mas[j][i]=9553                          #Растановка вертикальных палок
            if 0<j<9 and 0<i<9:
                mas[j][i]=32                             #Растановка пустых клеток
            if j==0 and i==0 or j==9 and i==0:           #Растановка левых углов
                if j==0:
                    mas[j][i]=9556
                if j==9:
                    mas[j][i]=9562
            if j==0 and i==9 or j==9 and i==9:           #Растановка правых углов
                if j==0:
                    mas[j][i]=9559
                if j==9:
                    mas[j][i]=9565
    return mas

def random_apples(mas):
    '''Рандомная растановка яблок и установка игрока в массиве.'''
    count_all = 0
    while count_all != 16:
        j = randint(1, len(mas) - 1)
        i = randint(1, len(mas[0]) - 1)

        if mas[j][i]==32:
            mas[j][i]=9679          #Установка яблока
            count_all += 1
    mas[4][4] = 9786                                #Установка игрока
    return mas

def random_killers(mas):
    '''Рандомная растановка врагов в массиве.'''
    count_all = 0
    killers = []
    while count_all != 4:
        j = randint(1, len(mas)-1)
        i = randint(1, len(mas[0])-1)
        if mas[j][i] == 32:
            mas[j][i] = 9967
            killer = [j, i]
            count_all += 1
            killers.append(killer)
    return mas, killers

    # for j in range(len(mas)):
    #     count_row = 0
    #     killer = []
    #     for i in range(0, len(mas[0]), 2):
    #         if count_row==1:
    #             break
    #         if 0<j<9 and 0<i<9 and mas[j][i]==32:
    #             mas[j][i]=9967          #Установка врага
    #             count_all += 1
    #             killer.append(j)
    #             killer.append(i)
    #             count_row += 1
    #             killers.append(killer)
    #     if count_all==4:                           #Максимальное количество врагов на поле
    #         break
    # mas[4][4] = 9786  # Установка игрока
    # return mas, killers

def random_wall(mas):
    '''Рандомная растановка стенок в массиве.'''
    count_all = 0
    while count_all != 9:
        j = randint(1, len(mas) - 1)
        i = randint(1, len(mas[0]) - 1)
        if mas[j][i]==32:
            mas[j][i]=choice([9553, 9552])       #Установка ограждения
            count_all += 1

    return mas

def apples_in_mas(mas):
    '''Подсчет яблок на поле.'''
    res = 0
    for i in range(len(mas)):
        for j in range(len(mas[0])):
            if mas[i][j] == 9679:
                res += 50
    return res

def killers_step(mas, killers):
    '''Каждый киллер с координатами в списке шагает на новую позицию,
     функция возвращает новый массив и список с координатами'''
    # Шаг врагов на новое положение
    for killer in killers:
        old_killer = [killer[0], killer[1]]
        killer[randint(0, 1)] += 1

        # Проверка на расположение killer относительно яблок, игрока и стенок
        if mas[killer[0]][killer[1]] == 9679 or mas[killer[0]][killer[1]] == 9552 or mas[killer[0]][killer[1]] == 9553 or mas[killer[0]][killer[1]] == 9786:
            killer = old_killer  #Ничего не происходит
        else:
            #Шаг врага
            mas[killer[0]][killer[1]], mas[old_killer[0]][old_killer[1]] = mas[old_killer[0]][old_killer[1]], mas[killer[0]][killer[1]]
    return mas, killers

def good(mas, user):
    '''Проверяет положение тела относительно ограждений, если тело находиться в притык,
     то при шаге его броает на самую дальнюю точку позади него.'''
    long_weight = len(mas[0])-1
    long_hight = len(mas)-1
    #user = [высота, длина]
    if user[0] == 0:
        user[0] = long_hight - 1
    elif user[0] == long_hight:
        user[0] = 1
    elif user[1] == 0:
        user[1] = long_weight-1
    elif user[1] == long_weight:
        user[1] = 1
    return user

def go_to(inp, mas, user):
    '''Движение игрока параметром(1-влево,2-вверх,3-вниз,4-вправо) '''
    # Движение влево
    old_user = [user[0], user[1]]
    if inp == 1:  # Движение влево
        user[1] = user[1] - 1
    elif inp == 2:  # Движение вверх
        user[0] = user[0] - 1
    elif inp == 3:  # Движение вниз
        user[0] = user[0] + 1
    elif inp == 4:  # Движение вправо
        user[1] = user[1] + 1
    else:
        print('Ты нажал не ту клавишу....0_о...')
    return
    user = good(mas, user)  # Проверка на расположение игрока относително границ поля

    # Шаг игрока на новое положение
    mas[user[0]][user[1]], mas[old_user[0]][old_user[1]] = mas[old_user[0]][old_user[1]], mas[user[0]][user[1]]
    print(mas)
    print(user)
    return (mas, user)

print(text)
while True:
    if input()=='':
        break
    else:
        print('Ты нажал не на ту клавишу...0_О...')

mas = [[1 if i==0 or i==9 or j==0 or j==9 else 0 for i in range(0, 10)] for j in range(0, 10)]

#Растановка границ поля
mas = realize_field(mas)

#Рандомное раставление стенок в поле
mas = random_wall(mas)


# Рандомное раставление яблок в поле
mas = random_apples(mas)

#Рандомная растановка врагов
mas, killers = random_killers(mas)

print_mas(mas)

# user = [столбец, строка] - начальное положение игрока
user = [4, 4]
score = 0

# Количесто яблок в массиве для условия выигрыша
apples = apples_in_mas(mas)

#Запуск
while True:
    inp = input()
    old_user = [user[0], user[1]]                   #Cтарое положение игрока

    if inp == 'A' or inp == 'a' or inp == 'Ф' or inp == 'ф':  # Движение влево
        user[1] = user[1] - 1
    elif inp == 'W' or inp == 'w' or inp == 'Ц' or inp == 'ц':  # Движение вверх
        user[0] = user[0] - 1
    elif inp == 'Ы' or inp == 'ы' or inp == 'S' or inp == 's':  # Движение вниз
        user[0] = user[0] + 1
    elif inp == 'D' or inp == 'd' or inp == 'В' or inp == 'в':  # Движение вправо
        user[1] = user[1] + 1
    else:
        print('Ты нажал не ту клавишу....0_о...')
    user = good(mas, user)                                     # Проверка на расположение игрока относително границ поля

    if mas[user[0]][user[1]] == 9679:           #Проверка на расположение игрока относительно яблок
        score += 50
        mas[user[0]][user[1]] = 32                                          #Съедание яблок


    if mas[user[0]][user[1]] == 9967:           #Проверка на расположение игрока относительно врагов
        mas[old_user[0]][old_user[1]] = 32
        print("Ты програл, тебя сьели........-_-......")
        print_mas(mas)
        break                                           #Съедание игрока

    if mas[user[0]][user[1]] == 9552 or mas[user[0]][user[1]] == 9553:           #Проверка на расположение игрока относительно врагов
        print("Ты не можешь туда шагнуть...там вообще-то стена......-_-......")
        print_mas(mas)
        user = old_user
        continue

    # Шаг игрока на новое положение
    mas[user[0]][user[1]], mas[old_user[0]][old_user[1]] = mas[old_user[0]][old_user[1]], mas[user[0]][user[1]]

    print_mas(mas)
    print(f'{score} очков')
    if apples == score:
        print('Поздравляю, ты выиграл!')
        break