from typing import Union
from typing import List

import os

from libqtile import bar, widget
import libqtile
import libqtile.widget
from libqtile.log_utils import logger
from libqtile.lazy import lazy
from libqtile.config import Screen
from libqtile.log_utils import logger

from functions import PWA, Functions
# widget_defaults = dict(
#     font="Ubuntu Mono",
#     fontsize = 12,
#     padding = 2,
#     background=colors[2]
# )

barSize = 22
barSizeFontOffset = 5

# extension_defaults = widget_defaults.copy()
def spawn(com:str):
    logger.warning(f"Trying to spawn command '{com}'")
    try:
        lazy.spawncmd(com)
    except Exception:
        logger.exception("message")

def make_right_widget(
        widget_to_add,
        foreground: List[str],
        background: List[str],
        previous_background: List[str],
        icon: Union[str, None]= None
    ):
        separator_style = (' ', barSize - 2)
        # separator_style = ('<b></b>', barSize + 10)
        widgets = [
            widget.TextBox(
                text= separator_style[0],
                background=previous_background,
                foreground=background,
                padding=0,
                fontsize= separator_style[1],
            )]
        if icon:
            widgets += [
            widget.TextBox(
                text=icon,
                foreground=foreground,
                background=background,
                padding=0,
                mouse_callbacks={
                    "Button1": lambda : spawn("pavucontrol")}
            )]
        if type(widget_to_add) == list:
            widgets += widget_to_add
        else:
            widgets += [widget_to_add]
        return widgets


