from objects import *
from enemy import Enemy


class Level:
    def __init__(self, screen, total_coins=0) -> None:
        self.screen = screen
        self.checkpoints = []
        self.enemies = []
        self.borders = []
        self.rectangles = []
        self.coins = []
        self.total_coins = total_coins
        if self.total_coins != 0:
            self.coin_sound = pygame.mixer.Sound("assets/coin_sound.mp3")
        self.coin_count = 0
        self.completed = False

    def draw_level(self, player, dt):
        player_rect = player.get_rect()
        for rectangle in self.rectangles:
            rectangle.draw(self.screen)
        for border in self.borders:
            border.draw(self.screen)
        for checkpoint in self.checkpoints:
            checkpoint.draw(self.screen)
            # sets the players spawn to the checkpoint
            if checkpoint.get_rect().colliderect(player_rect):

                # remove any coins collected from the list
                for coin in self.coins:
                    if coin.is_collected:
                        self.coins.remove(coin)

                # if it is the last checkpoint we want to end the level
                if checkpoint.last_checkpoint() and len(self.coins) == 0:
                    self.completed = True
                spawn = checkpoint.get_spawn_loc()
                player.set_spawn_point(spawn[0], spawn[1])

        for enemy in self.enemies:
            enemy.draw(self.screen, dt)

        for coin in self.coins:
            coin.draw(self.screen)
            if coin.collect_player(player_rect):
                pygame.mixer.Sound.play(self.coin_sound)
                self.coin_count += 1

    def get_borders(self):
        return self.borders

    def get_enemies(self):
        return self.enemies

    def reset_coins(self):
        for coin in self.coins:
            if coin.is_collected:
                self.coin_count -= 1
            coin.is_collected = False


def level_one(screen):
    bw = Border.width
    level = Level(screen)
    # first checkpoint
    check_dim = Dim(100, 260, 100, 225)
    first_check = Checkpoint(check_dim, False)
    first_check.calc_borders((1, 2, 3, 4))
    first_check.right_border.dim.h -= 30 + bw
    level.checkpoints.append(first_check)
    first_check.add_borders(level)

    # rectangle leading out of first checkpoint
    small_rect_dim = Dim(
        first_check.right_border.dim.x +
        bw,
        first_check.right_border.dim.y +
        first_check.right_border.dim.h,
        60,
        30)
    small_rect = Rectangle(small_rect_dim)
    small_rect.calc_borders((2, 3, 4))
    small_rect.top_border.dim.w -= 30 - bw
    small_rect.fix_dims((1,))
    level.rectangles.append(small_rect)
    small_rect.add_borders(level)

    # big rectangle
    big_rect_dim = Dim(
        first_check.right_border.dim.x +
        30 +
        bw *
        2,
        check_dim.y +
        30,
        300,
        160)
    big_rect = Rectangle(big_rect_dim)
    big_rect.calc_borders((1, 2, 3, 4))
    big_rect.bottom_border.dim.x += 30
    big_rect.bottom_border.dim.w -= 30
    big_rect.top_border.dim.w -= 30
    level.rectangles.append(big_rect)
    big_rect.add_borders(level)

    # small rect leading to final checkpoint
    fin_rect_dim = Dim(big_rect.right_border.dim.x - 30,
                       big_rect.right_border.dim.y - 30, 60, 30)
    final_rect = Rectangle(fin_rect_dim)
    final_rect.calc_borders((1, 2, 4))
    final_rect.bottom_border.dim.x += 30 + bw
    final_rect.bottom_border.dim.w -= 30 + bw
    level.rectangles.append(final_rect)
    final_rect.add_borders(level)

    last_check_dim = Dim(
        big_rect.dim.x +
        big_rect.dim.w +
        30,
        big_rect.right_border.dim.y -
        30,
        100,
        225)
    last_checkpoint = Checkpoint(last_check_dim, True)
    last_checkpoint.calc_borders((1, 2, 3, 4))
    last_checkpoint.left_border.dim.y += 30 + bw
    last_checkpoint.left_border.dim.h -= 30 + bw
    level.checkpoints.append(last_checkpoint)
    last_checkpoint.add_borders(level)

    # add the enemies
    mov_a = [(1, 0, big_rect.dim.w - Enemy.radius),
             (-1, 0, big_rect.dim.w - Enemy.radius)]
    start_a = big_rect.dim.x + Enemy.radius

    mov_b = [(-1, 0, big_rect.dim.w - Enemy.radius),
             (1, 0, big_rect.dim.w - Enemy.radius)]
    start_b = big_rect.dim.x + big_rect.dim.w

    dis_between = Enemy.radius * 2 + 10
    enemy_y = big_rect.dim.y + Enemy.radius * 2
    for i in range(5):
        if i % 2 == 0:
            level.enemies.append(
                Enemy((start_a, enemy_y + i * dis_between), mov_a))
        else:
            level.enemies.append(
                Enemy((start_b, enemy_y + i * dis_between), mov_b))

    return level


