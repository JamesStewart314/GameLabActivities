import random

from pplay.gameimage import *
from pplay.sprite import *
from pplay.keyboard import *
from pplay.sound import *
from pplay.mouse import *
from pplay.animation import *
from sys import setrecursionlimit  # Para modificar o limite máximo de recursoes permitidas.
import Constants  # Constantes referentes ao jogo.
import Botoes
import Funcoes

Janela = Window(Constants.ScrWdt, Constants.ScrHgt)  # Janela do jogo.
Janela.set_title("SpaceInvaders")  # Título nada suspeito.
Fundo = GameImage("Assets/MenuWallpaper.jpg")  # Fundo do menu.
FundoMenuDiff = GameImage("Assets/DiffMenuWallpaper.jpg")  # Fundo do menu de dificuldades.
Cursor = Mouse()  # Entrada de dados do cursor.
Teclado = Keyboard()  # Entrada de dados do teclado.

setrecursionlimit(10 ** 5)  # Aumentando o limite máximo de recursões permitidas

current_difficulty = Constants.current_difficulty  # Dificuldade padrão do jogo inicializada como "1".

random.seed()  # Semente aleatória utilizada para a geração do jogo.

Bullet_Sound = Sound("Assets/Space_Invaders_Shoot_Sound.ogg")  # Obtendo o efeito sonoro de disparo.
Menu_Sound = Sound("Assets/Evil_unknown.ogg")
Menu_Sound.loop = True
Battle_Sound = Sound("Assets/Space-Battle-Theme.ogg")
Battle_Sound.loop = True

fundo_infinito_1 = Sprite("Assets/infinity_background.png")
fundo_infinito_2 = Sprite("Assets/infinity_background.png")

fundo_infinito_1.y = 0
fundo_infinito_2.y = -fundo_infinito_2.height

enemy_speed = Constants.Enemy_Speed
enemy_direction = -1
Reversed = False

last_enemy_shot = 0
enemy_x = 0
enemy_y = 0

# -------------------------------------- Informaçoes de Batalha ------------------------------------- #

# Numero de linhas da matriz de inimigos
matrix_x = int(random.uniform(3, Constants.MAXSIZE))

# Numero de coluna da matriz de inimigos
matrix_y = int(random.uniform(1, Constants.MAXSIZE))

# Criando a matriz vazia de inimigos
Enemy_Matrix = [[0 for x0 in range(matrix_y)] for x1 in range(matrix_x)]  # Criando a matriz vazia de inimigos.

bullets_shooted = []  # Disparos do jogador
enemies_bullets_shooted = []  # Disparos dos inimigos

original_pos = 20  # Salvando a posição do primeiro inimigo criado, para não perdê-la quando o mesmo morrer.

# ---------------------------------------------------------------------------------------------------------------- #


# Definindo as funções do jogo:


# ------------------------------- Colisão de Balas do Jogador com os Inimmigos ---------------------------------- #

def check_bullet_enemy_collision() -> None:

    # Verifica se algum projétil do jogador colidiu com os inimigos e, em caso afirmativo,
    # elimina o inimigo e o projétil.

    global bullets_shooted
    global Enemy_Matrix

    for bullet in bullets_shooted:
        for x in range(matrix_x):
            for y in range(matrix_y):
                if Enemy_Matrix[x][y]:  # Avalia se o elemento não é nulo ( " 0 => False " )
                    if bullet.collided(Enemy_Matrix[x][y]):
                        Enemy_Matrix[x][y] = 0
                        bullets_shooted.remove(bullet)
                        return None
                        # Encerra a funçao, caso contrário, avançaria o laço e checaria a colisão da bala
                        # com o próximo inimigo, mas a bala não existe mais.

# ---------------------------------------------------------------------------------------------------------------- #


# --------------------------------- Atualiza a Posição dos Inimigos ---------------------------------------------- #

def enemy_movement() -> None:

    # Por algum motivo que desconheço ainda, a matriz de inimigos fornecida no jogo é a transposta da matriz criada.
    # Se conseguir descobrir a causa e solucionar este problema, eu ficaria muito grato.

    # Acessando variáveis globais
    global enemy_speed
    global Janela
    global Reversed
    global original_pos
    global Enemy_Matrix
    global matrix_x, matrix_y

    if original_pos + (red_enemy.width + 20) * matrix_x >= Constants.ScrWdt:
        Reversed = True
    if original_pos < 20:
        Reversed = False

    if not Reversed:
        original_pos += enemy_speed * Janela.delta_time()
    else:
        original_pos -= enemy_speed * Janela.delta_time()

    # Percorre toda a matriz de inimigos
    for row in range(matrix_x):
        for column in range(matrix_y):
            # Caso a posição esteja ocupada, isto é, o inimigo
            # ainda esteja vivo, efetua as ações em seguida.
            if Enemy_Matrix[row][column] != 0:
                if not Reversed:
                    Enemy_Matrix[row][column].x += enemy_speed * Janela.delta_time()
                else:
                    Enemy_Matrix[row][column].x -= enemy_speed * Janela.delta_time()
                Enemy_Matrix[row][column].shoot_delay = random.uniform(0, 15) / Constants.current_difficulty

