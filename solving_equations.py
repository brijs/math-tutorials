from manim import *
# from manim_voiceover import VoiceoverScene
# from manim_voiceover.services.gtts import GTTSService


class EquationIntro(Scene):

    def construct(self):
        NUM_COLOR = BLUE
        VAR_COLOR = ORANGE
        OP_COLOR = GREEN

        labels = [Tex(l).shift(UP*2) for l in ["","Equal sign", "Variables", "Numbers", "Operators"]]

        def switch_labels(i: int):
            return AnimationGroup(
                FadeOut(labels[i], shift=UP),
                FadeIn(labels[i+1], shift=UP)
            )

        def IndicateAnimGroup(*tex_items):
            return AnimationGroup(
                    *[Indicate(e.get_parts_by_tex(i), scale_factor=1.5) for i in tex_items],
                    lag_ratio = 0.8
                )

        e = MathTex("4", "\\times", "(x-3)", "=", "5", "-", "(x+3)", "+", r'\frac{y}{4}', substrings_to_isolate=["(", ")", "-", "+", "3", "4", "5"])
        e.set_color_by_tex_to_color_map({
                "3": NUM_COLOR,
                "4": NUM_COLOR,
                "5":NUM_COLOR,
                "x": VAR_COLOR,
                "y": VAR_COLOR,
                "-": OP_COLOR,
                "=": OP_COLOR,
                "(": OP_COLOR,
                ")": OP_COLOR,
                "+": OP_COLOR
            })
        # below doesn't work :(
        # e = MathTex("5 \\cdot (x-3) = 4 - \\frac{y}{4} + 3", substrings_to_isolate=["(", ")", "-", "+", "3", "4", "5", '\{y\}'])
        self.play(Write(e))
        self.wait()

        # Equal
        self.play(
            AnimationGroup(
                switch_labels(0),
                IndicateAnimGroup("="),
                lag_ratio=0.8
            ),
            run_time=3
        )
        self.wait()

        # Variables
        self.play(
            AnimationGroup(
                switch_labels(1),
                IndicateAnimGroup("x", "y"),
                lag_ratio=0.8
            ),
            run_time=3
        )
        self.wait()

        # Numbers
        self.play(
            AnimationGroup(
                switch_labels(2),
                IndicateAnimGroup("3", "4", "5"),
                lag_ratio=0.8
            ),
            run_time=3
        )
        self.wait()

        # operators
        self.play(
            AnimationGroup(
                switch_labels(3),
                IndicateAnimGroup("+", "-", "\\frac", "\\cdot", "\\times"),
                lag_ratio=0.8
            ),
            run_time=4
        )
        self.wait()


