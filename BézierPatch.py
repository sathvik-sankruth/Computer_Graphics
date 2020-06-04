
import numpy as np
import sys

def resolve( resolution, patch, vertices, trace = False ) :
  
  uRange = np.linspace( 0.0, 1.0, resolution )
  vRange = np.linspace( 0.0, 1.0, resolution )

  if ( trace ) :
    print( f'uRange {uRange}' )
    print( f'vRange {vRange}' )
    print( '' )

  
  controlPts = [ vertices[ vNum ] for vNum in patch ]

  
  points = list()

  for u in uRange :
    for v in vRange :
      pt = bernstein( u, v, controlPts, trace )
      points.append( pt )


  return points

def bernstein( u, v, controlPts, trace = False ) :
  x, y, z = 0.0, 0.0, 0.0

  coeffs = coefficients( u, v, trace )

  for c, cp in zip( coeffs, controlPts ) :
    dx = c*cp[0]
    dy = c*cp[1]
    dz = c*cp[2]

    rx = x + dx
    ry = y + dy
    rz = z + dz

    if ( trace ) :
      print()
      print( f'x {x:.6f} + ( {c:.6f} * {cp[0]:.6f} ) -> {x:.6f} + {dx:.6f} -> {rx:.6f}' )
      print( f'y {y:.6f} + ( {c:.6f} * {cp[1]:.6f} ) -> {y:.6f} + {dy:.6f} -> {ry:.6f}' )
      print( f'z {z:.6f} + ( {c:.6f} * {cp[2]:.6f} ) -> {z:.6f} + {dz:.6f} -> {rz:.6f}' )

    x = rx
    y = ry
    z = rz

  return ( x, y, z )

def coefficients( u, v, trace = False ) :
  u2 = u*u
  u3 = u2*u

  mu  = 1.0 - u
  mu2 = mu*mu
  mu3 = mu2*mu

  v2 = v*v
  v3 = v2*v

  mv  = 1.0 - v
  mv2 = mv*mv
  mv3 = mv2*mv

  r00 =      mu3*mv3; r01 = 3   *v*mu3*mv2; r02 = 3   *v2*mu3*mv; r03 =      v3*mu3
  r10 = 3*u *mu2*mv3; r11 = 9*u *v*mu2*mv2; r12 = 9*u *v2*mu2*mv; r13 = 3*u *v3*mu2
  r20 = 3*u2*mu *mv3; r21 = 9*u2*v*mu *mv2; r22 = 9*u2*v2*mu *mv; r23 = 3*u2*v3*mu
  r30 =   u3    *mv3; r31 = 3*u3*v    *mv2; r32 = 3*u3*v2    *mv; r33 =   u3*v3

  if ( trace ) :
    print( f' u {u:.6f} {u2:.6f} {u3:.6f}, mu {mu:.6f} {mu2:.6f}, {mu3:.6f}' )
    print( f' v {v:.6f} {v2:.6f} {v3:.6f}, mv {mv:.6f} {mv2:.6f}, {mv3:.6f}' )

    print( '' )

    print( f'r0 {r00:.6f} {r01:.6f} {r02:.6f} {r03:.6f}' )
    print( f'r1 {r10:.6f} {r11:.6f} {r12:.6f} {r13:.6f}' )
    print( f'r2 {r20:.6f} {r21:.6f} {r22:.6f} {r23:.6f}' )
    print( f'r3 {r30:.6f} {r31:.6f} {r32:.6f} {r33:.6f}' )

  return (
    r00, r01, r02, r03,
    r10, r11, r12, r13,
    r20, r21, r22, r23,
    r30, r31, r32, r33 )

def testBézierPatch( trace = False ) :
  print( '=== testBézierPatch ===' )

  vertices = [
    ( 1.0, 4.0, 0.0 ),
    ( 2.0, 4.0, 1.0 ),
    ( 3.0, 4.0, 1.0 ),
    ( 4.0, 4.0, 0.0 ),
    ( 1.0, 3.0, 1.0 ),
    ( 2.0, 3.0, 2.0 ),
    ( 3.0, 3.0, 2.0 ),
    ( 4.0, 3.0, 1.0 ),
    ( 1.0, 2.0, 1.0 ),
    ( 2.0, 2.0, 2.0 ),
    ( 3.0, 2.0, 2.0 ),
    ( 4.0, 2.0, 1.0 ),
    ( 1.0, 1.0, 0.0 ),
    ( 2.0, 1.0, 1.0 ),
    ( 3.0, 1.0, 1.0 ),
    ( 4.0, 1.0, 0.0 ),
  ]

  patch = list( range( 16 ) )

  resolution = 5
  rng = np.linspace( 0.0, 1.0, resolution )

  surface = resolve( resolution, patch, vertices, trace )

  print( '' )

  uv = [ ( u, v ) for u in rng for v in rng ]

  for ( u, v ), pt in zip( uv, surface ) :
    print( f'( u = {u:4.2f}, v = {v:4.2f} ) -> ( {pt[0]:8.6f}, {pt[1]:8.6f}, {pt[2]:8.6f} )' )

if ( __name__ == '__main__' ) :
  trace = len( sys.argv ) > 1 and sys.argv[1].lower() in [ 'y', 't', '1' ]

  testBézierPatch( trace )
