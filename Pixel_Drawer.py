#!/usr/bin/env python

#INCLUDES
import pygame
import Tkinter
import tkFileDialog
import tkColorChooser

pygame.init() #start game engine

#GLOBAL VARS
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RGB = (0,0,0)

#INITIAL - VARS
PJ = []
initial_PJ = (15,24)
PJ_width = 15
PJ_height = 24
for row in range(PJ_height):
	r = []
	for column in range(PJ_width):
		r.append(WHITE)
	PJ.append(r)

font_size = 20
font = pygame.font.Font(None, font_size)
font2 = pygame.font.Font(None, 15)
pixel_size = 10
grid_color = RED
pointer_color = BLUE

#MAIN - WINDOW MANAGER
MARGIN = 150
screen = pygame.display.set_mode((pixel_size*PJ_width+MARGIN,pixel_size*PJ_height))
pygame.display.set_caption("Pixel Drawer by Razorbreak")
clock = pygame.time.Clock()
FPS = 60 # Frames Por Segundo
screen.fill(WHITE)

#File Dialog Options
#file_opt = options = {}
#options['defaultextension'] = '.pix' # couldn't figure out how this works
#options['filetypes'] = [('Pixel Art files', '.pix')]
#options['initialdir'] = 'C:\\'
#options['initialfile'] = 'my_project.pix'
#options['parent'] = root
#options['title'] = 'This is a title'

#Hide Tkinter Manager
root = Tkinter.Tk()
root.withdraw()



