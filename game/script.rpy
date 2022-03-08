init python:
    import pygame
    from random import randint


    def cross(obj1, obj2):
        for i in range(obj1['pos'], obj1['pos'] + obj1['size']):
            if i in range(obj2['pos'], obj2['pos'] + obj2['size']):
                return True

    class Enemy:

        def __init__(self, color, x, y, xs, ys):
            self.xpos = x
            self.ypos = y
            self.xsize = xs
            self.ysize = ys
            self.color = color

        def dict(self):
            return {"xpos": self.xpos, "ypos": self.ypos, 'color': self.color, 'xsize': self.xsize, 'ysize': self.ysize}


    class Game(renpy.Displayable):

        def __init__(self, display_size, speed, enemy_size, **kwargs):
            super(Game, self).__init__(**kwargs)

            self.ex = enemy_size[0]
            self.ey = enemy_size[1]
            self.obj = renpy.displayable(Solid('#0000FF', xsize=28, ysize=15))
            self.display_size = int(display_size*0.9)
            self.speed = speed
            self.y = self.display_size
            self.enemys = []
            self.lose = False
            self.credits = 0

        def generate_enemy(self):
            if len(self.enemys) < 3:
                x_spawn = randint(400, 1280)
                y_spawn = randint(int(450*0.4)-self.ex*0.5, self.display_size-self.ex*0.5)
                self.enemys.append(
                        Enemy('#FF0000', x_spawn, y_spawn, self.ex, self.ey)
                    )

        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
            obj = renpy.render(self.obj, width, height, st, at)
            render.blit(obj, (0, self.y))
            for enemy in self.enemys:
                obj1 = renpy.displayable(Solid(**enemy.dict()))
                render.blit(renpy.render(obj1, self.ex, self.ey, st, at), (enemy.xpos, enemy.ypos))
                renpy.redraw(obj1, 0)

            self.generate_enemy()
            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[pygame.K_SPACE]:
                if self.y < int(self.display_size*0.4):
                    self.y = int(self.display_size*0.4)
                else:
                    self.y -= self.speed
            else:
                if self.y > self.display_size:
                    self.y = self.display_size
                else:
                    self.y += self.speed
            renpy.redraw(self.obj, 0)

            for i, enemy in enumerate(self.enemys):
                if_first = cross({'pos': enemy.xpos, 'size': enemy.xsize}, {'pos': 0, 'size': 28})
                if_second = cross({'pos': enemy.ypos, 'size': enemy.ysize}, {'pos': self.y, 'size': 15})
                if if_first and if_second:
                    self.lose = True
                    renpy.timeout(0)
                if enemy.xpos < -self.ex:
                    del self.enemys[i]
                    self.credits += 1
                    creds = self.credits
                else:
                    enemy.xpos -= self.speed

            return render

        def event(self, ev, x, y, st):
            if self.lose:
                return self.credits
            else:
                raise renpy.IgnoreEvent()

        def visit(self):
            return_objects = []
            if self.enemys:
                for enemy in self.enemys:
                    return_objects.append(renpy.displayable(Solid(**enemy.dict())))
            return return_objects

screen main:

    frame:
        xsize 1280
        ysize 750
        add Game(450, 7, [100, 100])
        add Solid('#000000', xsize=1280, ysize=4) ypos 450-int(450*0.05) xalign 0.5
        add Solid('#000000', xsize=1280, ysize=4) ypos int(450*0.4)-int(450*0.05) xalign 0.5


label start:

    call screen main

    'you lose :( your credits: [_return]'