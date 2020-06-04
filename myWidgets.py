
import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog

import math
import ModelData
from ModelData import constructTransform

class cl_widgets :
  def __init__( self, ob_root_window, ob_world = [] ) :
    self.ob_root_window = ob_root_window
    self.ob_world = ob_world
    self.m_clip=tk.BooleanVar()
    self.m_clip.set(True)
    self.persp=tk.BooleanVar()
    self.persp.set(False)
    self.euler=tk.BooleanVar()
    self.euler.set(False)


    self.menu = cl_menu( self )
    self.model=ModelData.ModelData()
    


    self.toolbar = cl_toolbar( self )
    

    self.statusBar_frame = cl_statusBar_frame( self.ob_root_window )
    self.statusBar_frame.pack( side = tk.BOTTOM, fill = tk.X )
    self.statusBar_frame.set( 'This is the status bar' )

    self.ob_canvas_frame = cl_canvas_frame( self )
    self.ob_world.add_canvas( self.ob_canvas_frame.canvas )

class cl_canvas_frame :
  def __init__( self, master ) :
    self.master = master
    self.canvas = tk.Canvas(
      master.ob_root_window, width=1, height=1, bg='#ffcc66' )

    self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
    self.canvas.bind( '<Configure>',       self.canvas_resized_callback )
    self.canvas.bind( '<ButtonPress-1>',   self.left_mouse_click_callback )
    self.canvas.bind( '<ButtonRelease-1>', self.left_mouse_release_callback )
    self.canvas.bind( '<B1-Motion>',       self.left_mouse_down_motion_callback )
    self.canvas.bind( '<ButtonPress-2>',   self.middle_mouse_click_callback )
    self.canvas.bind( '<ButtonRelease-2>', self.middle_mouse_release_callback )
    self.canvas.bind( '<B2-Motion>',       self.middle_mouse_down_motion_callback )
    self.canvas.bind( '<ButtonPress-3>',   self.right_mouse_click_callback )
    self.canvas.bind( '<ButtonRelease-3>', self.right_mouse_release_callback )
    self.canvas.bind( '<B3-Motion>',       self.right_mouse_down_motion_callback )
    self.canvas.bind( '<Key>',             self.key_pressed_callback )
    self.canvas.bind( '<Up>',              self.up_arrow_pressed_callback )
    self.canvas.bind( '<Down>',            self.down_arrow_pressed_callback )
    self.canvas.bind( '<Right>',           self.right_arrow_pressed_callback )
    self.canvas.bind( '<Left>',            self.left_arrow_pressed_callback )
    self.canvas.bind( '<Shift-Up>',        self.shift_up_arrow_pressed_callback )
    self.canvas.bind( '<Shift-Down>',      self.shift_down_arrow_pressed_callback )
    self.canvas.bind( '<Shift-Right>',     self.shift_right_arrow_pressed_callback )
    self.canvas.bind( '<Shift-Left>',      self.shift_left_arrow_pressed_callback )

  def key_pressed_callback( self, event ) :
    msg = f'{event.char!r} ({ord( event.char )})' \
      if len( event.char ) > 0 else '<non-printing char>'

    self.master.statusBar_frame.set(
      f'{msg} pressed at ({event.x},{event.y})' )

  def up_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Up arrow pressed' )

  def down_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Down arrow pressed' )

  def right_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Right arrow pressed' )

  def left_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Left arrow pressed' )

  def shift_up_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Shift up arrow pressed' )

  def shift_down_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Shift down arrow pressed' )

  def shift_right_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Shift right arrow pressed' )

  def shift_left_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Shift left arrow pressed' )

  def left_mouse_click_callback( self, event ) :
    self.master.statusBar_frame.set( f'LMB down. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y
    self.canvas.focus_set()

  def left_mouse_release_callback( self, event ) :
    self.master.statusBar_frame.set( f'LMB released. ({event.x}, {event.y})' )
    self.x = None
    self.y = None

  def left_mouse_down_motion_callback( self, event ) :
    self.master.statusBar_frame.set( f'LMB dragged. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y

  def middle_mouse_click_callback( self, event ) :
    self.master.statusBar_frame.set( f'MMB down. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y
    self.canvas.focus_set()

  def middle_mouse_release_callback( self, event ) :
    self.master.statusBar_frame.set( f'MMB released. ({event.x}, {event.y})' )
    self.x = None
    self.y = None

  def middle_mouse_down_motion_callback( self, event ) :
    self.master.statusBar_frame.set( f'MMB dragged. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y

  def right_mouse_click_callback( self, event ) :
    self.master.statusBar_frame.set( f'RMB down. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y

  def right_mouse_release_callback( self, event ) :
    self.master.statusBar_frame.set( f'RMB released. ({event.x}, {event.y})' )
    self.x = None
    self.y = None

  def right_mouse_down_motion_callback( self, event ) :
    self.master.statusBar_frame.set( f'RMB dragged. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y

  def canvas_resized_callback( self, event ) :
    self.canvas.config( width = event.width-4, height = event.height-4 )

    self.master.statusBar_frame.pack( side = tk.BOTTOM, fill = tk.X )
    self.master.statusBar_frame.set(
      f'Canvas width, height ({self.canvas.cget( "width" )}, ' +
      f'{self.canvas.cget( "height" )})' )

    self.canvas.pack()

    self.master.ob_world.redisplay( self.master.ob_canvas_frame.canvas, event )

class cl_statusBar_frame( tk.Frame ) :
  def __init__( self, master ) :
    tk.Frame.__init__( self, master )
    self.label = tk.Label( self, bd = 1, relief = tk.SUNKEN, anchor = tk.W )
    self.label.pack( fill = tk.X )

  def set( self, formatStr, *args ) :
    self.label.config( text ="sxs0847: "+ formatStr % args )
    self.label.update_idletasks()

  def clear( self ) :
    self.label.config( text='' )
    self.label.update_idletasks()

class cl_menu :
  def __init__( self, master ) :
    self.master = master
    self.menu = tk.Menu( master.ob_root_window )
    master.ob_root_window.config( menu = self.menu )

    self.filemenu = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'File', menu = self.filemenu )
    self.filemenu.add_command( label = 'New', command = lambda : self.menu_callback( 'file>new' ) )
    self.filemenu.add_command( label = 'Open...', command = lambda : self.menu_callback( 'file>open' ) )
    self.filemenu.add_separator()
    self.filemenu.add_command( label = 'Exit', command = lambda : self.menu_callback( 'file>exit' ) )

    self.dummymenu = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'Settings', menu = self.dummymenu )
    self.dummymenu.add_checkbutton( label = 'Clipping',onvalue=1, offvalue=False, variable=self.master.m_clip ,command = lambda : self.menu_callback( 'settings>clipping' ) )
    self.dummymenu.add_checkbutton( label = 'Perspective',onvalue=1, offvalue=False, variable=self.master.persp, command = lambda : self.menu_callback( 'settings>Perspective' ) )
    self.dummymenu.add_checkbutton( label = 'Euler',onvalue=1, offvalue=False, variable=self.master.euler, command = lambda : self.menu_callback( 'settings>Euler' ) )


    self.helpmenu = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'Help', menu = self.helpmenu )
    self.helpmenu.add_command( label = 'About...', command = lambda : self.menu_callback( 'help>about' ) )

  def menu_callback( self, which = None ) :
    item = 'menu' if which is None else which
    self.master.statusBar_frame.set( f'{item!r} callback' )

#----------------------------------------------------------------------
class cl_toolbar :
  def __init__( self, master ) :
    self.master = master
    self.toolbar = tk.Frame( master.ob_root_window )
    self.button = tk.Button( self.toolbar, text = 'Resolution', width = 8, command = self.toolbar_resolution_callback)
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'Distance', width = 8, command = self.toolbar_perspective_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'ϕ', width = 2, command = self.toolbar_eulerphi_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'θ', width = 2, command = self.toolbar_eulertheta_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'ψ', width = 2, command = self.toolbar_eulerpsi_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'Reset', width = 8, command = self.toolbar_reset_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'Load', width = 8, command = self.toolbar_load_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'Draw', width = 8, command = self.toolbar_draw_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.toolbar.pack( side = tk.TOP, fill = tk.X )
    self.res=4
    self.pd=1.0
    self.phi=0.0
    self.theta=0.0
    self.psi=0.0

  def toolbar_reset_callback( self ) :
    self.master.ob_world.reset()
    self.master.statusBar_frame.set( 'Reset callback' )
  def toolbar_resolution_callback(self):
    self.master.statusBar_frame.set('Resolution callback')
    self.res=simpledialog.askinteger(title='Resolution', prompt='enter Resolution', minvalue=4, initialvalue=4)
    self.res=4 if self.res == None else self.res
    self.master.statusBar_frame.set('Resolution set to {0}'.format(self.res))
  def toolbar_perspective_callback(self):
  	self.master.statusBar_frame.set('Perspective callback')
  	self.pd=simpledialog.askfloat(title='Perspective', prompt='enter Distance', minvalue=1.0, initialvalue=1.0)
  	self.pd = 1.0 if self.pd == None else self.pd
  	self.master.statusBar_frame.set('Perspective distance set to {0}'.format(self.pd))

  def toolbar_eulerphi_callback(self):
    self.master.statusBar_frame.set('euler callback')
    self.phi=simpledialog.askfloat(title='Euler', prompt='enter phi angle', minvalue=-180, maxvalue=180, initialvalue=0.0)
    self.phi = 0.0 if self.phi == None else self.phi
    self.master.statusBar_frame.set('Phi Angle is set to {0}'.format(self.phi))

  def toolbar_eulertheta_callback(self):
    self.master.statusBar_frame.set('euler callback')
    self.theta=simpledialog.askfloat(title='Euler', prompt='enter theta angle', minvalue=-180, maxvalue=180, initialvalue=0.0)
    self.theta = 0.0 if self.theta == None else self.theta
    self.master.statusBar_frame.set('Theta Angle is set to {0}'.format(self.theta))

  def toolbar_eulerpsi_callback(self):
    self.master.statusBar_frame.set('euler callback')
    self.psi=simpledialog.askfloat(title='Euler', prompt='enter psi angle', minvalue=-180, maxvalue=180, initialvalue=0.0)
    self.psi = 0.0 if self.psi == None else self.psi
    self.master.statusBar_frame.set('Psi Angle is set to {0}'.format(self.psi))

  def toolbar_load_callback( self ) :
    self.master.statusBar_frame.set( 'Load callback' )
    self.master.model=ModelData.ModelData()
    fName=filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files","*"),("text files","*.txt")))
    if len(fName)==0:
      self.master.statusBar_frame.set('no file selected')
    else:
      self.master.model.loadFile(fName)
      self.master.statusBar_frame.set( 'File Loaded' )

  def toolbar_draw_callback( self ) :
    if self.master.model is None:
      self.master.statusBar_frame.set( 'File Not Loaded' )
    else:
      w = self.master.model.getWindow()
      v = self.master.model.getViewport()
      width= int(self.master.ob_canvas_frame.canvas.cget('width'))
      height= int(self.master.ob_canvas_frame.canvas.cget('height'))
      if(len(w)==0 or len(v)==0):
        self.master.statusBar_frame.set( 'File Not Loaded' )
      else:
        (ax,ay,sx,sy)=constructTransform(w,v,width,height)
        self.master.model.specifyTransform(ax,ay,sx,sy,self.pd)
        self.master.model.specifyEulerAngles(self.phi,self.theta,self.psi)
        self.master.ob_world.create_graphic_objects( self.master.ob_canvas_frame.canvas,self.master.model,self.master.m_clip.get()==1, self.master.persp.get()==1, self.master.euler.get()==1, self.res)
        self.master.statusBar_frame.set( 'Draw callback' )

