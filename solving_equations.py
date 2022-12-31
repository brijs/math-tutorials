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

        # Equation simplification
        lines = VGroup(
            MathTex("S", "-", "7", "=", "5", " \\times", "(", "J", "-", "7", ")", substrings_to_isolate=["S","J"]),
            MathTex("S", "-", "7", "=", "5", "J","-", "35", substrings_to_isolate=["S","J"]),
            MathTex("S", "=", "5", "J","-", "35", "+", "7", substrings_to_isolate=["S","J"]),
            MathTex("S", "=", "5", "J","-", "28", substrings_to_isolate=["S","J"]),
        )


        lines.arrange(DOWN, buff=MED_LARGE_BUFF)
        for i, line in enumerate(lines):
            # align equations on equal to sign
            if i > 0:
                shift_x = line.get_part_by_tex("=").get_x() - lines[i-1].get_part_by_tex("=").get_x()
                line.shift(np.array((-shift_x, 0, 0)))

            line.set_color_by_tex_to_color_map({
                "5": NUM_COLOR,
                "7": NUM_COLOR,
                "35":NUM_COLOR,
                "28": NUM_COLOR,
                "S": VAR_COLOR,
                "J": VAR_COLOR,
                "-": OP_COLOR,
                "=": OP_COLOR,
                "(": OP_COLOR,
                ")": OP_COLOR,
                "+": OP_COLOR,
                "\\times": OP_COLOR
            })

        play_kw = {"run_time": 2}

        self.play(TransformMatchingShapes(extractedTexes, lines[0]), path_arc=90*DEGREES, **play_kw)
        self.wait(2)

        for i in range(1,3):
            self.play(TransformMatchingTex(lines[i-1].copy(), lines[i], key_map={"-7": "+7"}), 
                path_arc=180*DEGREES, **play_kw)
            self.wait(2)

        self.play(TransformMatchingTex(lines[2].copy(), lines[3], key_map={"-7": "+7"}, transform_mismatches=True), 
            path_arc=180*DEGREES, **play_kw)
        self.wait(2)

        sr = SurroundingRectangle(lines[-1], buff=MED_SMALL_BUFF)
        br = Brace(sr, DOWN, buff=MED_SMALL_BUFF)
        br_text = Text("Equation 1").next_to(br, DOWN)

        self.play (AnimationGroup(
            Flash(lines[-1], flash_radius=1.8, num_lines=20),
            Create(sr),
            Create(VGroup(br, br_text)),
            lag_ratio=0.8
            ))
            
        self.wait(2)
      


