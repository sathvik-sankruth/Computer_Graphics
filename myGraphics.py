
import CohenSutherland
import BézierPatch as bp
class cl_world :
  def __init__( self, objects = [], canvases = [] ) :
    self.objects = objects
    self.canvases = canvases

  def add_canvas( self, canvas ) :
    self.canvases.append( canvas )
    canvas.world = self

  def reset( self ) :
    self.objects = []
    for canvas in self.canvases :
      canvas.delete( 'all' )

  def create_graphic_objects( self, canvas, model,doclip, dopersp, doeuler, resolution ) :

    x1,y1,x2,y2=model.getViewport()
    width=int(canvas.cget('width'))
    height=int(canvas.cget('height'))
    self.objects.append( canvas.create_rectangle(
      x1*width, y1*height, x2*width, y2*height ) )
    tup=(x1*width, y1*height, x2*width, y2*height)
    vert=model.getVertices()
    patches=model.getPatches()
    face=model.getFaces()
    for f in face:
        v1=model.getTransformedVertex(f[0],dopersp,doeuler)
        v2=model.getTransformedVertex(f[1],dopersp,doeuler)
        v3=model.getTransformedVertex(f[2],dopersp,doeuler)
        if(doclip):
          dodraw,p1x,p1y,p2x,p2y=CohenSutherland.clipLine(v1[0],v1[1],v2[0],v2[1],tup)
          if(dodraw):
            self.objects.append(canvas.create_line(p1x,p1y,p2x,p2y))
          dodraw1,p1x,p1y,p2x,p2y=CohenSutherland.clipLine(v2[0],v2[1],v3[0],v3[1],tup)
          if(dodraw1):
            self.objects.append(canvas.create_line(p1x,p1y,p2x,p2y))
          dodraw2,p1x,p1y,p2x,p2y=CohenSutherland.clipLine(v3[0],v3[1],v1[0],v1[1],tup)
          if(dodraw2):
            self.objects.append(canvas.create_line(p1x,p1y,p2x,p2y))
        else:
          self.objects.append(canvas.create_line(v1[0],v1[1],v2[0],v2[1]))
          self.objects.append(canvas.create_line(v2[0],v2[1],v3[0],v3[1]))
          self.objects.append(canvas.create_line(v3[0],v3[1],v1[0],v1[1]))

    
    for pat in patches:
      pointlist=bp.resolve(resolution,pat,vert)

      for row in range(0,resolution-1):
        rowStart = row * resolution
        for col in range(0,resolution-1):
          here = rowStart +col 
          there = here + resolution

          triangleA = (pointlist[here],pointlist[there],pointlist[there+1])
          v1=model.TransformXYZ(triangleA[0][0],triangleA[0][1],triangleA[0][2],dopersp,doeuler)
          v2=model.TransformXYZ(triangleA[1][0],triangleA[1][1],triangleA[1][2],dopersp,doeuler)
          v3=model.TransformXYZ(triangleA[2][0],triangleA[2][1],triangleA[2][2],dopersp,doeuler)
          self.drawTriangle(canvas,v1,v2,v3,doclip,tup)

          triangleB = (pointlist[there+1],pointlist[here+1],pointlist[here])

          v1=model.TransformXYZ(triangleB[0][0],triangleB[0][1],triangleB[0][2],dopersp,doeuler)
          v2=model.TransformXYZ(triangleB[1][0],triangleB[1][1],triangleB[1][2],dopersp,doeuler)
          v3=model.TransformXYZ(triangleB[2][0],triangleB[2][1],triangleB[2][2],dopersp,doeuler)
          self.drawTriangle(canvas,v1,v2,v3,doclip,tup)

  def drawTriangle(self,canvas, v1,v2,v3,doclip,tup):
      if(doclip):
        dodraw,p1x,p1y,p2x,p2y=CohenSutherland.clipLine(v1[0],v1[1],v2[0],v2[1],tup)
        if(dodraw):
          self.objects.append(canvas.create_line(p1x,p1y,p2x,p2y))
        dodraw1,p1x,p1y,p2x,p2y=CohenSutherland.clipLine(v2[0],v2[1],v3[0],v3[1],tup)
        if(dodraw1):
          self.objects.append(canvas.create_line(p1x,p1y,p2x,p2y))
        dodraw2,p1x,p1y,p2x,p2y=CohenSutherland.clipLine(v3[0],v3[1],v1[0],v1[1],tup)
        if(dodraw2):
          self.objects.append(canvas.create_line(p1x,p1y,p2x,p2y))
      else:
          self.objects.append(canvas.create_line(v1[0],v1[1],v2[0],v2[1]))
          self.objects.append(canvas.create_line(v2[0],v2[1],v3[0],v3[1]))
          self.objects.append(canvas.create_line(v3[0],v3[1],v1[0],v1[1]))

  def redisplay( self, canvas, event ) :
    pass

#----------------------------------------------------------------------
