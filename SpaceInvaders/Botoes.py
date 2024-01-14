from pplay.sprite import *
import Constants  # Constantes referentes ao jogo.

janela_temp = Window(Constants.ScrWdt, Constants.ScrHgt)  # Janela descartável, caso não haja, os sprites não carregam.

# Botões do menu:
PlayButton = Sprite("Assets/PlayButton.png", 1)  # Botão "JOGAR" do menu principal.
PlayButtonPressed = Sprite("Assets/PlayButtonPressed.png", 1)  # Botão "JOGAR" do menu principal pressionado.
DiffButton = Sprite("Assets/DiffButton.png", 1)  # Botão "DIFICULDADE" do menu principal.
DiffButtonPressed = Sprite("Assets/DiffButtonPressed.png", 1)  # Botão "DIFICULDADE" do menu principal pressionado.
RankButton = Sprite("Assets/RankingButton.png", 1)  # Botão "RANKING" do menu principal.
RankButtonPressed = Sprite("Assets/RankingButtonPressed.png", 1)  # Botão "RANKING" do menu principal pressionado.
ExitButton = Sprite("Assets/ExitButton.png", 1)  # Botão "SAIR" do menu principal.
ExitButtonPressed = Sprite("Assets/ExitButtonPressed.png", 1)  # Botão "SAIR" do menu principal pressionado.

# Botões do Menu de dificuldades:
EasyButton = Sprite("Assets/EasyButton.png", 1)  # Botão "FACIL" do menu de dificuldade.
EasyButtonPressed = Sprite("Assets/EasyButtonPressed.png", 1)  # Botão "FACIL" do menu de dificuldade pressionado.
MedButton = Sprite("Assets/MedButton.png", 1)  # Botão "MEDIO" do menu de dificuldade.
MedButtonPressed = Sprite("Assets/MedButtonPressed.png", 1)  # Botão "MEDIO" do menu de dificuldade pressionado.
HardButton = Sprite("Assets/HardButton.png", 1)  # Botão "DIFICIL" do menu de dificuldade.
HardButtonPressed = Sprite("Assets/HardButtonPressed.png", 1)  # Botão "DIFICIL" do menu de dificuldade pressionado.