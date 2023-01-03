from manim import *


class Logo(VMobject):
    """Represents a Progress List for a specified number of items"""

    def __init__(self, **kwargs) -> None:
        # initialize the vmobject
        super().__init__(**kwargs)

        FONT = 'Hack'

        c = Circle(radius=2, color='#43798A', fill_opacity=0.6)
        k = Text("K", font_size=220, color=TEAL_D, stroke_width=2, weight=BOLD,  font=FONT, fill_opacity=1).shift(LEFT*0.3)
        b = Text("B", font_size=170, color='#8A3D52', stroke_width=2, font=FONT).shift(RIGHT*0.35+DOWN * 0.60)

        arc1 = c.get_left()
        arc3 = c.get_right()

        ap = ArcPolygon(arc1, arc3, color='#D6D189', fill_opacity=0.8,
                arc_config=[
                    {'radius':2.8, 'angle':90*DEGREES},
                    {'radius':2, 'angle':180*DEGREES},
                ]).rotate(39*DEGREES, about_point=c.get_center())

        # ap = CubicBezier(arc1, arc2+UP*1.5, arc2+DOWN*1.5, arc3)

        self.circle = c
        self.arc_poly = ap
        self.k = k
        self.b = b

        v = VGroup(c, ap, k, b)
        self.add(v)