class Item:
    valid_colors = ["red", "blue", "yellow", "green"]
    valid_shapes = ["triangle", "square", "circle"]

    def __init__(self, color, shape, position, id):
        if color not in Item.valid_colors:
            raise ValueError(f"Invalid color: {color}. Valid options are: {Item.valid_colors}")
        if shape not in Item.valid_shapes:
            raise ValueError(f"Invalid shape: {shape}. Valid options are: {Item.valid_shapes}")

        self.__color = color
        self.__shape = shape
        self.__position = position
        self.__id = id

    def getPosition(self):
        
        return self.__position

    def getInfo(self):
        readyItem = {
            "color": self.__color,
            "shape": self.__shape,
            "position": self.__position,
            "id": self.__id
        }
        return readyItem