# ------------------------------------------------------------------------------------------------------------ #


# --------------------------------- Colisão entre Projéteis -------------------------------------------------- #

def bullets_collision() -> None:

    global bullets_shooted
    global enemies_bullets_shooted

    for bullet in bullets_shooted:
        for enemy_bullet in enemies_bullets_shooted:
            if bullet.collided(enemy_bullet):
                bullets_shooted.remove(bullet)
                enemies_bullets_shooted.remove(enemy_bullet)
                return None

# ------------------------------------------------------------------------------------------------------------ #


# --------------------------------- Atualiza a Posição de Todos os Projéteis --------------------------------- #

def bullets_update() -> None:

    global bullets_shooted
    global enemies_bullets_shooted
    global Janela

    for bullet in bullets_shooted:
        bullet.y += (-1) * 300 * Janela.delta_time() * Constants.current_difficulty
        bullet.draw()
        if bullet.y + bullet.height <= 0:
            bullets_shooted.remove(bullet)
    for bullet in enemies_bullets_shooted:
        bullet.y += 300 * Janela.delta_time() * Constants.current_difficulty
        bullet.draw()
        if bullet.y >= Constants.ScrHgt:
            enemies_bullets_shooted.remove(bullet)

    bullets_collision()

# ----------------------------------------------------------------------------------------------------- #


# ---------------------------------------- Reinicia o Jogo -------------------------------------------- #

def restart() -> None:  # Reinicia as variáveis de jogo.

    # Gera o acesso às variáveis globais
    global matrix_x
    global matrix_y
    global Enemy_Matrix
    global bullets_shooted
    global enemies_bullets_shooted
    global Player
    global last_enemy_shot

    # Deleta todos os objetos enemies e bullets
    bullets_shooted = []
    enemies_bullets_shooted = []
    last_enemy_shot = 0

    # Retorna o jogador à posição e pontuação inicial do jogo
    Player.score = 0
    Player.set_position((Constants.ScrWdt - Player.width) / 2,
                        (Constants.ScrHgt - Player.height - Constants.ScrHgt / 50))

    # Cria uma nova matriz de inimigos
    matrix_x = int(random.uniform(3, 10))
    matrix_y = int(random.uniform(1, 10))
    Enemy_Matrix = [[0 for x0 in range(matrix_y)] for x1 in range(matrix_x)]
    Funcoes.spawn_enemy(matrix_x, matrix_y, Enemy_Matrix)

# ----------------------------------------------------------------------------------------------------- #


# ---------------------------------- Ajuste da Posição de Projétil ----------------------------------- #

def adjust_bullet(actor, bullet) -> None:  # Ajusta a posição do projétil baseando-se quem disparou.

    # Calcula posição X da bala, utilizando como referência o
    # centro do ator e armazena em x_fire
    x_fire = actor.x + (actor.width - bullet.width) / 2

    # Calcula posição Y do projétil, utilizando como referência
    # a direção de movimento e o tamanho do jogador, salvando
    # o resultado na variável y_fire
    if actor.direction == -1:
        y_fire = actor.y
    elif actor.direction == 1:
        y_fire = actor.y + actor.height - bullet.height

    # Transfere o valor das variáveis auxiliares x_fire e y_fire
    # para o projétil
    bullet.x = x_fire
    bullet.y = y_fire

    # Define direção do projétil
    bullet.direction = actor.direction

# ----------------------------------------------------------------------------------------------------- #


# ------------------------------------ Produzir um Projétil ------------------------------------------- #

def shoot(shooter) -> None:

    global bullets_shooted

    # Cria uma nova bullet, dependendo de quem for que atirou
    if shooter.direction == -1:
        b = Sprite("Assets/shoot.png")
    elif shooter.direction == 1:
        b = Sprite("Assets/shoot_enemy.png")

    # Ajusta a posição inicial e a direção do projétil
    adjust_bullet(shooter, b)

    # Adiciona o novo projétil que criamos para ser desenhado na tela
    if shooter.direction == 1:
        enemies_bullets_shooted.append(b)
    else:
        if not shooter.shooted and Janela.time_elapsed() - shooter.last_shot >= 500 * Constants.current_difficulty:
            bullets_shooted.append(b)
            Bullet_Sound.play()
            shooter.shooted = True
            shooter.last_shot = Janela.time_elapsed()

        if shooter.shooted:
            shooter.shooted = False

