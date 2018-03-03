import svgwrite
from burger_data import BurgerElement

colors = {
    BurgerElement.crown: '#d3af37',
    BurgerElement.lettuce: '#00ff00',
    BurgerElement.tomato: '#ff0000',
    BurgerElement.cheese: '#ffff00',
    BurgerElement.patty: '#b32134',
    BurgerElement.heel: '#d3af37',
}


def svg_burger(layers):
  dwg = svgwrite.Drawing(height='10cm', width='10cm')
  dwg.viewbox(0, 0, 128, 256)

  y = (256 - len(layers)*32)/2
  outer = dwg.g(transform="translate(0,%d)" % y)
  dwg.add(outer)

  y = 0
  for layer in layers:

    g = dwg.g(id=layer, transform="translate(0,%d)" % y)

    p = dwg.path(d="M 16, 0",
                 fill=colors[layer],
                 stroke="none")
    p.push("h 96")
    p.push_arc(target=(0, 32), rotation=180, r=(16, 16), large_arc=False, angle_dir='+', absolute=False)
    p.push("h -96")
    p.push_arc(target=(0, -32), rotation=180, r=(16, 16), large_arc=True, angle_dir='+', absolute=False)

    g.add(p)

    outer.add(g)

    y += 32

  return dwg

# svg_burger([
#     BurgerElement.crown,
#     BurgerElement.lettuce,
#     BurgerElement.tomato,
#     BurgerElement.cheese,
#     BurgerElement.patty,
#     BurgerElement.cheese,
#     BurgerElement.patty,
#     BurgerElement.heel
# ]).saveas("test.svg")
