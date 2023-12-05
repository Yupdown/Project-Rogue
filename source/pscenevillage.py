from psceneworld import *
from picowork.picowork import *
from picowork.pspriteobject import *
from picowork.pscrollpattern import *
from picowork.pfixedbackground import *
from picowork.ptextuiobject import *
from tilemapgeneration import *
from tilemap import *
from portal import *
from coin import *
from monster import *
import globalvariables


class PSceneVillage(PSceneWorld):
    def __init__(self):
        super().__init__()
        self.player = None

        background_sky = PFixedBackground('skybox.png')
        self.add_element(background_sky)

        background = PScrollPattern('bg16_cloud_far.png', 3)
        background.set_position(Vector2(0, 12))
        self.add_element(background)

        background = PScrollPattern('bg_near.png', 2)
        background.set_position(Vector2(0, 10.5))
        self.add_element(background)

        gate = PSpriteObject('gate_parts.png')
        gate.set_position(Vector2(14.5, 10))
        self.add_element(gate)

        gate = PSpriteObject('gate_parts.png')
        gate.set_scale(Vector2(-1, 1))
        gate.set_position(Vector2(17.5, 10))
        self.add_element(gate)

        wagon = PSpriteObject('wagon.png')
        wagon.set_position(Vector2(12, 9.5))
        self.add_element(wagon)

        character = PSpriteObject("merchant_01.png")
        character.set_position(Vector2(19, 9.3))
        character.set_scale(Vector2(-1, 1))
        self.add_element(character)

        self.tilemap = Tilemap(32, 32, 'terr01_%02d.png', ['fill01b.png', 'fill01.png'])
        generate_tilemap_village(self.tilemap, 32, 32)
        self.add_element(self.tilemap)

        import scenemanagement
        self.portal = Portal(self.tilemap, scenemanagement.load_scene_dungeon)
        self.portal.set_position(Vector2(16, 9.5))
        self.add_world_object(self.portal)

        self.ui_main_menu = None
        if not globalvariables.SHOW_MAIN_MENU:
            self.start_game()
            camera._position = Vector2(8, 9)
        else:
            camera._position = Vector2(16, 18)

        if globalvariables.SHOW_MAIN_MENU:
            self.ui_main_menu = InterfaceMainMenu()
            self.add_element(self.ui_main_menu, 5)
            globalvariables.SHOW_MAIN_MENU = False

    def update(self, delta_time):
        super().update(delta_time)

        new_campos = lerp(camera._position, Vector2(16, 9) if self.player is None else self.player.get_position(), delta_time * 6)
        hsw = camera._size * get_canvas_width() / get_canvas_height()
        new_campos = Vector2(clamp(hsw, new_campos.x, 32 - hsw), new_campos.y)
        magnitude = clamp(-0.5, (new_campos - camera._position).x * 50, 0.5)

        camera._position = new_campos
        camera._rotation = magnitude
        camera._size = 4 # + 4 * (t % 1) ** 0.05

        if self.ui_main_menu is not None:
            self.ui_main_menu.update(delta_time)

    def start_game(self):
        if self.ui_main_menu is not None:
            self.remove_element(self.ui_main_menu)
            self.ui_main_menu = None
        self.player = Player(self.tilemap)
        self.player.set_position(Vector2(8, 9))
        self.add_world_object(self.player, 2)


