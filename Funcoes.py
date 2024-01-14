import random
from pplay.gameimage import *
from pplay.sprite import *
from pplay.keyboard import *
from pplay.sound import *
from pplay.mouse import *
from sys import setrecursionlimit  # Para modificar o limite máximo de recursoes permitidas.
import Constants  # Constantes referentes ao jogo.
import Botoes

random.seed()


def spawn_enemy(i, j, enemy_matrix):

    # for x e for y percorrem cada elemento da matriz
    for x in range(i):
        for y in range(j):
            # Cria o Sprite do inimigo
            enemy = Sprite("Assets/red_enemy.png", 1)
            # Define a posição
            enemy.set_position(x * (enemy.width + 20), y * enemy.height)
            # Define a direção do movimento, no caso para baixo
            enemy.direction = 1  # 1 = para baixo
            # Define randomicamente o intervalo entre os disparos
            enemy.shoot_delay = random.uniform(0, 15) / Constants.current_difficulty
            # Zera a variável de controle de disparos
            enemy.shoot_tick = 0
            # Coloca o inimigo recém criado na matriz
            enemy_matrix[x][y] = enemy