def level_two(screen):
    bw = Border.width
    level = Level(screen, 9)

    first_check_dim = Dim(85, 300, 100, 150)
    first_check = Checkpoint(first_check_dim, False)
    first_check.calc_borders((1, 2, 3, 4))
    r_bord_h = (first_check_dim.h - 30) / 2
    first_check.right_border.dim.h = r_bord_h + bw
    level.borders.append(
        Border(Dim(185, 300 + r_bord_h + 30 + bw, bw, r_bord_h)))
    level.checkpoints.append(first_check)
    first_check.add_borders(level)

    # first tiny rect
    f_tiny_rec = Rectangle(Dim(185 + bw, 300 + r_bord_h + bw, 30, 30))
    f_tiny_rec.calc_borders((2, 4))
    f_tiny_rec.fix_dims((1, 3))
    f_tiny_rec.add_borders(level)
    level.rectangles.append(f_tiny_rec)

    # large rect
    big_rect = Rectangle(Dim(f_tiny_rec.dim.x + 30 + bw, 250, 350, 250))
    big_rect.calc_borders((2, 4))
    big_rect.add_borders(level)
    level.rectangles.append(big_rect)
    big_rect_bh = (big_rect.dim.h - 30) / 2
    top_left_b = Border(
        Dim(big_rect.dim.x - bw, big_rect.dim.y, bw, big_rect_bh))
    bot_left_b = Border(Dim(top_left_b.dim.x, top_left_b.dim.y +
                        top_left_b.dim.h + 30 + bw, bw, big_rect_bh))
    top_right_b = Border(Dim(big_rect.dim.x + big_rect.dim.w,
                         big_rect.dim.y - bw, bw, big_rect_bh + bw))
    bot_right_b = Border(
        Dim(top_right_b.dim.x, bot_left_b.dim.y, bw, big_rect_bh))
    level.borders.append(top_left_b)
    level.borders.append(bot_left_b)
    level.borders.append(top_right_b)
    level.borders.append(bot_right_b)

    # last tiny rect
    l_tiny_rec = Rectangle(
        Dim(top_right_b.dim.x + bw, bot_right_b.dim.y - 30, 30, 30))
    l_tiny_rec.calc_borders((2, 4))
    l_tiny_rec.fix_dims((1, 3))
    l_tiny_rec.add_borders(level)
    level.rectangles.append(l_tiny_rec)

    # last checkpoint
    last_check = Checkpoint(
        Dim(l_tiny_rec.dim.x + l_tiny_rec.dim.w, 300, 100, 150), True)
    last_check.calc_borders((2, 3, 4))
    last_check.add_borders(level)
    level.checkpoints.append(last_check)
    final_top_border = Border(
        Dim(last_check.dim.x - bw, last_check.dim.y, bw, r_bord_h + bw))
    final_bot_border = Border(
        Dim(final_top_border.dim.x, last_check.dim.y + r_bord_h + 30 + bw, bw, r_bord_h))

    level.borders.append(final_top_border)
    level.borders.append(final_bot_border)

    # enemies
    dis_between = Enemy.radius + 25
    e_start_x = big_rect.dim.x + Enemy.radius + 5

    mov_a = [(0, 1, big_rect.dim.h - Enemy.radius * 2),
             (0, -1, big_rect.dim.h - Enemy.radius * 2)]
    y_a = big_rect.dim.y + Enemy.radius
    mov_b = [(0, -1, big_rect.dim.h - Enemy.radius * 2),
             (0, 1, big_rect.dim.h - Enemy.radius * 2)]
    y_b = big_rect.dim.y + big_rect.dim.h - Enemy.radius

    for i in range(10):
        if i % 2 == 0:
            level.enemies.append(
                Enemy(
                    (e_start_x +
                     i *
                     dis_between,
                     y_a),
                    mov_a,
                    speed=215))
        else:
            level.enemies.append(
                Enemy(
                    (e_start_x +
                     i *
                     dis_between,
                     y_b),
                    mov_b,
                    speed=215))

    # coins
    coin_dis_bet = 20
    coin_start_x = big_rect.dim.x + big_rect.dim.w / 2 - Coin.width - coin_dis_bet
    coin_start_y = big_rect.dim.y + big_rect.dim.h / 2 - Coin.width - coin_dis_bet

    # first row
    for i in range(3):
        level.coins.append(
            Coin(
                (coin_start_x +
                 coin_dis_bet *
                 i,
                 coin_start_y)))

    # second row
    coin_start_y += coin_dis_bet
    for i in range(3):
        level.coins.append(
            Coin(
                (coin_start_x +
                 coin_dis_bet *
                 i,
                 coin_start_y)))

    # third row
    coin_start_y += coin_dis_bet
    for i in range(3):
        level.coins.append(
            Coin(
                (coin_start_x +
                 coin_dis_bet *
                 i,
                 coin_start_y)))

    return level


