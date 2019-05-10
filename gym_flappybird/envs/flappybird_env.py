import gym
from gym import error, spaces, utils
from gym.utils import seeding

from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *
import os

FPS = 30
SCREENWIDTH  = 288
SCREENHEIGHT = 512
PIPEGAPSIZE  = 100 # gap between upper and lower part of pipe
BASEY        = SCREENHEIGHT * 0.79
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

PLAYER_WIDTH = 34
PLAYER_HEIGHTS = 24

BACKGROUNDS_WIDTH = 288
BACKGROUNDS_HEIGHTS = 512

BASE_WIDTH = 336
BASE_HEIGHTS = 112

PIPE_WIDTH = 52
PIPE_HEIGHTS = 320

NUMBER_WIDTH = 24
NUMBER_HEIGHT = 36

# absoulte path from the system
ASSETS_PATH = os.path.dirname(__file__) + os.path.join('/assets/')
# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        ASSETS_PATH + 'sprites/redbird-upflap.png',
        ASSETS_PATH + 'sprites/redbird-midflap.png',
        ASSETS_PATH + 'sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        ASSETS_PATH + 'sprites/bluebird-upflap.png',
        ASSETS_PATH + 'sprites/bluebird-midflap.png',
        ASSETS_PATH + 'sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        ASSETS_PATH + 'sprites/yellowbird-upflap.png',
        ASSETS_PATH + 'sprites/yellowbird-midflap.png',
        ASSETS_PATH + 'sprites/yellowbird-downflap.png',
    ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
    ASSETS_PATH + 'sprites/background-day.png',
    ASSETS_PATH + 'sprites/background-night.png',
)

# list of pipes
PIPES_LIST = (
    ASSETS_PATH + 'sprites/pipe-green.png',
    ASSETS_PATH + 'sprites/pipe-red.png',
)


try:
    xrange
except NameError:
    xrange = range


