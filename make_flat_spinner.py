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

do_circle = False

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

col1 = array((0xff, 0xa2, 0x00))
col2 = array((0x66, 0x66, 0x66))

#col2 = col1 * 0.1 + col2 * 0.9
col1 = array((0xff, 0xa2, 0x33))
col1 = array((0xff, 0xff, 0xe8))


blobw = 8
blobpitch = 25


def decay(blobs):
  return blobs * 0.92

written_frames = []

def write_frame(i, blobs):
  global written_frames
  content = []

  x = 0
  y = 0
  bN = len(blobs)
  for b in blobs:
    color = col1 * (float(b)) + col2 * (float(1.0-b))
    col = '#%02x%02x%02x' % tuple([int(c) for c in color])
    if do_circle:
      r = float(blobw) / 2
      a = circle % (x + r, float(y) + r, r, col)
    else:
      a = rect % (x, y, blobw, blobw, col)
    content.append(a)
    x += blobpitch

  w = blobpitch * (N - 1) + blobw

  name = 'frame%03d' % i
  svg_name = name + '.svg'
  png_name = name + '.png'

  f = open(svg_name, 'w')
  f.write(svg % (w, blobw, '\n'.join(content)))
  f.close()

  cmd = ('inkscape', '-e', png_name, svg_name)
  print ' '.join(cmd)
  subprocess.call(cmd)
  written_frames.append(png_name)


N = 12
blobs = zeros(N)

decay_steps = 2
for_frames = (N + N - 2) * decay_steps
start_at = (N + N - 1) * decay_steps - 1

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
    if blob_pos >= 0:
      if blob_pos >= (N - 1):
        blob_pos = -2
      else:
        blob_pos += 1
    else:
      if blob_pos <= -(N - 1):
        blob_pos = 0
      else:
        blob_pos -= 1

  if frame is not None:
    write_frame(frame, blobs)

  i += 1

cmd = ('convert', '-loop', '0', '-delay', '16') + tuple(written_frames) + ('flat_spinner.gif', )
print ' '.join(cmd)
subprocess.call(cmd)