class FirstEquation(Scene):
    def construct(self):
        NUM_COLOR = BLUE
        VAR_COLOR = ORANGE
        OP_COLOR = GREEN

        COLOR_MAP = {
                "5": NUM_COLOR,
                "7": NUM_COLOR,
                "35":NUM_COLOR,
                "28": NUM_COLOR,
                "-": OP_COLOR,
                "=": OP_COLOR,
                "(": OP_COLOR,
                ")": OP_COLOR,
                "+": OP_COLOR,
                "\\times": OP_COLOR,
                "S": VAR_COLOR,
                "J": VAR_COLOR,
            }
       
        
        sentence = Tex("Exactly seven years ago, Sam was 5 times the age of Janet", 
                        font_size=40, 
                        substrings_to_isolate=["seven", "Sam", "5", "Janet", "ago", "timex_truncates_str"])
        sentence.to_edge(UP)
        self.play(Write(sentence))

        def extractTexFromSentence(tex, color, new_tex):
            this_tex = sentence.get_part_by_tex(tex)
            new_tex.set_color(color).scale(1.5).next_to(this_tex, DOWN, buff=1)

            return AnimationGroup(
                this_tex.animate.set_color(color),
                Indicate(this_tex, scale_factor=1.5, color=color),
                FadeIn(new_tex, shift=DOWN*1.5),
                lag_ratio=1)

        key_texes = ["seven", "5", "Sam", "Janet", "ago", "times"]
        key_colors = [NUM_COLOR, NUM_COLOR, VAR_COLOR, VAR_COLOR, OP_COLOR, OP_COLOR]
        key_new_texes = [MathTex(s).scale(1.0) for s in ["7", "5", "S", "J", "-", "\\times"]]

        self.play(
            AnimationGroup(
                *[extractTexFromSentence(t, c, n) for (t,c,n) in zip(key_texes, key_colors, key_new_texes)],
                lag_ratio=1
            ))

        extractedTexes = VGroup(*key_new_texes)

        # Note that Manim also supports a custom syntax that allows splitting a TeX string into substrings easily: simply enclose parts of your formula that you want to isolate with double braces. In the string MathTex(r"{{ a^2 }} + {{ b^2 }} = {{ c^2 }}"), the rendered mobject will consist of the substrings a^2, +, b^2, =, and c^2. 

        # Equation simplification
        lines = VGroup(
            MathTex("S-7", "=", "5 \\times", "(J-7)"), 
            MathTex("S-7", "=", "5J-35"),
            MathTex("S-7", "+", "7", "=", "5J-35", "+", "7"),
            MathTex("S", "=", "5", "J","-", "35", "+", "7"),
            MathTex("S", "=", "5", "J","-", "28"),
        )        


        lines.arrange(DOWN, buff=MED_LARGE_BUFF)
        for i, line in enumerate(lines):
            # align equations so that all the equal signs line up
            if i > 0:
                shift_x = line.get_part_by_tex("=").get_x() - lines[i-1].get_part_by_tex("=").get_x()
                line.shift(np.array((-shift_x, 0, 0)))

            line.set_color_by_tex_to_color_map(COLOR_MAP)

        play_kw = {"run_time": 2}

        self.play(TransformMatchingShapes(extractedTexes, lines[0]), path_arc=90*DEGREES, **play_kw)
        
        br_sam = Brace(lines[0][0], UP, buff=SMALL_BUFF, color=YELLOW_A)
        br_sam_text = Text("Sam, 7 yrs ago", font_size=18, color=YELLOW_A).next_to(br_sam, UP)
        br_janet = Brace(lines[0][3], UP, buff=SMALL_BUFF, color=YELLOW_A)
        br_janet_text = Text("Janet, 7 yrs ago", font_size=18, color=YELLOW_A).next_to(br_janet, UP)

        self.play (AnimationGroup(
            Create(VGroup(br_sam, br_sam_text)),
            Create(VGroup(br_janet, br_janet_text)),
            lag_ratio=0.2
            ))

        self.wait(2)

        line0_new = MathTex("S-2", "=", "5 \\times (J-7)")
        line0_new.replace(lines[0])
        line0_new.match_style(lines[0])
        line0_new.set_color_by_tex_to_color_map(COLOR_MAP)

        self.play(TransformMatchingTex(lines[0].copy(), lines[1], key_map={"5 \\times (J-7)": "5J-35"}), 
            path_arc=90*DEGREES, **play_kw)
        self.wait(2)

        # line1_new = MathTex("S", "-", "7", "=", "5", "J","-", "35")
        # line1_new.replace(lines[1])
        # line1_new.match_style(lines[1])
        self.play(TransformMatchingTex(lines[1].copy(), lines[2]), 
            path_arc=90*DEGREES, **play_kw)
        self.wait(2)

        # Create a new MathTex with same equation, but with different isolated subMobs to 
        # better animate next line
        line2_new = MathTex("S-7+7", "=", "5", "J","-", "35", "+", "7")
        line2_new.replace(lines[2])
        line2_new.match_style(lines[2])
        line2_new.set_color_by_tex_to_color_map(COLOR_MAP)
        self.play(TransformMatchingTex(line2_new, lines[3], key_map={"S-7+7": "S"}),  #, key_map={"S-7+7": "S"}
            path_arc=90*DEGREES, **play_kw)
        self.wait(2)

        self.play(TransformMatchingTex(lines[3].copy(), lines[4], transform_mismatches=True), 
            path_arc=90*DEGREES, **play_kw)
        self.wait(2)

        sr = SurroundingRectangle(lines[-1], buff=MED_SMALL_BUFF)
        br = Brace(sr, DOWN, buff=MED_SMALL_BUFF)
        br_text = Text("Equation 1").next_to(br, DOWN)

        self.play (AnimationGroup(
            Flash(lines[-1], flash_radius=1.5, num_lines=20),
            Create(sr),
            Create(VGroup(br, br_text)),
            lag_ratio=0.8
            ))
            
        self.wait(2)
      


