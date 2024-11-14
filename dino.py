import pygame
from settings import SCREEN_HEIGHT, GRAVITY, JUMP_STRENGTH  # Certifique-se de que esses valores estão no settings.py

class Dino(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position):
        super().__init__()

        # Carrega as imagens para o estado normal e de pulo
        self.normal_image = pygame.image.load('img/dino.png').convert_alpha()
        self.normal_image = pygame.transform.scale(self.normal_image, (64, 64))
        
        self.jump_image = pygame.image.load('img/dinoPULO.png').convert_alpha()
        self.jump_image = pygame.transform.scale(self.jump_image, (64, 64))

        # Define a imagem atual como a normal
        self.image = self.normal_image
        self.rect = self.image.get_rect(topleft=(x_position, y_position))

        # Cria uma máscara de colisão
        self.mask = pygame.mask.from_surface(self.image)

        # Propriedades de movimento
        self.is_jumping = False
        self.jump_height = JUMP_STRENGTH
        self.gravity = GRAVITY
        self.velocity = 0

    def update(self):
        """Atualiza a posição do dinossauro e aplica a física do pulo."""
        if self.is_jumping:
            self.image = self.jump_image  # Alterna para a imagem de pulo
            self.rect.y -= self.velocity
            self.velocity -= self.gravity

            # Quando toca o chão, volta ao estado normal
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                self.is_jumping = False
                self.velocity = 0
                self.image = self.normal_image  # Volta para a imagem normal

    def jump(self):
        """Inicia o pulo do dinossauro."""
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = self.jump_height

    def draw(self, screen):
        """Desenha o dinossauro na tela."""
        screen.blit(self.image, self.rect)

    def get_mask(self):
        """Retorna a máscara de colisão do dinossauro."""        
        return self.mask


class DemonDino:
    def __init__(self, x_position, y_position):
        """Inicializa o DemonDino com posição e imagens de movimento."""
        
        # Imagem normal e de pulo
        self.normal_image = pygame.image.load("img/DEMONSAURO.png").convert_alpha()
        self.normal_image = pygame.transform.scale(self.normal_image, (64, 64))
        
        self.jump_image = pygame.image.load("img/DEMONSAUROPULO.png").convert_alpha()
        self.jump_image = pygame.transform.scale(self.jump_image, (64, 64))

        # Define a imagem inicial e retângulo
        self.image = self.normal_image
        self.rect = self.image.get_rect(topleft=(x_position, y_position))

        # Máscara de colisão
        self.mask = pygame.mask.from_surface(self.image)

        # Controle de movimento
        self.is_jumping = False
        self.y_velocity = 0
        self.jump_strength = -JUMP_STRENGTH
        self.gravity = GRAVITY

    def jump(self):
        """Faz o DemonDino pular."""        
        if not self.is_jumping:
            self.is_jumping = True
            self.y_velocity = self.jump_strength

    def update(self):
        """Atualiza a posição do DemonDino e aplica a gravidade."""
        if self.is_jumping:
            self.image = self.jump_image  # Alterna para a imagem de pulo
            self.rect.y += self.y_velocity
            self.y_velocity += self.gravity

            # Quando toca o chão, volta ao estado normal
            if self.rect.bottom >= SCREEN_HEIGHT - 50:
                self.rect.bottom = SCREEN_HEIGHT - 50
                self.is_jumping = False
                self.image = self.normal_image  # Volta para a imagem normal

    def draw(self, screen):
        """Desenha o DemonDino na tela."""
        screen.blit(self.image, self.rect.topleft)

    def get_mask(self):
        """Retorna a máscara de colisão do DemonDino."""        
        return self.mask


def check_collision(dino, demon_dino):
    """Verifica a colisão entre o Dino e o DemonDino usando máscaras."""
    dino_mask = dino.get_mask()
    demon_dino_mask = demon_dino.get_mask()
    offset = (dino.rect.x - demon_dino.rect.x, dino.rect.y - demon_dino.rect.y)
    if dino_mask.overlap(demon_dino_mask, offset) is not None:
        print("Colisão detectada!")
        return True
    return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    dino = Dino(x_position=50, y_position=SCREEN_HEIGHT - 50)
    demon_dino = DemonDino(x_position=150, y_position=SCREEN_HEIGHT - 50)

    show_demon_dino = False
    running = True
    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            dino.jump()
        if keys[pygame.K_d]:
            show_demon_dino = True
        else:
            show_demon_dino = False

        dino.update()
        if show_demon_dino:
            demon_dino.update()

        # Verifica a colisão
        if check_collision(dino, demon_dino):
            print("Colisão detectada!")

        dino.draw(screen)
        if show_demon_dino:
            demon_dino.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
