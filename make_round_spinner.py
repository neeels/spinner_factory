#!/usr/bin/env python

from numpy import *
import subprocess

svg = r'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   sodipodi:docname="New document 1"
   inkscape:version="0.48.4 r9939"
   version="1.1"
   id="svg2"
   width="%d"
   height="%d">
  <sodipodi:namedview
     id="base"
     pagecolor="#666666"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="0.78255208"
     inkscape:cx="512"
     inkscape:cy="384"
     inkscape:document-units="px"
     inkscape:current-layer="layer1"
     showgrid="false"
     inkscape:window-width="1436"
     inkscape:window-height="854"
     inkscape:window-x="0"
     inkscape:window-y="18"
     inkscape:window-maximized="0" />
  <defs
     id="defs4" />
  <metadata
     id="metadata7">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     id="layer1"
     inkscape:groupmode="layer"
     inkscape:label="Layer 1">
    %s
  </g>
</svg>
'''

do_circle = True

circle = '''<circle
       cx="%fpx"
       cy="%fpx"
       r="%dpx"
       id="rect2985"
       style="color:#666666;fill:%s;fill-opacity:1;fill-rule:nonzero;stroke:#666666;stroke-width:1px;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate" />'''

rect = '''<rect
       x="%fpx"
       y="%fpx"
       width="%dpx"
       height="%dpx"
       id="rect2985"
       style="color:#666666;fill:%s;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1px;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate" />'''

col1 = array((0xed, 0x90, 0x04))
col2 = array((0x66, 0x66, 0x66))

col1 = array((0xff, 0xff, 0xe8))
col1 = array((0xff, 0xa2, 0x33))
col1 = array((0xff, 0xff, 0xff))


blobr = 7
blob_circle_r = 35

image_w = (blob_circle_r + blobr + 1) * 2
origin = image_w / 2


def decay(blobs):
  #return array([b * 0.85 if b < 0.8 else b*0.95 for b in blobs])
  return blobs * .905

written_frames = []

def write_frame(i, blobs):
  global written_frames
  content = []

  x = 0
  y = 0
  bN = len(blobs)
  if bN & 1:
    ang = -0.5 * pi
  else:
    ang = 0
  ang_step = 2.*pi / bN
  for b in blobs:
    x = origin + blob_circle_r * cos(ang)
    y = origin + blob_circle_r * sin(ang)

    color = col1 * (float(b)) + col2 * (float(1.0-b))
    col = '#%02x%02x%02x' % tuple([int(c) for c in color])

    if do_circle:
      a = circle % (x, y, blobr, col)
    else:
      a = rect % (x - blobr, y - blobr, 2*blobr, 2*blobr, col)
    content.append(a)
    ang += ang_step

  name = 'frame%03d' % i
  svg_name = name + '.svg'
  png_name = name + '.png'

  f = open(svg_name, 'w')
  f.write(svg % (image_w, image_w, '\n'.join(content)))
  f.close()

  cmd = ('inkscape', '-e', png_name, svg_name)
  print ' '.join(cmd)
  subprocess.call(cmd)
  written_frames.append(png_name)


N = 10
blobs = zeros(N)

decay_steps = 2
for_frames = N  * decay_steps
start_at = for_frames

i = 0
frame = None
blob_pos = 0
decay_steps_done = 0
while True:
  if i >= start_at:
    frame = i - start_at
    if frame >= for_frames:
      break

  blobs = decay(blobs)
  decay_steps_done += 1

  if decay_steps_done >= decay_steps:
    decay_steps_done = 0
    blobs[blob_pos] = 1.0
    if blob_pos >= (N - 1):
      blob_pos = 0
    else:
      blob_pos += 1

  if frame is not None:
    write_frame(frame, blobs)

  i += 1

cmd = ('convert', '-loop', '0', '-delay', '12') + tuple(written_frames) + ('round_spinner.gif', )
print ' '.join(cmd)
subprocess.call(cmd)
