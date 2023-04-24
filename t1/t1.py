import pygame
import sys

pygame.init()

# Configurações da janela
size = (400, 300)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Janela com caixa de texto")

# Cor de fundo da janela
background_color = (255, 255, 255)

# Fonte e tamanho do texto na caixa de texto
font = pygame.font.Font(None, 36)

# Caixa de texto
input_box = pygame.Rect(50, 50, 200, 32)
input_text = ''

def encode_bits(bits):
    encoded_bits = []
    count = 1
    last_bit = bits[0]

    # Realiza a codificação de linha
    for bit in bits[1:]:
        if bit == last_bit:
            count += 1
        else:
            encoded_bits.append((last_bit, count))
            count = 1
            last_bit = bit
    encoded_bits.append((last_bit, count))

    return encoded_bits

# Fonte e tamanho do texto na caixa de texto
font = pygame.font.Font(None, 36)

def draw_encoded_bits(encoded_bits, screen):
    # Configurações do desenho
    wave_width = 20
    wave_height = 50
    x_pos = 50
    y_pos = 100
    last_bit = encoded_bits[0][0]

    # Desenha as ondas do sinal digital de acordo com a codificação de linha
    for bit, count in encoded_bits:
        if bit != last_bit:
            pygame.draw.line(screen, (0, 0, 0), (x_pos, y_pos), (x_pos, y_pos + wave_height))
        if bit == '1':
            pygame.draw.line(screen, (0, 0, 0), (x_pos, y_pos), (x_pos + count * wave_width, y_pos))
        else:
            pygame.draw.line(screen, (0, 0, 0), (x_pos, y_pos + wave_height), (x_pos + count * wave_width, y_pos + wave_height))
        x_pos += count * wave_width
        last_bit = bit

first = False

# Loop principal do jogo
while True:

    # Trata eventos do Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                
                bits = encode_bits(input_text)
                first = True

                input_text = ''
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    # Desenha a tela
    screen.fill(background_color)
    pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
    text_surface = font.render(input_text, True, (0, 0, 0))
    screen.blit(text_surface, (input_box.x+5, input_box.y+5))
    
    if(first):
        draw_encoded_bits(bits, screen)
    pygame.display.flip()


import pygame
import sys

# Código principal
pygame.init()

# Configurações da janela
size = (400, 300)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Janela com caixa de texto")

# Cor de fundo da janela
background_color = (255, 255, 255)

# Configurações da janela
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Codificação de linha")

# Caixa de texto
input_box = pygame.Rect(50, 50, 200, 32)
input_text = ''

# Loop principal do jogo
while True:
    # Trata eventos do Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                #desenha si


                input_text = ''
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    # Desenha a tela
    screen.fill(255,255,255)
    pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
    text_surface = font.render(input_text, True, (0, 0, 0))
    screen.blit(text_surface, (input_box.x+5, input_box.y+5))
    pygame.display.flip()
