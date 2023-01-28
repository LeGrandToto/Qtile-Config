from libqtile.config import Group
from icons import group_icons

class CreateGroups:
    group_names = group_icons 

    def init_groups(self):
        """
        Return the groups of Qtile
        """
        #### First and last
        default_layout = "monadtall"
        layout_lookup = {
                    0: "max",
                    len(self.group_names) - 1: "floating"
                }
        groups = [Group(name, layout= layout_lookup.get(index, default_layout)) for index, name in enumerate(self.group_names)]

        return groups

