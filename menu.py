import random
from datetime import datetime
import os
from game_settings import *
from cursor import cursor, cur
from sound import sound

all_sprites = pygame.sprite.Group()


#функция загрузка спрайтов
def load_image(name, color_key=None):
    fullname = os.path.join('', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        raise FileNotFoundError(f"{fullname}")
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image

# функция создания частиц
def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))

# класс частиц
class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    try:
        fire = [load_image("./data/star/star.png", -1)]
    except:
        print('Не найден графический файл звёзд !')
        sys.exit()

    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость - это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой
        self.gravity = gravity

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()

# класс меню
class Menu:
    def __init__(self, menu_item):
        self.menu_item = menu_item

    def render(self, screen, font, num_menu_item):
        try:
            font = pygame.font.Font('fonts/Maestroc.otf', 60)
        except:
            print('Не найден файл шрифта !')
            sys.exit()

        screen.blit(font.render('Liu Kang Adventures in city Vladimir', 1, 'red'), (300, 100))

        try:
            font = pygame.font.Font('fonts/Asessorc.otf', 30)
        except:
            print('Не найден файл шрифта !')
            sys.exit()
        screen.blit(font.render('Copyright 2021-2022', 1, 'green'), (450, 700))

        try:
            font = pygame.font.Font('fonts/Acsiomasupershockc.otf', 50)
        except:
            print('Не найден файл шрифта !')
            sys.exit()

        for i in self.menu_item:
            if num_menu_item == i[5]:
                screen.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                screen.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    #функция создания меню
    def menu(self):
        sound.stop("game_over")
        sound.play('Lymez', 10, 0.3)
        active_menu = True
        pygame.key.set_repeat(0, 0)
        font_menu = pygame.font.Font('fonts/Acsiomasupershockc.otf', 50)
        menu_item = 0
        while active_menu:
            screen.fill((0, 100, 200))
            mouse_coords = pygame.mouse.get_pos()

            for i in self.menu_item:
                if i[0] < mouse_coords[0] < i[0] + 155 \
                        and i[1] < mouse_coords[1] < i[1] + 50:
                    menu_item = i[5]

            self.render(screen, font_menu, menu_item)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if menu_item == 0:
                            sound.stop('Lymez')
                            active_menu = False
                        if menu_item == 1:
                            sys.exit()
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_UP:
                        if menu_item > 0:
                            menu_item -= 1
                    if event.key == pygame.K_DOWN:
                        if menu_item < len(self.menu_item) - 1:
                            menu_item += 1
                if event.type == pygame.MOUSEMOTION:
                    cur.rect = event.pos
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if menu_item == 0:
                        sound.stop('Lymez')
                        active_menu = False
                    if menu_item == 1:
                        rules()
                    if menu_item == 2:
                        score()
                    if menu_item == 3:
                        sys.exit()

            if pygame.mouse.get_focused():
                cursor.draw(screen)

            else:
                position = (random.randint(0, screen_width), random.randint(0, screen_height))
                create_particles(position)

            all_sprites.draw(screen)
            all_sprites.update()
            clock1.tick(fps)

            pygame.display.update()


# класс экрана DIED
class EndMenu:
    def __init__(self, menu_items):
        self.menu_items = menu_items

    def render(self, screen, font, num_menu_item):
        font = pygame.font.SysFont("Times new Roman", 120)
        screen.blit(font.render("YOU DIED", 1, "red"), (312, 220))

        font = pygame.font.SysFont("Times New Roman", 30)

        for i in self.menu_items:
            if num_menu_item == i[5]:
                screen.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                screen.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        active_menu = True
        pygame.key.set_repeat(0, 0)
        font_menu = pygame.font.SysFont('Times New Roman', 50)
        menu_item = 0
        while active_menu:
            sound.stop("game4")
            screen.fill((0, 0, 0))
            mouse_coords = pygame.mouse.get_pos()

            if pygame.mouse.get_focused():
                cursor.draw(screen)

            for i in self.menu_items:
                if i[0] < mouse_coords[0] < i[0] + 150 \
                        and i[1] < mouse_coords[1] < i[1] + 50:
                    menu_item = i[5]

            self.render(screen, font_menu, menu_item)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if menu_item == 0:
                            active_menu = False
                            menu.menu()
                        if menu_item == 1:
                            sys.exit()
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_UP:
                        if menu_item > 0:
                            menu_item -= 1
                    if event.key == pygame.K_DOWN:
                        if menu_item < len(self.menu_items) - 1:
                            menu_item += 1
                if event.type == pygame.MOUSEMOTION:
                    cur.rect = event.pos
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if menu_item == 0:
                        active_menu = False
                        menu.menu()
                    if menu_item == 1:
                        sys.exit()

            if pygame.mouse.get_focused():
                cursor.draw(screen)

            pygame.display.update()


