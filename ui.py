import sys
import sdl2.ext
import sdl2.sdlimage

sdl2.ext.init()

window = sdl2.ext.Window("Pengüin Chess", size=(1024, 1024))
window.show()
sdl2.sdlimage.IMG_Init(sdl2.sdlimage.IMG_INIT_PNG)
b_background_img = sdl2.ext.image.load_img("assets/square gray dark _png_shadow_128px.png")
w_background_img = sdl2.ext.image.load_img("assets/square gray light _png_shadow_128px.png")

factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
x = sdl2.ext.SoftwareSprite(b_background_img,size=(2,2))
spriterenderer = factory.create_sprite_render_system(window)
spriterenderer.render(x)
while True: pass