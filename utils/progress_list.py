from manim import *


# See: https://slama.dev/manim/objects-animations-and-plugins/

# General Tips to create custom Mobject classes
# - Inherit from Mobject or VMobject
#  - call super().__init__() in constructor
#  - call self.add(list_of_custom_composed_mobjects) 
# - Define custom methods for behaviors
#  - return Animation | AnimationGroup when you want that behavior to be animated 
#  - in the caller code, this can be passed into self.play()



class ProgressList(VMobject):
    """Represents a Progress List for a specified number of items"""
    
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

