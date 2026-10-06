import os
import sys
import random
import pygame as pg
import time
import math

WIDTH, HEIGHT = 1100, 650

DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))    

def get_kk_imgs() -> dict[tuple[int,int],pg.Surface]:
    base_img = pg.image.load("fig/3.png")
    flipped_img = pg.transform.flip(base_img, True, False)  # 左右反転
    
    KK_imge = {
        (0, 0): pg.transform.rotozoom(base_img, 0, 0.9),
        (-5, 0): pg.transform.rotozoom(base_img, 0, 0.9),
        (-5, -5): pg.transform.rotozoom(base_img, -45, 0.9),
        (0, -5): pg.transform.rotozoom(flipped_img, 90, 0.9),
        (+5, -5): pg.transform.rotozoom(flipped_img, 45, 0.9),
        (+5, 0): pg.transform.rotozoom(flipped_img, 0, 0.9),
        (+5, +5): pg.transform.rotozoom(flipped_img, -45, 0.9),
        (0, +5): pg.transform.rotozoom(flipped_img, -90, 0.9),
        (-5, +5): pg.transform.rotozoom(base_img, 45, 0.9),
    }
    return KK_imge


def gameover(screen:pg.Surface) -> None:
    # 1. 画面全体の半透明黒Surfaceを作成
    black_out = pg.Surface((WIDTH,HEIGHT))
    black_out.fill((0,0,0))
    black_out.set_alpha(160)
    
    # 2. Game Over 文字列Surfaceを作成
    font = pg.font.Font(None,80)
    txt_surf = font.render("Game Over",True,(255,255,255))
    txt_rct = txt_surf.get_rect()
    txt_rct.center = WIDTH // 2,HEIGHT // 2
    
    # 3. 泣いているこうかとんSurfaceを作成（fig/8.pngなど）
    kk_crying_img = pg.transform.rotozoom(pg.image.load("fig/8.png"),0,0.9)
    kk_rct1 = kk_crying_img.get_rect()
    kk_rct1.center = WIDTH // 2-200,HEIGHT // 2
    kk_rct2 = kk_crying_img.get_rect()
    kk_rct2.center = WIDTH // 2+200,HEIGHT // 2
    
    # 4. 画面に貼り付けて更新
    screen.blit(black_out, [0, 0])
    screen.blit(txt_surf, txt_rct)
    screen.blit(kk_crying_img, kk_rct1)
    screen.blit(kk_crying_img, kk_rct2)
    pg.display.update()
    
    # 5. 5秒間停止
    time.sleep(5)

def check_bound(obj_rct: pg.Rect) -> tuple[bool,bool]:
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko =False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    
    clock = pg.time.Clock()
    tmr = 0
    
    #呼び出し
    kk_imgs = get_kk_imgs()
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, delta in DELTA.items():
            if key_lst[key]:
                sum_mv[0]+=delta[0]
                sum_mv[1]+=delta[1]
                
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img,kk_rct)
        
        bb_rct.move_ip(vx, vy)
        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img,bb_rct)
        
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        
        #呼び出し
        kk_img = kk_imgs[tuple(sum_mv)]
        
        screen.blit(bg_img,[0,0])
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