class MyWidgets:
    def __init__(self):
        self.colors = [["#292d3e", "#292d3e"],  # panel background
                       # background for current screen tab
                       ["#434758", "#434758"],
                       ["#ffffff", "#ffffff"],  # font color for group names
                       # border line color for current tab
                       ["#bc13fe", "#bc13fe"],  # Group down color
                       # border line color for other tab and odd widgets
                       ["#8d62a9", "#8d62a9"],
                       ["#668bd7", "#668bd7"],  # color for the even widgets
                       ["#e1acff", "#e1acff"],  # window name

                       ["#000000", "#000000"],
                       ["#AD343E", "#AD343E"],
                       ["#f76e5c", "#f76e5c"],
                       ["#F39C12", "#F39C12"],
                       ["#F7DC6F", "#F7DC6F"],
                       ["#cc050F", "#cc050F"],
                       ["#33bb5e", "#33bb5e"],
                       ["#33dd5e", "#33dd5e"],
                       ["#f1ffff", "#f1ffff"],
                       ["#4c566a", "#4c566a"], ]

        self.termite = "termite"

    def init_widgets_list(self):
        '''
        Function that returns the desired widgets in form of list
        '''
        widgets_list = [
            widget.Sep(
                linewidth=0,
                padding=6,
                foreground=self.colors[2],
                background=self.colors[0]
            ),
            # widget.Image(
            #     filename="~/.config/qtile/icons/terminal-iconx14.png",
            #     mouse_callbacks={
            #         'Button1': lambda: spawn('dmenu_run -p "Run: "')}
            # ),
             widget.TextBox(
                text=' ',
                background=self.colors[0],
                foreground=self.colors[13],
                padding=0,
                fontsize=barSize - barSizeFontOffset,
                mouse_callbacks= {'Button1': Functions.open_main_menu()}
            ),
            widget.Sep(
                linewidth=0,
                padding=5,
                foreground=self.colors[2],
                background=self.colors[0]
            ),
            widget.GroupBox(
                font="Ubuntu Bold",
                fontsize=12,
                margin_y=2,
                margin_x=0,
                padding_y=5,
                padding_x=3,
                borderwidth=3,
                active=self.colors[-2],
                inactive=self.colors[-1],
                # rounded=True,
                rounded=False,
                # highlight_color=self.colors[9],
                # highlight_method="line",
                highlight_method='block',
                urgent_alert_method='block',
                # urgent_border=self.colors[9],
                this_current_screen_border=self.colors[9],
                this_screen_border=self.colors[4],
                other_current_screen_border=self.colors[0],
                other_screen_border=self.colors[0],
                foreground=self.colors[2],
                background=self.colors[0],
                disable_drag=True
            ),
            widget.WindowName(
                foreground=self.colors[6],
                background=self.colors[0],
                padding=0
            ),
            widget.Systray(
                background=self.colors[0],
                padding=5
            ),
        ]
        widgets_list += make_right_widget(
                            [
                                widget.CPU(
                                    foreground= self.colors[7],
                                    background= self.colors[5],
                                    format= '{load_percent:>5}%',
                                ),
                                widget.CPUGraph(
                                    graph_color= self.colors[0],
                                    margin_y= 0,
                                    border_width= 0,
                                    background= self.colors[5],
                                    fill_color= self.colors[0],
                                ),
                            ],
                            foreground=self.colors[7],
                            background=self.colors[5],
                            previous_background= self.colors[0],
                            icon= "  ",
                )
        widgets_list += make_right_widget(
                widget.ThermalSensor(
                    tag_sensor= "Tctl", # Use psensor to know the full list
                    background= self.colors[12],
                    foreground= self.colors[7],
                    foreground_alert= "ffff00",
                ),
                foreground=self.colors[7],
                background=self.colors[12],
                previous_background= self.colors[5],
                icon= "  "
                )
        widgets_list += make_right_widget(
                            [
                                widget.Net(
                                    foreground= self.colors[7],
                                    background= self.colors[14],
                                    # format= '{down}{down_suffix} ↓↑ {up}{up_suffix}',
                                    format= '{down:>10} ↓↑ {up:>10}',
                                    prefix= "M",
                                    use_bits= True,
                                ),
                                widget.NetGraph(
                                    graph_color= self.colors[0],
                                    margin_y= 0,
                                    border_width= 0,
                                    background= self.colors[14],
                                    fill_color= self.colors[0],
                                ),
                            ],
                            foreground=self.colors[7],
                            background=self.colors[14],
                            previous_background= self.colors[12],
                            icon= "  ",
                )
        widgets_list += make_right_widget(
                            widget.Memory(
                            foreground=self.colors[7],
                            background=self.colors[11],
                            mouse_callbacks={'Button1': lambda : lazy.spawncmd(self.termite + ' -e htop')},
                            padding=5
                        ),
                        foreground= self.colors[7],
                        background= self.colors[11],
                        previous_background= self.colors[14],
                        icon= " 🖬",
                    )
        widgets_list += make_right_widget(
                        widget.Volume(
                            foreground=self.colors[7],
                            background=self.colors[10],
                            padding=5
                        ),
                        foreground= self.colors[7],
                        background= self.colors[10],
                        previous_background= self.colors[11],
                        icon= "  ",
                    )
        widgets_list += make_right_widget(
                        [
                            widget.CurrentLayoutIcon(
                                custom_icon_paths=[os.path.expanduser(
                                    "~/.config/qtile/icons")],
                                foreground=self.colors[0],
                                background=self.colors[9],
                                padding=0,
                                scale=0.7
                            ),
                            widget.CurrentLayout(
                                foreground=self.colors[7],
                                background=self.colors[9],
                                padding=5
                            ),
                        ],
                        foreground= self.colors[7],
                        background= self.colors[9],
                        previous_background= self.colors[10],
                    )
        widgets_list += make_right_widget(
                             widget.Clock(
                                foreground=self.colors[7],
                                background=self.colors[8],
                                mouse_callbacks={
                                    "Button1": lambda qtile: qtile.cmd_spawn(PWA.calendar())},
                                format=" %H:%M "
                            ),
                        foreground= self.colors[7],
                        background= self.colors[8],
                        previous_background= self.colors[9],
                        icon= "  ",
                    )
        widgets_list += [
           widget.Sep(
                linewidth=0,
                padding=10,
                foreground=self.colors[0],
                background=self.colors[8]
            ),
        ]
        return widgets_list

    def init_widgets_screen(self):
        '''
        Function that returns the widgets in a list.
        It can be modified so it is useful if you  have a multimonitor system
        '''
        widgets_screen = self.init_widgets_list()
        return widgets_screen

    def init_widgets_screen2(self):
        '''
        Function that returns the widgets in a list.
        It can be modified so it is useful if you  have a multimonitor system
        '''
        widgets_screen2 = self.init_widgets_screen()
        return widgets_screen2

    def init_screen(self):
        '''
        Init the widgets in the screen
        '''
        return [Screen(top=bar.Bar(widgets=self.init_widgets_screen(), opacity=0.90, size=barSize)),
                Screen(top=bar.Bar(widgets=self.init_widgets_screen2(), opacity=0.90, size=barSize)),
                ]