class SecondEquation(Scene):
    def construct(self):
        NUM_COLOR = BLUE
        VAR_COLOR = ORANGE
        OP_COLOR = GREEN

        COLOR_MAP = {
                "5": NUM_COLOR,
                "7": NUM_COLOR,
                "35":NUM_COLOR,
                "28": NUM_COLOR,
                "-": OP_COLOR,
                "=": OP_COLOR,
                "(": OP_COLOR,
                ")": OP_COLOR,
                "+": OP_COLOR,
                "\\times": OP_COLOR,
                "S": VAR_COLOR,
                "J": VAR_COLOR,
            }
       
        
        sentence = Tex("Exactly two years ago, Sam was 3 times the age of Janet.", 
                        font_size=40, 
                        substrings_to_isolate=["two", "Sam", "3", "Janet", "ago", "timex_truncates_str"])
        sentence.to_edge(UP)
        self.play(Write(sentence))

        def extractTexFromSentence(tex, color, new_tex):
            this_tex = sentence.get_part_by_tex(tex)
            new_tex.set_color(color).scale(1.5).next_to(this_tex, DOWN, buff=1)

            return AnimationGroup(
                this_tex.animate.set_color(color),
                Indicate(this_tex, scale_factor=1.5, color=color),
                FadeIn(new_tex, shift=DOWN*1.5),
                lag_ratio=1)

        key_texes = ["two", "3", "Sam", "Janet", "ago", "times"]
        key_colors = [NUM_COLOR, NUM_COLOR, VAR_COLOR, VAR_COLOR, OP_COLOR, OP_COLOR]
        key_new_texes = [MathTex(s).scale(1.0) for s in ["2", "3", "S", "J", "-", "\\times"]]

        self.play(
            AnimationGroup(
                *[extractTexFromSentence(t, c, n) for (t,c,n) in zip(key_texes, key_colors, key_new_texes)],
                lag_ratio=0.7
            ))

        extractedTexes = VGroup(*key_new_texes)

        # Equation simplification
        lines = VGroup(
            MathTex("S-2", "=", "3 \\times", "(J-2)"), 
            MathTex("S-2", "=", "3J-6"),
            MathTex("S-2", "+", "2", "=", "3J-6", "+", "2"),
            MathTex("S", "=", "3", "J","-", "6", "+", "2"),
            MathTex("S", "=", "3", "J","-", "4"),
        )        


        lines.arrange(DOWN, buff=MED_LARGE_BUFF)
        for i, line in enumerate(lines):
            # align equations so that all the equal signs line up
            if i > 0:
                shift_x = line.get_part_by_tex("=").get_x() - lines[i-1].get_part_by_tex("=").get_x()
                line.shift(np.array((-shift_x, 0, 0)))

            line.set_color_by_tex_to_color_map(COLOR_MAP)

        play_kw = {"run_time": 2}

        self.play(TransformMatchingShapes(extractedTexes, lines[0]), path_arc=90*DEGREES, **play_kw)
        
        br_sam = Brace(lines[0][0], UP, buff=SMALL_BUFF, color=YELLOW_A)
        br_sam_text = Text("Sam, 2 yrs ago", font_size=18, color=YELLOW_A).next_to(br_sam, UP)
        br_janet = Brace(lines[0][3], UP, buff=SMALL_BUFF, color=YELLOW_A)
        br_janet_text = Text("Janet, 2 yrs ago", font_size=18, color=YELLOW_A).next_to(br_janet, UP)

        self.play (AnimationGroup(
            Create(VGroup(br_sam, br_sam_text)),
            Create(VGroup(br_janet, br_janet_text)),
            lag_ratio=0.2
            ))

        self.wait(2)

        line0_new = MathTex("S-2", "=", "3 \\times (J-2)")
        line0_new.replace(lines[0])
        line0_new.match_style(lines[0])
        line0_new.set_color_by_tex_to_color_map(COLOR_MAP)
        self.play(TransformMatchingTex(line0_new, lines[1], key_map={"3 \\times (J-2)": "3J-6"}), 
            path_arc=90*DEGREES, **play_kw)
        self.wait(2)

        self.play(TransformMatchingTex(lines[1].copy(), lines[2]), 
            path_arc=90*DEGREES, **play_kw)
        self.wait(2)

        # Create a new MathTex with same equation, but with different isolated subMobs to 
        # better animate next line
        line2_new = MathTex("S-2+2", "=", "3", "J","-", "6", "+", "2")
        line2_new.replace(lines[2])
        line2_new.match_style(lines[2])
        line2_new.set_color_by_tex_to_color_map(COLOR_MAP)
        self.play(TransformMatchingTex(line2_new, lines[3], key_map={"S-2+2": "S"}),  #, key_map={"S-7+7": "S"}
            path_arc=90*DEGREES, **play_kw)
        self.wait(2)

        self.play(TransformMatchingTex(lines[3].copy(), lines[4], transform_mismatches=True), 
            path_arc=90*DEGREES, **play_kw)
        self.wait(2)

        sr = SurroundingRectangle(lines[-1], buff=MED_SMALL_BUFF)
        br = Brace(sr, DOWN, buff=MED_SMALL_BUFF)
        br_text = Text("Equation 2").next_to(br, DOWN)

        self.play (AnimationGroup(
            Flash(lines[-1], flash_radius=1.5, num_lines=20),
            Create(sr),
            Create(VGroup(br, br_text)),
            lag_ratio=0.8
            ))
            
        self.wait(2)
      

  


