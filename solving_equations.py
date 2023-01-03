from manim import *

from utils.progress_list import ProgressList
from utils.logo import Logo
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
      

class SolvingTwoEquations(Scene):
    def construct(self):
        line1_str = """Exactly seven years ago, \\\\
                        Sam was 5 times the age of Janet."""
        line1_eqns = [
            " \\to ",
            " S-7 = 5 \\times (J-7) ",
            " \\to ",
            " S = 5J - 28 "
        ]
        line2_str = """Exactly two years ago, \\\\
                         Sam was 3 times the age of Janet."""
        line2_eqns = [
            " \\to ",
            " S-2 = 3 \\times (J-2) ",
            " \\to ",
            " S = 3J - 4 "
        ]
        line3_str = """What is the sum of their ages \\\\
                        today?"""
        line3_eqns = [
            " \\to ",
            " S + J = ?",
        ]
        v1 = self.gen_summary_line(line1_str, line1_eqns)
        v2 = self.gen_summary_line(line2_str, line2_eqns)
        v3 = self.gen_summary_line(line3_str, line3_eqns)

        v1.shift(LEFT)
        v2.align_to(v1, LEFT)
        v3.align_to(v1, LEFT)

        t1, t2, t3 = v1[1], v2[1], v3[1]
        t1.shift(RIGHT)
        t2.align_to(t1, LEFT)
        t3.align_to(t1, LEFT)

        self.animate_line(v1)
        self.play(v1.animate.shift(UP*1))
        self.animate_line(v2)
        self.play(v1.animate.shift(UP*1.5), v2.animate.shift(UP*1.5))
        self.animate_line(v3, False)


        self.wait()
        eqn1_copy = v1[1][-1].copy()
        self.add(eqn1_copy)
        self.play(FadeOut(v1, v2, v3))
        self.wait()
        #
        # Equation 
        lines = VGroup(
            MathTex("S = 5J - 28"),
            MathTex("S", "=", "5", "J","-", "28"),
            MathTex("3J-4", "=", "5", "J","-", "28"),
            MathTex("3J-4", "+", "4", "=", "5", "J","-", "28", "+", "4"),
            MathTex("3J", "=", "5", "J","-", "28", "+", "4"),
            MathTex("3J", "=", "5", "J","-", "24"),
            MathTex("5", "J","-", "24", "=", "3J"),

            MathTex("5", "J", "-", "3J" "=", "24"),
            MathTex("2J" "=", "24"),
            MathTex("J" "=", "12"),
        )        


        lines.arrange(DOWN, buff=MED_LARGE_BUFF).scale(0.8)
        for i, line in enumerate(lines):
            # align equations so that all the equal signs line up
            if i > 0:
                shift_x = line.get_part_by_tex("=").get_x() - lines[i-1].get_part_by_tex("=").get_x()
                line.shift(np.array((-shift_x, 0, 0)))

            # line.set_color_by_tex_to_color_map(COLOR_MAP)

        play_kw = {"run_time": 2}

        self.play(TransformMatchingShapes(eqn1_copy, lines[0]), path_arc=90*DEGREES, **play_kw)
        # line2_new = MathTex("S-7+7", "=", "5", "J","-", "35", "+", "7")
        # line2_new.replace(lines[2])
        # line2_new.match_style(lines[2])

        for i, t in enumerate(lines):
            if i < len(lines)-1:
                self.play(TransformMatchingTex(lines[i].copy(), lines[i+1]), 
                    path_arc=90*DEGREES, **play_kw)
                self.wait(2)

        # Create a new MathTex with same equation, but with different isolated subMobs to 
        # better animate next line
        # line2_new = MathTex("S-7+7", "=", "5", "J","-", "35", "+", "7")
        # line2_new.replace(lines[2])
        # line2_new.match_style(lines[2])
        # line2_new.set_color_by_tex_to_color_map(COLOR_MAP)
        # self.play(TransformMatchingTex(line2_new, lines[3], key_map={"S-7+7": "S"}),  #, key_map={"S-7+7": "S"}
        #     path_arc=90*DEGREES, **play_kw)
        # self.wait(2)

        # self.play(TransformMatchingTex(lines[3].copy(), lines[4], transform_mismatches=True), 
        #     path_arc=90*DEGREES, **play_kw)
        # self.wait(2)



    def gen_summary_line(self, str, eqns):
        NUM_COLOR = BLUE
        VAR_COLOR = ORANGE
        OP_COLOR = GREEN

        s = Tex(str)
        t = MathTex(*eqns) # substrings_to_isolate=["S", "J", "+", "-", "(", ")", "="])
        t.arrange(RIGHT, buff=MED_LARGE_BUFF)
        t.set_color_by_tex_to_color_map({
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
        v = VGroup(s, t).arrange(RIGHT).scale(0.6)
        return v

    def animate_line(self, v, show_rect=True):
        s,t = v
        self.play(Write(s))
        self.wait()
        self.play(Write(t[0]))
        self.wait()
        self.play(Write(t[1]))
        self.wait()
        if show_rect:
            self.play(Write(t[2]))
            self.wait()
            self.play(Write(t[3]))
            r = SurroundingRectangle(t[3], buff=MED_SMALL_BUFF)
            v.add(r)
            self.play(Create(r))
            self.wait()

        # self.play(LaggedStart(
        #     Write(s),
        #     *[Write(i) for i in t],
        #     lag_ratio=1
        # ), run_time=8)
            # "Exactly seven years ago, \\newline Sam was 5 times the age of Janet.",
            # "$ \\to $",
            # "S-7 = 5 \\times (J-7)",
            # " \\to "
            # "S = 5J - 28"

        #      Exactly two years ago, Sam was 3 times the age of Janet. \\\\
        #      What is the sum of their ages today?"
        # )


class Outline(Scene):

    def construct(self):
        
        l = ProgressList("Read", "Translate", "Simplify", "Substitute", list_dir=DOWN).to_corner(UL)

        # l = ProgressList("a", "sdfsdfb", "csdf", "dfd", "e", "sdfdsff", "gdsfsf", list_dir=RIGHT).scale(1).to_corner(UL)
        self.play(Write(l), run_time=2)

        self.play(l.set_current_item(2), run_time=2)
        self.wait(2)

        # self.play(l.set_current_item(2), run_time=2)
        # self.wait(2)

        self.play(l.set_current_item(0), run_time=5)
        self.wait(2)


        self.play(l.set_current_item(1), run_time=2)
        self.wait(2)

        self.play(l.set_current_item(3), run_time=2)
        self.wait(2)

        self.play(l.set_all_done(), run_time=2)
        self.wait(2)


class LogoAnimation(Scene):

    def construct(self):

        logo = Logo()
        self.play(Write(logo), run_time=3)
        self.wait()

        self.play(logo.animate.scale(0.15).to_corner(DR), run_time=2)


class Main(Scene):
    def saveOutlineListState(self, ol):
        # This copy is necessary, because we want to FadeIn/Out this Object 
        # multiple times in the scene and, these animations also add/remove 
        # # objects form scene (ie not just hide & show)
        self.ol_v = ol.copy()

    def getSavedOutlineList(self):
        return self.ol_v

    def construct(self):
        #1 Logo
        self.logo = Logo()
        self.play(Write(self.logo), run_time=3)
        self.wait()

        #2 Title
        self.title = Title("Solving Equations")
        self.play(LaggedStart(
            self.logo.animate.scale(0.15).to_corner(DR),
            Create(self.title), 
            lag_ratio=0.6),
            run_time=3)

        #3 Outline
        ol_verbose = ProgressList("Read sentences", "Translate sentences into Equations", "Simplify Equations", "Substitute", list_dir=DOWN).scale(1.2)
        ol_verbose.next_to(self.title, DOWN).shift(DOWN)
        ol_v = ProgressList("Read", "Translate", "Simplify", "Substitute", list_dir=DOWN)
        ol_v.to_edge(LEFT).shift(UP)

        self.saveOutlineListState(ol_v)
        

        self.play(Create(ol_verbose), run_time=4)
        self.wait()
        self.play(ReplacementTransform(ol_verbose, ol_v), run_time=2)
        self.remove(ol_v)

        #4 Display 4 Sections
        self.section_sentence_parts()
        self.section_equation1()

        self.wait()


    def section_sentence_parts(self):
        ol_v = self.getSavedOutlineList()
        self.add(ol_v)

        # Fade out outline & title
        self.play(ol_v.set_current_item(0), run_time=2)
        self.saveOutlineListState(ol_v)

        self.play(Indicate(ol_v.get_item(0)), run_time=2)
        self.play(AnimationGroup(
            FadeOut(ol_v, shift=LEFT),
            FadeOut(self.title, shift=UP)
            ))

        s = ["Exactly seven years ago, Sam was 5 times the age of Janet.", 
             " Exactly two years ago, Sam was 3 times the age of Janet.", 
             " What is the sum of their ages today?"]

        sentences = Tex(*s, color=BLUE).scale(0.7).to_edge(LEFT).shift(RIGHT+UP)
        self.play(Write(sentences), run_time=3)
        self.wait()

        sentences_v = VGroup(*[Tex(s_i, color=BLUE).scale(0.7) for s_i in s])
        sentences_v.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT).to_edge(LEFT).shift(2*RIGHT+1*UP)
        self.play(TransformMatchingShapes(sentences, sentences_v), run_time=3)
        self.wait()

        self.play(LaggedStart(*[Indicate(i) for i in sentences_v], lag_ratio=0.8), run_time=3)
        self.wait()

        self.play(FadeOut(sentences_v))
        self.wait()


    def section_equation1(self):
        ol_v = self.getSavedOutlineList()
    
        # Fade in & out outline & title
        self.play(FadeIn(ol_v, shift=RIGHT))
        self.play(ol_v.set_current_item(1))
        self.saveOutlineListState(ol_v)

        self.play(Indicate(ol_v.get_item(1),run_time=2))
        self.play(FadeOut(ol_v, shift=LEFT))




class Test (Scene):
    def construct(self):
        s = Square()
        c = Circle().next_to(s)
        self.add(s,c)
        self.wait()

        self.play(s.animate.shift(LEFT).fade(0.8))
        self.play(s.animate.shift(RIGHT).fade(1))

        # self.play(c.animate.fade(1))
        # self.play(c.animate.fade(0))


        f = Variable(0.3, 'fade_val', num_decimal_places=2).next_to(c, UP)
        self.add(f)
        c.add_updater(lambda c: c.fade(f.tracker.get_value()))

        self.play(f.tracker.animate.set_value(1), run_time=5, rate_func=linear)


        self.wait()
        self.play(Write(Text("Done")))
        self.wait()


        