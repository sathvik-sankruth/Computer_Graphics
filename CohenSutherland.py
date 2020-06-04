
import sys

INSIDE  = 0
LEFT    = 1
RIGHT   = 2
BELOW   = 4
ABOVE   = 8

MAX_COMPONENT = 1e15
EPSILON = 1e-13


def clipLine( p1x, p1y, p2x, p2y, portal ) :
  ( xMin, yMin, xMax, yMax ) = portal

  p1x = max( min( p1x, MAX_COMPONENT ), -MAX_COMPONENT )
  p1y = max( min( p1y, MAX_COMPONENT ), -MAX_COMPONENT )
  p2x = max( min( p2x, MAX_COMPONENT ), -MAX_COMPONENT )
  p2y = max( min( p2y, MAX_COMPONENT ), -MAX_COMPONENT )

  p1Code = _regionCode( p1x, p1y, xMin, yMin, xMax, yMax )
  p2Code = _regionCode( p2x, p2y, xMin, yMin, xMax, yMax )

  while ( True ) :
    if ( ( p1Code | p2Code ) == 0 ) :
      doDraw = True
      break

    if ( ( p1Code & p2Code ) != 0 ) :
      doDraw = False
      break

    aRegionCode = p2Code if p1Code == INSIDE else p1Code


    if ( aRegionCode & ABOVE ) :
      x = p1x + ( p2x - p1x )*( yMax - p1y )/( p2y - p1y )
      y = yMax

    elif ( aRegionCode & BELOW ) :
      x = p1x + ( p2x - p1x )*( yMin - p1y )/( p2y - p1y )
      y = yMin

    elif ( aRegionCode & RIGHT ) :
      x = xMax
      y = p1y + ( p2y - p1y )*( xMax - p1x )/( p2x - p1x )

    elif ( aRegionCode & LEFT ) :
      x = xMin
      y = p1y + ( p2y - p1y )*( xMin - p1x )/( p2x - p1x )

    else :
      raise ValueError( 'Code %s did not match any region?' % aRegionCode )


    if ( aRegionCode == p1Code ) :
      p1x = x
      p1y = y
      p1Code = _regionCode( p1x, p1y, xMin, yMin, xMax, yMax )

    else :
      p2x = x
      p2y = y
      p2Code = _regionCode( p2x, p2y, xMin, yMin, xMax, yMax )


  return ( doDraw, p1x, p1y, p2x, p2y )

def _regionCode( x, y, xMin, yMin, xMax, yMax ) :
  code = INSIDE


  if ( ( xMin - x ) > EPSILON ) :
    code = code | LEFT
  elif ( ( x - xMax ) > EPSILON ) :
    code = code | RIGHT

  if ( ( yMin - y ) > EPSILON ) :
    code = code | BELOW
  elif ( ( y - yMax ) > EPSILON ) :
    code = code | ABOVE

  return code



def clipPoint( x, y, portal ) :
  return x >= portal[0] and y >= portal[1] and x <= portal[2] and y <= portal[3]

