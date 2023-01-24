import pygame
import os
import sys
import random
from board import Board
import time


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def finish(points):
    ans = False
    for i in range(len(points)):
        for j in range(len(points[0])):
            if points[i][j][0] == 'black':
                ans = True
                break
        if ans:
            break
    return ans


def circle(x, y, color):
    pygame.draw.circle(screen, color, (x, y), 12)


def proverka(points):
    double = [[0, 0]]
    answer = list()
    act_color = points[0][0][0]
    for x in range(9):
        for y in range(9):
            if act_color == points[x][y][0] and points[x][y][0] != 'black':
                double.append([x, y])
            else:
                if len(answer) < len(double):
                    answer.clear()
                    for h in double:
                        answer.append(h.copy())

                act_color = points[x][y][0]
                double.clear()
                double.append([x, y])
        if len(answer) >= 5:
            return answer
    for y in range(9):
        for x in range(9):
            if act_color == points[x][y][0] and points[x][y][0] != 'black':
                double.append([x, y])
            else:
                if len(answer) < len(double):
                    answer.clear()
                    for h in double:
                        answer.append(h.copy())
                act_color = points[x][y][0]
                double.clear()
                double.append([x, y])
        if len(answer) >= 5:
            return answer
    return None


class Lines(Board):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.answer = None
        self.width = w  # высота сетки в клетках
        self.height = h  # ширина сетки в клетках
        self.board = [[1] * w for _ in range(h)]  # используется в поиске прохода шарика
        self.color = [[['black', False]] * w for _ in range(h)]  # статус каждой клетки (цвет кружка)
        self.left = 10  # отступ слева
        self.top = 10  # отступ сверху
        self.cell_size = 30  # сторона клетки
        self.active = False  # есть ли выбранный кружочек
        self.act_col = 'black'  # цвет выбранного шарика
        self.coords = [99, 99]  # координаты выбранного кружочка
        self.num = 1  # расстояние от А к В
        self.balls = [(104, 227, 219), (147, 74, 181), (58, 186, 47),
                      (240, 171, 67), (237, 240, 77), (4, 105, 219), (255, 99, 211)]  # список цетов шариков
        self.result = 0
        self.end = False
        self.hint = [random.choice(self.balls) for _ in range(3)]

    # анимация передвижения шарика
    def go(self, other, x, y):
        self.active = False
        last_point = [y, x]
        chod = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        answer = list()
        while self.num != 'A':
            for i in range(4):
                new_x = last_point[0] + chod[i][0]
                new_y = last_point[1] + chod[i][1]
                if 0 <= new_x < self.height and 0 <= new_y < self.width:
                    if self.num - 1 == 0:
                        self.num = 'A'
                        break
                    elif self.board[new_x][new_y] == self.num - 1:
                        last_point = [new_x, new_y]
                        answer.append([new_x, new_y])
                        self.num -= 1
                        break

        # выше этого коммента это нахождения кратчайшего пути
        answer.append([self.coords[1], self.coords[0]])
        answer.reverse()
        clock = pygame.time.Clock()
        for i in range(len(answer)):
            self.color[answer[i][0]][answer[i][1]] = [self.act_col, True]
            screen.fill((120, 120, 120))
            other.drawing(screen, True)
            clock.tick(15)
        for i in range(len(answer)):
            self.color[answer[i][0]][answer[i][1]] = ['black', False]
        screen.fill((120, 120, 120))
        other.drawing(screen, True)
        self.color[y][x] = [self.act_col, False]
        other.drawing(screen)

    # изменение статуса клетки - активна или нет
    def on_click(self, cell_coords, other):
        x = cell_coords[1]
        y = cell_coords[0]
        if self.color[x][y][0] == 'black' and self.active:
            ans = other.has_path(self.coords[1], self.coords[0], x, y)
            if ans:
                other.go(other, y, x)
                self.active = False
                self.coords = [99, 99]
                self.act_col = 'black'
                time.sleep(0.5)
                other.chod()
        elif self.color[x][y][0] != 'black':
            self.active = True
            self.coords = [y, x]
            self.act_col = self.color[x][y][0]

    # проверяет наличие пути от A к В
    def has_path(self, x1, y1, x2, y2):
        points = [[x1, y1]]
        self.board = list()
        chod = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        for x in range(len(self.color)):
            meg = list()
            for y in range(len(self.color[0])):
                if x == x1 and y == y1:
                    meg.append('A')
                elif x == x2 and y == y2:
                    meg.append('B')
                else:
                    if self.color[x][y][0] != 'black':
                        meg.append(-1)
                    else:
                        meg.append(0)
            self.board.append(meg)
        self.num = 1
        run = True
        while run:
            new = list()
            last_map = list()
            for h in self.board:
                k = h.copy()
                last_map.append(k)
            for x in range(len(points)):
                if run:
                    for y in range(4):
                        new_x = points[x][0] + chod[y][0]
                        new_y = points[x][1] + chod[y][1]
                        if 0 <= new_x < self.height and 0 <= new_y < self.width:
                            if last_map[new_x][new_y] == 0:
                                last_map[new_x][new_y] = self.num
                                new.append([new_x, new_y])
                            elif last_map[new_x][new_y] == 'B':
                                return True
            if last_map == self.board:
                return False
            else:
                self.num += 1
                points = new.copy()
                self.board = last_map

    def new_game(self):
        f = open('rekord.txt', encoding='utf-8')
        line = f.readlines()[0]
        if self.result > int(line):
            open('rekord.txt', 'w').write(str(self.result))
        f.close()
        self.end = False
        self.result = 0
        for i in range(self.height):
            for j in range(self.width):
                self.color[i][j] = ['black', False]

    def chod(self):
        delet = proverka(self.color)
        if delet is not None:
            self.result += len(delet)
            for i in range(len(delet)):
                self.color[delet[i][0]][delet[i][1]][0] = ['black', False]
            delet.clear()
        else:
            numi = 0
            for i in range(self.height):
                for j in range(self.width):
                    if self.color[i][j][0] == 'black':
                        numi += 1
            c = 0
            if numi >= 3:
                fin = 3
            else:
                fin = numi
            while c != fin:
                x = random.randrange(self.height)
                y = random.randrange(self.width)
                if self.color[x][y][0] == 'black':
                    self.color[x][y] = [self.hint[c], False]
                    c += 1
        delet = proverka(self.color)
        if delet is not None:
            self.result += len(delet)
            for i in range(len(delet)):
                self.color[delet[i][0]][delet[i][1]] = ['black', False]
        self.hint = [random.choice(self.balls) for _ in range(3)]

    def render(self, sc):
        board = Lines(self.width, self.height)
        board.set_view(10, 10, 50)
        running = True
        board.chod()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if board.get_cell(event.pos) is not None:
                        board.on_click(board.get_cell(event.pos), board)
                        k = finish(board.color)
                        if not k:
                            board.end = True
                    elif 490 <= event.pos[0] <= 621 and 10 <= event.pos[1] <= 50:
                        board.new_game()
                        board.chod()
                    elif 490 <= event.pos[0] <= 670 and 60 <= event.pos[1] <= 100:
                        board.chod()
                        board.chod()
                        k = finish(board.color)
                        if not k:
                            board.end = True
            sc.fill((120, 120, 120))
            board.drawing(sc)
            pygame.display.flip()

    def drawing(self, sc, way=False):
        for i in range(self.height):
            for j in range(self.width):
                if [j, i] == self.coords:
                    pygame.draw.rect(sc, (100, 100, 100),
                                     (j * self.cell_size + self.left, i * self.cell_size + self.top,
                                      self.cell_size, self.cell_size))
                if self.color[i][j][0] != 'black':
                    if self.color[i][j][1]:
                        circle(j * self.cell_size + self.left + self.cell_size // 2,
                               i * self.cell_size + self.top + self.cell_size // 2, self.color[i][j][0])
                    else:
                        pygame.draw.circle(sc, self.color[i][j][0],
                                           (j * self.cell_size + self.left + self.cell_size // 2,
                                            i * self.cell_size + self.top + self.cell_size // 2),
                                           self.cell_size // 2 - 4)
                pygame.draw.rect(sc, 'white', (j * self.cell_size + self.left, i * self.cell_size + self.top,
                                               self.cell_size, self.cell_size), 1)
        font = pygame.font.Font(None, 30)
        text = font.render("Новая игра", True, (0, 0, 0))
        text_w = text.get_width()
        text_h = text.get_height()
        image = load_image('button.png')
        image1 = pygame.transform.scale(image, (text_w + 20, text_h + 20))
        screen.blit(image1, (490, 10))
        screen.blit(text, (500, 20))
        font = pygame.font.Font(None, 30)
        text = font.render("Счёт:" + str(self.result), True, (0, 0, 0))
        screen.blit(text, (500, 140))
        font = pygame.font.Font(None, 30)
        text = font.render("Пропустить ход", True, (0, 0, 0))
        text_w = text.get_width()
        text_h = text.get_height()
        image = load_image('button.png')
        image1 = pygame.transform.scale(image, (text_w + 20, text_h + 20))
        screen.blit(image1, (490, 60))
        screen.blit(text, (500, 70))
        f = open('rekord.txt', encoding='utf-8')
        line = f.readlines()[0]
        if self.result > int(line):
            open('rekord.txt', 'w').write(str(self.result))
        f.close()
        text = font.render("Рекорд:" + line, True, (0, 0, 0))
        screen.blit(text, (500, 160))
        text = font.render("Подсказка", True, (0, 0, 0))
        screen.blit(text, (500, 190))
        f.close()
        circle(515, 220, self.hint[0])
        circle(545, 220, self.hint[1])
        circle(575, 220, self.hint[2])
        if self.end:
            font = pygame.font.Font(None, 30)
            text = font.render("Игра окончена!", True, (0, 0, 0))
            screen.blit(text, (500, 300))
        font = pygame.font.Font(None, 20)
        text = font.render("Автор: Атапина Полина из ЯЛицея", True, (0, 0, 0))
        screen.blit(text, (470, 450))
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 700, 470
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Игра "lines"')
    screen.fill((150, 150, 150))
    bord = Lines(9, 9)
    bord.render(screen)
    pygame.display.flip()
    pygame.quit()
