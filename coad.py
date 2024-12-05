import random
import sys
import os
import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT
FPS=32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'pics/bd.png'
BACKGROUND = 'pics/bg.png'
PIPE = 'pics/pipe.png'
SPACE = 'pics/space.png'


def welcomeScreen():
  playerx = int(SCREENWIDTH / 6)
  playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
  messagex = 43
  GAME_SOUNDS['swoosh'].play()

  while True:
    for event in pygame.event.get():
      if event.type == QUIT or (event.type == KEYDOWN
                                and event.key == K_ESCAPE):
        pygame.quit()
        sys.exit()
      elif event.type == KEYDOWN and (event.key == K_SPACE
                                      or event.key == K_UP):
        return
      else:
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        SCREEN.blit(GAME_SPRITES['message'], (messagex, 30))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        SCREEN.blit(GAME_SPRITES['space'], (70, 150))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def mainGame():
  score = 0
  playerx = int(SCREENWIDTH / 5)
  playery = int(SCREENWIDTH / 2)
  newPipe1 = getRandomPipe()
  newPipe2 = getRandomPipe()

  upperPipes = [{
      'x': SCREENWIDTH + 200,
      'y': newPipe1[0]['y']
  }, {
      'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2),
      'y': newPipe2[0]['y']
  }]

  lowerPipes = [{
      'x': SCREENWIDTH + 200,
      'y': newPipe1[1]['y']
  }, {
      'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2),
      'y': newPipe2[1]['y']
  }]

  pipeVelx = -4
  playerVelY = -9
  playerMaxVelY = 10
  playerAccY = 1
  playerFlapAcc = -8
  playerFlapped = False

  while True:
    for event in pygame.event.get():
      if event.type == QUIT or (event.type == KEYDOWN
                                and event.key == K_ESCAPE):
        pygame.quit()
        sys.exit()
      elif event.type == KEYDOWN and (event.key == K_SPACE
                                      or event.key == K_UP):
        if playery > 0:
          playerVelY = playerFlapAcc
          playerFlapped = True
          GAME_SOUNDS['wing'].play()

    crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
    if crashTest:
      GAME_SOUNDS['swoosh'].stop()
      while True:
        for event in pygame.event.get():
          if event.type == QUIT or (event.type == KEYDOWN
                                    and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
          if event.type == KEYDOWN and (event.key == K_SPACE
                                        or event.key == K_UP):
            return
        SCREEN.blit(GAME_SPRITES['space'], (70, SCREENHEIGHT / 2))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
    for pipe in upperPipes:
      pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
      if pipeMidPos <= playerMidPos < pipeMidPos + 4:
        score += 1
        GAME_SOUNDS['point'].play()

    if playerVelY < playerMaxVelY and not playerFlapped:
      playerVelY += playerAccY

    if playerFlapped:
      playerFlapped = False
    playerHeight = GAME_SPRITES['player'].get_height()
    playery = playery + min(playerVelY, SCREENHEIGHT - playery - playerHeight)

    for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
      upperPipe['x'] += pipeVelx
      lowerPipe['x'] += pipeVelx

    if 0 < upperPipes[0]['x'] < 5:
      newPipe = getRandomPipe()
      upperPipes.append(newPipe[0])
      lowerPipes.append(newPipe[1])

    if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
      upperPipes.pop(0)
      lowerPipes.pop(0)

    SCREEN.blit(GAME_SPRITES['background'], (0, 0))
    for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
      SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
      SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
    SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

    myDigits = [int(x) for x in list(str(score))]
    width = 0
    for digit in myDigits:
      width += GAME_SPRITES['numbers'][digit].get_width()
    Xoffset = (SCREENWIDTH - width) / 2
    for digit in myDigits:
      SCREEN.blit(GAME_SPRITES['numbers'][digit],
                  (Xoffset, SCREENHEIGHT * 0.12))
      Xoffset += width / len(myDigits)

    pygame.display.update()
    FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
  if playery < 0 or playery > SCREENHEIGHT - 50:
    GAME_SOUNDS['die'].play()
    return True

  for pipe in upperPipes:
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    playerHeight = GAME_SPRITES['player'].get_height()
    if (playery < pipeHeight + pipe['y'] and pipe['x'] <= playerx <=
        pipe['x'] + GAME_SPRITES['pipe'][0].get_width() - 50):
      GAME_SOUNDS['die'].play()
      return True

  for pipe in lowerPipes:
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    playerHeight = GAME_SPRITES['player'].get_height()
    if (playery + playerHeight > pipe['y'] and pipe['x'] <= playerx <=
        pipe['x'] + GAME_SPRITES['pipe'][0].get_width() - 50):
      GAME_SOUNDS['die'].play()
      return True
  return False


def getRandomPipe():
  pipeHeight = GAME_SPRITES['pipe'][0].get_height()
  offset = SCREENHEIGHT / 3 + 30
  pipex = SCREENWIDTH + 10
  y2 = offset + random.randrange(0, int(SCREENHEIGHT - 1.2 * offset))
  y1 = pipeHeight - y2 + offset
  pipe = [{'x': pipex, 'y': -y1}, {'x': pipex, 'y': y2}]
  return pipe


if __name__ == "__main__":
  pygame.init()
  FPSCLOCK = pygame.time.Clock()

  pygame.display.set_caption("Flappy Bird")
  ICON = pygame.image.load(PLAYER)
  pygame.display.set_icon(ICON)

  GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert_alpha()
  GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
  GAME_SPRITES['numbers'] = (pygame.image.load('pics/0.png').convert_alpha(),
                             pygame.image.load('pics/1.png').convert_alpha(),
                             pygame.image.load('pics/2.png').convert_alpha(),
                             pygame.image.load('pics/3.png').convert_alpha(),
                             pygame.image.load('pics/4.png').convert_alpha(),
                             pygame.image.load('pics/5.png').convert_alpha(),
                             pygame.image.load('pics/6.png').convert_alpha(),
                             pygame.image.load('pics/7.png').convert_alpha(),
                             pygame.image.load('pics/8.png').convert_alpha(),
                             pygame.image.load('pics/9.png').convert_alpha())
  GAME_SPRITES['message'] = pygame.image.load('pics/wel.jpg').convert_alpha()
  GAME_SPRITES['space'] = pygame.image.load(SPACE).convert_alpha()
  GAME_SPRITES['pipe'] = (pygame.transform.rotate(
      pygame.image.load(PIPE).convert_alpha(),
      180), pygame.image.load(PIPE).convert_alpha())

  GAME_SOUNDS['die'] = pygame.mixer.Sound('aud/dead.mp3')
  GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('aud/game.mp3')
  GAME_SOUNDS['point'] = pygame.mixer.Sound('aud/point.mp3')
  GAME_SOUNDS['wing'] = pygame.mixer.Sound('aud/fly.mp3')

  while True:
    welcomeScreen()
    mainGame()