def _testCohenSutherland() :
  import itertools
  import time

  limits = ( 1, 2, 3, 4 )
  xMin, yMin, xMax, yMax = limits


  xOK   = [ xMin ] + [ xMin + d/10.0 for d in range( 1, (xMax - xMin )*10 ) ] + [ xMax ]
  yOK   = [ yMin ] + [ yMin + d/10.0 for d in range( 1, (yMax - yMin )*10 ) ] + [ yMax ]

  xLOW  = [ xMin-1 ] + [ xMin-1 + d/4.0 for d in range( 1, 4 ) ]
  xHIGH = [ xMax + d/4.0 for d in range( 1, 5 ) ]
  yLOW  = [ yMin-1 ] + [ yMin-1 + d/4.0 for d in range( 1, 4 ) ]
  yHIGH = [ yMax + d/4.0 for d in range( 1, 5 ) ]

  xANY  = xLOW + xOK + xHIGH
  yANY  = yLOW + yOK + yHIGH


  OKPoints    = list( itertools.product( xOK, yOK ) )

  xLOWPoints  = list( itertools.product( xLOW, yANY ) )
  xHIGHPoints = list( itertools.product( xHIGH, yANY ) )

  yLOWPoints  = list( itertools.product( xANY, yLOW ) )
  yHIGHPoints = list( itertools.product( xANY, yHIGH ) )

  horMiddle   = list( itertools.product( xANY, yOK ) )
  verMiddle   = list( itertools.product( xOK, yANY ) )

  lowerLeft   = list( itertools.product( xLOW, yLOW ) )
  lowerRight  = list( itertools.product( xHIGH, yLOW ) )
  upperLeft   = list( itertools.product( xLOW, yHIGH ) )
  upperRight  = list( itertools.product( xHIGH, yHIGH ) )

  numTests  = 0
  numErrors = 0
  startTime = time.time()

  for p1 in OKPoints :
    for p2 in OKPoints :
      numTests += 1

      ( doDraw, p1x, p1y, p2x, p2y ) = clipLine( p1[0], p1[1], p2[0], p2[1], limits )
      if ( not doDraw ) :
        print( 'For OK points %s, %s, doDraw was False.' % ( p1, p2 ) )
        numErrors += 1

      if ( p1 != ( p1x, p1y ) ) :
        print( 'For OK points %s, %s, p1 came back ( %s, %s ).' % ( p1, p2, p1x, p1y ) )
        numErrors += 1

      if ( p2 != ( p2x, p2y ) ) :
        print( 'For OK points %s, %s, p2 came back ( %s, %s ).' % ( p1, p2, p2x, p2y ) )
        numErrors += 1

  elapsedTime = time.time() - startTime
  perTest     = 1000000 * elapsedTime / numTests
  print( '%d error%s detected in %s trivial accept tests. %.2fS, %.2fμS/test.' % (
    numErrors, '' if numErrors == 1 else 's', numTests, elapsedTime, perTest ) )

  numTests  = 0
  numErrors = 0
  startTime = time.time()

  for ( testName, points ) in [
    ( 'X Low', xLOWPoints ), ('X High', xHIGHPoints ),
    ( 'Y Low', yLOWPoints ), ( 'Y High', yHIGHPoints ) ] :

    for p1 in points :
      for p2 in points :
        numTests += 1

        ( doDraw, p1x, p1y, p2x, p2y ) = clipLine( p1[0], p1[1], p2[0], p2[1], limits )
        if ( doDraw ) :
          print( 'For Same Side test %s points %s, %s, doDraw was True ( %s, %s ), ( %s, %s ).' % (
            testName, p1, p2, p1x, p1y, p2x, p2y ) )
          numErrors += 1

  elapsedTime = time.time() - startTime
  perTest     = 1000000 * elapsedTime / numTests
  print( '%d error%s detected in %s trivial reject tests. %.2fS, %.2fμS/test.' % (
    numErrors, '' if numErrors == 1 else 's', numTests, elapsedTime, perTest ) )

  numTests  = 0
  numErrors = 0
  startTime = time.time()

  for ( testName, points1, points2 ) in [
    ( 'Horizontal Middle', horMiddle, horMiddle ), ('Vertical Middle', verMiddle, verMiddle ),
    ( 'Diag UR-LL', upperRight, lowerLeft ), ( 'Diag LR-UL', lowerRight, upperLeft ),
    ( 'Diag LL-UR', lowerLeft, upperRight ), ( 'Diag UL-LR', upperLeft, lowerRight ) ] :

    for p1 in points1 :
      for p2 in points2 :
        p1Code = _regionCode( p1[0], p1[1], xMin, yMin, xMax, yMax )
        p2Code = _regionCode( p2[0], p2[1], xMin, yMin, xMax, yMax )

        if ( (p1Code | p2Code) == 0 or (p1Code & p2Code != 0 ) ) :
          continue

        numTests += 1

        ( doDraw, p1x, p1y, p2x, p2y ) = clipLine( p1[0], p1[1], p2[0], p2[1], limits )
        if ( doDraw ) :
          
          ( shouldBeP1, shouldBeP2 ) = _directClipLine( p1, p2, xMin, yMin, xMax, yMax )

          if ( _pointsMatch( shouldBeP1, ( p1x, p1y ) ) ) :
            
            if ( not _pointsMatch( shouldBeP2, ( p2x, p2y ) ) ) :
              
              print( '(%s) ① For Opposite Side test %s points %s, %s,'
                '\npoints do not match expected ( %s, %s ), ( %s, %s ) ≠ ( %s, %s ), ( %s, %s ).' % (
                numTests, testName, p1, p2, p1x, p1y, p2x, p2y, shouldBeP1[0], shouldBeP1[1], shouldBeP2[0], shouldBeP2[1] ) )
              numErrors += 1

          elif ( _pointsMatch( shouldBeP1, ( p2x, p2y ) ) ) :
            if ( not _pointsMatch( shouldBeP2, ( p1x, p1y ) ) ) :
              
              print( '(%s) ② For Opposite Side test %s points %s, %s,'
                '\npoints do not match expected ( %s, %s ), ( %s, %s ) ≠ ( %s, %s ), ( %s, %s ).' % (
                numTests, testName, p1, p2, p1x, p1y, p2x, p2y, shouldBeP1[0], shouldBeP1[1], shouldBeP2[0], shouldBeP2[1] ) )
              numErrors += 1

          else :
            
            print( '(%s) ③ For Opposite Side test %s points %s, %s,'
              '\npoints do not match expected ( %s, %s ), ( %s, %s ) ≠ ( %s, %s ), ( %s, %s ).' % (
              numTests, testName, p1, p2, p1x, p1y, p2x, p2y, shouldBeP1[0], shouldBeP1[1], shouldBeP2[0], shouldBeP2[1] ) )
            numErrors += 1

        else :
          
          print( '(%s) For Opposite Side test %s points %s, %s,\ndoDraw was False ( %s, %s ), ( %s, %s ).' % (
            numTests, testName, p1, p2, p1x, p1y, p2x, p2y ) )
          numErrors += 1

  elapsedTime = time.time() - startTime
  perTest     = 1000000 * elapsedTime / numTests
  print( '%d error%s detected in %s opposite side tests. %.2fS, %.2fμS/test.' % (
    numErrors, '' if numErrors == 1 else 's', numTests, elapsedTime, perTest ) )

