#
#   *  *   *   *    *  ROBOT EXODUS *   *   *  *  * 
# 
#   - toimintapeli
#   - A ja W napit liikuttaa robottia ja hiiren kursorin koordinaatteihin 
#     lähetetään tappava kuolemansäde hiiren nappulasta klikkaamalla.. 
#     tarkoitus olisi ettei ulkoavaruuden haamuiksi muuntautuneena oliot pääsisi hapettamaan viimeistä rintamaa.
#       
#     onnea matkaan!
# 
#   
#
# TEE PELI TÄHÄN =)

from random import randint
from typing import Text
import math
import pygame

class Kolikko:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.tila = True

    def piirra_kolikko(self, x: int, y: int, kohde_x: int, kohde_y: int, laser: int):
        if self.tila == True:
            naytto.blit(lantti, (x, y))
        if laser:
            if kohde_x >= x and kohde_x <= x +30:
                if kohde_y >= y and kohde_y <= y +30:
                    self.tila = False

class Morko:

    def __init__(self):
        self.x = randint(15, 570)
        self.y = -randint(100, 400)
        self.nopeus = 2

    def piirra_morko(self):
        if self.y < 500: 
            self.y += self.nopeus
        else: 
            self.__init__()
        naytto.blit(stemu, (self.x, self.y))

    def missa_morko(self):
        return [self.x, self.y]


def game_over():
    fontti = pygame.font.SysFont("Arial", 60)
    teksti = fontti.render(f"GAME OVER", True, (255, 0, 0))
    naytto.blit(ovi, (x, 395))
    naytto.blit(teksti, (130, 200))  
    pygame.display.flip()
    pygame.time.delay(6000)

def botti(x: int):
    naytto.blit(robo, (x, 355))

def sattuuko(x: int, lukema: int, morot: list):
    for morko in morot:
        kx, ky = morko.missa_morko()
        if ky > 290:
            if kx >= x and kx < x + 50:
                morko.__init__()
                lukema -= 1
                if lukema <= 0:
                    game_over() 
    return lukema

def laskuri():
    pygame.draw.line(naytto, (120+lukema, 0, 0), (20, 456), (lukema*62, 456), 20)
    teksti = fontti.render(f"Pisteet: {lukema}", True, (255, 0, 0))
    naytto.blit(teksti, (500, 10))  

def sateet(rx: int, x: int, y: int, ampu: bool):
    pygame.draw.line(naytto, (0, 35, 0), (rx + 17, 369), (x, y), 1)
    pygame.draw.line(naytto, (0, 35, 0), (rx + 31, 369), (x, y), 1)

    if ampu:
        pygame.draw.circle(naytto, (155, 0, 155), (x, y), 15)  
        pygame.draw.circle(naytto, (255, 255, 255), (x, y), 10)  
        pygame.draw.line(naytto, (255, 0, 255), (rx + 17, 369), (x, y), 8)
        pygame.draw.line(naytto, (255, 0, 255), (rx + 31, 369), (x, y), 8)
        pygame.draw.line(naytto, (255, 255, 255), (rx + 17, 369), (x, y), 3)
        pygame.draw.line(naytto, (255, 255, 255), (rx + 31, 369), (x, y), 3)
        pygame.draw.circle(naytto, (255, 5, 255), (rx + 17, 369), 15)  
        pygame.draw.circle(naytto, (255, 5, 255), (rx + 31, 369), 15)  

def laatikko():
    naytto.fill((0, 15, 5))
    pygame.draw.rect(naytto, (60, 60, 60), (10, 10, 620, 460))
    pygame.draw.rect(naytto, (20, 20, 20), (15, 15, 610, 430))


pygame.init()
naytto = pygame.display.set_mode((640, 480))

stemu = pygame.image.load("hirvio.png")
ovi = pygame.image.load("ovi.png")
robo = pygame.image.load("robo.png")
lantti = pygame.image.load("kolikko.png")

kello = pygame.time.Clock()
fontti = pygame.font.SysFont("Arial", 24)

morot = []
kolikot = []

# Robotin muuttujat
vasemmalle = False
oikealle = False
laser = False
x = 240

nopeus = 4 #mörkön putoamisnopeus muuttuja
lukema = 10 #pistelaskuri

# Lasersäteiden muuttujat
kohde_x = 0 
kohde_y = 0

# Kolikko muuttujat
kolikko_x = 0 
kolikko_y = 0
kulma = 0 # kolikon kulmamuuttuja
kolikot = [] 
kulma_suunta = bool

for i in range(0, 4): # Luodaan möröt
    morko = Morko()
    morot.append(morko)

for i in range(0, 8): # luodaan kolikot
    kolikko = Kolikko()
    kolikot.append(kolikko)

while True:
    laatikko() # Piirretään ruudun reunukset ja pistelaskurin paikat yms.

# Luetaan peliin liittyviä tietoja laitteilta. "näppäimet, hiiren positio"
    for tapahtuma in pygame.event.get(): 
        if tapahtuma.type == pygame.QUIT: exit()
        if tapahtuma.type == pygame.KEYDOWN:
            if tapahtuma.key == pygame.K_a:
                vasemmalle = True
            if tapahtuma.key == pygame.K_d:
                oikealle = True
        if tapahtuma.type == pygame.KEYUP:
            if tapahtuma.key == pygame.K_a:
                vasemmalle = False
            if tapahtuma.key == pygame.K_d:
                oikealle = False
        if tapahtuma.type == pygame.MOUSEMOTION:
            kohde_x = tapahtuma.pos[0]
            kohde_y = tapahtuma.pos[1]
        if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
            laser = True
            kulma_suunta = not kulma_suunta

    if vasemmalle: # robotin liikkuttelua ja piirtämistä.
        x -= nopeus
    if oikealle:
        x += nopeus
    botti(x)

    for morko in morot: # putoavien mörköjen piirtämistä
        morko.piirra_morko()

    for i in range(len(kolikot)): # pyörivien kolikoiden piirtämistä
        kolikko_x = 300+math.cos(kulma+2*math.pi*i/8)*250
        kolikko_y = 130+math.sin(kulma+2*math.pi*i/8)*100
        kolikot[i].piirra_kolikko(kolikko_x, kolikko_y, kohde_x, kohde_y, laser)
        if kulma_suunta: kulma += 0.01
        else: kulma -= 0.01

    sateet(x, kohde_x, kohde_y, laser) # robotin silmistä lähtevän laser pulssin piirto
    laser = False

    lukema = sattuuko(x, lukema, morot) # Osuuko putoava mörkö robottiin
    laskuri()

    pygame.display.flip() # Muistissa olevan grafiikan siirtäminen näytön muisti alueelle
    kello.tick(60) # Pelin nopeuden rajoittamista.