class FlappybirdEnv(gym.Env):
  metadata = {'render.modes': ['human', 'rgb_array']}
  ACTION = [0, 1] # 1 => jump

  def __init__(self):
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    try:
      SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
      pygame.display.set_caption('Flappy Bird')
    except Exception as e:
      pass
    self._load()
    self._showWelcomeAnimation()

  def reset(self):
    self._load()
    self._showWelcomeAnimation()
    return self.observation, self.score, self.done, self.info

  def render(self, mode='human', close=False):
    try:
      pygame.display.update()
    except Exception as e:
      pass
    FPSCLOCK.tick(FPS)

  def close(self):
    try:
        self.done = True
        pygame.display.quit()
        pygame.quit()
    except Exception:
        pass

  def _load(self):
    print('loading ..')
    # numbers sprites for score display
    """
    IMAGES['numbers'] = (
                    pygame.image.load(ASSETS_PATH + 'sprites/0.png').convert_alpha(),
                    pygame.image.load(ASSETS_PATH + 'sprites/1.png').convert_alpha(),
                    pygame.image.load(ASSETS_PATH + 'sprites/2.png').convert_alpha(),
                    pygame.image.load(ASSETS_PATH + 'sprites/3.png').convert_alpha(),
                    pygame.image.load(ASSETS_PATH + 'sprites/4.png').convert_alpha(),
                    pygame.image.load(ASSETS_PATH + 'sprites/5.png').convert_alpha(),
                    pygame.image.load(ASSETS_PATH + 'sprites/6.png').convert_alpha(),
                    pygame.image.load(ASSETS_PATH + 'sprites/7.png').convert_alpha(),
                    pygame.image.load(ASSETS_PATH + 'sprites/8.png').convert_alpha(),
                    pygame.image.load(ASSETS_PATH + 'sprites/9.png').convert_alpha()
                )

                # game over sprite
                IMAGES['gameover'] = pygame.image.load(ASSETS_PATH + 'sprites/gameover.png').convert_alpha()
                # message sprite for welcome screen
                IMAGES['message'] = pygame.image.load(ASSETS_PATH + 'sprites/message.png').convert_alpha()
                # base (ground) sprite
                IMAGES['base'] = pygame.image.load(ASSETS_PATH + 'sprites/base.png').convert_alpha()
    """

    # sounds
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'
    """
        # # SOUNDS['die']    = pygame.mixer.Sound(ASSETS_PATH + 'audio/die' + soundExt)
        # SOUNDS['hit']    = pygame.mixer.Sound(ASSETS_PATH + 'audio/hit' + soundExt)
        # SOUNDS['point']  = pygame.mixer.Sound(ASSETS_PATH + 'audio/point' + soundExt)
        # SOUNDS['swoosh'] = pygame.mixer.Sound(ASSETS_PATH + 'audio/swoosh' + soundExt)
        # SOUNDS['wing']   = pygame.mixer.Sound(ASSETS_PATH + 'audio/wing' + soundExt)
    """
    #  welcome screen - select random background sprites
    """
                randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
                IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()
    """
    # select random player sprites
    """
                randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
                IMAGES['player'] = (
                    pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
                    pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
                    pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
                )
    """

    # select random pipe sprites
    """
        pipeindex = random.randint(0, len(PIPES_LIST) - 1)
        IMAGES['pipe'] = (
            pygame.transform.flip(
                pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), False, True),
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
        )
    """
        # hismask for pipes
    """
    # get values in normal mode and paste it here
        HITMASKS['pipe'] = (
            self._getHitmask(IMAGES['pipe'][0]),
            self._getHitmask(IMAGES['pipe'][1]),
        )
    """
    HITMASKS['pipe'] = [[],[]]
    # print(HITMASKS)

    filepath = ASSETS_PATH + "hitmask/pipes"
    from os import listdir
    from os.path import isfile, join
    pipefiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]

    for i, pipeFile in enumerate(pipefiles):
      with open(ASSETS_PATH + "hitmask/pipes/" + pipeFile) as fp:
         for cnt, line in enumerate(fp):
             # print("Line {}: {}".format(cnt, line))
             HITMASKS['pipe'][i] += [True if l == 'True' else False for l in line.split(',')]

    HITMASKS['player'] = [[], [], []]
    filepath = ASSETS_PATH + "hitmask/players"
    playerfiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]

    for i, playerFile in enumerate(playerfiles):
      with open(ASSETS_PATH + "hitmask/players/" + playerFile) as fp:
         for cnt, line in enumerate(fp):
             # print("playerFile Line {}: {}".format(cnt, line))
             HITMASKS['player'][i] += [True if l == 'True' else False for l in line.split(',')]

    # print(HITMASKS)
    """    # hitmask for player
            HITMASKS['player'] = (
                self._getHitmask(IMAGES['player'][0]),
                self._getHitmask(IMAGES['player'][1]),
                self._getHitmask(IMAGES['player'][2]),
            )

    """
    # index of player to blit on screen
    self.playerIndex = 0
    self.playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    self.loopIter = 0

    self.playerx = int(SCREENWIDTH * 0.2)
    self.playery = int((SCREENHEIGHT *0.2))
      # IMAGES['player'][0].get_height()) / 2)
      # height is 512
      # width is 288
    self.messagex = int((SCREENWIDTH*0.1))
      # IMAGES['message'].get_width()) / 2)
    self.messagey = int(SCREENHEIGHT * 0.12)

    self.basex = 0
    # amount by which base can maximum shift to left
    self.baseShift = 336 - 288
     # IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # player shm for up-down motion on welcome screen
    self.playerShmVals = {'val': 0, 'dir': 1}
    self.score = self.playerIndex = self.loopIter = 0
    self.playerx, self.playery = int(SCREENWIDTH * 0.2), int(SCREENWIDTH * 0.2)

    self.baseShift =  336 - 288
    # IMAGES['base'].get_width() - IMAGES['background'].get_width()
    self.done = False

    playerMidPosX = self.playerx + 34 / 2
    playerMidPosY = self.playery + 24 / 2
    self.observation = {
      'playerMidPosX': playerMidPosX,
      'playerMidPosY': playerMidPosY
    }
    self.info = {
      'upperPipes': [
        {'x': int(SCREENWIDTH), 'y': int(SCREENHEIGHT) }
      ],

      'lowerPipes': [
        {'x': int(SCREENWIDTH), 'y': int(SCREENHEIGHT) }
      ]
    }

  def _showWelcomeAnimation(self):
    """Shows welcome screen animation of flappy bird"""

    """
    # when you want to start manually by pressing space button
    while True:
      for event in pygame.event.get():
          if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
              pygame.quit()
              sys.exit()
          if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
              self.playery = self.playery + self.playerShmVals['val']
              return self.step(1, {'firstFlap': True})

      # adjust playery, playerIndex, basex
      if (self.loopIter + 1) % 5 == 0:
          self.playerIndex = next(self.playerIndexGen)
      self.loopIter = (self.loopIter + 1) % 30
      self.basex = -((-self.basex + 4) % self.baseShift)
      self._playerShm(self.playerShmVals)

      # draw sprites
      SCREEN.blit(IMAGES['background'], (0,0))
      SCREEN.blit(IMAGES['player'][self.playerIndex],
                  (self.playerx, self.playery + self.playerShmVals['val']))
      SCREEN.blit(IMAGES['message'], (self.messagex, self.messagey))
      SCREEN.blit(IMAGES['base'], (self.basex, BASEY))

      pygame.display.update()
      FPSCLOCK.tick(FPS)
    """

    # Automatically start
    self.playery = self.playery + self.playerShmVals['val']
    return self.step(1, {'firstFlap': True})

  def step(self, action, options={'firstFlap': False}):
    # make first flap sound and return values for mainGame

    if options['firstFlap'] == True and action == 1:
      # first flap options

      # get 2 new pipes to add to upperPipes lowerPipes list
      newPipe1 = self._getRandomPipe()
      newPipe2 = self._getRandomPipe()

      # list of upper pipes
      self.upperPipes = [
          {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
          {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
      ]

      # list of lowerpipe
      self.lowerPipes = [
          {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
          {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
      ]

      self.pipeVelX = -4

      # player velocity, max velocity, downward accleration, accleration on flap
      self.playerVelY    =  -9   # player's velocity along Y, default same as playerFlapped
      self.playerMaxVelY =  10   # max vel along Y, max descend speed
      self.playerMinVelY =  -8   # min vel along Y, max ascend speed
      self.playerAccY    =   1   # players downward accleration
      self.playerRot     =  45   # player's rotation
      self.playerVelRot  =   3   # angular speed
      self.playerRotThr  =  20   # rotation threshold
      self.playerFlapAcc =  -9   # players speed on flapping
      self.playerFlapped = False # True when player flaps

      try:
        SCREEN.blit(IMAGES['background'], (0,0))
        SCREEN.blit(IMAGES['player'][self.playerIndex],
                    (self.playerx, self.playery + self.playerShmVals['val']))
        SCREEN.blit(IMAGES['message'], (self.messagex, self.messagey))
        SCREEN.blit(IMAGES['base'], (self.basex, BASEY))
      except Exception as e:
        pass
    elif options['firstFlap'] == False and action == 1:
      # SOUNDS['wing'].play()
      # secoond flap onwards
      if self.playery > -2 * PLAYER_HEIGHTS:
        self.playerVelY = self.playerFlapAcc
        self.playerFlapped = True
        # SOUNDS['wing'].play()
      # check for crash here
      crashTest = self._checkCrash({
        'x': self.playerx,
        'y': self.playery,
        'index': self.playerIndex
        },
        self.upperPipes, self.lowerPipes)

      # check for score
      playerMidPosX = self.playerx + PLAYER_WIDTH / 2
      playerMidPosY = self.playery + PLAYER_HEIGHTS / 2


      self.observation['playerMidPosX'] = playerMidPosX
      self.observation['playerMidPosY'] = playerMidPosY
      self.info['upperPipes'] = self.upperPipes
      self.info['lowerPipes'] = self.lowerPipes

      for pipe in self.upperPipes:
          pipeMidPos = pipe['x'] + PIPE_WIDTH / 2
          if pipeMidPos <= playerMidPosX < pipeMidPos + 4:
              self.score += 1
              # SOUNDS['point'].play()

      if crashTest[0]:
        # """
        # # when want to show gameover on screen
        # return {
        #     'y': self.playery,
        #     'groundCrash': crashTest[1],
        #     'basex': self.basex,
        #     'upperPipes': self.upperPipes,
        #     'lowerPipes': self.lowerPipes,
        #     'score': self.score,
        #     'playerVelY': self.playerVelY,
        #     'playerRot': self.playerRot
        # }
        # """
        self.done = True
        self.reset()
        return self.observation, self.score, self.done, self.info

      # playerIndex basex change
      if (self.loopIter + 1) % 3 == 0:
          self.playerIndex = next(self.playerIndexGen)
      self.loopIter = (self.loopIter + 1) % 30
      self.basex = -((-self.basex + 100) % self.baseShift)

      # rotate the player
      if self.playerRot > -90:
          self.playerRot -= self.playerVelRot

      # player's movement
      if self.playerVelY < self.playerMaxVelY and not self.playerFlapped:
          self.playerVelY += self.playerAccY
      if self.playerFlapped:
          self.playerFlapped = False

          # more rotation to cover the threshold (calculated in visible rotation)
          self.playerRot = 45

      self.playerHeight = PLAYER_HEIGHTS
      self.playery += min(
        self.playerVelY, BASEY - self.playery - self.playerHeight)

      # move pipes to left
      for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
          uPipe['x'] += self.pipeVelX
          lPipe['x'] += self.pipeVelX

      # add new pipe when first pipe is about to touch left of screen
      if 0 < self.upperPipes[0]['x'] < 5:
          newPipe = getRandomPipe()
          self.upperPipes.append(newPipe[0])
          self.lowerPipes.append(newPipe[1])

      # remove first pipe if its out of the screen
      if self.upperPipes[0]['x'] < -PIPE_WIDTH:
          self.upperPipes.pop(0)
          self.lowerPipes.pop(0)

      # draw sprites
      try:
        SCREEN.blit(IMAGES['background'], (0,0))
      except Exception as e:
        pass

      for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
        try:
          SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
          SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))
          SCREEN.blit(IMAGES['base'], (self.basex, BASEY))
        except Exception as e:
          pass

      # print score so player overlaps the score
      self._showScore(self.score)

      # Player rotation has a threshold
      visibleRot = self.playerRotThr
      if self.playerRot <= self.playerRotThr:
          visibleRot = self.playerRot

      try:
        playerSurface = pygame.transform.rotate(
          IMAGES['player'][self.playerIndex], visibleRot)
        SCREEN.blit(playerSurface, (self.playerx, self.playery))
      except Exception as e:
        pass

    try:
      pygame.display.update()
    except Exception as e:
      pass
    FPSCLOCK.tick(FPS)
    return self.observation, self.score, self.done, self.info

  def _showGameOverScreen(self, crashInfo):
    """crashes the player down ans shows gameover image"""
    score = crashInfo['score']
    playerx = SCREENWIDTH * 0.2
    playery = crashInfo['y']
    playerHeight = PLAYER_HEIGHTS
    playerVelY = crashInfo['playerVelY']
    playerAccY = 2
    playerRot = crashInfo['playerRot']
    playerVelRot = 7

    basex = crashInfo['basex']

    upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

    # play hit and die sounds
    # SOUNDS['hit'].play()
    if not crashInfo['groundCrash']:
        # SOUNDS['die'].play()
        pass

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery + playerHeight >= BASEY - 1:
                    return

        # player y shift
        if playery + playerHeight < BASEY - 1:
            self.playery += min(
              playerVelY, BASEY - playery - playerHeight)

        # player velocity change
        if playerVelY < 15:
            self.playerVelY += playerAccY

        # rotate only when it's a pipe crash
        if not crashInfo['groundCrash']:
            if playerRot > -90:
                self.playerRot -= playerVelRot

        try:
          # draw sprites
          SCREEN.blit(IMAGES['background'], (0,0))

          for uPipe, lPipe in zip(pperPipes, owerPipes):
              SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
              SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

          SCREEN.blit(IMAGES['base'], (basex, BASEY))
        except Exception as e:
          pass
        self._showScore(self.score)

        try:

          playerSurface = pygame.transform.rotate(IMAGES['player'][1],
            self.playerRot)
          SCREEN.blit(playerSurface, (playerx,self.playery))
          SCREEN.blit(IMAGES['gameover'], (50, 180))
        except Exception as e:
          pass

        FPSCLOCK.tick(FPS)
        try:
          pygame.display.update()
        except Exception as e:
          pass


  def _playerShm(self, playerShm):
    """oscillates the value of playerShm['val'] between 8 and -8"""
    if abs(playerShm['val']) == 8:
        playerShm['dir'] *= -1

    if playerShm['dir'] == 1:
         playerShm['val'] += 1
    else:
        playerShm['val'] -= 1


  def _getRandomPipe(self):
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    pipeHeight = PIPE_HEIGHTS
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
    ]


  def _showScore(self, score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += NUMBER_WIDTH

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
      try:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()
      except Exception as e:
        pass


  def _checkCrash(self, player, upperPipes, lowerPipes):
    """returns True if player collders with base or pipes."""
    pi = player['index']
    player['w'] = PLAYER_WIDTH
    player['h'] = PLAYER_HEIGHTS

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True] # yes crashed, with base
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])
        pipeW = PIPE_WIDTH
        pipeH = PIPE_HEIGHTS

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = self._pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = self._pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False] # yes crashed but not with base,its pipe

    return [False, False]

  def _pixelCollision(self, rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            # need to verify this line: previously it was and
            # TypeError: 'bool' object is not subscriptable
            print('x1 ', x1, ' ', y1 )
            print('x2 ', x2, ' ', y2)
            print('hitmask1[x1+x]1 ', hitmask1[x1+x])
            if hitmask1[x1+x][y1+y]:
              print('hitmask1[x1+x][y1+y] ', hitmask1[x1+x][y1+y])
              if hitmask2[x2+x][y2+y]:
                print('hitmask2[x2+x][y2+y] ', hitmask2[x2+x][y2+y])
                return True
    return False

  def _getHitmask(self, image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask
