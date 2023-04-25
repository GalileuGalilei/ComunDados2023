import pygame
import sys

pygame.init()

# Configurações da janela
size = (900, 300)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Trab 1 - Comunicação de Dados")

# Cor de fundo da janela
background_color = (255, 255, 255)

# Fonte e tamanho do texto na caixa de texto
font = pygame.font.Font(None, 36)

# Caixa de texto
input_box = pygame.Rect(50, 50, 785, 32)
input_text = ''


# Fonte e tamanho do texto na caixa de texto
font = pygame.font.Font(None, 36)

wave_width = 20
wave_height = 50
x_pos = 50
y_pos = 160

def vertical_line():
    pygame.draw.line(screen, (255, 50, 50), (x_pos, y_pos), (x_pos, y_pos + wave_height),3)

def horizontal_line_up(count):
    pygame.draw.line(screen, (255, 50, 50), (x_pos, y_pos), (x_pos + wave_width, y_pos),3)

def horizontal_line_down(count):
    pygame.draw.line(screen, (255, 50, 50), (x_pos, y_pos + wave_height), (x_pos + wave_width, y_pos + wave_height),3)

def horizontal_line_mid(count):
    pygame.draw.line(screen, (255, 50, 50), (x_pos, y_pos + wave_height/2), (x_pos + wave_width, y_pos + wave_height/2),3)

def horizontal_line_half_up(count):
    pygame.draw.line(screen, (255, 50, 50), (x_pos, y_pos), (x_pos + wave_width/2, y_pos),3)

def horizontal_line_half_down(count):
    pygame.draw.line(screen, (255, 50, 50), (x_pos, y_pos + wave_height), (x_pos + wave_width/2, y_pos + wave_height),3)

def vertical_half_up(count):
    pygame.draw.line(screen, (255, 50, 50), (x_pos, y_pos), (x_pos, y_pos + wave_height/2),3)

def vertical_half_down(count):
    pygame.draw.line(screen, (255, 50, 50), (x_pos, y_pos + wave_height/2), (x_pos, y_pos + wave_height),3)

def vertical_half_up(count):
    pygame.draw.line(screen, (255, 50, 50), (x_pos, y_pos), (x_pos, y_pos + wave_height/2),3)

def vertical_half_down(count):
    pygame.draw.line(screen, (255, 50, 50), (x_pos, y_pos + wave_height/2), (x_pos, y_pos + wave_height),3)

def draw_encoded_nrz_L(encoded_bits, screen):
    text = font.render("NRZ-L", True, (0, 0, 0))
    screen.blit(text, (50, 20))

    # Configurações do desenho
    last_bit = 'x'
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


def draw_bits(bits, screen):
    x = x_pos + 5
    count = 0

    # Desenha os bits na tela
    for bit in bits:
        text = font.render(bit, True, (0, 0, 0))
        screen.blit(text, (x, 230))
        pygame.draw.line(screen, (0, 0, 0), (x - 5, 160), (x - 5, 260), 1)
        
        x += wave_width
        count += 1

first = False
selected_function = draw_encoded_pseudoternary

# Função para desenhar os botões de escolha de função
def draw_function_buttons(screen, function_names, button_width, button_height, x_pos, y_pos, font_size):
    y = 100
    x = 50
    font = pygame.font.Font(None, font_size)
    button_spacing = 10
    buttons = []
    
    for i, function_name in enumerate(function_names):
        button_x = x + (button_width + button_spacing) * i
        button_y = y
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        button_text = font.render(function_name, True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        
        pygame.draw.rect(screen, (255, 255, 255), button_rect)
        pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)
        screen.blit(button_text, button_text_rect)
        
        buttons.append(button_rect)
    
    return buttons

function_list = [draw_encoded_nrz_I, draw_encoded_nrz_L, draw_encoded_AMI, draw_encoded_pseudoternary, draw_encoded_machester, draw_encoded_differencial_machester]
function_names = ["NRZ-I", "NRZ-L", "AMI", "Pseudoternário", "Manchester", "M.Diferencial"]
selected_function = function_list[0]

# Loop principal do jogo
while True:

    # Trata eventos do Pygame
    screen.fill(background_color)
    buttons = draw_function_buttons(screen, function_names, 120, 50, x_pos, y_pos, 20)
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Verifica se algum botão de função foi clicado
            for i, button in enumerate(buttons):
                if button.collidepoint(event.pos):
                    selected_function = function_list[i]
                    first = True
    
    pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
    text_surface = font.render(input_text, True, (0, 0, 0))
    screen.blit(text_surface, (input_box.x+5, input_box.y+5))
    wave_width = 20
    wave_height = 50
    x_pos = 50
    y_pos = 160
    
    draw_bits(input_text, screen)
    selected_function(input_text, screen)
    
    pygame.display.flip()
