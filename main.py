#操控 sprite
import pygame
import random
import os
#(設定好不會去改變的變數，設為大寫)
FPS = 60

WIDTH = 500
HEIGHT = 650
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0) 
YELLOW = (255,255,0)
GRAY = (220,220,220)
PURPLE = (255,0,255)

#遊戲初始化 and #創建視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("我想吃蘋果")
clock = pygame.time.Clock()

#加入圖片
background_img = pygame.image.load(os.path.join("img", "apple tree1.png")).convert()
apple_img = pygame.image.load(os.path.join("img", "apple5.png")).convert()
person_img = pygame.image.load(os.path.join("img", "person3.png")).convert()
cherry_img = pygame.image.load(os.path.join("img", "cherry.png")).convert()
blueberry_img = pygame.image.load(os.path.join("img", "blueberry.png")).convert()
apple_mini_img = pygame.image.load(os.path.join("img", "apple5.png")).convert()
apple_mini_img.set_colorkey(BLACK)
apple_mini_img = pygame.transform.scale(apple_mini_img,(50,50))
pygame.display.set_icon(apple_mini_img)


font_name = os.path.join("word","font.ttf")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
    
def draw_init():
    draw_text(screen,'我想吃蘋果', 60, WIDTH/2, HEIGHT*4/20)
    draw_text(screen,'規則：', 22, WIDTH/2, HEIGHT*9/20)
    draw_text(screen,'(請先切換成英文輸入法)', 20, WIDTH/2, HEIGHT*10/20)
    draw_text(screen,'按← →即可移動人物', 20, WIDTH/2, HEIGHT*11/20)
    draw_text(screen,'接住蘋果加10分，接住櫻桃扣3分，', 20, WIDTH/2, HEIGHT*12/20)
    draw_text(screen,'接住藍莓炸彈即遊戲結束', 20, WIDTH/2, HEIGHT*13/20)
    draw_text(screen,'----按任意鍵開始遊戲----', 24, WIDTH/2, HEIGHT*16/20)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False
        
    
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(person_img,(100,88))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center,self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT + 10
        self.speedx = 7
    
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0   

        
class Apple(pygame.sprite.Sprite):
    def __init__(self,im):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = im
        self.image = self.image_ori.copy()
        self.image = pygame.transform.scale(apple_img,(70,70))
        self.image_ori. set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 18
        #pygame.draw.circle(self.image, RED, self.rect.center,self.radius)
        self.rect.x = random.randrange(0,WIDTH-self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(3,5)
        self.speedx = random.randrange(-3,3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3,3)
    
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori,self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
    
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0,WIDTH-self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(3,5)
            self.speedx = random.randrange(-3,3)
    def reset2top(self):
        self.rect.x = random.randrange(0,WIDTH-self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(3,5)
        self.speedx = random.randrange(-3,3)
        

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

apples = pygame.sprite.Group()
for i in range (8):
    a= Apple(apple_img)
    all_sprites.add(a)
    apples.add(a)
    
cherrys = pygame.sprite.Group()
for i in range (3):
    c= Apple(cherry_img)
    all_sprites.add(c)
    cherrys.add(c)
    
blueberrys = pygame.sprite.Group()
for i in range (3):
    b= Apple(blueberry_img)
    all_sprites.add(b)
    blueberrys.add(b)   
    
    
score = 0


#遊戲迴圈
show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    
    #更新遊戲 
    all_sprites.update()
    
    hits = pygame.sprite.spritecollide(player, apples ,False, pygame.sprite.collide_circle)
    if hits:
        score += 10
    
    hits = pygame.sprite.spritecollide(player, cherrys ,False, pygame.sprite.collide_circle)
    if hits:
        score += -3
        
    hits = pygame.sprite.spritecollide(player, blueberrys ,False, pygame.sprite.collide_circle)
    if hits:
        running = False
            
            
    
    for a in apples:
        hit = pygame.sprite.spritecollide(player, [a], False, pygame.sprite.collide_circle)  
        if hit:
            a.reset2top()
            
    for c in cherrys:
        hit = pygame.sprite.spritecollide(player, [c], False, pygame.sprite.collide_circle)  
        if hit:
            c.reset2top()
            
    for b in blueberrys:
        hit = pygame.sprite.spritecollide(player, [b], False, pygame.sprite.collide_circle)  
        if hit:
            b.reset2top()
                
        
    
    #畫面顯示
    screen.blit(background_img,(0,0))
    background_img = pygame.transform.scale(background_img,(500,650))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 24, WIDTH/2, 10)
    pygame.display.update()
    
pygame.quit()