# ----------------------------------------------------------------------------------------------------- #


# ---------------------------------- Animação de Fundo do Jogo ---------------------------------------- #

def scrolling(bg_bottom, bg_top, roll_speed, janela) -> None:

    # Modifica a velocidade do fundo baseado na dificuldade atual
    roll_speed *= Constants.current_difficulty
    # Movimenta ambos os Sprites verticalmente
    bg_bottom.y += roll_speed * janela.delta_time()
    bg_top.y += roll_speed * janela.delta_time()

    # Se a imagem do topo já tiver sido completamente exibida,
    # retorna ambas imagens às suas posições iniciais
    if bg_top.y >= 0:
        bg_bottom.y = 0
        bg_top.y = -bg_top.height

    # Renderiza as duas imagens de fundo
    bg_bottom.draw()
    bg_top.draw()

# --------------------------------------------------------------------------------------------------------------- #


# --------------------------------- Gerador de Ataque Aleatório do Inimigo --------------------------------------- #

def enemy_random_attack() -> None:

    global matrix_x
    global matrix_y
    global Enemy_Matrix
    global Janela
    global current_difficulty
    global last_enemy_shot
    global enemy_x
    global enemy_y

    shoot_cooldown = 1000 / current_difficulty

    if not last_enemy_shot:
        last_enemy_shot = Janela.time_elapsed()

    enemy_x = (enemy_x + 1) % matrix_x
    enemy_y = (enemy_y + 1) % matrix_y

    if Enemy_Matrix[enemy_x][enemy_y]:  # Verifica se a posição não é nula.
        if Janela.time_elapsed() - last_enemy_shot >= shoot_cooldown:  # Verifica o cooldown de disparo
            if bool(random.randint(0, 1)):  # Variável booleana para tornar o disparo ainda mais aleatório.
                shoot(Enemy_Matrix[enemy_x][enemy_y])
                last_enemy_shot = Janela.time_elapsed()

# ------------------------------------------------------------------------------------------------------------ #


# ----------------------------------------------- Início do Jogo ------------------------------------------- #

def Play() -> None:  # Inicia o jogo.

    global Janela
    global enemy_speed
    global current_difficulty
    global original_pos
    global Enemy_Matrix

    Funcoes.spawn_enemy(matrix_x, matrix_y, Enemy_Matrix)  # Cria uma nova matriz de inimigos

    current_difficulty = Constants.current_difficulty  # Atualizando a dificuldade antes do início do jogo.

    # Salvando a posição do primeiro inimigo criado, para não perdê-la quando o mesmo morrer :
    original_pos = Enemy_Matrix[0][0].x

    # Atualizando a velocidade inimiga conforme a dificuldade:
    enemy_speed = Constants.Enemy_Speed * Constants.current_difficulty

    Battle_Sound.play()

    while True:

        # Efeito de animação da tela de fundo do jogo:
        scrolling(fundo_infinito_1, fundo_infinito_2, Constants.background_roll_speed, Janela)

        Player.draw()  # Desenha o jogador.

        enemy_movement()  # Movendo a matriz de inimigos.

        # Desenhando a matriz de imimigos:
        for x in range(matrix_x):
            for y in range(matrix_y):
                if Enemy_Matrix[x][y]:
                    Enemy_Matrix[x][y].draw()

        check_bullet_enemy_collision()  # Verifica se houve colisão dos projéteis do jogador com algum inimigo.

        enemy_random_attack()  # Gera o ataque aleatório da matriz de inimigos atual.

        bullets_update()  # Atualiza a posição de todos os projéteis do jogo.

        for bullet in enemies_bullets_shooted:
            if bullet.collided(Player):
                print("Você Perdeu !")
                restart()
                Battle_Sound.stop()
                Menu()

        if Teclado.key_pressed("ESC"):
            restart()
            Battle_Sound.stop()
            Menu()
        if Teclado.key_pressed("A") or Teclado.key_pressed("LEFT"):
            if Player.x >= 0:
                Player.x += (-1) * Constants.Player_Speed * current_difficulty * Janela.delta_time()
        if Teclado.key_pressed("D") or Teclado.key_pressed("RIGHT"):
            if Player.x <= Constants.ScrWdt - Player.width:
                Player.x += Constants.Player_Speed * current_difficulty * Janela.delta_time()
        if Teclado.key_pressed("SPACE"):
            shoot(Player)

        Janela.update()

