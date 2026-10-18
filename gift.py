import math
import random
import pygame
import os

# ล็อกตำแหน่งโฟลเดอร์ให้ดึงรูป heart.png ได้อย่างถูกต้อง
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# เริ่มต้นระบบ Pygame
pygame.init()
WIDTH, HEIGHT = 1050, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sweet Love Letter 💌🐻✨")
clock = pygame.time.Clock()

# 1. ดาวฉากหลังระยิบระยับ
stars = []
for _ in range(120):
    stars.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(0, HEIGHT),
        'size': random.randint(2, 4),
        'speed': random.uniform(0.02, 0.06)
    })

# 2. หัวใจลอยพริ้วไหว
floating_hearts = []
for _ in range(40):
    floating_hearts.append({
        'x': random.randint(40, WIDTH - 40),
        'y': random.randint(HEIGHT, HEIGHT + 500),
        'size': random.randint(14, 26),
        'speed': random.uniform(1.2, 2.8),
        'offset': random.uniform(0, 6.28),
        'alpha': random.randint(150, 230)
    })

# 3. ระบบพลุฉลอง
fireworks = []

def create_fireworks(x, y):
    colors = [(255, 105, 180), (255, 182, 193), (255, 215, 0), (255, 240, 245), (255, 160, 122)]
    for _ in range(90):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(3, 12)
        fireworks.append({
            'x': x,
            'y': y,
            'vx': math.cos(angle) * speed,
            'vy': math.sin(angle) * speed - random.uniform(1, 3.5),
            'color': random.choice(colors),
            'alpha': 255,
            'size': random.randint(3, 8)
        })

# โหลดรูปหมี/แพนด้าของคุณ (heart.png)
image_filename = "heart.png"
try:
    raw_photo = pygame.image.load(image_filename).convert_alpha()
    bear_img = pygame.transform.smoothscale(raw_photo, (220, 220))
    print("✨ โหลดรูปน้องหมีสำเร็จแล้วครับ!")
except Exception as e:
    print(f"⚠️ ยังไม่พบไฟล์ {image_filename} ในโฟลเดอร์ LoveGift น้า:", e)
    bear_img = None

# กำหนดฟอนต์
font_title = pygame.font.SysFont("Arial", 46, bold=True)
font_card = pygame.font.SysFont("Arial", 24, bold=True)

# ข้อความหวานๆ ที่จะค่อยๆ พิมพ์
love_message = "You are my favorite person in this world <3"
typed_text = ""
type_index = 0
type_timer = 0

# สถานะของจดหมาย
is_opened = False
letter_progress = 0.0  # 0.0 ถึง 1.0
fireworks_triggered = False

running = True
global_time = 0

