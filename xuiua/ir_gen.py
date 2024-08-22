from xdsl.dialects.builtin import ModuleOp


from xuiua.ast import (
    Item,
    Items,
)


class ModuleBuilder:
    module: ModuleOp

    def __init__(self):
        self.module = ModuleOp([])
        self.funcs = {}

    # region Item

    def build_item(self, item: Item) -> None:
        raise NotImplementedError

    # endregion

    def build_items(self, items: tuple[Item, ...]):
        for item in items:
            self.build_item(item)

    def build_module(self, items: Items):
        for item_tuple in items:
            self.build_items(item_tuple)

        return self.module


def build_module(items: Items):
    b = ModuleBuilder()
    b.build_module(items)
    return b.module
