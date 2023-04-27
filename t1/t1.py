import pygame
import sys

pygame.init()

# Configurações da janela
size = (1060, 300)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Trab 1 - Comunicação de Dados")

# Cor de fundo da janela
background_color = (255, 255, 255)

# Fonte e tamanho do texto na caixa de texto
font = pygame.font.Font(None, 36)

# Caixa de texto
input_box = pygame.Rect(30, 50, 1002, 32)
input_text = ''

# variável para controlar o loop principal
wave_width = 20
wave_height = 50
x_pos = 50
y_pos = 160

def set_global_variables():
    global wave_width
    global wave_height
    global x_pos
    global y_pos
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
    draw_bits(encoded_bits, screen)
    text = font.render("NRZ-L", True, (0, 0, 0))
    screen.blit(text, (50, 20))

    # primeiro bit
    last_bit = '1'
    count = 0

    # Desenha as ondas do sinal digital de acordo com a codificação de linha
    for bit in encoded_bits:
        if bit != last_bit:
            vertical_line()
        if bit == '1':
            horizontal_line_down(count)
        else:
            horizontal_line_up(count)
        global x_pos
        x_pos += wave_width
        count += 1
        last_bit = bit

def draw_encoded_nrz_I(encoded_bits, screen):
    draw_bits(encoded_bits, screen)
    text = font.render("NRZ-i", True, (0, 0, 0))
    screen.blit(text, (50, 20))

    # primeiro bit
    global x_pos
    is_down = False
    count = 0

    # Desenha as ondas do sinal digital de acordo com a codificação de linha
    for bit in encoded_bits:
        if bit == '1':
            vertical_line()
            is_down = is_down == False

        if not is_down:
            horizontal_line_down(count)
        else:
            horizontal_line_up(count)
        x_pos += wave_width
        count += 1


'''
A codificação MLT-3 (Multi-Level Transmission 3) é uma técnica de codificação de linha utilizada em transmissões 
 de dados que permite a transmissão de vários níveis de sinal em um único canal. A técnica baseia-se em uma sequência
 de três níveis de sinal, representados por sinais positivos, negativos ou nulos.

Na codificação MLT-3, o primeiro bit é codificado como nulo. Para os bits subsequentes, a técnica determina 
o nível de sinal a ser utilizado da seguinte forma:

* Se o bit atual for igual ao bit anterior, o nível de sinal permanece inalterado (nulo).
* Se o bit atual for diferente do bit anterior e o bit atual for 1, o nível de sinal é alternado para o próximo nível (positivo ou negativo) em relação ao nível atual.
* Se o bit atual for diferente do bit anterior e o bit atual for 0, o nível de sinal é alternado para o próximo nível em relação ao nível anterior.
'''
def draw_encoded_MLT_3(encoded_bits, screen):
    draw_bits(encoded_bits, screen)
    text = font.render("MLT-3", True, (0, 0, 0))
    screen.blit(text, (50, 20))

    # primeiro bit
    global x_pos
    is_down = False
    state = 0
    count = 0

    # Desenha as ondas do sinal digital de acordo com a codificação de linha
    for bit in encoded_bits:
        if bit == '1':

            if state == 1:
                vertical_half_up(count)
                horizontal_line_mid(count)
            elif state == -1:
                vertical_half_down(count)
                horizontal_line_mid(count)
            else:
                if is_down:
                    vertical_half_down(count)
                    horizontal_line_down(count)
                else:
                    vertical_half_up(count)
                    horizontal_line_up(count)

            if is_down:
                state -= 1
            else:
                state += 1

            if state == 1:
                is_down = True
            elif state == -1:
                is_down = False
        else:
            if state == 1:
                horizontal_line_up(count)
            elif state == -1:
                horizontal_line_down(count)
            else:
                horizontal_line_mid(count)


        x_pos += wave_width
        count += 1

fourBtoFiveB = {
    '0000': '11110',
    '0001': '01001',
    '0010': '10100',
    '0011': '10101',
    '0100': '01010',
    '0101': '01011',
    '0110': '01110',
    '0111': '01111',
    '1000': '10010',
    '1001': '10011',
    '1010': '10110',
    '1011': '10111',
    '1100': '11010',
    '1101': '11011',
    '1110': '11100',
    '1111': '11101'
}
'''
A codificação 4B/5B é uma técnica de codificação de linha utilizada em redes de comunicação de dados para
 transmitir informações digitais de forma confiável e eficiente. Essa técnica é baseada na conversão de grupos
 de 4 bits em símbolos de 5 bits, permitindo a transmissão de mais informações por unidade de tempo.

Cada grupo de 4 bits é mapeado em um símbolo de 5 bits de acordo com uma tabela de codificação predefinida. 
Essa tabela de codificação garante que os símbolos gerados tenham um número limitado de transições de bits e, 
 portanto, são menos propensos a erros de transmissão. Além disso, alguns símbolos são reservados para fins especiais,
 como o início e o fim de uma sequência de bits.
'''
def draw_encoded_4b_5b(encoded_bits, screen):
    text = font.render("4B/5B", True, (0, 0, 0))
    screen.blit(text, (50, 20))

    # primeiro bit
    global x_pos
    count = 0
    converted = ''

    # Desenha as ondas do sinal digital de acordo com a codificação de linha
    while(True):

        if len(encoded_bits) - count < 4:
            break

        count += 4
        sub = encoded_bits[count - 4 : count]
        converted += (fourBtoFiveB[sub])

    last_bit = 'x'
    count = 0
    draw_bits(converted, screen)
    # Desenha as ondas do sinal digital de acordo com a codificação de linha
    for bit in converted:
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


def draw_encoded_machester(encoded_bits, screen):
    draw_bits(encoded_bits, screen)
    text = font.render("Manchester", True, (0, 0, 0))
    screen.blit(text, (50, 20))

    #primeiro bit
    last_bit = 'x' 
    global x_pos
    count = 0

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
    draw_bits(encoded_bits, screen)
    text = font.render("Manchester Diferencial", True, (0, 0, 0))
    screen.blit(text, (50, 20))

    #primeiro bit
    last_bit = 'x'
    is_down = True
    count = 0
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
    draw_bits(encoded_bits, screen)
    text = font.render("Bipolar-AMI", True, (0, 0, 0))
    screen.blit(text, (50, 20))

    #primeiro bit
    is_down = False
    last_bit = '0'
    global x_pos
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
        x_pos += wave_width
        count += 1
        last_bit = bit

def draw_encoded_pseudoternary(encoded_bits, screen):
    draw_bits(encoded_bits, screen)
    text = font.render("Pseudoternary", True, (0, 0, 0))
    screen.blit(text, (50, 20))

    #primeiro bit
    is_down = False
    last_bit = '0'
    global x_pos
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

# Função para desenhar os botões de escolha de função
def draw_function_buttons(screen, function_names, button_width, button_height, x_pos, y_pos, font_size):
    y = 100
    x = 30
    font = pygame.font.Font(None, font_size)
    button_spacing = 6
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

function_list = [draw_encoded_nrz_I, draw_encoded_nrz_L, draw_encoded_AMI, draw_encoded_pseudoternary, draw_encoded_machester, draw_encoded_differencial_machester, draw_encoded_MLT_3, draw_encoded_4b_5b]
function_names = ["NRZ-I", "NRZ-L", "AMI", "Pseudoternário", "Manchester", "D. Manchester", "MLT-3", "4B/5B"]
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
    
    set_global_variables()
    selected_function(input_text, screen)
    
    pygame.display.flip()