while running:
    global_time += 1

    # สีพื้นหลังพาสเทลชมพูละมุนตา
    screen.fill((255, 240, 246))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        
        # คลิกเมาส์เพื่อเปิดซองจดหมาย
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not is_opened:
                is_opened = True

    # --- 1. วาดดาวฉากหลัง ---
    for s in stars:
        alpha_star = int(100 + 130 * abs(math.sin(global_time * s['speed'])))
        star_surf = pygame.Surface((s['size'] * 2, s['size'] * 2), pygame.SRCALPHA)
        pygame.draw.circle(star_surf, (255, 182, 193, alpha_star), (s['size'], s['size']), s['size'])
        screen.blit(star_surf, (s['x'], s['y']))

    # คำนวณการเปิดจดหมาย
    if is_opened and letter_progress < 1.0:
        letter_progress = min(1.0, letter_progress + 0.03)
        if letter_progress >= 0.5 and not fireworks_triggered:
            fireworks_triggered = True
            create_fireworks(WIDTH // 2, HEIGHT // 2 - 50)
            create_fireworks(WIDTH // 2 - 280, HEIGHT // 2 - 120)
            create_fireworks(WIDTH // 2 + 280, HEIGHT // 2 - 120)

    # --- 2. เอฟเฟกต์พิมพ์ข้อความ ---
    if is_opened and letter_progress >= 0.8:
        type_timer += 1
        if type_timer % 3 == 0 and type_index < len(love_message):
            typed_text += love_message[type_index]
            type_index += 1

    # --- 3. อัปเดตและวาดพลุ ---
    for fw in fireworks[:]:
        fw['x'] += fw['vx']
        fw['y'] += fw['vy']
        fw['vx'] *= 0.98
        fw['vy'] += 0.16
        fw['alpha'] -= 4
        if fw['alpha'] <= 0:
            fireworks.remove(fw)
        else:
            fw_surf = pygame.Surface((fw['size'] * 2, fw['size'] * 2), pygame.SRCALPHA)
            color_with_alpha = (*fw['color'], max(0, int(fw['alpha'])))
            pygame.draw.circle(fw_surf, color_with_alpha, (fw['size'], fw['size']), fw['size'])
            screen.blit(fw_surf, (fw['x'], fw['y']))

    # --- 4. หัวใจลอยฉากหลัง ---
    if letter_progress > 0.2:
        for fh in floating_hearts:
            fh['y'] -= fh['speed']
            fh['x'] += math.sin(global_time * 0.04 + fh['offset']) * 0.9
            if fh['y'] < -50:
                fh['y'] = HEIGHT + random.randint(10, 100)
                fh['x'] = random.randint(40, WIDTH - 40)

            h_surf = pygame.Surface((fh['size'] * 2, fh['size'] * 2), pygame.SRCALPHA)
            sz = fh['size'] * 0.7
            pygame.draw.circle(h_surf, (255, 105, 180, fh['alpha']), (int(sz // 2 + 2), int(sz // 2)), int(sz // 2))
            pygame.draw.circle(h_surf, (255, 105, 180, fh['alpha']), (int(sz + sz // 2 + 2), int(sz // 2)), int(sz // 2))
            pts = [(2, int(sz // 2 + 1)), (int(sz * 2 + 2), int(sz // 2 + 1)), (int(sz + 2), int(sz * 2))]
            pygame.draw.polygon(h_surf, (255, 105, 180, fh['alpha']), pts)
            screen.blit(h_surf, (fh['x'], fh['y']))

    # --- 5. กรณีคลิกเปิดแล้ว: ซองจดหมายจะตกลงด้านล่าง และน้องหมีกับการ์ดจะลอยเด่นขึ้นมาตรงกลาง ---
    if is_opened:
        # การ์ดข้อความและน้องหมีลอยเด่นตรงกลางจอแบบสวยๆ
        card_w, card_h = 460, 320
        card_cx, card_cy = WIDTH // 2, HEIGHT // 2 + 20
        card_rect = pygame.Rect(card_cx - card_w // 2, card_cy - card_h // 2, card_w, card_h)

        # พื้นหลังการ์ดสีครีมขอบทองพรีเมียม
        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, (255, 253, 248), card_surf.get_rect(), border_radius=20)
        pygame.draw.rect(card_surf, (245, 215, 160), card_surf.get_rect(), width=4, border_radius=20)
        screen.blit(card_surf, card_rect.topleft)

        # วาดน้องหมีตรงกลางการ์ดแบบเด่นๆ
        if bear_img:
            pulse = math.sin(global_time * 0.1) * 6
            animated_w = int(220 + pulse)
            animated_h = int(220 + pulse)
            animated_bear = pygame.transform.smoothscale(bear_img, (animated_w, animated_h))
            bear_rect = animated_bear.get_rect(center=(card_cx, card_cy - 45))
            
            # ออร่าเรืองแสงรอบน้องหมี
            glow_surf = pygame.Surface((animated_w + 30, animated_h + 30), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (255, 192, 203, 140), glow_surf.get_rect(), border_radius=30)
            screen.blit(glow_surf, (bear_rect.x - 15, bear_rect.y - 15))
            
            screen.blit(animated_bear, bear_rect.topleft)

        # ข้อความพิมพ์ดีดด้านล่างน้องหมีในการ์ด
        if letter_progress >= 0.8:
            type_timer += 1
            if type_timer % 3 == 0 and type_index < len(love_message):
                typed_text += love_message[type_index]
                type_index += 1

            cursor = "|" if (global_time // 15) % 2 == 0 and type_index < len(love_message) else ""
            msg_surf = font_card.render(typed_text + cursor, True, (200, 30, 80))
            screen.blit(msg_surf, msg_surf.get_rect(center=(card_cx, card_cy + 110)))

    else:
        # --- 6. ตอนยังไม่เปิด: แสดงซองจดหมายสวยๆ อยู่ตรงกลาง ---
        env_cx, env_cy = WIDTH // 2, HEIGHT // 2 + 60
        env_w, env_h = 420, 260

        # เงาใต้ซอง
        shadow_surf = pygame.Surface((env_w + 30, 35), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (200, 150, 170, 60), shadow_surf.get_rect())
        screen.blit(shadow_surf, (env_cx - (env_w + 30) // 2, env_cy + env_h // 2 - 10))

        env_rect = pygame.Rect(env_cx - env_w // 2, env_cy - env_h // 2, env_w, env_h)
        pygame.draw.rect(screen, (255, 222, 235), env_rect, border_radius=18)
        
        poly_left = [(env_rect.left, env_rect.top), (env_cx, env_cy + 20), (env_rect.left, env_rect.bottom)]
        poly_right = [(env_rect.right, env_rect.top), (env_cx, env_cy + 20), (env_rect.right, env_rect.bottom)]
        poly_bottom = [(env_rect.left, env_rect.bottom), (env_cx, env_cy - 10), (env_rect.right, env_rect.bottom)]
        
        pygame.draw.polygon(screen, (255, 192, 205), poly_left)
        pygame.draw.polygon(screen, (255, 192, 205), poly_right)
        pygame.draw.polygon(screen, (255, 168, 188), poly_bottom)

        ribbon_rect = pygame.Rect(env_cx - 15, env_rect.top, 30, env_h)
        pygame.draw.rect(screen, (245, 215, 130), ribbon_rect)
        pygame.draw.rect(screen, (255, 105, 180), env_rect, width=4, border_radius=18)

        # ฝาซองปิด
        flap_poly = [(env_rect.left, env_rect.top), (env_cx, env_cy + 60), (env_rect.right, env_rect.top)]
        pygame.draw.polygon(screen, (255, 135, 165), flap_poly)
        pygame.draw.polygon(screen, (255, 90, 140), flap_poly, width=3)
        
        # ตราประทับหัวใจ
        seal_cx, seal_cy = env_cx, env_cy + 40
        pygame.draw.circle(screen, (245, 215, 130), (seal_cx, seal_cy), 22)
        pygame.draw.circle(screen, (220, 40, 80), (seal_cx, seal_cy), 18)

    # --- 7. หัวข้อด้านบน ---
    if not is_opened:
        title_surf = font_title.render("A Special Love Letter For You", True, (200, 40, 90))
        sub_surf = font_card.render("Click anywhere to open your surprise!", True, (220, 80, 120))
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, 90)))
        screen.blit(sub_surf, sub_surf.get_rect(center=(WIDTH // 2, 145)))
    else:
        title_surf = font_title.render("I Love You So Much <3", True, (210, 20, 80))
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, 80)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()