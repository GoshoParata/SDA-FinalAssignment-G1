class Item:
    valid_colors = ["red", "blue", "yellow", "green"]
    valid_shapes = ["triangle", "square", "circle"]

    def __init__(self, color, shape, position):
        if color not in Item.valid_colors:
            raise ValueError(f"Invalid color: {color}. Valid options are: {Item.valid_colors}")
        if shape not in Item.valid_shapes:
            raise ValueError(f"Invalid shape: {shape}. Valid options are: {Item.valid_shapes}")

        self.__color = color
        self.__shape = shape
        self.__position = position

    def getInfo(self):
        return (self.__color, self.__shape, self.__position)
