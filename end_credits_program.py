import pygame
import sys

pygame.init()

# -----------
# ---SETUP---
# -----------

# Screen refresh rate 
FPS = 60

# Window size
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

# Gravity and initial text velocity, and angle
GRAVITY = 0.1
Y_VELOCITY_0 = 1.3
UPWARD_FORCE = -5
TEXT_ANGLE = 0
TEXT_ZOOM = 1

# Text initial x, y coordinates
X_TEXT_INITIAL = 530
Y_TEXT_INITIAL = -60

# Clock
fpsClock = pygame.time.Clock()


class Moving_Font(pygame.font.Font):
    def __init__(self, name, size: int, x_pos: int, y_pos: int, velocity: int) -> None:
        super().__init__(name, size)
        self.name = name # name of the font
        self.size = size
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.velocity = velocity
        

def exit_pygame():
    """For the exception handling paths, code snippet for quitting pygame
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def error_message(line1: str, line2: str):
    """Displaying a 2 line error message

    Args:
        line1 (str): The first line of the error message
        line2 (str): The second line of the error message
    """
    first_line = pygame.font.SysFont(None, 30, False, True)
    first_line_surface = first_line.render(line1, True, "green")
    first_line_rect = first_line_surface.get_rect()
    first_line_rect.center = (530, 150)
    screen.blit(first_line_surface, first_line_rect)
    
    second_line = pygame.font.SysFont(None, 30, False, False)
    second_line_surface = second_line.render(line2, True, "green")
    second_line_rect = second_line_surface.get_rect()
    second_line_rect.center = (530, 210)
    screen.blit(second_line_surface, second_line_rect)
                 
        
# Initializing the main window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption('End Credits')


# -------------------
# ---Main function---
# -------------------
def main():
    """This is the main function of the program, containing the main loop and the logic for the text crawl.
    """
    # initializing upward force for the bouncing movement
    velocity_up = UPWARD_FORCE
    rotation_angle = TEXT_ANGLE
    rotation_zoom = TEXT_ZOOM
    
    # initializing the main font
    # Copyright: The font is a free to use font downloaded from: https://ttfonts.net/font/17298_Futura.htm
    # Checking if the required font is present. If not an error message is displayed
    try:
        futura_font = Moving_Font('16020_FUTURAM.ttf', 50, X_TEXT_INITIAL, Y_TEXT_INITIAL, Y_VELOCITY_0)
    except FileNotFoundError:
        while True:
            # event loop
            exit_pygame()      
            # Displaying error message
            error_message('File error: 16020_FUTURAM.ttf not found. Download from ttffonts.net', 'Add file to the same directory as the ".py" file')
            pygame.display.update()
            fpsClock.tick(60)
    
    # Checking if there is a save file. If yes, read the content to a variable
    saved_line = []
    try:
        with open("save.txt", 'r') as file:
            for line in file:
                saved_line.append(line.rstrip('\n'))
    except FileNotFoundError:
        pass
    
    print(saved_line)
        
    # Checking if end_credits.txt exist. If yes, enter the main program, if not display an error message.
    try: 
        # open end_credits.txt and read contents line by line to a list.
        end_credits = []
        with open('end_credits.txt', 'r') as file:
            for line in file:
                end_credits.append(line.rstrip('\n'))
    
        print(end_credits)
    # Checking if the saved line is in the end credits. Saving will save only one line,
    # so if saved_line has more than one element, it is sure that it is not correct.
    # If the saved_line is empty, it means that either save does not exists or the file is empty,
    # so we start with the first line of the end_credits.
        current_line = ''
        index = 0       
        if len(saved_line) == 1 and saved_line[0] in end_credits:
            index = end_credits.index(saved_line[0])
            current_line = end_credits[index]
        else:
            current_line = end_credits[index]
            
            
            
        # main loop
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # saving before quitting.
                    with open('save.txt', 'w') as file:
                        file.write(current_line)
                    # closing the window and all processes
                    pygame.quit()
                    sys.exit()
            
            # Background     
            screen_surface = screen.fill("black")
                
            # Font display and animation first phase - drop down:
                
            futura_surface = futura_font.render(current_line, True, "Green")
            futura_surface = pygame.transform.rotozoom(futura_surface, rotation_angle, rotation_zoom)
            futura_surface_rect = futura_surface.get_rect()
            futura_surface_rect.center = (futura_font.x_pos, futura_font.y_pos)
            
            screen.blit(futura_surface, futura_surface_rect)
            
            futura_font.velocity += GRAVITY
            futura_font.y_pos += futura_font.velocity
        
            # Bounce and stop and transform          
            if futura_font.y_pos >= 400:
                futura_font.velocity = velocity_up
                if velocity_up <= -0.5:
                    velocity_up += 0.5
                else:
                    # rolling to the right
                    velocity_up = 0
                    futura_font.velocity = 0
                    futura_font.y_pos = 400
                    futura_font.x_pos += 10
                    rotation_angle += -5
                    rotation_zoom -= 0.02
                    # reset if out of screen
                    if futura_font.x_pos > 1100:
                        index += 1
                        if index + 1 <= len(end_credits):
                            current_line = end_credits[index]
                            futura_font.x_pos = X_TEXT_INITIAL
                            futura_font.y_pos = Y_TEXT_INITIAL
                            futura_font.velocity = Y_VELOCITY_0
                            rotation_angle = TEXT_ANGLE
                            rotation_zoom = TEXT_ZOOM
                            velocity_up = UPWARD_FORCE
                        else: 
                            exit_pygame()
                            error_message('', 'END OF PROGRAM')
            
            pygame.display.update()
            fpsClock.tick(60)

    # executed if end_credits.txt does not exist
    except FileNotFoundError:
        while True:
            # event loop
            exit_pygame()      
            # Displaying error message
            error_message('File error: end_credits.txt not found.', 'Add file to the same directory as the ".py" file')
            pygame.display.update()
            fpsClock.tick(60)        
            

if __name__ == '__main__':
    main()
    