def _directClipLine( p1, p2, xMin, yMin, xMax, yMax ) :
  if ( p1[0] == p2[0] ) :
    
    shouldBeP1 = ( p1[0], max( min( p1[1], p2[1] ), yMin ) )
    shouldBeP2 = ( p1[0], min( max( p1[1], p2[1] ), yMax ) )

  elif ( p1[1] == p2[1] ) :
    
    shouldBeP1 = ( max( min( p1[0], p2[0] ), xMin ), p1[1] )
    shouldBeP2 = ( min( max( p1[0], p2[0] ), xMax ), p1[1] )

  else :
    
    slope = ( p1[1] - p2[1] )/( p1[0] - p2[0] )
    intercept = p1[1] - slope*p1[0]

    def yFromX( x ) :
      return slope * x + intercept

    def xFromY( y ) :
      return ( y - intercept )/slope

    
    leastX    = max( min( p1[0], p2[0] ), xMin )
    leastXY   = yFromX( leastX )

    if ( leastXY > yMax ) :
      leastX  = xFromY( yMax )
      leastXY = yMax

    if ( leastXY < yMin ) :
      leastX  = xFromY( yMin )
      leastXY = yMin


    greatestX = min( max( p1[0], p2[0] ), xMax )
    greatestXY   = yFromX( greatestX )


    if ( greatestXY > yMax ) :
      greatestX  = xFromY( yMax )
      greatestXY = yMax

    if ( greatestXY < yMin ) :
      greatestX  = xFromY( yMin )
      greatestXY = yMin

    shouldBeP1 = ( leastX, leastXY )
    shouldBeP2 = ( greatestX, greatestXY )

  return ( shouldBeP1, shouldBeP2 )


def _pointsMatch( p1, p2 ) :
  xMatch = abs( p1[0] - p2[0] ) < EPSILON
  yMatch = abs( p1[1] - p2[1] ) < EPSILON

  return xMatch and yMatch

if ( __name__ == '__main__' ) :
  _testCohenSutherland()