# функция отображения экрана правил
def rules():
    try:
        font = pygame.font.Font('fonts/KhakiStd1.otf', 40)
    except:
        print('Не найден файл шрифта !')
        sys.exit()

    active_menu = True
    while active_menu:
        screen.fill((0, 100, 200))

        screen.blit(font.render('Hello! This rules of game:', 3, 'red'), (50, 100))
        screen.blit(font.render('', 3, 'red'), (50, 150))
        screen.blit(font.render('Control Hero: W,A,S,D,Space', 1, 'red'), (50, 200))
        screen.blit(font.render('Exit from menu : ESCAPE', 1, 'red'), (50, 250))
        screen.blit(font.render('It is impossible to close the game during the passage of the level,', 1, 'red'), (50, 300))
        screen.blit(font.render('it is necessary to find the finish', 1, 'red'), (50, 350))
        screen.blit(font.render('', 3, 'red'), (50, 400))
        screen.blit(font.render('Thanks !!!', 1, 'red'), (50, 450))
        screen.blit(font.render('', 3, 'red'), (50, 500))
        screen.blit(font.render('When you move the cursor behind the menu screen, stars are made', 1, 'red'), (50, 550))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                active_menu = False
            if event.type == pygame.MOUSEMOTION:
                cur.rect = event.pos

        if pygame.mouse.get_focused():
            cursor.draw(screen)

        else:
            position = (random.randint(0, screen_width), random.randint(0, screen_height))
            create_particles(position)

        all_sprites.draw(screen)
        all_sprites.update()
        clock1.tick(fps)

        pygame.display.update()


# функция отображения экрана лучших игр из БД
def score():
    try:
        font = pygame.font.Font('fonts/Agitpropc.otf', 30)
    except:
        print('Не найден файл шрифта !')
        sys.exit()

    result = connection.cursor()
    result = result.execute("SELECT id, date, score FROM results").fetchall()
    result = sorted(result, key=lambda x: x[0], reverse=True)

    active_menu = True
    while active_menu:
        screen.fill((0, 100, 200))
        i = 0
        pygame.draw.line(screen, pygame.Color('white'), (64, 64 * i + 64), (screen_width - 64, 64 * i + 64), 5)

        columns_name = ['Date and time', 'Score']
        for i in range(2):
            name = columns_name[i]
            naimenovania = font.render(name, 1, pygame.Color('yellow'))
            naimenovania_rect = naimenovania.get_rect()
            naimenovania_rect.x = 500 * i + 128
            naimenovania_rect.y = 64 + 12
            screen.blit(naimenovania, naimenovania_rect)

        for i in range(9):
            pygame.draw.line(screen, pygame.Color('white'), (64, 64 * (i + 1) + 64),
                             (screen_width - 64, 64 * (i + 1) + 64), 5)

            if i < 8:
                for k in range(2):
                    text_rend = font.render(str(result[i][k + 1]), 1, pygame.Color('yellow'))
                    text_rect = text_rend.get_rect()
                    text_rect.x = 500 * k + 128
                    text_rect.y = (64 * (i + 1) + 76)
                    screen.blit(text_rend, text_rect)

            for k in range(3):
                pygame.draw.line(screen, pygame.Color('white'), (535 * k + 64, 64 * i + 64),
                                 (535 * k + 64, 64 * (i + 1) + 64), 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                active_menu = False
            if event.type == SHOOTING_EVENT:
                position = (random.randint(0, screen_width), random.randint(0, screen_height))
                create_particles(position)
            if event.type == pygame.MOUSEMOTION:
                cur.rect = event.pos

        if pygame.mouse.get_focused():
            cursor.draw(screen)

        all_sprites.draw(screen)
        all_sprites.update()
        clock1.tick(fps)

        pygame.display.update()

# функция отображения результатов прохождения уровня и записи их в БД
def result_level(coins, lifes, enemy_kill):
    coin = coins
    life = lifes
    enemy = enemy_kill
    score = coins + life + enemy_kill

    #запись набранных очков в БД
    result = connection.cursor()

    now_date = datetime.now()
    day = str(now_date.day)
    month = str(now_date.month)
    year = str(now_date.year)
    hour = str(now_date.hour)
    minute = str(now_date.minute)

    zapis = f'{day}.{month.rjust(2, "0")}.{year} ' f'{hour.rjust(2, "0")}:{minute.rjust(2, "0")}'

    result.execute('INSERT INTO results(date, score) VALUES(?, ?)', (zapis, score))
    connection.commit()
    result.close()

    sound.play('game3', 10, 0.3)
    try:
        font = pygame.font.Font('fonts/Asessorc.otf', 40)
    except:
        print('Не найден файл шрифта !')
        sys.exit()

    active_result_level = True
    while active_result_level:
        screen.fill((0, 100, 200))

        screen.blit(font.render('Результаты прохождения уровня:', 3, 'yellow'), (300, 100))
        screen.blit(font.render(f'Вы заработали {score} очков', 1, 'yellow'), (300, 200))
        screen.blit(font.render(f'Количество собранных монет: {coin}', 1, 'yellow'), (300, 300))
        screen.blit(font.render('Количество убитых врагов: 0', 1, 'yellow'), (300, 400))
        screen.blit(font.render(f'Количество оставшегося здоровья: {life}', 1, 'yellow'), (300, 500))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                sound.stop('game3')
                active_result_level = False
            if event.type == SHOOTING_EVENT:
                position = (random.randint(0, screen_width), random.randint(0, screen_height))
                create_particles(position)
            if event.type == pygame.MOUSEMOTION:
                cur.rect = event.pos

        if pygame.mouse.get_focused():
            cursor.draw(screen)

        all_sprites.draw(screen)
        all_sprites.update()
        clock1.tick(fps)

        pygame.display.update()


# создание меню

menu_items = [(510, 210, u'Game', 'yellow', 'blue', 0),
              (520, 280, u'Rules', 'yellow', 'green', 1),
              (530, 350, u'Best', 'yellow', 'brown', 2),
              (530, 420, u'Quit', 'yellow', 'black', 3)]
end_menu_items = [(515, 500, u'Back to Menu', 'white', 'red', 0),
                  (575, 550, u'Exit', 'white', 'red', 1)]
end_menu = EndMenu(end_menu_items)
menu = Menu(menu_items)
