import pygame
import sys
from game import Game
from menu import Menu  # Certifique-se de que o menu.py está no mesmo diretório

# Inicializa o Pygame
pygame.init()

# Definindo a tela
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo Dinofauro")

# Cria uma instância do menu e do jogo
menu = Menu(screen)
game = Game(screen)

# Função principal do jogo
def main():
    running = True
    in_game = False  # Variável para controlar se estamos no jogo ou no menu
    action = None

    while running:
        if not in_game:
            # Exibe o menu e aguarda a seleção do jogador
            menu.display_menu()
            action = menu.handle_events()  # Captura os eventos no menu

            if action == "iniciar_jogo":
                in_game = True  # Muda para o estado de jogo
                game.restart()  # Reinicia o jogo antes de começar
                game.run()  # Inicia o jogo
                in_game = False  # Retorna para o menu após o fim do jogo
            elif action == "configurações":
                # Aqui você pode adicionar lógica para abrir um menu de configurações
                print("Abrindo configurações...")  # Placeholder para lógica de configurações
            elif action == "sair":
                pygame.quit()
                sys.exit()

        # Atualiza a tela
        pygame.display.flip()

if __name__ == "__main__":
    main()
