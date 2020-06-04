
import sys
_RECURSION_LIMIT = 3000

if ( sys.getrecursionlimit() < _RECURSION_LIMIT ) :
  print( f'System recursion limit was {sys.getrecursionlimit()}, setting to {_RECURSION_LIMIT}.' )
  sys.setrecursionlimit( _RECURSION_LIMIT )


import tkinter as tk
import myWidgets
import myGraphics

def onClosing() :
  if tk.messagebox.askokcancel( "Really Quit?", "Do you really wish to quit?" ) :
    tk.Tk().quit()

def main() :
  ob_root_window = tk.Tk()
  ob_root_window.protocol( "WM_DELETE_WINDOW", onClosing )

  ob_world = myGraphics.cl_world()

  myWidgets.cl_widgets( ob_root_window, ob_world )

  ob_root_window.mainloop()
  print( '... mainloop has exited.' )

if ( __name__ == "__main__" ) :
  main()

