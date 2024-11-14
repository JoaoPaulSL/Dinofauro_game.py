import pygame
import random
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Obstacle(pygame.sprite.Sprite):  
    def __init__(self, x):
        super().__init__()

        # Carrega a imagem do obstáculo com transparência e redimensiona para uma altura aleatória
        self.image = pygame.image.load("img/fire1(obstacle).png").convert_alpha()
        
        # Altura aleatória para o obstáculo
        self.height = random.choice([48, 64, 80])
        
        # Redimensiona a imagem para a largura fixa de 64px e a altura aleatória
        self.image = pygame.transform.scale(self.image, (64, self.height))

        # Define a posição inicial do obstáculo
        self.rect = self.image.get_rect(topleft=(x, SCREEN_HEIGHT - self.height))

        # Cria uma máscara precisa da imagem redimensionada para colisão
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, speed):
        """Move o obstáculo para a esquerda na tela."""
        self.rect.x -= speed

    def draw(self, screen, debug=False):
        """Desenha o obstáculo na tela e, opcionalmente, o contorno da máscara para depuração."""
        screen.blit(self.image, self.rect.topleft)
        
        if debug:
            mask_outline = self.mask.outline()
            pygame.draw.lines(screen, (255, 0, 0), True, [(self.rect.x + x, self.rect.y + y) for x, y in mask_outline], 2)

    def get_mask(self):
        """Retorna a máscara de colisão do obstáculo."""
        return self.mask

    def is_off_screen(self):
        """Verifica se o obstáculo saiu da tela."""
        return self.rect.x < -self.rect.width


# Variáveis globais para controle dos obstáculos
obstacle_list = pygame.sprite.Group()  
spawn_timer = 0  # Temporizador de geração de obstáculos
spawn_interval = 1500  # Intervalo de tempo para geração de novos obstáculos em ms
game_over_flag = False  # Flag para o estado de Game Over

def update_obstacles(speed, screen, clock, dino, debug=False):
    """Atualiza, gera, desenha e remove obstáculos conforme necessário."""
    global spawn_timer, game_over_flag

    if not game_over_flag:
        # Atualiza o temporizador de geração de obstáculos
        spawn_timer += clock.get_time()

    # Gera novo obstáculo se o intervalo de tempo for alcançado
    if spawn_timer > spawn_interval and not game_over_flag:
        new_obstacle = Obstacle(SCREEN_WIDTH)
        obstacle_list.add(new_obstacle)  # Adiciona ao grupo de obstáculos
        spawn_timer = 0  # Reseta o temporizador

    # Move, desenha e remove obstáculos fora da tela
    for obstacle in obstacle_list:
        obstacle.move(speed)
        obstacle.draw(screen, debug=debug)  # Habilita o modo de depuração se necessário

        # Verifica se ocorreu uma colisão entre o dinossauro e o obstáculo
        if check_collision(dino, obstacle):
            game_over()  # Função para tratar o game over

        if obstacle.is_off_screen():
            obstacle_list.remove(obstacle)  # Remove do grupo

def check_collision(dino, obstacle):
    """Verifica se o dinossauro colidiu com um obstáculo usando a silhueta das máscaras."""
    dino_mask = dino.get_mask()
    obstacle_mask = obstacle.get_mask()

    # Calcula o deslocamento entre o dinossauro e o obstáculo
    offset_x = obstacle.rect.x - dino.rect.x
    offset_y = obstacle.rect.y - dino.rect.y
    offset = (offset_x, offset_y)

    # Verifica a sobreposição entre as máscaras
    if dino_mask.overlap(obstacle_mask, offset):
        return True
    return False


def game_over():
    """Função que trata a lógica do game over."""
    global game_over_flag
    game_over_flag = True
    print("Fim de jogo! Pressione R para reiniciar.")
    # Aqui você pode pausar o jogo ou apresentar uma tela de fim de jogo.

def reset_obstacles():
    """Reseta a lista de obstáculos e o temporizador."""
    global obstacle_list, spawn_timer, game_over_flag
    obstacle_list.empty()  # Limpa o grupo de obstáculos
    spawn_timer = 0  # Reseta o temporizador de geração de obstáculos
    game_over_flag = False  # Reseta a flag de game over

# Função para reiniciar o jogo
def handle_restart():
    """Reinicia o jogo se o jogador pressionar a tecla 'R'."""
    global game_over_flag
    if game_over_flag:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            reset_obstacles()  # Reseta os obstáculos e a flag
            print("Jogo reiniciado.")
            game_over_flag = False