#CLASSES & FUNCTIONS
#-------------------
def print_mouse_position():
	#Muestra en pantalla la posicion del raton
	pos = pygame.mouse.get_pos()
	text = font.render(str((pos[0]//pixel_size+1,pos[1]//pixel_size+1)),True,BLACK)
	x = pos[0]
	y = pos[1]
	pygame.draw.line(screen,pointer_color,(x-2,y),(x-4,y),1)
	pygame.draw.line(screen,pointer_color,(x+2,y),(x+4,y),1)
	pygame.draw.line(screen,pointer_color,(x,y-2),(x,y-4),1)
	pygame.draw.line(screen,pointer_color,(x,y+2),(x,y+4),1)
	if x < PJ_width*pixel_size:
		if y < 10: y += 8
		if x > PJ_width*pixel_size-len(str(pos))*pixel_size/1.3: x -= len(str(pos))*pixel_size/1.3
		if y > PJ_height*pixel_size-10: y -= 8
		screen.blit(text,(x+8,y-8))
#-----------------------
def draw_Limits():
	pygame.draw.line(screen,BLACK,(pixel_size*PJ_width,0),(pixel_size*PJ_width,pixel_size*PJ_height),1)
	pygame.draw.line(screen,BLACK,(pixel_size*PJ_width+2,0),(pixel_size*PJ_width+2,pixel_size*PJ_height),1)
#-----------------------
def draw_Matrix():
	#Carga en pantalla la matriz de dibujado
	for j in range(PJ_height):
		for i in range(PJ_width):
			pygame.draw.rect(screen,PJ[j][i],(i*pixel_size,j*pixel_size,pixel_size,pixel_size))
			if grid: pygame.draw.rect(screen,grid_color,(i*pixel_size,j*pixel_size,pixel_size,pixel_size),1)
#-----------------------
def reset_Matrix():
	global PJ,PJ_width,PJ_height
	PJ = []
	PJ_width = initial_PJ[0]
	PJ_height = initial_PJ[1]
	for row in range(PJ_height):
		r = []
		for column in range(PJ_width):
			r.append(WHITE)
		PJ.append(r)
	reload_window()
#-----------------------
def expand_Matrix(option):
	global PJ_width,PJ_height,PJ
	if option == 8 and PJ_height > 1: 
		PJ_height -= 1
	if option == 4 and PJ_width > 1: 
		PJ_width -= 1
	if option == 6: 
		PJ_width += 1
		for j in range(PJ_height): PJ[j].append(WHITE)
	if option == 2: 
		PJ_height += 1
		r = []
		for i in range(PJ_width): r.append(WHITE)
		PJ.append(r)
	reload_window()
	draw_Matrix()
#-----------------------
def choose_color():
	global RGB
	(RGB,color) = tkColorChooser.askcolor(initialcolor=RGB)
	if RGB == None: RGB = BLACK
#-----------------------
def load_file():
	#Lee un fichero y lo decodifica en pantalla
	global PJ
	global PJ_width
	global PJ_height
	filename = tkFileDialog.askopenfilename(defaultextension='.pix',filetypes=[('Pixel Art files','.pix')])
	if filename != "":
		print "Cargando fichero:",filename
		f = open(filename,'r')
		PJ = f.read()
		f.close()
		PJ = PJ.split('\n')
		PJ_height = len(PJ)
		for j in range(PJ_height): #Primero se almacena el fichero en PJ y se particiona
			PJ[j] = PJ[j].split(':')
			for i in range(len(PJ[j])): #Luego se convierten los tipos
				PJ[j][i] = eval(PJ[j][i])
		PJ_width = len(PJ[0])
		reload_window()
#-----------------------
def save_file():
	#Codifica en un fichero el contenido de la pantalla
	filename = tkFileDialog.asksaveasfilename(defaultextension='.pix',filetypes=[('Pixel Art files','.pix')],initialfile='new_project.pix')
	if filename != "":
		print "Guardando fichero:",filename
		f = open(filename,'w')
		for j in range(PJ_height):
			for i in range(PJ_width):
				f.write(str(PJ[j][i]))
				if(i<PJ_width-1): f.write(':')
			if(j<PJ_height-1): f.write('\n')
		f.close()
#-----------------------
def reload_window():
	#Modifica el aspecto de la pantalla
	global screen
	screen = pygame.display.set_mode((pixel_size*PJ_width+MARGIN,pixel_size*PJ_height))
	pygame.display.set_caption("Pixel Drawer by Razorbreak")
	screen.fill(WHITE)
	draw_Limits()
	show_bar()
#-----------------------
def show_bar():
	x = PJ_width*pixel_size
	y = PJ_height*pixel_size
	pygame.draw.rect(screen,WHITE,(x+5,0,x+MARGIN,y))
	screen.blit(font.render("Colour:",True,BLACK),(x+10,10))
	pygame.draw.rect(screen,RGB,(x+70,10,30,15))
	pygame.draw.rect(screen,BLACK,(x+70,10,30,15),1)
	screen.blit(font2.render("C: Pick Color",True,BLACK),(x+10,40))
	screen.blit(font2.render("A: Open File",True,BLACK),(x+10,55))
	screen.blit(font2.render("S: Save File",True,BLACK),(x+10,70))
	screen.blit(font2.render("G: Grid",True,BLACK),(x+10,85))
	screen.blit(font2.render("P: Pointer",True,BLACK),(x+10,100))
	screen.blit(font2.render("L Mouse: Draw",True,BLACK),(x+10,115))
	screen.blit(font2.render("R Mouse: Change B&W",True,BLACK),(x+10,130))
	screen.blit(font2.render("C Mouse: Change RGB",True,BLACK),(x+10,145))
	screen.blit(font2.render("Re Pag: Zoom +",True,BLACK),(x+10,160))
	screen.blit(font2.render("Av Pag: Zoom -",True,BLACK),(x+10,175))
	screen.blit(font2.render("N: New Project",True,BLACK),(x+10,190))
	screen.blit(font2.render("E: Extend draw zone",True,BLACK),(x+10,205))
	screen.blit(font2.render("R: Retract draw zone",True,BLACK),(x+10,220))
#-----------------------

	
#-MAIN
draw_Limits()
show_bar()
exit = False
pointer = False
grid = False
color = [BLACK,WHITE,RED,GREEN,BLUE]
color_index = 0
while not exit:
	#FETCH EVENTS
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit = True #Finish
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			mouse_button = pygame.mouse.get_pressed()
			if mouse_button == (True,False,False):
				#print("L_Mouse")
				if pos[0] < PJ_width*pixel_size:
					if not pointer:
						PJ[pos[1]//pixel_size][pos[0]//pixel_size] = RGB
						draw_Matrix()
			elif mouse_button == (False,False,True): #Cambia entre B y W
				#print("R_Mouse")
				if color[color_index] == BLACK:
					color_index = 1
					RGB = color[color_index]
				else:
					color_index = 0
					RGB = color[color_index]
				print "Color cambiado a:",RGB
				show_bar()
			elif mouse_button == (False,True,False): #Cambia colores RGB
				#print("C_Mouse")
				if 1 < color_index < 4:
					color_index = ((color_index + 1) % (len(color)))
					RGB = color[color_index]
				else:
					color_index = 2
					RGB = color[color_index]
				print "Color cambiado a:",RGB
				show_bar()
		if event.type == pygame.KEYDOWN:
			#print "Keyboard:",event.key #Debug - Keyboard codes
			if event.key == pygame.K_a: #Press A
				load_file()
				draw_Matrix()
			elif event.key == pygame.K_s: #Press S
				save_file()
			elif event.key == pygame.K_g: #Press G
				if grid: 
					print "Rejilla desactivada"
					grid = False
					draw_Matrix()
				else: 
					print "Rejilla activada"
					grid = True
					draw_Matrix()
			elif event.key == pygame.K_p: #Press P
				if pointer:
					print "Puntero desactivado"
					pygame.mouse.set_visible(True)
					pointer = False
					draw_Matrix()
					show_bar()
				else:
					print "Puntero activado"
					pygame.mouse.set_visible(False)
					pointer = True
			elif event.key == pygame.K_PAGEUP: #Press Re Pag
				if pixel_size < 20: 
					pixel_size += 1
					print "Aumentando zoom a ",pixel_size," pixels"
					reload_window()
					draw_Matrix()
			elif event.key == pygame.K_PAGEDOWN: #Press Av Pag
				if pixel_size > 2: 
					pixel_size -= 1
					print "Disminuyendo zoom a ",pixel_size," pixels"
					reload_window()
					draw_Matrix()
			elif event.key == pygame.K_c: #Press C
				choose_color()
				print "Color personalizado:",RGB
				show_bar()
			elif event.key == pygame.K_n: #Press N
				print "Nuevo proyecto"
				reset_Matrix()
			elif event.key == pygame.K_e: #Press E
				print "Extendiendo lienzo"
				expand_Matrix(6)
				expand_Matrix(2)
			elif event.key == pygame.K_r: #Press R
				print "Recortando lienzo"
				expand_Matrix(4)
				expand_Matrix(8)
			elif event.key == pygame.K_KP2: #Press 2
				print "Extendiendo lienzo"
				expand_Matrix(2)
			elif event.key == pygame.K_KP4: #Press 4
				print "Recortando lienzo"
				expand_Matrix(4)
			elif event.key == pygame.K_KP6: #Press 6
				print "Extendiendo lienzo"
				expand_Matrix(6)
			elif event.key == pygame.K_KP8: #Press 8
				print "Recortando lienzo"
				expand_Matrix(8)
	#RENDERING SCREEN
	if not exit:
		# Dibujado en pantalla
		if pointer:
			screen.fill(WHITE)
			draw_Limits()
			print_mouse_position()
		# Fin dibujado
		clock.tick(FPS)
		pygame.display.flip()

pygame.quit() #Close game engine

#--------------------------
#--Created by Razorbreak---
#--------------------------
#--------------------------
