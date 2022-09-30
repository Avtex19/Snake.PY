import enum
import os

import pygame
import random

pygame.init()


# extensions implemented:
# Forbid 180 degree turns, Scoreboard, Ending Screen, Advanced Scoreboard, Use image for food

class Directions(enum.Enum):
    RIGHT = 'right'
    LEFT = 'left'
    UP = 'up'
    DOWN = 'down'


class Snake:
    VEL = 20
    eatGoldenAppleSound = pygame.mixer.Sound(os.path.join("SnakeFiles/EatingApple .ogg"))

    def __init__(self):
        self.head = pygame.Rect(600, 350, 20, 20)
        self.body = [pygame.Rect(580, 350, 20, 20), pygame.Rect(560, 350, 20, 20), pygame.Rect(540, 350, 20, 20),
                     pygame.Rect(520, 350, 20, 20)]
        self.direction = Directions.RIGHT

    def drawSnake(self, screen):
        for index, singleBody in enumerate(self.body):
            if index == 0:
                pygame.draw.rect(screen, (255, 255, 255), self.head)
            else:
                pygame.draw.rect(screen, (0, 255, 0), singleBody)

    def collision(self, borders):
        for border in borders:
            if self.head.colliderect(border):
                return True

    def moveSnake(self):
        self.changeDirections()
        if self.direction == Directions.RIGHT:
            self.head.x += self.VEL
        if self.direction == Directions.UP:
            self.head.y -= self.VEL
        if self.direction == Directions.LEFT:
            self.head.x -= self.VEL
        if self.direction == Directions.DOWN:
            self.head.y += self.VEL
        self.moveBody()

    def moveBody(self):
        self.body.insert(0, self.head)
        for index in range(len(self.body) - 1, 0, -1):
            self.body[index].x = self.body[index - 1].x
            self.body[index].y = self.body[index - 1].y
        self.body.remove(self.head)

    def addOneBody(self):
        self.body.append(pygame.Rect(self.body[-1].x, self.body[-1].y, 20, 20))

    def changeDirections(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.direction != Directions.DOWN:
                self.direction = Directions.UP
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.direction != Directions.LEFT:
                self.direction = Directions.RIGHT
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.direction != Directions.RIGHT:
                self.direction = Directions.LEFT
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if self.direction != Directions.UP:
                self.direction = Directions.DOWN

    def eatGoldenApple(self, apple):
        if self.head.colliderect(apple):
            self.addOneBody()
            self.eatGoldenAppleSound.play()
            return True

    def eatItself(self):
        for index in range(1, len(self.body) - 1):
            if self.head == self.body[index]:
                return True


class GoldenApple:
    goldenApple = pygame.Rect(random.randint(50, 950), random.randint(150, 550), 40, 40)
    goldenApplePNG = pygame.transform.scale(pygame.image.load("SnakeFiles/GoldenApple.png"), (40, 40))

    def __init__(self):
        self.apple = self.goldenApple

    def drawGoldenApple(self, screen):
        screen.blit(self.goldenApplePNG, (self.apple.x, self.apple.y))

    def changeApplePosition(self):
        self.apple.x = random.randint(50, 1100)
        self.apple.y = random.randint(150, 650)

    def getRectangle(self):
        return self.apple


class App:
    borders = [pygame.Rect(20, 100, 10, 570), pygame.Rect(1170, 100, 10, 580), pygame.Rect(20, 100, 1150, 10),
               pygame.Rect(20, 670, 1150, 10)]
    scoreFont = pygame.font.Font("SnakeFiles/Anton-Regular.ttf", 40)
    score = 0
    highScore = []
    gameStarted = True

    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        self.snake = Snake()
        self.apple = GoldenApple()

    def run(self):
        self.init()
        FPS = 30
        while self.running:
            self.clock.tick(FPS)
            self.render()
            self.update()
            pygame.display.update()
        self.cleanUp()

    def init(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Snake")

        self.clock = pygame.time.Clock()
        self.running = True

    def update(self):
        self.events()
        self.displayScore()
        self.borderCollision()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        self.cleanUp()
        self.drawBorder()
        self.displayHighScore()
        self.snake.drawSnake(self.screen)
        if self.gameStarted:
            self.snake.moveSnake()
        self.apple.drawGoldenApple(self.screen)
        if self.snake.eatGoldenApple(self.apple.getRectangle()):
            self.apple.changeApplePosition()
            self.score += 1

    def cleanUp(self):
        self.screen.fill(0)

    def drawBorder(self):
        for border in self.borders:
            pygame.draw.rect(self.screen, (0, 0, 240), border)

    def displayScore(self):
        scoreText = self.scoreFont.render(f"Score: {self.score}", False, (240, 240, 240))
        self.screen.blit(scoreText, (20, 30))

    def borderCollision(self):
        if self.snake.collision(self.borders) or self.snake.eatItself():
            self.drawEndingScreen()
            self.gameStarted = False
            self.highScore.append(self.score)
            if pygame.key.get_pressed()[pygame.K_r]:
                app = App()
                app.run()
            elif pygame.key.get_pressed()[pygame.K_q]:
                self.running = False

    def displayHighScore(self):
        if len(self.highScore) == 0:
            HighScoreText = self.scoreFont.render(f"High Score:{0}", False,
                                                  (240, 240, 240))
            self.screen.blit(HighScoreText, (980, 30))
        else:
            HighScoreText = self.scoreFont.render(f"High Score:{max(self.highScore)}", False,
                                                  (240, 240, 240))
            self.screen.blit(HighScoreText, (980, 30))

    def drawEndingScreen(self):
        endingScreen = self.scoreFont.render("Game Over!", False, (240, 240, 240))
        self.screen.blit(endingScreen, (450, 200))
        playAgainScreen = self.scoreFont.render("For Play Again - Press R!", False, (240, 240, 240))
        self.screen.blit(playAgainScreen, (450, 300))
        quitGameScreen = self.scoreFont.render("For Quit Game - Press Q!", False, (240, 240, 240))
        self.screen.blit(quitGameScreen, (450, 400))


if __name__ == "__main__":
    app = App()
    app.run()
