
import sys
import numpy as np

class ModelData() :
  def __init__( self, inputFile = None ) :
    self.m_Vertices = []
    self.m_Faces    = []
    self.m_Window   = []
    self.m_Viewport = []
    self.m_Patches  = []
    self.trans=[]
    self.xmin=float('inf')
    self.xmax=float('-inf')
    self.ymin=float('inf')
    self.ymax=float('-inf')
    self.zmin=float('inf')
    self.zmax=float('-inf')
    self.pd=0
    self.sx=0
    self.sy=0
    self.ax=0
    self.ay=0
    self.r00=0
    self.r01=0
    self.r02=0
    self.r10=0
    self.r11=0
    self.r12=0
    self.r20=0
    self.r21=0
    self.r22=0
    self.ex=0
    self.ey=0
    self.ez=0
    self.xp=0
    self.yp=0
    self.zp=0

    if inputFile is not None :
      self.loadFile( inputFile )

  def loadFile( self, inputFile ) :
    count=0
    scount=0
    with open(inputFile, 'r') as fp:
      lines= fp.read().replace('\r','').split('\n')
      

    for(index,line) in enumerate(lines,start=1):
      line=line.strip()
      
      if not line.startswith("#"):
        if line.startswith('f'):
          line=line.replace("f",'')
          inval=[]
          
          try:
            for x in line.split():
              inval.append(int(x)-1)
            if(len(inval)>3):
              print("Line",index,"is a malformed face spec")
            else:
              self.m_Faces.append(tuple(inval))
          except:
            print("Line",index,"is a malformed face spec")
        if line.startswith('p'):
          line=line.replace("p",'')
          valp=[]
          try:
            for xy in line.split():
              valp.append(int(xy)-1)
            if(len(valp)>16):
              print("Line",index,"is a malformed patch spec")
            else:
              self.m_Patches.append(tuple(valp))
          except:
            print("Line",index,"is a malformed patch spec")

            
        if line.startswith('v'):
          line=line.replace("v",'')
          valv=[]
          try:
            for y in line.split():
              valv.append(float(y))
            if(len(valv)>3):
              print("Line",index,"is a malformed vertex spec")
            else:
              self.m_Vertices.append(tuple(valv))
              if(valv[0]<self.xmin):
                self.xmin=valv[0]
              if(valv[0]>self.xmax):
                self.xmax=valv[0]
              if(valv[1]<self.ymin):
                self.ymin=valv[1]
              if(valv[1]>self.ymax):
                self.ymax=valv[1]
              if(valv[2]<self.zmin):
                self.zmin=valv[2]
              if(valv[2]>self.zmax):
                self.zmax=valv[2]
          except:
            print("Line",index,"is a malformed vertex spec")

        if line.startswith('w'):
          line=line.replace("w",'')
          valw=[]
          
          try:
            for z in line.split():
              valw.append(float(z))
            if(len(valw)>4):
              print("Line",index,"is a malformed window spec")
            elif count==1:
              print("Line",index,"is a duplicate window spec")
              self.m_Window=list(self.m_Window)
              self.m_Window.pop()
              tuplew=tuple(valw)
              self.m_Window=tuplew
                
            else:
              count=1
              tuplew=tuple(valw)
              self.m_Window=tuplew
          except:
            print("Line",index,"is a malformed window spec")
        if line.startswith('s'):
          line=line.replace("s",'')
          vals=[]
          try:
            for xz in line.split():
              vals.append(float(xz))
            if(len(vals)>4):
              print("Line",index,"is a malformed viewport spec")
            elif scount==1:
              print("Line",index,"is a duplicate viewport spec")
              self.m_Viewport=list(self.m_Viewport)
              self.m_Viewport.pop()
              tuples=tuple(vals)
              self.m_Viewport=tuples
                
            else:
              scount=1
              tuples=tuple(vals)
              self.m_Viewport=tuples
          except:
            print("Line",index,"is a malformed viewport spec")
        



  def getBoundingBox( self ) :
    return (self.xmin,self.xmax,self.ymin,self.ymax,self.zmin,self.zmax)


  def specifyTransform( self, ax, ay, sx, sy, pd ) :
    len1=self.m_Vertices
    trans1=[]
    trans2=[]
    trans3=[]
    self.pd=pd
    self.sx=sx
    self.sy=sy
    self.ax=ax
    self.ay=ay


  def specifyEulerAngles(self,phi,theta,psi):

    xmi,xma,ymi,yma,zmi,zma=self.getBoundingBox()
    tx=(xmi+xma)/2.0
    ty=(ymi+yma)/2.0
    tz=(zmi+zma)/2.0
    phi=phi*np.pi/180.0
    theta=theta*np.pi/180.0
    psi=psi*np.pi/180.0
    
    cosPhi,   sinPhi   = np.cos( phi ),   np.sin( phi )
    cosTheta, sinTheta = np.cos( theta ), np.sin( theta )
    cosPsi,   sinPsi   = np.cos( psi ),   np.sin( psi )

    cPhiXcPsi = cosPhi*cosPsi
    cPhiXsPsi = cosPhi*sinPsi
    sPhiXcPsi = sinPhi*cosPsi
    sPhiXsPsi = sinPhi*sinPsi

    self.r00 = cosPsi * cosTheta
    self.r01 = -cosTheta * sinPsi
    self.r02 = sinTheta

    self.r10 = cPhiXsPsi + sPhiXcPsi*sinTheta
    self.r11 = cPhiXcPsi - sPhiXsPsi*sinTheta
    self.r12 = -cosTheta*sinPhi

    self.r20 = -cPhiXcPsi*sinTheta + sPhiXsPsi
    self.r21 = cPhiXsPsi*sinTheta + sPhiXcPsi
    self.r22 = cosPhi*cosTheta
    
    self.ex  = -self.r00*tx - self.r01*ty - self.r02*tz + tx
    self.ey  = -self.r10*tx - self.r11*ty - self.r12*tz + ty
    self.ez  = -self.r20*tx - self.r21*ty - self.r22*tz + tz
    

    

  def getTransformedVertex( self, vNum, dopersp,doeuler) :
    vertex=self.m_Vertices[vNum]
    transformedvertex=[]
    xcomp=vertex[0]
    ycomp=vertex[1]
    zcomp=vertex[2]
    xval=0.0
    yval=0.0
    if(doeuler):
      xp  = self.r00*xcomp + self.r01*ycomp + self.r02*zcomp + self.ex
      yp  = self.r10*xcomp + self.r11*ycomp + self.r12*zcomp + self.ey
      zp  = self.r20*xcomp + self.r21*ycomp + self.r22*zcomp + self.ez
      xcomp,ycomp,zcomp=xp,yp,zp

    if(dopersp):
        xval=(self.sx *(xcomp/(1-(zcomp/self.pd))))+self.ax
        yval=(self.sy *(ycomp/(1-(zcomp/self.pd))))+self.ay
        
    
    else:
      xval=self.ax+(self.sx*xcomp)
      yval=self.ay+(self.sy*ycomp)
    zval=0.0
      
    return ((xval,yval,zval))

  def TransformXYZ(self,x,y,z,dopersp,doeuler):
    xval=0.0
    yval=0.0
    if(doeuler):
      xp  = self.r00*x + self.r01*y + self.r02*z + self.ex
      yp  = self.r10*x + self.r11*y + self.r12*z + self.ey
      zp  = self.r20*x + self.r21*y + self.r22*z + self.ez
      x,y,z=xp,yp,zp

    if(dopersp):
        xval=(self.sx *(x/(1-(z/self.pd))))+self.ax
        yval=(self.sy *(y/(1-(z/self.pd))))+self.ay
        
    
    else:
      xval=self.ax+(self.sx*x)
      yval=self.ay+(self.sy*y)
    zval=0.0
    return ((xval,yval,zval))

  def getFaces( self )    : return self.m_Faces
  def getVertices( self ) : return self.m_Vertices
  def getViewport( self ) : return self.m_Viewport
  def getWindow( self )   : return self.m_Window
  def getPatches( self )  : return self.m_Patches