class InterfaceMainMenu(PObject):
    panel_sprite = None
    outfits = [
        'avatar_body0000.png',
        'avatar_body0001.png',
        'avatar_body0002.png',
        'avatar_body0003.png',
        'avatar_body0004.png',
        'avatar_body0005.png',
        'avatar_body0006.png',
        'avatar_body0007.png',
        'avatar_body0008.png',
        'avatar_body0009.png',
        'avatar_body0010.png',
        'avatar_body0011.png',
        'avatar_body0012.png',
        'avatar_body0013.png',
        'avatar_body0014.png',
        'avatar_body0015.png',
        'avatar_body0016.png',
        'avatar_body0017.png',
        'avatar_body0018.png',
        'avatar_body0019.png',
        'avatar_body0020.png',
        'avatar_body0021.png',
        'avatar_body0022.png',
        'avatar_body0023.png',
        'avatar_body0024.png',
        'trader.png',
        'kobold01.png',
        'werewolf01.png',
        'undead01.png',
        'scarecraw01.png'
    ]
    def __init__(self):
        super().__init__()
        if InterfaceMainMenu.panel_sprite is None:
            InterfaceMainMenu.panel_sprite = get_image('splash_solid.png')
        self.time = 0
        self.figure = PlayerFigure()
        self.add_element(self.figure)
        self.buttons = [
            ('Start Game', self.start_game),
            ('Change Outfit', self.change_outfit),
            ('Quit Game', quit_application)
        ]
        self.ui_buttons = []
        for index in range(len(self.buttons)):
            obj = PTextUIObject(self.buttons[index][0])
            obj.set_position(Vector2(72, 90 * (len(self.buttons) - index)))
            self.add_element(obj)
            self.ui_buttons.append(obj)

        self.ui_title = PTextUIObject('Project-Rogue')
        self.ui_title.set_position(Vector2(72, get_canvas_height() - 100))
        self.add_element(self.ui_title)

        self.index = 0
        self.select_index(self.index)

        self.index_outfit = 5
        globalvariables.CHARACTER_OUTFIT = InterfaceMainMenu.outfits[self.index_outfit]
        self.figure.change_outfit(InterfaceMainMenu.outfits[self.index_outfit])

    def select_index(self, new_index):
        button = self.ui_buttons[self.index]
        button.set_position(Vector2(72, button.get_position().y))

        self.index = new_index

        for index in range(len(self.buttons)):
            self.ui_buttons[index].set_text(('> ' if index == new_index else '') + self.buttons[index][0])

    def start_game(self):
        self.get_parent().start_game()

    def change_outfit(self):
        self.index_outfit = (self.index_outfit + 1) % len(InterfaceMainMenu.outfits)
        outfit = InterfaceMainMenu.outfits[self.index_outfit]
        globalvariables.CHARACTER_OUTFIT = outfit
        self.figure.change_outfit(outfit)

    def update(self, delta_time):
        self.time += delta_time

        if get_keydown(SDLK_s) or get_keydown(SDLK_DOWN):
            self.select_index((self.index + 1) % len(self.buttons))
        if get_keydown(SDLK_w) or get_keydown(SDLK_UP):
            self.select_index((self.index + len(self.buttons) - 1) % len(self.buttons))
        if get_keydown(SDLK_SPACE) or get_keydown(SDLK_RETURN):
            self.buttons[self.index][1]()

        button = self.ui_buttons[self.index]
        button.set_position(Vector2(72 + abs(sin(self.time * 4)) * 8, button.get_position().y))

        self.figure.update(delta_time)

    def on_draw(self):
        InterfaceMainMenu.panel_sprite.opacify(0.5)
        InterfaceMainMenu.panel_sprite.draw_to_origin(0, 0, get_canvas_width(), get_canvas_height())
        InterfaceMainMenu.panel_sprite.opacify(1)


class PlayerFigure(PObject):
    def __init__(self):
        super().__init__()
        self.renderer = None
        self.animator = AvatarAnimator()
        self.time = 0
        self.animator.set_state(AnimationIdle)

    def update(self, delta_time):
        self.set_position(camera._position + Vector2(5.2, -3))
        self.set_scale(Vector2(1, 1) * (10 / camera._size))
        self.time += delta_time
        if self.renderer is not None:
            self.animator.update(self, delta_time)

    def change_outfit(self, new_outfit):
        self.remove_element(self.renderer)
        self.renderer = Avatar(get_image(new_outfit))
        self.add_element(self.renderer)

        sobj_weapon = PSpriteObject(PSprite('weapons01.png', 89, 139, 17, 7))
        sobj_weapon.set_position(Vector2(-7 / PIXEL_PER_UNIT, 0))
        self.renderer.sobj_arm_bl.add_element(sobj_weapon)