from pygame import draw

def draw_text_on_surface(surface, font, color, text, text_x, text_y):
    text_img = font.render(text, True, color)
    surface.blit(text_img, (text_x, text_y))