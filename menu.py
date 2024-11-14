import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.options = ["Iniciar Jogo", "Configurações", "Sair"]
        self.selected_option = 0  # Índice da opção selecionada

    def display_menu(self):
        self.screen.fill((135, 206, 235))  # Cor de fundo azul claro
        title = self.font.render("Jogo Dinofauro", True, (255, 255, 255))
        self.draw_text(title, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        for index, option in enumerate(self.options):
            color = (255, 255, 0) if index == self.selected_option else (255, 255, 255)
            option_text = self.font.render(f"{index + 1}. {option}", True, color)
            self.draw_text(option_text, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + index * 60)

        pygame.display.flip()

    def draw_text(self, text, x, y):
        """Desenha o texto na tela em uma posição específica."""
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected_option].lower().replace(" ", "_")  # Retorna a opção selecionada formatada
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Botão esquerdo do mouse
                mouse_x, mouse_y = event.pos
                action = self.check_mouse_click(mouse_x, mouse_y)
                if action:
                    return action  # Retorna a ação se uma opção foi clicada

    def check_mouse_click(self, mouse_x, mouse_y):
        """Verifica se uma opção foi clicada com o mouse."""
        for index in range(len(self.options)):
            option_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + index * 60 - 20, 200, 40)  # Área clicável
            if option_rect.collidepoint(mouse_x, mouse_y):
                self.selected_option = index
                return self.options[self.selected_option].lower().replace(" ", "_")  # Retorna a opção selecionada formatada
        return None  # Retorna None se nenhuma opção foi clicada

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Menu do Jogo")
    menu = Menu(screen)

    while True:
        menu.display_menu()
        action = menu.handle_events()

        if action == "iniciar_jogo":
            print("Iniciando o jogo...")
            # Aqui você pode chamar a função para iniciar o jogo
        elif action == "configurações":
            print("Abrindo configurações...")
            # Aqui você pode chamar a função para abrir as configurações
        elif action == "sair":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