# ----------------------------------------------------------------------------------------------------- #


# ------------------------------------------ Menu Principal ------------------------------------------- #

def Menu() -> None:  # Exibe o menu principal.

    global Cursor, Teclado, Janela, Fundo, PlayButton, DiffButton, RankButton, ExitButton

    Menu_Sound.play()

    while True:

        # especificando as posições dos elementos da tela de menu.
        PlayButton.set_position((Janela.width - PlayButton.width) / 2, (1 * Janela.height - 4 * PlayButton.height) / 8)
        PlayButtonPressed.set_position((Janela.width - PlayButton.width) / 2,
                                       (1 * Janela.height - 4 * PlayButton.height) / 8)
        DiffButton.set_position((Janela.width - PlayButton.width) / 2, (3 * Janela.height - 4 * PlayButton.height) / 8)
        DiffButtonPressed.set_position((Janela.width - PlayButton.width) / 2,
                                       (3 * Janela.height - 4 * PlayButton.height) / 8)
        RankButton.set_position((Janela.width - RankButton.width) / 2, (5 * Janela.height - 4 * RankButton.height) / 8)
        RankButtonPressed.set_position((Janela.width - RankButton.width) / 2,
                                       (5 * Janela.height - 4 * RankButton.height) / 8)
        ExitButton.set_position((Janela.width - PlayButton.width) / 2, (7 * Janela.height - 4 * PlayButton.height) / 8)
        ExitButtonPressed.set_position((Janela.width - PlayButton.width) / 2,
                                       (7 * Janela.height - 4 * PlayButton.height) / 8)

        Fundo.draw()  # Desenhando o fundo do menu.

        PlayButton.draw()  # Desenhando o botão "JOGAR" do menu.
        DiffButton.draw()  # Desenhando o botão "DIFICULDADE" do menu.
        RankButton.draw()  # Desenhando o botão "RANKING" do menu.
        ExitButton.draw()  # Desenhando o botão "SAIR" do menu.

        if Teclado.key_pressed("ESC"):  # Código preventivo para evitar conflitos
            if Cursor.is_over_object(PlayButton):
                PlayButtonPressed.draw()

            if Cursor.is_over_object(DiffButton):
                DiffButtonPressed.draw()

            if Cursor.is_over_object(RankButton):
                RankButtonPressed.draw()

            if Cursor.is_over_object(ExitButton):
                ExitButtonPressed.draw()

            Janela.update()

        else:
            # Verificando interações do Cursor:
            if Cursor.is_over_object(PlayButton):
                PlayButtonPressed.draw()
                if Cursor.is_button_pressed(1):
                    Menu_Sound.stop()
                    Play()  # Avança para a gameplay.

            if Cursor.is_over_object(DiffButton):
                DiffButtonPressed.draw()
                if Cursor.is_button_pressed(1):
                    Difficulty_Menu()  # Abre a aba de menu de dificuldades.

            if Cursor.is_over_object(RankButton):
                RankButtonPressed.draw()
                if Cursor.is_button_pressed(1):
                    pass  # Não implementado ainda

            if Cursor.is_over_object(ExitButton):
                ExitButtonPressed.draw()
                if Cursor.is_button_pressed(1):
                    Sair()  # Encerra a gameplay.

        Janela.update()

# ----------------------------------------------------------------------------------------------------- #


# -------------------------------------- Menu de Dificuldades ----------------------------------------- #