def level_three(screen):
    bw = Border.width
    level = Level(screen, 4)
    sq_w = 30

    # first checkpoint
    first_check = Checkpoint(Dim(260, 300, 275, 200), True)
    first_check.calc_borders((2, 4))
    first_check.add_borders(level)
    level.checkpoints.append(first_check)

    # left side borders for checkpoint
    check_bh = (first_check.dim.h - 30) / 2
    level.borders.append(
        Border(Dim(first_check.dim.x - bw, first_check.dim.y, bw, check_bh)))
    level.borders.append(Border(
        Dim(first_check.dim.x - bw, first_check.dim.y + check_bh + sq_w, bw, check_bh)))

    long_rect_w = sq_w * 2 + first_check.dim.w

    # square outside of checkpoint
    small_y_pos = first_check.dim.y + (first_check.dim.h - 30) / 2
    left_tiny_sq = Rectangle(
        Dim(first_check.dim.x - sq_w, small_y_pos, 30, 30))
    left_tiny_sq.calc_borders((2, 4))
    left_tiny_sq.fix_dims((1,))
    left_tiny_sq.add_borders(level)
    level.rectangles.append(left_tiny_sq)

    right_tiny_sq = Rectangle(
        Dim(first_check.dim.x + first_check.dim.w + bw, small_y_pos, 30, 30))
    right_tiny_sq.calc_borders((2, 4))
    right_tiny_sq.fix_dims((1,))
    right_tiny_sq.add_borders(level)
    level.rectangles.append(right_tiny_sq)

    # right side border for checkpoint
    level.borders.append(
        Border(Dim(right_tiny_sq.dim.x, first_check.dim.y - bw, bw, check_bh + bw)))
    level.borders.append(Border(Dim(
        right_tiny_sq.dim.x, first_check.dim.y + check_bh + sq_w, bw, check_bh + bw)))

    # long rectangles on left side
    big_left_rect_dim = Dim(
        left_tiny_sq.dim.x -
        30,
        first_check.dim.y -
        sq_w *
        2 -
        bw,
        sq_w,
        long_rect_w)
    big_left_rect = Rectangle(big_left_rect_dim)
    big_left_rect.calc_borders((1, 2, 4))
    big_left_rect.left_border.dim.h -= sq_w
    big_left_rect.add_borders(level)
    level.rectangles.append(big_left_rect)

    # small square with coin on left side
    left_coin_sq_dim = Dim(big_left_rect.dim.x -
                           sq_w, big_left_rect.left_border.dim.y +
                           big_left_rect.left_border.dim.h, sq_w, sq_w)
    left_coin_sq = Rectangle(left_coin_sq_dim)
    left_coin_sq.calc_borders((1, 2, 4))
    left_coin_sq.add_borders(level)
    level.rectangles.append(left_coin_sq)

    # long rectangle on right side
    big_right_rect_dim = Dim(
        right_tiny_sq.dim.x +
        right_tiny_sq.dim.w,
        big_left_rect.dim.y,
        sq_w,
        long_rect_w)
    big_right_rect = Rectangle(big_right_rect_dim)
    big_right_rect.calc_borders((2, 3, 4))
    big_right_rect.right_border.dim.y += sq_w + bw
    big_right_rect.right_border.dim.h -= sq_w + bw
    big_right_rect.bottom_border.dim.x -= sq_w - bw
    big_right_rect.bottom_border.dim.w += sq_w - bw
    big_right_rect.add_borders(level)
    level.rectangles.append(big_right_rect)

    # small right side sq
    small_right_sq = Rectangle(
        Dim(big_right_rect.dim.x + sq_w + bw, big_right_rect.dim.y, sq_w, sq_w))
    small_right_sq.calc_borders((2, 3, 4))
    small_right_sq.fix_dims((1,))
    small_right_sq.add_borders(level)
    level.rectangles.append(small_right_sq)

    # long rectangle on the bottom
    bot_rect = Rectangle(Dim(left_tiny_sq.dim.x +
                             bw, left_coin_sq.dim.y, long_rect_w, sq_w))
    bot_rect.fix_dims((1, 3))
    bot_rect.calc_borders((2, 4))
    bot_rect.top_border.dim.x += bw
    bot_rect.top_border.dim.w -= bw
    bot_rect.bottom_border.dim.w -= sq_w * 2
    bot_rect.add_borders(level)
    level.rectangles.append(bot_rect)

    # small square on bottom
    x_off = bot_rect.bottom_border.dim.x + bot_rect.bottom_border.dim.w
    small_bot_sq = Rectangle(
        Dim(x_off, bot_rect.dim.y + sq_w + bw, sq_w, sq_w))
    small_bot_sq.calc_borders((1, 3, 4))
    small_bot_sq.fix_dims((2,))
    small_bot_sq.add_borders(level)
    level.rectangles.append(small_bot_sq)

    # long rectangle on top
    top_rect = Rectangle(
        Dim(bot_rect.dim.x, big_left_rect.dim.y, long_rect_w, sq_w))
    top_rect.calc_borders((2, 4))
    top_rect.top_border.dim.x += sq_w * 2 + bw
    top_rect.top_border.dim.w -= sq_w * 2
    top_rect.bottom_border.dim.x += bw
    top_rect.add_borders(level)
    top_rect.fix_dims((3,))
    top_rect.fix_dims((3,))
    level.rectangles.append(top_rect)

    # right borders for long left rectangle
    long_rect_bh = (long_rect_w - sq_w * 3) / 2
    level.borders.append(
        Border(Dim(top_rect.dim.x, top_rect.dim.y + sq_w, bw, long_rect_bh - bw)))
    level.borders.append(Border(
        Dim(top_rect.dim.x, top_rect.dim.y + sq_w * 2 + long_rect_bh, bw, long_rect_bh)))
    # left borders for long right rectangle
    level.borders.append(Border(
        Dim(big_right_rect.dim.x - bw, top_rect.dim.y + sq_w, bw, long_rect_bh - bw)))
    level.borders.append(Border(Dim(big_right_rect.dim.x -
                                    bw, top_rect.dim.y +
                                    sq_w *
                                    2 +
                                    long_rect_bh, bw, long_rect_bh)))

    # border before small checkpoint on top
    level.borders.append(
        Border(Dim(top_rect.dim.x, top_rect.dim.y - bw, sq_w, bw)))

    # small checkpoint on top
    spawn_loc = (top_rect.dim.x + sq_w + 5, top_rect.dim.y - sq_w)
    top_check = Checkpoint(Dim(top_rect.dim.x +
                               sq_w, top_rect.dim.y -
                               sq_w -
                               bw, 30, 30), True, spawn_loc=spawn_loc)
    top_check.calc_borders((1, 2, 3))
    top_check.fix_dims((4,))
    top_check.add_borders(level)
    level.checkpoints.append(top_check)

    # coins
    def coin_loc(rect):
        mid = rect.calc_mid()
        return (mid[0] - Coin.width / 2, mid[1] - Coin.width / 2)

    level.coins.append(Coin(coin_loc(top_check)))
    level.coins.append(Coin(coin_loc(left_coin_sq)))
    level.coins.append(Coin(coin_loc(small_bot_sq)))
    level.coins.append(Coin(coin_loc(small_right_sq)))

    # enemies
    e_center = Enemy.radius + Enemy.radius / 2
    speed = 165
    dis_between = Enemy.radius * 2
    start_x = big_left_rect.dim.x + e_center
    start_y = bot_rect.dim.y + e_center

    top_right_y = big_right_rect.dim.y + e_center
    top_right_x = big_right_rect.dim.x + e_center
    top_left_x = big_left_rect.dim.x + e_center
    bot_left_y = bot_rect.dim.y + e_center
    bot_right_y = big_right_rect.dim.y + big_right_rect.dim.h - e_center

    # 16 that start on the left side
    start_x = big_left_rect.dim.x + e_center
    start_y = bot_rect.dim.y + e_center
    for i in range(16):
        y_off = start_y - i * dis_between
        x_dis = top_right_x - start_x
        y_dis = start_y - top_right_y
        mov = []
        mov.append((0, -1, y_off - top_right_y))
        mov.append((1, 0, x_dis))
        mov.append((0, 1, y_dis))
        mov.append((-1, 0, x_dis))
        mov.append((0, -1, bot_left_y - y_off))
        level.enemies.append(Enemy((start_x, y_off), mov, speed=speed))

    # 5 that start on top
    start_x += e_center
    start_y = top_right_y
    for i in range(5):
        x_off = start_x + i * dis_between
        x_dis = top_right_x - top_left_x
        y_dis = bot_right_y - top_right_y
        mov = []
        mov.append((1, 0, top_right_x - x_off))  # top left to right
        mov.append((0, 1, y_dis))  # top right to bottom right
        mov.append((-1, 0, x_dis))  # bottom right to bottom left
        mov.append((0, -1, y_dis))  # bottom left to top left
        # back to starting offset
        mov.append((1, 0, x_off - start_x + e_center))
        level.enemies.append(Enemy((x_off, start_y), mov, speed=speed))

    # 16 that start on the right side
    start_x = big_right_rect.dim.x + e_center
    # the y pos where the first enemy spawns
    start_y = top_right_y
    for i in range(16):
        # offset from the first enemy
        y_off = start_y + i * dis_between
        x_dis = start_x - top_left_x
        y_dis = bot_right_y - start_y
        mov = []
        mov.append((0, 1, bot_right_y - y_off))  # top right to bottom right
        mov.append((-1, 0, x_dis))  # bot right to bot left
        mov.append((0, -1, y_dis))  # bot left to top left
        mov.append((1, 0, x_dis))  # top left to to top right
        mov.append((0, 1, y_off - top_right_y))  # top right to starting pos
        level.enemies.append(Enemy((start_x, y_off), mov, speed=speed))
    # 5 that on bottom
    start_x -= e_center
    start_y = bot_right_y
    for i in range(5):
        x_off = start_x - i * dis_between
        x_dis = top_right_x - top_left_x
        y_dis = start_y - top_right_y
        mov = []
        mov.append((-1, 0, x_off - top_left_x))  # bot right to left
        mov.append((0, -1, y_dis))  # bot left to top left
        mov.append((1, 0, x_dis))  # top left to top right
        mov.append((0, 1, y_dis))  # top right to bottom right
        # back to starting offset
        mov.append((-1, 0, start_x - x_off + e_center))
        level.enemies.append(Enemy((x_off, start_y), mov, speed=speed))

    return level


LEVELS = [level_one, level_two, level_three]
MAX_LEVEL = 3
