import pygame

class SoundManager:
    def __init__(self):
        # Inicializa o mixer
        pygame.mixer.init()

        # Carrega os sons
        self.jump_sound = pygame.mixer.Sound('sounds/sound_jump.mp3')  # Som do pulo
        self.collision_sound = pygame.mixer.Sound('sounds/colisao_sound.mp3')  # Som de colisão

    def play_jump_sound(self):
        """Toca o som do pulo."""
        self.jump_sound.play()

    def play_collision_sound(self):
        """Toca o som de colisão."""
        self.collision_sound.play()

# Exemplo de uso
if __name__ == "__main__":
    pygame.init()  # Inicializa o Pygame
    screen = pygame.display.set_mode((800, 600))  # Tamanho da tela (800x600)
    sound_manager = SoundManager()  # Cria uma instância do SoundManager

    # Loop para manter a janela aberta
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Exemplo: tocando o som de pulo quando pressionar a tecla 'space'
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            sound_manager.play_jump_sound()  # Toca o som de pulo

        # Exemplo: tocando o som de colisão quando pressionar a tecla 'c'
        if keys[pygame.K_c]:
            sound_manager.play_collision_sound()  # Toca o som de colisão

    pygame.quit()
