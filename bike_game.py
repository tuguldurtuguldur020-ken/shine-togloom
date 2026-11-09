import pygame
import random
import math

pygame.init()
W, H = 400, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Desert Bike Rider')
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 22, bold=True)
small = pygame.font.SysFont('arial', 14, bold=True)
large = pygame.font.SysFont('arial', 36, bold=True)

HORIZON = 225
BIKE_Y = 490

def reset():
    return {'x': 200.0, 'distance': 0.0, 'score': 0, 'speed': 6.0,
            'obstacles': [], 'spawn': 0, 'over': False}

state = reset()

def road_bounds(y):
    t = max(0, min(1, (y-HORIZON)/(H-HORIZON)))
    return 194-187*t, 206+187*t

def cactus(x, y, s):
    x, y = int(x), int(y)
    thick = max(3, int(8*s))
    tall = max(12, int(40*s))
    green = (24, 116, 65)
    pygame.draw.line(screen, green, (x,y), (x,y-tall), thick)
    pygame.draw.line(screen, green, (x,y-int(tall*.5)), (x-int(13*s),y-int(tall*.5)), max(3,int(5*s)))
    pygame.draw.line(screen, green, (x-int(13*s),y-int(tall*.5)), (x-int(13*s),y-int(tall*.85)), max(3,int(5*s)))
    pygame.draw.line(screen, green, (x,y-int(tall*.7)), (x+int(13*s),y-int(tall*.7)), max(3,int(5*s)))
    pygame.draw.line(screen, green, (x+int(13*s),y-int(tall*.7)), (x+int(13*s),y-int(tall*1.05)), max(3,int(5*s)))

def background():
    for y in range(HORIZON+1):
        t = y/HORIZON
        pygame.draw.line(screen, (int(104+145*t), int(64+102*t), int(125-51*t)), (0,y),(W,y))
    pygame.draw.circle(screen, (255,221,143), (205,173), 48)
    pygame.draw.polygon(screen,(139,79,104),[(0,217),(38,190),(82,211),(125,183),(174,220),(234,192),(284,216),(340,184),(400,218),(400,250),(0,250)])
    pygame.draw.rect(screen,(238,173,103),(0,HORIZON,W,H-HORIZON))
    for y in range(255,H,60):
        pygame.draw.rect(screen,(230,161,92),(0,y,W,18))

def road():
    pygame.draw.polygon(screen,(62,61,66),[(194,HORIZON),(206,HORIZON),(393,H),(7,H)])
    pygame.draw.line(screen,(255,250,240),(194,HORIZON),(7,H),6)
    pygame.draw.line(screen,(255,250,240),(206,HORIZON),(393,H),6)
    offset = state['distance'] % 85
    for base in range(0,460,85):
        y = HORIZON + ((base+offset) % 460)
        if y >= H: continue
        t = (y-HORIZON)/(H-HORIZON)
        for side in (-1,1):
            x = 200 + side*62*t
            pygame.draw.line(screen,(255,250,235),(int(x),int(y)),(int(x+side*7*t),min(H,int(y+max(4,40*t)))),max(1,int(4*t)))

def scenery():
    for i in range(9):
        y = HORIZON + ((i*73+state['distance']*.6) % 395)
        if y > H: continue
        t = (y-HORIZON)/(H-HORIZON)
        l,r = road_bounds(y)
        s = .25+1.25*t
        cactus(l-27*s,y,s)
        cactus(r+27*s,y,s)

def bike(x):
    x = int(x)
    y = BIKE_Y
    pygame.draw.ellipse(screen,(106,67,52),(x-29,y+35,58,13))
    pygame.draw.ellipse(screen,(22,23,29),(x-12,y-10,24,53))
    pygame.draw.polygon(screen,(234,69,34),[(x-15,y-27),(x+15,y-27),(x+12,y+20),(x-12,y+20)])
    pygame.draw.rect(screen,(26,29,39),(x-11,y-14,22,25),border_radius=5)
    pygame.draw.line(screen,(26,29,39),(x-30,y-19),(x+30,y-19),5)
    pygame.draw.line(screen,(25,28,36),(x-9,y-29),(x-26,y-19),6)
    pygame.draw.line(screen,(25,28,36),(x+9,y-29),(x+26,y-19),6)
    pygame.draw.ellipse(screen,(245,246,250),(x-15,y-56,30,36))
    pygame.draw.line(screen,(242,104,40),(x,y-54),(x,y-25),5)
    pygame.draw.rect(screen,(255,190,30),(x-5,y+10,10,8))

def obstacle_position(obj):
    y = obj['y']
    t = max(0,(y-HORIZON)/(H-HORIZON))
    return 200+obj['lane']*105*t, .3+1.3*t

def obstacles():
    for obj in state['obstacles'][:]:
        if not state['over']:
            obj['y'] += state['speed']*(.32+max(0,(obj['y']-HORIZON))/300)
        x,s = obstacle_position(obj)
        cactus(x,obj['y'],s)
        if not state['over'] and BIKE_Y-42 < obj['y'] < BIKE_Y+30 and abs(x-state['x']) < 14+12*s:
            state['over'] = True
        if obj['y'] > H+40:
            state['obstacles'].remove(obj)
            state['score'] += 10

def ui():
    for x in (10,294):
        pygame.draw.rect(screen,(34,30,50),(x,10,96,52),border_radius=8)
    screen.blit(small.render('SCORE',True,'white'),(20,14))
    screen.blit(font.render(str(state['score']),True,(255,214,55)),(20,31))
    screen.blit(small.render('SPEED',True,'white'),(304,14))
    screen.blit(font.render(str(int(state['speed']*22)),True,(75,255,145)),(304,31))

running = True
while running:
    dt = clock.tick(60)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and state['over']:
            state = reset()

    if not state['over']:
        keys = pygame.key.get_pressed()
        direction = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        state['x'] += direction*280*dt
        left,right = road_bounds(BIKE_Y)
        state['x'] = max(left+19,min(right-19,state['x']))
        state['distance'] += state['speed']*2
        state['spawn'] += dt
        if state['spawn'] >= 1.6:
            state['obstacles'].append({'lane':random.choice([-1,0,1]),'y':HORIZON+8})
            state['spawn'] = 0
        state['speed'] = min(12,6+state['score']/100)

    background()
    road()
    scenery()
    obstacles()
    bike(state['x'])
    ui()
    if state['over']:
        veil = pygame.Surface((W,H),pygame.SRCALPHA)
        veil.fill((0,0,0,155))
        screen.blit(veil,(0,0))
        title = large.render('GAME OVER',True,'white')
        screen.blit(title,title.get_rect(center=(W//2,265)))
        sub = font.render(f"Score: {state['score']}",True,(255,220,65))
        screen.blit(sub,sub.get_rect(center=(W//2,312)))
        hint = small.render('Press R to restart',True,'white')
        screen.blit(hint,hint.get_rect(center=(W//2,350)))
    pygame.display.flip()
pygame.quit()
