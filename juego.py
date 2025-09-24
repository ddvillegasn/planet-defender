import pygame
import random
import sys
import time

# Configuración de pantalla
ANCHO = 800
ALTO = 600

# Inicialización de Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Planet Defender")

# Cargar imágenes
fondo = pygame.image.load("fondo.jpg").convert()
fondo = pygame.transform.smoothscale(fondo, (ANCHO, ALTO))  # Escalar suavemente el fondo
meteorito_imagen = pygame.image.load("meteoritos.png").convert_alpha()
meteorito_imagen = pygame.transform.scale(meteorito_imagen, (30, 30))  # Ajustar tamaño de los meteoritos
nave_imagen = pygame.image.load("nave.png").convert_alpha()
nave_imagen = pygame.transform.scale(nave_imagen, (50, 50))  # Ajustar tamaño de la nave
poder_imagen = pygame.image.load("poder.png").convert_alpha()
poder_imagen = pygame.transform.scale(poder_imagen, (50, 50))  # Ajustar tamaño del poder

# Configuración del reloj
reloj = pygame.time.Clock()
# Cargar el sonido de disparo
pygame.mixer.init()
sonido_disparo = pygame.mixer.Sound("sonidodisparo.mp3")
# Cargar el sonido de fondo
sonido_fondo = pygame.mixer.Sound("sonidofondo.mp3")  
sonido_fondo.play(loops=-1, maxtime=0, fade_ms=0)
# Clases de objetos del juego
class Cannon:
    def __init__(self, x, y):
        self.imagen = nave_imagen
        self.rect = self.imagen.get_rect(center=(x, y))
        self.velocidad = 8

    def mover(self, direccion):
        if direccion == "izquierda" and self.rect.left > 0:
            self.rect.x -= self.velocidad
        elif direccion == "derecha" and self.rect.right < ANCHO:
            self.rect.x += self.velocidad
        elif direccion == "arriba" and self.rect.top > 0:
            self.rect.y -= self.velocidad
        elif direccion == "abajo" and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)


# Cargar la imagen del proyectil
proyectil_imagen = pygame.image.load("Proyectil.png").convert_alpha()

# Reducir el tamaño de la imagen del proyectil al 50% del tamaño original
nuevo_ancho = int(proyectil_imagen.get_width() * 0.01)
nuevo_alto = int(proyectil_imagen.get_height() * 0.01)
proyectil_imagen = pygame.transform.scale(proyectil_imagen, (nuevo_ancho, nuevo_alto))

class Proyectil:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = -10
        self.imagen = proyectil_imagen
        self.rect = self.imagen.get_rect(center=(x, y))

    def mover(self):
        self.y += self.velocidad
        self.rect.y = self.y

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def fuera_de_pantalla(self):
        return self.y < 0

 
class Meteorito:
    def __init__(self, velocidad):
        self.x = random.randint(0, ANCHO - meteorito_imagen.get_width())
        self.y = 0
        self.velocidad = velocidad  # Velocidad depende del nivel de dificultad

    def mover(self):
        self.y += self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(meteorito_imagen, (self.x, self.y))

    def fuera_de_pantalla(self):
        return self.y > ALTO


class Poder:
    def __init__(self):
        self.x = random.randint(0, ANCHO - poder_imagen.get_width())
        self.y = random.randint(0, ALTO - poder_imagen.get_height())
        self.rect = pygame.Rect(self.x, self.y, poder_imagen.get_width(), poder_imagen.get_height())

    def dibujar(self, pantalla):
        pantalla.blit(poder_imagen, (self.x, self.y))

# Función para seleccionar el nivel de dificultad
def seleccionar_nivel():
    nivel = None
    fuente = pygame.font.Font(None, 36)
    texto_inicio = fuente.render("Selecciona dificultad (1: Fácil, 2: Medio, 3: Difícil)", True, (255, 255, 255))

    while nivel is None:
        pantalla.fill((0, 0, 0))
        pantalla.blit(texto_inicio, (100, 250))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    nivel = "fácil"
                elif event.key == pygame.K_2:
                    nivel = "medio"
                elif event.key == pygame.K_3:
                    nivel = "difícil"

    return nivel

