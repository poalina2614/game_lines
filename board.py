import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[1] * width for _ in range(height)]
        self.color = [['black'] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        pos_x = mouse_pos[0]
        pos_y = mouse_pos[1]
        if pos_x > self.width * self.cell_size + self.left or pos_y > self.height * self.cell_size + self.top:
            return None
        else:
            pos_x -= self.left
            pos_x //= self.cell_size
            pos_y -= self.top
            pos_y //= self.cell_size
            return pos_x, pos_y

    def on_click(self, cell_coords):
        x = cell_coords[0]
        y = cell_coords[1]
        if self.color[y][x] == 'black':
            self.color[y][x] = 'red'
        elif self.color[y][x] == 'red':
            self.color[y][x] = 'blue'
        else:
            self.color[y][x] = 'black'

    def render(self, sc):
        board = Board(5, 7)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if board.get_cell(event.pos) is not None:
                        board.on_click(board.get_cell(event.pos))
            sc.fill((0, 0, 0))
            board.drawing(sc)
            pygame.display.flip()

    def drawing(self, sc):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(sc, self.color[i][j], (j * self.cell_size + self.left, i * self.cell_size + self.top,
                                                        self.cell_size, self.cell_size))
                pygame.draw.rect(sc, 'white', (j * self.cell_size + self.left, i * self.cell_size + self.top,
                                               self.cell_size, self.cell_size), self.board[i][j])
        pygame.display.flip()

