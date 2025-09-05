from settings import *
import pygame
import pygame_menu
import sys

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))


class Personaje(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color=(255, 255, 255), path=None):
        super().__init__()
        img = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.smoothscale(img, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vivo = True


class Heroe(Personaje):
    def __init__(self, x, y, w=TAM_HEROE, h=TAM_HEROE):
        super().__init__(x, y, w, h, HEROE, SPRITE_HEROE)


class Enemigo(Personaje):
    def __init__(self, x, y, w=TAM_ENEMIGO, h=TAM_ENEMIGO):
        super().__init__(x, y, w, h, ENEMIGO, SPRITE_ENEMIGO)
        self.pos_inicial = (x, y)


class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TAM_BALA, TAM_BALA))
        self.image.fill(BALA)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def mover(self, dt):
        self.rect.y -= VEL_BALA * dt
        if self.rect.y < 0:
            self.kill()


def disparar(balas, heroe):
    # Limite de disparos
    if len(balas) < 5:
        nueva_bala = Bala(heroe.rect.centerx, heroe.rect.top)
        balas.add(nueva_bala)


def colisiones(balas, enemigos):
    puntos = 0
    for bala in balas.sprites():
        for enemigo in enemigos:
            if enemigo.vivo and bala.rect.colliderect(enemigo.rect):
                bala.kill()
                enemigo.vivo = False
                puntos += 10
                break
    return puntos


def mostrar_texto(pantalla, texto, x, y, tamaño=24):
    fuente = pygame.font.SysFont("Arial", tamaño)
    texto_render = fuente.render(texto, True, TEXTO)
    pantalla.blit(texto_render, (x, y))


def main(dificultad=0.1):

    pygame.display.set_caption("Space Invaders")
    reloj = pygame.time.Clock()

    fondo = pygame.image.load(FONDO_IMG).convert()
    fondo = pygame.transform.smoothscale(fondo, (ANCHO, ALTO))

    # Crear héroe
    heroe = Heroe(ANCHO//2 - TAM_HEROE//2, ALTO - 80)

    # Crear enemigos
    enemigos = []
    for fila in range(FILAS):
        for col in range(COLS):
            x = MARGEN + col * (TAM_ENEMIGO + GAP_X)
            y = MARGEN + fila * (TAM_ENEMIGO + GAP_Y)
            enemigo = Enemigo(x, y)
            enemigos.append(enemigo)

    balas = pygame.sprite.Group()

    vidas_extra = 0
    puntos = 0
    vidas = 3
    juego_terminado = False
    vel_enemigos = VEL_ENEMIGO * dificultad

    while True:
        dt = reloj.tick(60) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not juego_terminado:
                    disparar(balas, heroe)
                elif evento.key == pygame.K_r and juego_terminado:
                    # Reiniciar juego
                    for enemigo in enemigos:
                        enemigo.vivo = True
                        enemigo.rect.x, enemigo.rect.y = enemigo.pos_inicial
                    balas.empty()
                    puntos = 0
                    vidas = 3
                    juego_terminado = False
                    heroe.rect.centerx = ANCHO // 2

        # Controles
        teclas = pygame.key.get_pressed()
        if not juego_terminado:
            # Mover héroe
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                heroe.rect.x -= VEL_HEROE * dt
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                heroe.rect.x += VEL_HEROE * dt

            # Límites pantalla
            if heroe.rect.left < 0:
                heroe.rect.left = 0
            elif heroe.rect.right > ANCHO:
                heroe.rect.right = ANCHO

            # Mover balas
            for bala in balas:
                bala.mover(dt)

            # Mover enemigos y revisar colisiones con héroe
            perdio_vida = False
            for enemigo in enemigos:
                if enemigo.vivo:
                    enemigo.rect.y += vel_enemigos * dt
                    if enemigo.rect.bottom >= ALTO or enemigo.rect.colliderect(heroe.rect):
                        perdio_vida = True
                        break

            # Colisiones bala-enemigo
            puntos_ganados = colisiones(balas, enemigos)
            puntos += puntos_ganados

            # Si perdió vida
            if perdio_vida:
                vidas -= 1
                if vidas <= 0:
                    juego_terminado = True
                else:
                    # Reset posiciones
                    for enemigo in enemigos:
                        if enemigo.vivo:
                            enemigo.rect.x, enemigo.rect.y = enemigo.pos_inicial
                    heroe.rect.centerx = ANCHO // 2
                    balas.empty()

            # Revivir a todos los enemigos muertos
            if not any(enemigo.vivo for enemigo in enemigos):
                for enemigo in enemigos:
                    enemigo.vivo = True
                    enemigo.rect.x, enemigo.rect.y = enemigo.pos_inicial

        # Vida Extra
        if puntos >= vidas_extra + 1000:
            vidas += 1
            vidas_extra = puntos

        pantalla.blit(fondo, (0, 0))

        # Mostrar enemigos vivos
        for enemigo in enemigos:
            if enemigo.vivo:
                pantalla.blit(enemigo.image, enemigo.rect)

        pantalla.blit(heroe.image, heroe.rect)
        balas.draw(pantalla)

        # Textos
        mostrar_texto(pantalla, f"Puntos: {puntos}", 20, 20)
        mostrar_texto(pantalla, f"Vidas: {vidas}", ANCHO - 120, 20)

        if juego_terminado:
            mostrar_texto(pantalla, "GAME OVER - Presiona R para reiniciar",
                          ANCHO//2 - 250, ALTO//2, 32)

        pygame.display.flip()


def facil():
    main(0.1)


def medio():
    main(0.15)


def dificil():
    main(0.3)


def salir():
    pygame.quit()
    sys.exit()


def menu():

    menu = pygame_menu.Menu('Space Invaders', ANCHO,
                            ALTO, theme=pygame_menu.themes.THEME_DARK)

    menu.add.button('Fácil', facil)
    menu.add.button('Medio', medio)
    menu.add.button('Difícil', dificil)
    menu.add.button('Salir', salir)

    menu.mainloop(pantalla)


if __name__ == "__main__":
    menu()
