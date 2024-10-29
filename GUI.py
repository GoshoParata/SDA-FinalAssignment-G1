import pygame
from Item import Item

class GUI:
    def __init__(self, isItemSelected, itemOptions, isProcessLoading, errorMessage):
        self.__isItemSelected = isItemSelected
        self.__itemOptions = itemOptions
        self.__isProcessLoading = isProcessLoading
        self.__errorMessage = errorMessage
        self.__items = []

    def setItems(self, items):
        self.__items = items

    def renderItems(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Render Items')
        screen.fill((0, 0, 0))  # Black background

        unique_items = []
        seen_items = set()
        for item in self.__items:
            item_info = (item.getInfo()[0], item.getInfo()[1])  # Only consider color and shape for uniqueness
            if item_info not in seen_items:
                seen_items.add(item_info)
                unique_items.append(item_info)

        num_items = len(unique_items)
        if num_items == 0:
            pygame.display.flip()
            return

        item_width = 150  # Width of each item including spacing
        total_width = item_width * num_items
        start_x = (800 - total_width) // 2  # Center the items horizontally
        y_position = 300  # Fixed y position for all items

        x_offset = start_x
        for item_info in unique_items:
            color = self.getColor(item_info[0])
            shape = item_info[1]
            self.drawShape(screen, shape, color, (x_offset + item_width // 2, y_position))
            x_offset += item_width  # Move to the right for the next item

        pygame.display.flip()  # Update the display

        # Event loop to keep the window open
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.time.delay(100)  # Add a delay to prevent high CPU usage

        pygame.quit()

    def getColor(self, color_name):
        colors = {
            "red": (255, 0, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "green": (0, 255, 0)
        }
        return colors.get(color_name, (255, 255, 255))  # Default to white if color not found

    def drawShape(self, screen, shape, color, position):
        if shape == "triangle":
            pygame.draw.polygon(screen, color, [
                (position[0], position[1] - 40),  # Top point
                (position[0] - 40, position[1] + 40),  # Bottom left point
                (position[0] + 40, position[1] + 40)  # Bottom right point
            ])
        elif shape == "square":
            pygame.draw.rect(screen, color, (position[0] - 40, position[1] - 40, 80, 80))  # Centered larger square
        elif shape == "circle":
            pygame.draw.circle(screen, color, position, 40)  # Larger circle

    def itemSelected(self):
        """Handles item selection."""
        pass

    def throwError(self):
        """Handles error throwing."""
        pass

    def initCamera(self):
        """Initializes the camera."""
        pass

    def initDobot(self):
        """Initializes the Dobot."""
        pass

    def exit(self):
        """Exits the application."""
        pygame.quit()

# Example usage
items = [
    Item("red", "triangle", (50, 50)),
    Item("blue", "square", (150, 50)),
    Item("green", "circle", (250, 50)),
    Item("red", "triangle", (78, 50)),
    Item("red", "triangle", (100, 50)),
]

gui = GUI(False, [], False, "")
gui.setItems(items)
gui.renderItems()
