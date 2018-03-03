import svgwrite
from svgwrite import cm, mm
from svgwrite import utils

layers = [
    ['crown', '#d3af37'],
    ['lettuce', '#00ff00'],
    ['tomato', '#ff0000'],
    ['cheese', '#ffff00'],
    ['patty', '#b32134'],
    ['heel', '#d3af37'],
    ]

dwg = svgwrite.Drawing('elements.svg', height='10cm', width='10cm')
for name, color in layers:
  dwg.viewbox(0, 0, 200, 50)

  sw = 1

  p = dwg.path(d="M 25, 0",
               id=name,
               fill=color,
               stroke="none")
  p.push("h 150")
  p.push_arc(target=(0, 50), rotation=180, r=(10, 10), large_arc=False, angle_dir='+', absolute=False)
  p.push("h -150")
  p.push_arc(target=(0, -50), rotation=180, r=(10, 10), large_arc=True, angle_dir='+', absolute=False)
  dwg.add(p)

dwg.save()