class ProgressList(VMobject):
    COLOR_DONE = GREEN_D
    COLOR_CURR = ORANGE
    COLOR_PENDING = GRAY_D

    def __createItem(self, text, list_dir) -> VGroup:
        d = Dot(fill_opacity=1.0, color=ProgressList.COLOR_CURR)
        t = Text(text, font_size=20, color=ProgressList.COLOR_PENDING)

        if (list_dir==DOWN).all():
            t.next_to(d, RIGHT, buff=MED_SMALL_BUFF)
        else:
            t.next_to(d, DOWN, buff=MED_SMALL_BUFF).align_to(d, LEFT) 


        item = VGroup().set(d=d,t=t)
        item.add(d,t)
        return item

    def __init__(self, *text_strings, list_dir=DOWN, **kwargs) -> None:
        # initialize the vmobject
        super().__init__(**kwargs)

        self.__items = []
        self.__lines = []
        self.__curr_index = 0

        for i, t in enumerate(text_strings):
            # Create Item (dot & label)
            item = self.__createItem(t, list_dir)
            self.__items.append(item)
            self.add(item) # add to submobjects - IMP

            # Draw line to connect Items
            if i > 0:
                item.get_d().set_color(ProgressList.COLOR_PENDING)
                last_item_dot = self.__items[-2].get_d()
                last_item_text = self.__items[-2].get_t()
                line_length =  list_dir if (list_dir==DOWN).all() else ( max (1.0, last_item_text.width) * list_dir * 1.3)
                l = Line(start=last_item_dot.get_center(), end=last_item_dot.get_center()+line_length, buff=SMALL_BUFF, color=ProgressList.COLOR_PENDING)
                item.shift(l.end - item.get_d().get_center())

                self.__lines.append(l)
                self.add(l) # add to submobjects - order is important for animations

    def __animate_item_done(self, item, line) -> AnimationGroup :
        return AnimationGroup(
            item.animate.set_color(ProgressList.COLOR_DONE),
            line.animate.set_color(ProgressList.COLOR_DONE),
            lag_ratio=0.4
        )

    def __animate_item_reset(self, item, line) -> AnimationGroup :
        return AnimationGroup(
            item.animate.set_color(ProgressList.COLOR_PENDING),
            line.animate.set_color(ProgressList.COLOR_PENDING),
            lag_ratio=0.4
        )

        
    def set_all_done(self) -> AnimationGroup:
        anims = []

        anims.extend([self.__animate_item_done(self.__items[i], self.__lines[i]) for i in range(max(0, len(self.__items)-1))])
        anims.append(AnimationGroup(self.__items[len(self.__items)-1].animate.set_color(ProgressList.COLOR_DONE)))

        return AnimationGroup(*anims, lag_ratio=0.8)

    def set_current_item(self, new_curr_index) -> AnimationGroup:
        anims = []

        start_index = 0
        end_index = len(self.__items)

        if new_curr_index == self.__curr_index:
            return AnimationGroup(*anims, lag_ratio=1)
        elif new_curr_index > self.__curr_index:
            start_index = self.__curr_index
            end_index = new_curr_index
           

            anims.extend([self.__animate_item_done(self.__items[i], self.__lines[i]) for i in range(start_index, end_index)])
            # update current item
            anims.append(AnimationGroup(
                # Indicate(self.__items[end_index], scale_factor = 1.2, color=ProgressList.COLOR_CURR),
                self.__items[end_index].animate.set_color(ProgressList.COLOR_CURR),
                lag_ratio=1))
        else: # new_curr_index < self.__curr_index:
            start_index = new_curr_index
            end_index = self.__curr_index

            anims.extend([self.__animate_item_reset(self.__items[i+1], self.__lines[i]) for i in reversed(range(start_index, end_index))])
            # update current item
            anims.append(AnimationGroup(
                # Indicate(self.__items[start_index], scale_factor = 1.2, color=ProgressList.COLOR_CURR),
                self.__items[start_index].animate.set_color(ProgressList.COLOR_CURR),
                lag_ratio=1))

        self.__curr_index = new_curr_index
        return AnimationGroup(*anims, lag_ratio=1)


class Outline(Scene):

    def construct(self):
        
        # l = ProgressList("Extract", "Equations", "Simplify", "Substitute", list_dir=RIGHT).to_corner(UL)
        l = ProgressList("a", "sdfsdfb", "csdf", "dfd", "e", "sdfdsff", "gdsfsf", list_dir=RIGHT).scale(1).to_corner(UL)
        self.play(Write(l), run_time=2)

        self.play(l.set_current_item(2), run_time=2)
        self.wait(2)

        # self.play(l.set_current_item(2), run_time=2)
        # self.wait(2)

        self.play(l.set_current_item(0), run_time=5)
        self.wait(2)


        self.play(l.set_current_item(4), run_time=2)
        self.wait(2)

        self.play(l.set_all_done(), run_time=2)
        self.wait(2)