def constructTransform( w, v, width, height ) :
  wxmin=w[0]
  wymin=w[1]
  wxmax=w[2]
  wymax=w[3]
  vxmin=v[0]
  vymin=v[1]
  vxmax=v[2]
  vymax=v[3]
  fa = wxmin
  fx=-fa
  fb = wymin
  fy=-fb
  gx=width*vxmin
  gy=height*vymin
  sx= width*(vxmax-vxmin)/(wxmax-wxmin)
  sy=height*(vymax-vymin)/(wymax-wymin)
  ax=(fx*sx)+gx
  ay=(fy*sy)+gy
  return(ax,ay,sx,sy)

def _main() :
  fName  = sys.argv[1]
  width  = int( sys.argv[2] )
  height = int( sys.argv[3] )

  model = ModelData( fName )

  print( "%s: %d vert%s, %d face%s" % (
    fName,
    len( model.getVertices() ), 'ex' if len( model.getVertices() ) == 1 else 'ices',
    len( model.getFaces() ), '' if len( model.getFaces() ) == 1 else 's' ))

  print( 'First 3 vertices:' )
  for v in model.getVertices()[0:3] :
    print( '     ', v )

  print( 'First 3 faces:' )
  for f in model.getFaces()[0:3] :
    print( '     ', f )

  w = model.getWindow()
  v = model.getViewport()
  print( 'Window line:', w )
  print( 'Viewport line:', v )
  print( 'Canvas size:', width, height )

  print( 'Bounding box:', model.getBoundingBox() )

  ( ax, ay, sx, sy ) = constructTransform( w, v, width, height )
  print( f'Transform is {ax} {ay} {sx} {sy}' )

  model.specifyTransform( ax, ay, sx, sy )

  print( 'First 3 transformed vertices:' )
  for vNum in range( 3 ) :
    print( '     ', model.getTransformedVertex( vNum ) )


if __name__ == '__main__' :
  _main()

