import pygame as pg

import Model.main as model
from EventManager import *
from const_main import *
from View.const import *

# import Model.GameObject.model_const as mc

numberOfQuaffles = 2

class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """
    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

        self.isinitialized = False
        self.screen = None
        self.clock = None
        self.smallfont = None
        self.player_images = []
        self.player_bais = []
        self.stuns = []
    
    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, Event_EveryTick) and self.isinitialized:
            cur_state = self.model.state.peek()
            if cur_state == model.STATE_MENU:
                self.render_menu()
            if cur_state == model.STATE_PLAY:
                self.render_play()
            if cur_state == model.STATE_STOP:
                self.render_stop()

            self.display_fps()
            # limit the redraw speed to 30 frames per second
            self.clock.tick(FramePerSec)
            '''
        elif isinstance(event, Event_Action):
            player = self.evManager.players[event.PlayerIndex]
            if event.ActionIndex == 1 and player.mode == 0:
                self.stuns[player.index] = [player.positon, 0]
                '''
        elif isinstance(event, Event_Quit):
            # shut down the pygame graphics
            self.isinitialized = False
            pg.quit()
        elif isinstance(event, Event_Initialize):
            self.initialize()
    
    def render_menu(self):
        """
        Render the game menu.
        """
        # draw backgound
        self.screen.blit(self.background,(0,0))
        # write some word
        somewords = self.smallfont.render(
                    'You are in the Menu. Space to play. Esc exits.', 
                    True, (0, 255, 0))
        (SurfaceX, SurfaceY) = somewords.get_size()
        pos_x = (ScreenSize[0] - SurfaceX)/2
        pos_y = (ScreenSize[1] - SurfaceY)/2
        self.screen.blit(somewords, (pos_x, pos_y))
        # update surface
        pg.display.flip()
        
    def render_play(self):
        """
        Render the game play.
        """
        # draw backgound
        self.render_background()

        for i in range(PlayerNum):
            self.render_player_status(i)
        for i in range(PlayerNum):
            self.render_player_character(i)
            
        #for testing
        for i in range(4):
            self.render_player_status(i)
        #end test
            
 #      for i in range(numberOfQuaffles):
            #self.render_quaffle(i)
 #       for i in self.stuns:
 #           pass
        for stun in self.stuns:
            if stun[1] in range(9):
                self.blit_at_center(self.stun_images[stun[1]], stun[0])
                stun[1] += 1
#        for barrier in self.evManager.barriers:
#            self.render_barrier(barrier)

        # update surface
        pg.display.flip()
        
        
    def render_stop(self):
        """
        Render the stop screen.
        """
        # draw background
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.map_gray,(0,0))
    
        # display words
        somewords = self.smallfont.render(
                    'Pause',
                    True, (0, 255, 0))
        (SurfaceX, SurfaceY) = somewords.get_size()
        pos_x = (ScreenSize[0] - SurfaceX)/2
        pos_y = (ScreenSize[1] - SurfaceY)/2
        self.screen.blit(somewords, (pos_x, pos_y))
        # update surface
        pg.display.flip()

    def display_fps(self):
        """Show the programs FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format(GameCaption, self.clock.get_fps())
        pg.display.set_caption(caption)
        
    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """
        result = pg.init()
        pg.font.init()
        pg.display.set_caption(GameCaption)
        self.screen = pg.display.set_mode(ScreenSize)
        self.clock = pg.time.Clock()
        self.smallfont = pg.font.Font(None, 40)
        self.isinitialized = True
        self.player_bias = [0, 0, 0, 0]
        self.stuns = [[(0,0),-1] for _ in range(PlayerNum)]
        # load images
        ''' backgrounds '''
        self.map = pg.image.load('View/image/background/map.png')
        self.map_gray = pg.image.load('View/image/background/map_grayscale.png')
        self.time = pg.image.load('View/image/background/time.png')
        self.background = pg.image.load('View/image/background/backgroundfill.png')
        for i in range(4):
            self.playerInfo[i] = pg.image.load('View/image/background/info'+str(i+1)+'.png')
        ''' icons '''
        self.mode_images = [ pg.image.load('View/image/icon/icon_attack.png'),
                            pg.image.load('View/image/icon/icon_protectmode.png')]
        self.player_status0 = pg.image.load('View/image/icon/dizzyOninfo.png')
        self.player_status1 = pg.image.load('View/image/icon/shieldOninfo.png')
        self.player_status2 = pg.image.load('View/image/icon/shadowOningo.png')
        self.player_status_A = pg.image.load('View/image/icon/attackmodeOninfo.png')
        self.player_status_P = pg.image.load('View/image/icon/protectmodeOninfo.png')
        ''' skills '''
        self.stun_images = [ pg.image.load('View/image/skill/magicfield_'+str(i+1)+'.png') for i in range(9) ]
        self.mask_images = [ pg.image.load('View/image/skill/shield_'+str(i+1)+'.png' )for i in range(12) ]
        ''' balls '''
        self.ball_powered_images = [ pg.image.load('View/image/ball/ball'+str(i%2+1)+'_powered.png') for i in range(numberOfQuaffles) ]
        self.ball_normad_images = [ pg.image.load('View/image/ball/ball'+str(i%2+1)+'.png') for i in range(numberOfQuaffles) ]
        ''' characters '''
        self.take_ball_images = [ pg.image.load('View/image/icon/icon_haveball'+str(i%2+1)+'.png') for i in range(numberOfQuaffles)]
        directions = ['_leftup', '_left', '_leftdown', '_down']
        colors = ['_blue', '_yellow', '_red', '_green']
        self.player_freeze_images = [pg.image.load('View/image/player/player_down'+colors[i]+'_frost.png') for i in range(4)]

        self.player_photo = []
        self.player_photo.append( pg.image.load('View/image/cat/cat-normal-red.png'))
        self.player_photo.append( pg.image.load('View/image/silver/silver-normal-blue.png'))
        self.player_photo.append( pg.image.load('View/image/black/black-normal-green.png'))
        self.player_photo.append( pg.image.load('View/image/shining/shining-normal-yellow.png'))
        
        self.player_photo.append( pg.image.load('View/image/cat/cat-hurt-red.png'))
        self.player_photo.append( pg.image.load('View/image/silver/silver-hurt-blue.png'))
        self.player_photo.append( pg.image.load('View/image/black/black-hurt-green.png'))
        self.player_photo.append( pg.image.load('View/image/shining/shining-hurt-yellow.png'))
        
        def get_player_image(colorname, direction, suffix):
            if direction == 0:
                direction = 5
            if direction == 1:
                return pg.transform.flip(pg.image.load('View/image/player/player_down'+colorname+suffix+'.png'), 0, 1)
            elif direction in range(2,6):
                return pg.transform.flip(pg.image.load('View/image/player/player'+directions[direction-2]+colorname+suffix+'.png'), 1, 0)
            else:
                return pg.image.load('View/image/player/player'+directions[8-direction]+colorname+suffix+'.png')
        self.player_images = [ [get_player_image(colors[i],direction,'') for direction in range(9)] for i in range(4) ]
        self.player_invisable_images = [ [get_player_image(colors[i],direction,'_invisible') for direction in range(9)] for i in range(4) ]
        

    def render_background(self):
        self.screen.blit(self.map, Pos_map)
        self.screen.blit(self.time, Pos_time)
        self.blit_at_center(self.player_images[3][2], (200,500))
        self.blit_at_center(self.mode_images[1], (200,500))
        self.blit_at_center(self.take_ball_images[0], (200,500))
        self.blit_at_center(self.ball_powered_images[0], (500,500))
        self.blit_at_center(self.stun_images[0], (370,370))
        
    def render_player_status(self, index):
#     player = self.evManager.players[index]

#     background display
        info = self.playerInfo[index]
        pos_x , pos_y = 750 , 20 + 180*index
        pos = (pos_x,pos_y)
        self.screen.blit(info,pos)

#      player photo display
        if player.isFreeze or :
            self.screen.blit(self.player_photo[index + 4], pos + (20,20))
        else:
            self.screen.blit(self.player_photo[index],pos+(20,20))
        
        
#       icon display       
        if player.isFreeze:
            self.screen.blit(self.player_status0,pos+(150,20))
            
        #!!!!
        if self.model.players[index].isMask:                #not sure about this part
            self.screen.blit(self.player_status1,pos+(150,50))   
        #!!!!
            
        if !player.isVisible:
            self.screen.blit(self.player_status2,pos+(150,80))
        if player.mode == 1:
            self.screen.blit(self.player_status_P,pos+(150,110))
        elif player.mode == 0:
            self.screen.blit(self.player_status_A,pos+(150,110))
        pass

#      mana and score and name
        score = self.smallfont.render(str(player.score),  True, (255,200, 14))
        mana = self.smallfont.render(str(player.power),  True, (255,200, 14))
        name = self.smallfont.render(player.name,True,(255,200,14))
        self.screen.blit(score,pos + (215,95))
        self.screen.blit(mana,pos + (335,95))
        self.screen.blit(name,pos + (285,20))
                         
    def render_player_charcter(self, index):
        player = self.evManager.players[index]
        if pg.time.get_ticks() % (FramePerSec*3) == biasrand[index]:
            bias[index] = ( bias[index] + 1 ) % 2
        bias = (2,2) if self.player_bias[index] else (-2,-2)
        position = map(sum, zip(player.position, bias))
        # body
        if player.isVisible == False:
            direction = player.direction
            self.blit_at_center(self.player_invisible_images[index][direction], position)
        elif player.is_freeze == 1:
            self.blit_at_center(self.player_freeze_images[index], position)
        else:
            direction = player.direction
            self.blit_at_center(self.player_images[index][direction], position)
        # mode
        self.blit_at_center(self.mode_images[player.mode], position)
        # ball
        ball = player.takeball
        if ball != -1:
            self.blit_at_center(self.take_ball_images[ball])

        # mask
        if player.isMask == True:
            self.blit_at_center(self.mask_images[pg.time.get_ticks() % 12], position)

    def render_quaffle(self, index):
        quaffle = self.evManager.quaffles[index]
        if quaffle.state != 1:
            if quaffle.isStrengthened == True:
                self.blit_at_center(self.ball_powered_images[index], quaffle.position)
            else:
                self.blit_at_center(self.ball_normal_images[index], quaffle.position)

    def render_barrier(self,barrier):
        self.blit_at_center(self.barrier_images[barrier.playerIndex][barrier.direction], barrier.position)
        
    def blit_at_center(self, surface, position):
        (Xsize, Ysize) = surface.get_size()
        self.screen.blit(surface, (position[0]-Xsize/2, position[1]-Ysize/2))