def Difficulty_Menu() -> None:  # Exibe o menu de dificuldades.

    global Cursor, Teclado, Janela, FundoMenuDiff, EasyButton, MedButton, HardButton, current_difficulty

    EasyButton.set_position((Janela.width - PlayButton.width) / 2, (2 * Janela.height - 3 * PlayButton.height) / 6)
    EasyButtonPressed.set_position((Janela.width - PlayButton.width) / 2,
                                   (2 * Janela.height - 3 * PlayButton.height) / 6)
    MedButton.set_position((Janela.width - PlayButton.width) / 2, (3 * Janela.height - 3 * PlayButton.height) / 6)
    MedButtonPressed.set_position((Janela.width - PlayButton.width) / 2,
                                  (3 * Janela.height - 3 * PlayButton.height) / 6)
    HardButton.set_position((Janela.width - PlayButton.width) / 2, (4 * Janela.height - 3 * PlayButton.height) / 6)
    HardButtonPressed.set_position((Janela.width - PlayButton.width) / 2,
                                   (4 * Janela.height - 3 * PlayButton.height) / 6)

    FundoMenuDiff.draw()
    EasyButton.draw()
    MedButton.draw()
    HardButton.draw()

    Janela.delay(300)  # Pequeno atraso para evitar conflitos.

    Menu_Sound.play()

    while True:
        Janela.update()
        FundoMenuDiff.draw()
        EasyButton.draw()
        MedButton.draw()
        HardButton.draw()

        if Cursor.is_over_object(EasyButton):
            EasyButtonPressed.draw()
            if Cursor.is_button_pressed(1):
                Constants.current_difficulty = Constants.Difficulty_Levels[0]
                Menu_Sound.stop()
                Play()
            if Teclado.key_pressed("ESC"):
                Menu()

        if Cursor.is_over_object(MedButton):
            MedButtonPressed.draw()
            if Cursor.is_button_pressed(1):
                Constants.current_difficulty = Constants.Difficulty_Levels[1]
                Menu_Sound.stop()
                Play()
            if Teclado.key_pressed("ESC"):
                Menu()

        if Cursor.is_over_object(HardButton):
            HardButtonPressed.draw()
            if Cursor.is_button_pressed(1):
                Constants.current_difficulty = Constants.Difficulty_Levels[2]
                Menu_Sound.stop()
                Play()
            if Teclado.key_pressed("ESC"):
                Menu()

        if Teclado.key_pressed("ESC"):
            Menu()

        Janela.update()

# ----------------------------------------------------------------------------------------------------- #


# ---------------------------------------- Encerramento do Jogo --------------------------------------- #

def Sair() -> None:  # Encerra o jogo.
    global Janela
    Janela.close()

# ----------------------------------------------------------------------------------------------------- #
#                                          ________________
#                                         /// Observação \\\
#                                         ------------------
#
#   Descobri que é impossível carregar um Sprite antes de criar uma Window,
# Sei que pode soar algo bem frívolo e até trivial, mas é bom salientar. Possivelmente devido ao pygame não
# ter inicializado uma janela para associá-los corretamente.
#
# ----------------------------------------------------------------------------------------------------- #


# Botões do menu:
PlayButton = Botoes.PlayButton
PlayButtonPressed = Botoes.PlayButtonPressed  # Botão "JOGAR" do menu principal pressionado.
DiffButton = Botoes.DiffButton  # Botão "DIFICULDADE" do menu principal.
DiffButtonPressed = Botoes.DiffButtonPressed  # Botão "DIFICULDADE" do menu principal pressionado.
RankButton = Botoes.RankButton  # Botão "RANKING" do menu principal.
RankButtonPressed = Botoes.RankButtonPressed  # Botão "RANKING" do menu principal pressionado.
ExitButton = Botoes.ExitButton  # Botão "SAIR" do menu principal.
ExitButtonPressed = Botoes.ExitButtonPressed  # Botão "SAIR" do menu principal pressionado.

# Botões do Menu de dificuldades:
EasyButton = Botoes.EasyButton  # Botão "FACIL" do menu de dificuldade.
EasyButtonPressed = Botoes.EasyButtonPressed  # Botão "FACIL" do menu de dificuldade pressionado.
MedButton = Botoes.MedButton  # Botão "MEDIO" do menu de dificuldade.
MedButtonPressed = Botoes.MedButtonPressed  # Botão "MEDIO" do menu de dificuldade pressionado.
HardButton = Botoes.HardButton  # Botão "DIFICIL" do menu de dificuldade.
HardButtonPressed = Botoes.HardButtonPressed  # Botão "DIFICIL" do menu de dificuldade pressionado.

# --------------------------------- Carregando Arquivos do Joagdor --------------------------------- #

Player = Sprite("Assets/player.png", 1)  # Imagem da Nave do jogador.
Player.speed = Constants.Player_Speed
Player.direction = -1
Player.shooted = False
Player.last_shot = Janela.time_elapsed()
# Definindo a posiçao inicial do jogador:
Player.set_position((Constants.ScrWdt - Player.width) / 2, (Constants.ScrHgt - Player.height - Constants.ScrHgt / 50))
Player.score = 0  # Definindo a pontuação inicial do jogador.

# --------------------------------- Carregando Arquivos dos Inimigos --------------------------------- #

red_enemy = Sprite("Assets/red_enemy.png", 1)

# --------------------------------- Controladores Temporais ------------------------------------------ #

enemy_shoot_delay = 1 / Constants.Game_Speed

# Game Loop:
while True:
    # Iniciando o jogo pelo menu:
    Menu()

    Janela.update()  # Atualizando a janela do jogo.

# Perdão se o código ficou muito esparso ou desorganizado ksksks
# by: Allber Fellype
