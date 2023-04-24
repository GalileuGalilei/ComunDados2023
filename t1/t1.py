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


# Fonte e tamanho do texto na caixa de texto
font = pygame.font.Font(None, 36)

wave_width = 20
wave_height = 50
x_pos = 50
y_pos = 100

def vertical_line():
    pygame.draw.line(screen, (0, 0, 0), (x_pos, y_pos), (x_pos, y_pos + wave_height))

def horizontal_line_up(count):
    pygame.draw.line(screen, (0, 0, 0), (x_pos, y_pos), (x_pos + wave_width, y_pos))

def horizontal_line_down(count):
    pygame.draw.line(screen, (0, 0, 0), (x_pos, y_pos + wave_height), (x_pos + wave_width, y_pos + wave_height))

def horizontal_line_mid(count):
    pygame.draw.line(screen, (0, 0, 0), (x_pos, y_pos + wave_height/2), (x_pos + wave_width, y_pos + wave_height/2))

def horizontal_line_half_up(count):
    pygame.draw.line(screen, (0, 0, 0), (x_pos, y_pos), (x_pos + wave_width/2, y_pos))

def horizontal_line_half_down(count):
    pygame.draw.line(screen, (0, 0, 0), (x_pos, y_pos + wave_height), (x_pos + wave_width/2, y_pos + wave_height))

def vertical_half_up(count):
    pygame.draw.line(screen, (0, 0, 0), (x_pos, y_pos), (x_pos, y_pos + wave_height/2))

def vertical_half_down(count):
    pygame.draw.line(screen, (0, 0, 0), (x_pos, y_pos + wave_height/2), (x_pos, y_pos + wave_height))

def vertical_half_up(count):
    pygame.draw.line(screen, (0, 0, 0), (x_pos, y_pos), (x_pos, y_pos + wave_height/2))

def vertical_half_down(count):
    pygame.draw.line(screen, (0, 0, 0), (x_pos, y_pos + wave_height/2), (x_pos, y_pos + wave_height))

def draw_encoded_nrz_L(encoded_bits, screen):
    text = font.render("NRZ-L", True, (0, 0, 0))
    screen.blit(text, (50, 20))

    # Configurações do desenho
    last_bit = encoded_bits[0][0]
    count = 0

    # Desenha as ondas do sinal digital de acordo com a codificação de linha
    for bit in encoded_bits:
        if bit != last_bit:
            vertical_line()
        if bit == '1':
            horizontal_line_up(count)
        else:
            horizontal_line_down(count)
        global x_pos
        x_pos += wave_width
        count += 1
        last_bit = bit

def draw_encoded_nrz_I(encoded_bits, screen):
    text = font.render("NRZ-i", True, (0, 0, 0))
    screen.blit(text, (50, 20))

    is_down = False
    count = 0

    # Desenha as ondas do sinal digital de acordo com a codificação de linha
    for bit in encoded_bits:
        if bit == '1':
            vertical_line()
            is_down = is_down == False

        if not is_down:
            horizontal_line_up(count)
        else:
            horizontal_line_down(count)
        global x_pos
        x_pos += wave_width
        count += 1

def draw_encoded_machester(encoded_bits, screen):
    text = font.render("Manchester", True, (0, 0, 0))
    screen.blit(text, (50, 20))

    count = 0
    last_bit = 'x' # Valor inicial para não dar erro na comparação
    global x_pos

    # Desenha as ondas do sinal digital de acordo com a codificação de linha
    for bit in encoded_bits:
        if bit == last_bit:
            vertical_line()

        if bit == '0':
            horizontal_line_half_up(count)
            x_pos += wave_width * 0.5
            vertical_line()
            horizontal_line_half_down(count)
        else:
            horizontal_line_half_down(count)
            x_pos += wave_width * 0.5
            vertical_line()
            horizontal_line_half_up(count)
        x_pos += wave_width * 0.5
        count += 1
        last_bit = bit

def draw_encoded_differencial_machester(encoded_bits, screen):
    text = font.render("Manchester Diferencial", True, (0, 0, 0))
    screen.blit(text, (50, 20))

    count = 0
    last_bit = 'x' # Valor inicial para não dar erro na comparação
    is_down = True
    global x_pos

    # Desenha as ondas do sinal digital de acordo com a codificação de linha
    for bit in encoded_bits:
        if bit == '1':
            is_down = not is_down
        else:
            vertical_line()

        if not is_down:
            horizontal_line_half_up(count)
            x_pos += wave_width * 0.5
            vertical_line()
            horizontal_line_half_down(count)
        else:
            horizontal_line_half_down(count)
            x_pos += wave_width * 0.5
            vertical_line()
            horizontal_line_half_up(count)
        x_pos += wave_width * 0.5
        count += 1
        last_bit = bit

def draw_encoded_AMI(encoded_bits, screen):
    text = font.render("Bipolar-AMI", True, (0, 0, 0))
    screen.blit(text, (50, 20))

    is_down = False
    last_bit = '0'
    count = 0

    # Desenha as ondas do sinal digital de acordo com a codificação de linha
    for bit in encoded_bits:
        if bit == '1':
            if last_bit == bit:
                vertical_line()
            else:
                if is_down:
                    vertical_half_down(count)
                else:
                    vertical_half_up(count)

            if is_down:
                horizontal_line_down(count)
            else:
                horizontal_line_up(count)
            is_down = not is_down
        else:
            if(last_bit != bit):
                if(is_down):
                    vertical_half_up(count)
                else:
                    vertical_half_down(count)
            horizontal_line_mid(count)
        global x_pos
        x_pos += wave_width
        count += 1
        last_bit = bit

def draw_encoded_pseudoternary(encoded_bits, screen):
    text = font.render("Pseudoternary", True, (0, 0, 0))
    screen.blit(text, (50, 20))

    is_down = False
    last_bit = '0'
    count = 0

    # Desenha as ondas do sinal digital de acordo com a codificação de linha
    for bit in encoded_bits:
        if bit == '0':
            if last_bit == bit:
                vertical_line()
            else:
                if is_down:
                    vertical_half_down(count)
                else:
                    vertical_half_up(count)

            if is_down:
                horizontal_line_down(count)
            else:
                horizontal_line_up(count)
            is_down = not is_down
        else:
            if(last_bit != bit):
                if(is_down):
                    vertical_half_up(count)
                else:
                    vertical_half_down(count)
            horizontal_line_mid(count)
        global x_pos
        x_pos += wave_width
        count += 1
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
                first = True
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    
    screen.fill(background_color)
    pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
    text_surface = font.render(input_text, True, (0, 0, 0))
    screen.blit(text_surface, (input_box.x+5, input_box.y+5))
    
    if(first):
        wave_width = 20
        wave_height = 50
        x_pos = 50
        y_pos = 100
        draw_encoded_pseudoternary(input_text, screen)
    pygame.display.flip()