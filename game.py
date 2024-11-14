import pygame
import sys
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from dino import Dino
from obstacle import Obstacle
from sounds import SoundManager

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.dino = Dino(x_position=50, y_position=SCREEN_HEIGHT - 64)  # Passando x e y para Dino
        self.obstacles = pygame.sprite.Group()  # Usando Group para gerenciar obstáculos
        self.score = 0
        self.record = 0
        self.obstacle_speed = 5
        self.game_over = False

        # Configuração de eventos para geração de obstáculos e pontuação
        self.spawn_obstacle_event = pygame.USEREVENT
        pygame.time.set_timer(self.spawn_obstacle_event, 1500)  # A cada 1.5 segundos
        self.score_increment_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.score_increment_event, 100)  # A cada 100 ms

        # Inicializa o gerenciador de som
        self.sound_manager = SoundManager()

        # Carregar e redimensionar a imagem de fundo
        background_image = pygame.image.load('img/background.png').convert()
        self.background = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def restart(self):
        """Reinicia o jogo."""
        self.obstacles.empty()  # Limpa o grupo de obstáculos
        self.score = 0
        self.dino.rect.y = SCREEN_HEIGHT - 64
        self.dino.is_jumping = False
        self.game_over = False
        self.obstacle_speed = 5

    def run(self):
        """Loop principal do jogo."""
        while True:
            self.handle_events()
            if not self.game_over:
                self.dino.update()
                self.update_game_state()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        """Lida com eventos do jogo."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == self.spawn_obstacle_event:
                self.spawn_obstacle()
            elif event.type == self.score_increment_event and not self.game_over:
                self.score += 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.dino.is_jumping and not self.game_over:
                    self.dino.jump()
                    self.sound_manager.play_jump_sound()
                elif self.game_over and event.key == pygame.K_r:
                    self.restart()

    def spawn_obstacle(self):
        """Gera e adiciona um novo obstáculo ao grupo."""
        new_obstacle = Obstacle(SCREEN_WIDTH)
        self.obstacles.add(new_obstacle)

    def update_game_state(self):
        """Atualiza o estado do jogo, incluindo movimento de obstáculos e verificação de colisão."""
        for obstacle in self.obstacles:
            obstacle.move(self.obstacle_speed)

            if self.check_collision(self.dino, obstacle):
                self.sound_manager.play_collision_sound()
                self.game_over = True

            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
                self.score += 5

                # Aumenta a dificuldade ao longo do tempo
                self.increase_difficulty()

        # Atualiza o recorde se a pontuação atual for maior
        if self.score > self.record and not self.game_over:
            self.record = self.score

    def check_collision(self, dino, obstacle):
        """Verifica colisão entre o dinossauro e um obstáculo usando máscaras."""
        dino_mask = dino.get_mask()
        obstacle_mask = obstacle.get_mask()

        # Calcula o deslocamento entre as posições dos retângulos
        offset = (dino.rect.x - obstacle.rect.x, dino.rect.y - obstacle.rect.y)

        # Verifica se há sobreposição entre as máscaras usando o deslocamento
        return dino_mask.overlap(obstacle_mask, offset) is not None

    def increase_difficulty(self):
        """Aumenta a dificuldade com base na pontuação."""
        if self.score > 0 and self.score % 300 == 0:
            self.obstacle_speed += 1
            print(f"Velocidade dos obstáculos aumentada para: {self.obstacle_speed}")

    def draw(self):
        """Desenha todos os elementos na tela."""
        # Fundo
        self.screen.blit(self.background, (0, 0))

        # Dinossauro e obstáculos
        self.dino.draw(self.screen)
        self.obstacles.draw(self.screen)  # Draw todos os obstáculos de uma vez

        # Pontuação e recorde
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score} | Record: {self.record}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

        # Tela de Game Over
        if self.game_over:
            font_game_over = pygame.font.Font(None, 72)
            game_over_text = font_game_over.render("Game Over", True, (255, 0, 0))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

            restart_text = font.render("Pressione 'R' para reiniciar", True, (0, 0, 0))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 20))

        # Atualiza a tela
        pygame.display.flip()