# Función principal del juego
def main():
    # Selección del nivel de dificultad
    nivel_dificultad = seleccionar_nivel()

    # Configurar variables según el nivel de dificultad
    if nivel_dificultad == "fácil":
        velocidad_meteoritos = random.randint(1, 3)
        frecuencia_meteoritos = 70  # Menos meteoritos
    elif nivel_dificultad == "medio":
        velocidad_meteoritos = random.randint(3, 5)
        frecuencia_meteoritos = 50
    else:  # difícil
        velocidad_meteoritos = random.randint(5, 7)
        frecuencia_meteoritos = 30  # Más meteoritos

    # Inicialización de objetos
    cañones = [Cannon(ANCHO // 2, ALTO - 50)]
    proyectiles = []
    meteoritos = []
    poder = None
    puntaje = 0
    vidas = 10  # Agregar sistema de vidas
    fuente = pygame.font.Font(None, 36)
    tiempo_ultimo_poder = time.time()  # Tiempo para controlar aparición de poder
    # Bucle principal del juego
    corriendo = True
    while corriendo:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for cañon in cañones:
                        proyectiles.append(Proyectil(cañon.rect.centerx, cañon.rect.top))

        # Movimiento de los cañones
        keys = pygame.key.get_pressed()
        for cañon in cañones:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                cañon.mover("izquierda")
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                cañon.mover("derecha")
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                cañon.mover("arriba")
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                cañon.mover("abajo")

        # Movimiento de proyectiles
        for proyectil in proyectiles:
            proyectil.mover()
        proyectiles = [p for p in proyectiles if not p.fuera_de_pantalla()]

        # Generación y movimiento de meteoritos
        if random.randint(1, frecuencia_meteoritos) == 1:
            meteoritos.append(Meteorito(velocidad_meteoritos))

        for meteorito in meteoritos:
            meteorito.mover()

        # Colisión entre proyectiles y meteoritos
        for proyectil in proyectiles:
            for meteorito in meteoritos:
                if abs(proyectil.x - meteorito.x) < 20 and abs(proyectil.y - meteorito.y) < 20:
                    proyectiles.remove(proyectil)
                    meteoritos.remove(meteorito)
                    puntaje += 1
                    sonido_disparo.play()  # Reproducir el sonido
                    break

        # Colisión de meteoritos con la parte inferior de la pantalla
        for meteorito in meteoritos:
            if meteorito.fuera_de_pantalla():
                meteoritos.remove(meteorito)
                vidas -= 1  # Reducir una vida si un meteorito alcanza el planeta

        # Aparición del poder cada 5 segundos
        if time.time() - tiempo_ultimo_poder > 5:
            poder = Poder()
            tiempo_ultimo_poder = time.time()

        # Verificar colisión con el poder
        if poder:
            for cañon in cañones:
                if cañon.rect.colliderect(poder.rect):
                    cañones.append(Cannon(cañon.rect.x, cañon.rect.y))
                    poder = None
                    break
        # Aumentar la dificultad si el puntaje supera 15
        if puntaje > 15 and nivel_dificultad in ["fácil"]:
            velocidad_meteoritos = random.randint(3, 3)  # Aumenta la velocidad de los meteoritos
            frecuencia_meteoritos = 50  # Meteoritos más frecuentes
            texto_dificultad = fuente.render("¡Aumento de dificultad! Meteoritos más rápidos", True, (255, 0, 0))
            pantalla.blit(texto_dificultad, (ANCHO // 2 - 250, ALTO // 2 - 100))

        # Aumentar la dificultad si el puntaje supera 30
        if puntaje > 30 and nivel_dificultad in ["fácil"]:
            velocidad_meteoritos = random.randint(5, 5)  # Aumenta la velocidad de los meteoritos
            frecuencia_meteoritos = 60  # Meteoritos más frecuentes
            texto_dificultad = fuente.render("¡Aumento de dificultad! Meteoritos más rápidos", True, (255, 0, 0))
            pantalla.blit(texto_dificultad, (ANCHO // 2 - 250, ALTO // 2 - 100))

        # Aumentar la dificultad si el puntaje supera 15
        if puntaje > 15 and nivel_dificultad in ["medio"]:
            velocidad_meteoritos = random.randint(5, 5)  # Aumenta la velocidad de los meteoritos
            frecuencia_meteoritos = 40  # Meteoritos más frecuentes
            texto_dificultad = fuente.render("¡Aumento de dificultad! Meteoritos más rápidos", True, (255, 0, 0))
            pantalla.blit(texto_dificultad, (ANCHO // 2 - 250, ALTO // 2 - 100))

        # Aumentar la dificultad si el puntaje supera 30
        if puntaje > 30 and nivel_dificultad in ["medio"]:
            velocidad_meteoritos = random.randint(6, 6)  # Aumenta la velocidad de los meteoritos
            frecuencia_meteoritos = 30  # Meteoritos más frecuentes
            texto_dificultad = fuente.render("¡Aumento de dificultad! Meteoritos más rápidos", True, (255, 0, 0))
            pantalla.blit(texto_dificultad, (ANCHO // 2 - 250, ALTO // 2 - 100))

        # Aumentar la dificultad si el puntaje supera 30
        if puntaje > 30 and nivel_dificultad in ["difícil"]:
            velocidad_meteoritos = random.randint(7, 7)  # Aumenta la velocidad de los meteoritos
            frecuencia_meteoritos = 30  # Meteoritos más frecuentes
            texto_dificultad = fuente.render("¡Aumento de dificultad! Meteoritos más rápidos", True, (255, 0, 0))
            pantalla.blit(texto_dificultad, (ANCHO // 2 - 250, ALTO // 2 - 100))
        # Verificar si el jugador ha ganado
        if puntaje >= 50:
            texto_victoria = fuente.render("¡Felicitaciones! Has salvado el mundo", True, (0, 255, 0))
            texto_detalle = fuente.render("Eres el héroe del sistema Élarium.", True, (255, 255, 255))
            pantalla.blit(fondo, (0, 0))  # Dibujar el fondo nuevamente
            pantalla.blit(texto_victoria, (ANCHO // 2 - 250, ALTO // 2 - 50))
            pantalla.blit(texto_detalle, (ANCHO // 2 - 250, ALTO // 2))
            pygame.display.flip()
            time.sleep(5)  # Esperar unos segundos para mostrar el mensaje
            corriendo = False
            
        # Dibujar pantalla
        pantalla.blit(fondo, (0, 0))  # Dibujar el fondo
        for cañon in cañones:
            cañon.dibujar(pantalla)

        for proyectil in proyectiles:
            proyectil.dibujar(pantalla)

        for meteorito in meteoritos:
            meteorito.dibujar(pantalla)

        if poder:
            poder.dibujar(pantalla)

        # Mostrar puntaje y vidas
        texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
        texto_vidas = fuente.render(f"Vidas: {vidas}", True, (255, 255, 255))
        pantalla.blit(texto_puntaje, (10, 10))
        pantalla.blit(texto_vidas, (10, 50))

        # Verificar fin del juego
        if vidas <= 0:
            texto_final = fuente.render("¡Game Over!", True, (255, 0, 0))
            pantalla.blit(texto_final, (ANCHO // 2 - 100, ALTO // 2))
            pygame.display.flip()
            time.sleep(2)
            corriendo = False

        # Actualizar la pantalla
        pygame.display.update()
        reloj.tick(60)


    # Cerrar Pygame
    pygame.quit()
# Cargar la imagen del fondo de historia e instrucciones
fondo_historia = pygame.image.load("Historia.png").convert()
fondo_historia = pygame.transform.smoothscale(fondo_historia, (ANCHO, ALTO))  # Ajustar al tamaño de la pantalla

# Función para mostrar la historia
def mostrar_historia():
    fuente = pygame.font.Font(None, 24)
    historia = [
        "En un rincón olvidado del universo, el sistema Élarium prosperaba en paz.",
        "Pero desde las profundidades del cosmos, una lluvia de meteoritos amenaza con destruirlo.",
        "Eres el último defensor de Élarium, a bordo del poderoso Cañón Estelar.",
        "Tu misión:",
        "1. Destruye los meteoritos antes de que impacten los planetas.",
        "2. Recolecta poderes para mejorar tus armas.",
        "3. Resiste hasta el final para salvar a miles de millones.",
        "El destino del sistema solar está en tus manos. ¡Buena suerte!",
        "Presiona cualquier tecla para continuar..."
    ]

    corriendo_historia = True
    while corriendo_historia:
        pantalla.blit(fondo_historia, (0, 0))  # Dibujar el fondo

        for i, linea in enumerate(historia):
            texto = fuente.render(linea, True, (255, 255, 255))
            pantalla.blit(texto, (50, 50 + i * 40))  # Ajusta las posiciones verticales

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # Salir de la pantalla al presionar cualquier tecla
                corriendo_historia = False


# Función para mostrar las instrucciones
def mostrar_instrucciones():
    fuente = pygame.font.Font(None, 36)
    instrucciones = [
        "Instrucciones:",
        "1. Mueve tu cañón con las teclas de flecha o WASD.",
        "2. Dispara a los meteoritos con la barra espaciadora.",
        "3. Recolecta poderes para obtener cañones adicionales.",
        "4. Evita que los meteoritos lleguen al planeta.",
        "Presiona cualquier tecla para regresar al menú."
    ]

    corriendo_instrucciones = True
    while corriendo_instrucciones:
        pantalla.blit(fondo_historia, (0, 0))  # Dibujar el fondo

        for i, linea in enumerate(instrucciones):
            texto = fuente.render(linea, True, (255, 255, 255))
            pantalla.blit(texto, (50, 100 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                corriendo_instrucciones = False


# Modifica el menú principal para incluir la historia
def menu_principal():
    fuente_titulo = pygame.font.Font(None, 72)
    fuente_opciones = pygame.font.Font(None, 48)

    titulo = fuente_titulo.render("PLANET DEFENDER", True, (255, 255, 0))
    opciones = [
        "1. Jugar",
        "2. Historia",
        "3. Instrucciones",
        "4. Salir"
    ]

    opcion_seleccionada = 0
    corriendo_menu = True

    while corriendo_menu:
        pantalla.blit(fondo, (0, 0))

        # Animación del título
        titulo_rect = titulo.get_rect(center=(ANCHO // 2, 100))
        pantalla.blit(titulo, titulo_rect)

        # Dibujar opciones del menú
        for i, opcion in enumerate(opciones):
            color = (255, 255, 255) if i == opcion_seleccionada else (180, 180, 180)
            texto_opcion = fuente_opciones.render(opcion, True, color)
            texto_rect = texto_opcion.get_rect(center=(ANCHO // 2, 250 + i * 60))
            pantalla.blit(texto_opcion, texto_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
                if event.key == pygame.K_RETURN:
                    if opcion_seleccionada == 0:  # Jugar
                        main()
                    elif opcion_seleccionada == 1:  # Historia
                        mostrar_historia()
                    elif opcion_seleccionada == 2:  # Instrucciones
                        mostrar_instrucciones()
                    elif opcion_seleccionada == 3:  # Salir
                        pygame.quit()
                        sys.exit()

# Ejecutar el menú principal
menu_principal()
