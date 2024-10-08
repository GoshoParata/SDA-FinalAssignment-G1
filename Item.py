class Item:
    valid_colors = ["red", "blue", "yellow", "green"]
    valid_shapes = ["triangle", "square", "circle"]

    def __init__(self, color: str, shape: str, position: int, id: int):
        if color not in Item.valid_colors:
            raise ValueError(f"Invalid color: {color}. Valid options are: {Item.valid_colors}")
        if shape not in Item.valid_shapes:
            raise ValueError(f"Invalid shape: {shape}. Valid options are: {Item.valid_shapes}")
        
        self.color = color
        self.shape = shape
        self.position = position
        self.id = id

    def getPosition(self) -> int:
        """Returns the position of the item."""
        return self.position

    def getInfo(self) -> str:
        """Returns a formatted string with information about the item."""
        return f"Item ID: {self.id}, Color: {self.color}, Shape: {self.shape}, Position: {self.position}"
