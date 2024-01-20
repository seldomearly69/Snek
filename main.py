import os
import pygame
from pygame.locals import *
import time
import random
home_directory = os.path.expanduser( '~' )
SIZE = 40
text_color = (220,20,60)
screen_width = 1000
screen_height = 920

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load(f"{home_directory}/desktop/Snake game/resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*random.randint(0,24)
        self.y = SIZE*random.randint(0,22)

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = SIZE*random.randint(0,24)
        self.y = SIZE*random.randint(0,22)


class Snake:
    def __init__(self, parent_screen,player_num = 1):
        self.parent_screen = parent_screen
        if player_num == 1:
            self.body = pygame.image.load(f"{home_directory}/desktop/Snake game/resources/snake_body1.png").convert()
            self.head = pygame.image.load(f"{home_directory}/desktop/Snake game/resources/snake_head1.png").convert()
            self.dead_body = pygame.image.load(f"{home_directory}/desktop/Snake game/resources/snake_deadbody1.png").convert()
            self.dead_head = pygame.image.load(f"{home_directory}/desktop/Snake game/resources/snake_deadhead1.png").convert()
        else:
            self.body = pygame.image.load(f"{home_directory}/desktop/Snake game/resources/snake_body2.png").convert()
            self.head = pygame.image.load(f"{home_directory}/desktop/Snake game/resources/snake_head2.png").convert()
            self.dead_body = pygame.image.load(f"{home_directory}/desktop/Snake game/resources/snake_deadbody2.png").convert()
            self.dead_head = pygame.image.load(f"{home_directory}/desktop/Snake game/resources/snake_deadhead2.png").convert()
        self.x = [SIZE*random.randint(0,24)]
        self.y = [SIZE*random.randint(2,22)]
        self.score = 0
        self.direction = ["up","down","left","right"][random.randint(0,3)]

    def draw(self):
        for i in range(len(self.x)):
            if i == 0:
                if self.direction == "up":
                    self.parent_screen.blit(pygame.transform.rotate(self.head, 180), (self.x[i], self.y[i]))
                elif self.direction == "left":
                    self.parent_screen.blit(pygame.transform.rotate(self.head, 270), (self.x[i], self.y[i]))
                elif self.direction == "right":
                    self.parent_screen.blit(pygame.transform.rotate(self.head, 90), (self.x[i], self.y[i]))
                else:
                    self.parent_screen.blit(self.head, (self.x[i], self.y[i]))
            else:
                self.parent_screen.blit(self.body, (self.x[i], self.y[i]))
    
    def move_left(self):
        self.direction = "left"
    
    def move_right(self):
        self.direction = "right"
    
    def move_up(self):
        self.direction = "up"
    
    def move_down(self):
        self.direction = "down"
    
    def walk(self):
        for i in range(len(self.x)-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.direction == "up":
            self.y[0] -= 40
            if self.y[0] <= -40:
                self.y[0] += 920
        if self.direction == "right":
            self.x[0] += 40
            if self.x[0] >= 1000:
                self.x[0] -= 1000
        if self.direction == "left":
            self.x[0] -= 40
            if self.x[0] <= -40:
                self.x[0] += 1000
        if self.direction == "down":
            self.y[0] += 40
            if self.y[0] >= 920:
                self.y[0] -= 920

        self.draw()

    def grow(self):
        self.x.append(-1)
        self.y.append(-1)

class Game:
    # Class variables ====================================================================================
    modes = [" Classic", "2P versus"]
    mode_pointer = 0
    difficulties = [("  Easy",0.2,10),("Medium",0.1,8),("  Hard",0.05,6),(" Insane",0.01,5),("  GOD",0.005,5)]
    difficulty_pointer = 1

    # Initialize =========================================================================================
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 1000))
        self.render_bg()
        pygame.mixer.init()

    # Tools ==============================================================================================

    def wait(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                    if event.key == K_RETURN:
                        waiting = False
                elif event.type == QUIT:
                    pygame.quit()

    def is_collision(self,x1,x2,y1,y2):
        if x1 == x2 and y1 == y2:
            return True
        return False
    
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"{home_directory}/desktop/Snake game/resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_bg(self):
        bg = pygame.image.load(f"{home_directory}/desktop/Snake game/resources/background.jpg")
        self.surface.blit(bg, (0,0))

    def play_bg_music(self):
        pygame.mixer.music.load(f"{home_directory}/desktop/Snake game/resources/bg_music_1.mp3")
        pygame.mixer.music.play()


    # Main run ====================================================================================

    def run(self):
        
        while True:
            self.choose_mode()
            self.run_mode()
            self.execute_post_game()

    def execute_post_game(self):
        if self.mode_pointer == 0:
            self.execute_post_game_classic()
        if self.mode_pointer == 1:
            self.execute_post_game_2pversus()

    def run_mode(self):
        if self.mode_pointer == 0:
            self.run_classic()
        if self.mode_pointer == 1:
            self.run_2pversus()

    def choose_mode(self):
        choosing = True
        while choosing:
            
            self.display_choose_mode()

            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    
                    if (event.key == K_RIGHT or event.key == K_d) and self.mode_pointer < 1:
                        self.mode_pointer += 1
                    if (event.key == K_LEFT or event.key == K_a) and self.mode_pointer > 0:
                        self.mode_pointer -= 1
                    if event.key == K_RETURN:
                        choosing = False
                    if event.key == K_ESCAPE:
                        pygame.quit()

                if event.type == QUIT:
                        pygame.quit()

    def display_game_title(self):
        font = pygame.font.SysFont("arial", 200)
        title = font.render("S N E K", True, text_color)
        self.surface.blit(title,(145,100))

    def display_choose_mode(self):
        self.render_bg()
        self.display_game_title()
        font = pygame.font.SysFont("arial", 50)
        line1 = font.render("Choose game mode", True, text_color)
        modes = font.render(self.modes[self.mode_pointer], True, text_color)
        font = pygame.font.SysFont("arial", 30)
        arrows = font.render("<                                 >", True, text_color)
        instructions1 = font.render("Enter to choose", True, text_color)
        self.surface.blit(arrows, (337,515))
        self.surface.blit(line1, (265, 350))
        self.surface.blit(instructions1, (380, 700))
        self.surface.blit(modes, (383, 500))
        pygame.display.flip()

    def check_apple_collision(self,snake):
        if self.is_collision(snake.x[0],self.apple.x,snake.y[0],self.apple.y):
            self.play_sound("ding")
            self.apple.move()
            snake.grow()
            raise
    
    def check_snake_self_collision(self,snake):
        for i in range(3,len(snake.x)):
            if self.is_collision(snake.x[0],snake.x[i],snake.y[0],snake.y[i]):
                raise "self collision occured"

    def check_snake_snake_collision(self):
        snake1life = True
        snake2life = True
        for i in range(0,len(self.snake1.x)):
            if self.is_collision(self.snake2.x[0],self.snake1.x[i],self.snake2.y[0],self.snake1.y[i]):
                snake2life = False
                if i == 0:
                    return (False,False)
                break

        for i in range(1,len(self.snake2.x)):
            if self.is_collision(self.snake1.x[0],self.snake2.x[i],self.snake1.y[0],self.snake2.y[i]):
                snake1life = False
                break

        return (snake1life,snake2life)

    def ask_for_name(self,other_instructions):
        font = pygame.font.SysFont("arial", 50)
        text = ""
        asking = True
        while asking:
            self.render_bg()
            for a in other_instructions:
                a()
            line1 = font.render(f"Enter your name: {text}|", True, text_color)
            self.surface.blit(line1, (100,400))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                    if len(text) != 0 and event.key == K_BACKSPACE:
                        text = text[:-1]
                    if event.key == K_RETURN:
                        asking = False
                    elif event.key != K_BACKSPACE and len(text) < 11:
                        text += event.unicode
                elif event.type == QUIT:
                    pygame.quit()
        return text

    # Classic mode ====================================================================================

    def run_classic(self):
        self.snake1 = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.set_difficulty()
        self.timer = self.difficulties[self.difficulty_pointer][2]
        self.play_bg_music()
        start_time = time.time()

        running = True
        while running:
            
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                    
                    if event.key == K_w or event.key == K_UP:
                        if len(self.snake1.x) > 1:
                            if self.snake1.x[1] != self.snake1.x[0]:
                                self.snake1.move_up()
                        else:
                            self.snake1.move_up()
                    if event.key == K_s or event.key == K_DOWN:
                        if len(self.snake1.x) > 1:
                            if self.snake1.x[1] != self.snake1.x[0]:
                                self.snake1.move_down()
                        else:
                            self.snake1.move_down()
                    if event.key == K_a or event.key == K_LEFT:
                        if len(self.snake1.y) > 1:
                            if self.snake1.y[1] != self.snake1.y[0]:
                                self.snake1.move_left()
                        else:
                            self.snake1.move_left()
                    if event.key == K_d or event.key == K_RIGHT:
                        if len(self.snake1.y) > 1:
                            if self.snake1.y[1] != self.snake1.y[0]:
                                self.snake1.move_right()
                        else:
                            self.snake1.move_right()

                elif event.type == QUIT:
                    pygame.quit()

            
            self.render_bg()
            self.snake1.walk()
            self.apple.draw()
            self.display_score()
            self.display_timer()        

            pygame.display.flip()
            
            try:
                self.check_apple_collision(self.snake1)
            except Exception as e:
                self.timer = self.difficulties[self.difficulty_pointer][2]
                self.snake1.score += 1

            try:
                self.check_snake_self_collision(self.snake1)
                if self.update_timer(start_time):
                    start_time = time.time()
            except Exception as e:
                self.play_sound("lose")
                running = False
        
            time.sleep(self.difficulties[self.difficulty_pointer][1])

    def execute_post_game_classic(self):
        self.render_bg()
        pygame.mixer.music.pause()
        if self.is_highscore():
            self.update_highscore(self.ask_for_name([self.display_new_highscore_message,self.display_replay_instructions]))
            self.render_bg()
            self.display_highscores()
            self.display_replay_instructions()
            self.display_game_title()
            pygame.display.flip()
            self.wait()

        else:
            self.display_lol_noob()
            self.display_highscores()
            pygame.display.flip()
            self.wait()
        

    def display_replay_instructions(self):
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render("To play again press Enter", True, text_color)
        self.surface.blit(line1, (200, 700))
        line2 = font.render("To exit press Escape", True, text_color)
        self.surface.blit(line2, (200, 750))

    def display_new_highscore_message(self):
        font = pygame.font.SysFont("arial", 60)
        line1 = font.render(f"Congratulations!", True, text_color)
        line2 = font.render(f"You have a new highscore: {self.snake1.score}", True, text_color)

        self.surface.blit(line1, (250,150))
        self.surface.blit(line2, (100,200))
        self.display_replay_instructions()

    def display_lol_noob(self):
        font = pygame.font.SysFont("arial", 60)
        line1 = font.render(f"LOL noob! Your score is {self.snake1.score}", True, text_color)
        self.surface.blit(line1, (150,150))
        self.display_replay_instructions()
        pygame.display.flip()

    def display_highscores(self):
        all_scores = self.get_highscores()
        font = pygame.font.SysFont("arial", 50)
        header = font.render("HIGHSCORES", True, text_color)
        self.surface.blit(header, (200,300))
        font = pygame.font.SysFont("arial", 30)
        bumper = 50
        for i in range(5):
            line1 = font.render(f"{i+1}. {all_scores[i][0]}", True, text_color)
            line2 = font.render(f"{all_scores[i][1]}", True, text_color)
            self.surface.blit(line1, (220, 400+bumper*i))
            self.surface.blit(line2, (600, 400+bumper*i))

    def update_highscore(self,winner):

        all_scores = self.get_highscores()
        with open(f"{home_directory}/desktop/Snake game/resources/Highscore_{self.difficulties[self.difficulty_pointer][0]}", "w") as file:
            temp = []
            for a in all_scores:
                if self.snake1.score > a[0]:
                    temp.append((self.snake1.score,winner))
                    self.snake1.score = 0
                temp.append(a)
            all_scores = temp
            for i in range(5):
                file.write(f"{str(all_scores[i][0])}|{all_scores[i][1]}\n")

    def is_highscore(self):
        highscores = self.get_highscores()
        if min([a[0] for a in highscores]) < self.snake1.score:
            return True
        return False
    
    def get_highscores(self):
        temp = {}
        with open(f"{home_directory}/desktop/Snake game/resources/Highscore_{self.difficulties[self.difficulty_pointer][0]}") as file:
            for line in file:
                line = line.rstrip("\n").split("|")
                line[0] = int(line[0])
                temp.setdefault(line[0],[])
                temp[line[0]].append(line[1])
        temp_keys_sorted = list(temp.keys())
        temp_keys_sorted.sort(reverse=True)
        return [(a,b) for a in temp_keys_sorted for b in temp[a]]

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"Score: {self.snake1.score}", True, text_color)
        self.surface.blit(score, (800,10))

    def display_timer(self):
        font = pygame.font.SysFont("arial", 30)
        to_display = font.render(f"Time left: {self.timer}", True, text_color)
        self.surface.blit(to_display, (10, 10))

    def update_timer(self,start):
        if time.time() - start >= 1:
            self.timer -= 1
            return True
        if self.timer == 0:
            raise "Out of time"

    def set_difficulty(self):
        setting = True
        while setting:
            self.display_choose_difficulty()
            self.display_instructions()
            pygame.display.flip()
        
            for event in pygame.event.get():
                
                if event.type == KEYDOWN:
                    
                    if event.key == K_RETURN:
                        setting = False
                    if (event.key == K_d or event.key == K_RIGHT) and self.difficulty_pointer < 4:
                        self.difficulty_pointer += 1
                    if (event.key == K_a or event.key == K_LEFT) and self.difficulty_pointer > 0:
                        self.difficulty_pointer -= 1

                    if event.key == K_ESCAPE:
                        pygame.quit()
                
                if event.type == QUIT:
                    pygame.quit()
                
    
    def display_choose_difficulty(self):
        self.render_bg()
        font = pygame.font.SysFont("arial", 200)
        title = font.render("S N E K", True, text_color)
        font = pygame.font.SysFont("arial", 50)
        line1 = font.render("Choose difficulty", True, text_color)
        difficulties = font.render(f"{self.difficulties[self.difficulty_pointer][0]}", True, text_color)
        font = pygame.font.SysFont("arial", 30)
        arrows = font.render("<                                 >", True, text_color)
        instructions1 = font.render("Enter to choose", True, text_color)
        self.surface.blit(arrows, (337,515))
        self.surface.blit(title,(145,100))
        self.surface.blit(line1, (310, 350))
        self.surface.blit(instructions1, (380, 700))
        self.surface.blit(difficulties, (400, 500))
        
    
    def display_instructions(self):
        if self.mode_pointer == 0:
            self.display_classic_instructions()
        if self.mode_pointer == 1:
            self.display_2pversus_instructions()
    
    def display_classic_instructions(self):
        font = pygame.font.SysFont("arial", 30)
        instructions1 = font.render("WASD or Arrow keys to move, Eat the apple before time runs out!", True, text_color)
        self.surface.blit(instructions1, (70, 600))
        


    # 2P Versus mode ====================================================================================

    def run_2pversus(self):
        self.apple = Apple(self.surface)
        self.p1_name = self.ask_for_name([self.display_player1_title])
        self.p2_name = self.ask_for_name([self.display_player2_title])
        self.display_instructions()
        self.wait()
        self.countdown()
        self.play_bg_music()
        self.snake1.score = 3
        self.snake2.score = 3

        running = True
        while running:
            
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                    
                    if event.key == K_UP:
                        if self.snake1.x[1] != self.snake1.x[0]:
                                self.snake1.move_up()
                    if event.key == K_DOWN:
                        if self.snake1.x[1] != self.snake1.x[0]:
                                self.snake1.move_down()
                    if event.key == K_LEFT:
                         if self.snake1.y[1] != self.snake1.y[0]:
                                self.snake1.move_left()
                    if event.key == K_RIGHT:
                        if self.snake1.y[1] != self.snake1.y[0]:
                                self.snake1.move_right()
                    if event.key == K_w:
                        if self.snake2.x[1] != self.snake2.x[0]:
                                self.snake2.move_up()
                    if event.key == K_s:
                        if self.snake2.x[1] != self.snake2.x[0]:
                                self.snake2.move_down()
                    if event.key == K_a:
                        if self.snake2.y[1] != self.snake2.y[0]:
                                self.snake2.move_left()
                    if event.key == K_d:
                        if self.snake2.y[1] != self.snake2.y[0]:
                                self.snake2.move_right()

                elif event.type == QUIT:
                    pygame.quit()

            
            self.render_bg()
            self.snake1.walk()
            self.snake2.walk()
            self.apple.draw()
            self.display_scores_2p()       

            pygame.display.flip()
            
            try:
                self.check_apple_collision(self.snake1)
                
            except Exception as e:
                self.snake1.score += 1

            try:
                self.check_apple_collision(self.snake2)
                
            except Exception as e:
                self.snake2.score += 1

            lives = self.check_snake_snake_collision()
            if not lives[0] or not lives[1]:
                self.play_sound("lose")
                running = False
                if lives[0]:
                    self.winner = 1
                elif lives[1]:
                    self.winner = 2
                else:
                    self.winner = None
            time.sleep(0.1)
        pygame.mixer.music.pause()

    def execute_post_game_2pversus(self):
        self.render_bg()
        if self.winner == 1:
            self.display_snake_dead(self.snake2,(200,300))
            self.display_snake_alive(self.snake1,(600,300))
        elif self.winner == 2:
            self.display_snake_dead(self.snake1,(600,300))
            self.display_snake_alive(self.snake2,(200,300))
        else:
            self.display_snake_dead(self.snake1,(600,300))
            self.display_snake_dead(self.snake2,(200,300))
        self.display_post_game_message()
        
        font = pygame.font.SysFont("arial", 60)
        p1_name = font.render(self.p1_name, True, text_color)
        p2_name = font.render(self.p2_name, True, text_color)
        text_rect = p2_name.get_rect(center=(screen_width/4 + 40, 470))
        self.surface.blit(p2_name, text_rect)
        text_rect = p1_name.get_rect(center=(screen_width/4*3 - 40, 470))
        self.surface.blit(p1_name, text_rect)

        pygame.display.flip()
        self.wait()
    
    def display_post_game_message(self):
        font = pygame.font.SysFont("arial", 40)
        
        if self.winner:
            
            if self.winner == 1:
                winner = self.p1_name
                loser = self.p2_name

            else:
                winner = self.p2_name
                loser = self.p1_name
            taunts = [f"{winner} shat all over {loser}!",f"{loser} kana FUCKED!!!",f"{winner} clapped {loser}'s cheeks!",f"Looks like {loser} wont be sleeping tonight!",f"{winner} sent {loser} back to ITE!!!"]
            taunt = font.render(f"{taunts[random.randint(0,len(taunts)-1)]}", True, text_color)
        else:
            font = pygame.font.SysFont("arial", 30)
            taunt = font.render("Looks like you guys need to settle at parade square 12pm!!", True, text_color)
        
        
        
        restart_instructions = font.render("Press ENTER for revenge", True, text_color)
        text_rect = taunt.get_rect(center=(screen_width/2 , 720))
        self.surface.blit(taunt, text_rect)
        text_rect = restart_instructions.get_rect(center=(screen_width/2 , 770))
        self.surface.blit(restart_instructions, text_rect)

        
    def display_scores_2p(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"Player 1: {self.snake1.score}", True, text_color)
        self.surface.blit(score, (800,10))
        score = font.render(f"Player 2: {self.snake2.score}", True, text_color)
        self.surface.blit(score, (50,10))
    
    def countdown(self):
        for i in range(3,-1,-1):
            self.render_bg()
            self.snake1.draw()
            self.snake2.draw()
            font = pygame.font.SysFont("arial", 60)
            if i > 0:
                count = font.render(str(i), True, text_color)
            else:
                count = font.render("GO!", True, text_color)
            text_rect = count.get_rect(center=(screen_width/2, 470))
            self.surface.blit(count, text_rect)
            pygame.display.flip()
            time.sleep(1)

    def display_player1_title(self):
        font = pygame.font.SysFont("arial", 120)
        line1 = font.render(f"Player 1", True, text_color)
        self.surface.blit(line1, (280,200))

    def display_player2_title(self):
        font = pygame.font.SysFont("arial", 120)
        line1 = font.render(f"Player 2", True, text_color)
        self.surface.blit(line1, (280,200))

    def display_snake_dead(self,snake,buffer):
        """
        Starts drawing from bottom left corner
        """
        # font = pygame.font.SysFont("arial", 120)
        # line = font.render(".",True,text_color)
        # self.surface.blit(line, (buffer[0],buffer[1]))
        for i in range(len(snake.x)-1,0,-1):
            self.surface.blit(pygame.transform.rotate(snake.dead_body, random.randint(1,4)*90), (buffer[0] + random.randint(0,50), buffer[1] - random.randint(0,50)))
        self.surface.blit(pygame.transform.rotate(snake.dead_head, random.randint(1,4)*90), (buffer[0] + random.randint(0,50), buffer[1] - random.randint(0,50)))
    def display_snake_alive(self,snake,buffer):
        """
        Starts drawing from bottom left corner + 40
        """
        sets = (len(snake.x)-3)//4
        remainder = (len(snake.x)-3)%4
        for i in range(sets):
            for x in range(4):
                self.surface.blit(snake.body, (buffer[0] + x*40 , buffer[1] - i*40))
        if sets % 2 == 1:
            for m in range(remainder):
                self.surface.blit(snake.body, (buffer[0] + m*40 , buffer[1] - sets*40))
            self.surface.blit(snake.body, (buffer[0] + remainder*40 , buffer[1] - sets*40))
            self.surface.blit(pygame.transform.rotate(snake.head,180), (buffer[0] + 120-remainder*40 , buffer[1] - (sets+1)*40))
        else:
            for m in range(remainder):
                self.surface.blit(snake.body, (buffer[0] + (120 - m*40) , buffer[1] - (sets-1)*40))
            self.surface.blit(snake.body, (buffer[0] + 120-remainder*40 , buffer[1] - sets*40))
            self.surface.blit(pygame.transform.rotate(snake.head,180), (buffer[0] + 120-remainder*40 , buffer[1] - (sets+1)*40))
        self.surface.blit(snake.body, (buffer[0] + 120 , buffer[1]+40))
        

        
    def display_2pversus_instructions(self):
        self.render_bg()
        self.snake1 = Snake(self.surface,1)
        self.snake2 = Snake(self.surface,2)
        self.snake1.x += [0,0]
        self.snake1.y += [0,0]
        self.snake1.x, self.snake1.y= [680,680,680], [320,360,400]
        self.snake1.direction = "up"
        self.snake2.x += [0,0]
        self.snake2.y += [0,0]
        self.snake2.x, self.snake2.y = [280,280,280], [320,360,400]
        self.snake2.direction = "up"
        self.snake1.draw()
        self.snake2.draw()
        font = pygame.font.SysFont("arial", 60)
        p1_name = font.render(self.p1_name, True, text_color)
        p2_name = font.render(self.p2_name, True, text_color)
        font = pygame.font.SysFont("arial", 40)
        title = font.render("Press ENTER to start", True, text_color)
        p1_instructions = font.render("Arrow keys to move", True, text_color)
        p2_instructions = font.render("WASD to move", True, text_color)
        general_instructions1 = font.render("Each apple gives +1 length", True, text_color)
        general_instructions2 = font.render("Kill the other player to win!", True, text_color)
        text_rect = p2_name.get_rect(center=(screen_width/4 + 48, 470))
        self.surface.blit(p2_name, text_rect)
        text_rect = p1_name.get_rect(center=(screen_width/4*3 - 50, 470))
        self.surface.blit(p1_name, text_rect)
        text_rect = p2_instructions.get_rect(center=(screen_width/4 + 48, 570))
        self.surface.blit(p2_instructions, text_rect)
        text_rect = p1_instructions.get_rect(center=(screen_width/4*3 - 50, 570))
        self.surface.blit(p1_instructions, text_rect)
        text_rect = general_instructions1.get_rect(center=(screen_width/2 , 720))
        self.surface.blit(general_instructions1, text_rect)
        text_rect = general_instructions2.get_rect(center=(screen_width/2 , 770))
        self.surface.blit(general_instructions2, text_rect)
        text_rect = title.get_rect(center=(screen_width/2 , 170))
        self.surface.blit(title, text_rect)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()


