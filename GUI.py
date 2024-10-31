import pygame
from Item import Item
from Camera import Camera

class GUI:
    def __init__(self):
        self.__items = []
        self.__shape_positions = []
        self.__selected_shapes = []
        self.__selected_coordinates = []
        self.camera = Camera()
        self.button_rect = pygame.Rect(650, 550, 140, 40)
        self.screen = None

    def setItems(self, items):
        self.__items = items

    def renderItems(self):
        if not pygame.get_init():
            pygame.init()
        if not self.screen:
            self.screen = pygame.display.set_mode((800, 600))
            
        pygame.display.set_caption('Render Items')
        self.screen.fill((0, 0, 0))  # Black background

        # Get currently visible shapes and colors
        visible_items = {(item.getInfo()[0], item.getInfo()[1]) for item in self.__items}
        
        # Filter out selections that are no longer visible
        self.__selected_shapes = [
            (shape, color) for shape, color in self.__selected_shapes 
            if (shape, color) in visible_items
        ]

        unique_items = []
        seen_items = set()
        for item in self.__items:
            item_info = (item.getInfo()[0], item.getInfo()[1])  # Only consider shape and color for uniqueness
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

        self.__shape_positions = []  # Clear previous positions

        x_offset = start_x
        for item_info in unique_items:
            shape = item_info[0]
            color = item_info[1]
            position = (x_offset + item_width // 2, y_position)
            self.__shape_positions.append((shape, position, item_width, 80, color))  # Store shape, position, size, and color
            x_offset += item_width  # Move to the right for the next item

        # Draw shapes with outlines if selected
        for shape, position, width, height, color in self.__shape_positions:
            if (shape, color) in self.__selected_shapes:
                self.drawShape(self.screen, shape, (255, 255, 255), position, outline=True)
            self.drawShape(self.screen, shape, self.getColor(color), position)

        # Draw the button
        self.drawButton(self.screen)

        pygame.display.flip()  # Update the display

        # Update coordinates after filtering selections
        self.updateSelectedCoordinates()

    def getColor(self, color_name):
        colors = {
            "red": (255, 0, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "green": (0, 255, 0)
        }
        return colors.get(color_name, (255, 255, 255))  # Default to white if color not found

    def drawShape(self, screen, shape, color, position, outline=False):
        size_offset = 5 if outline else 0
        if shape == "triangle":
            pygame.draw.polygon(screen, color, [
                (position[0], position[1] - 40 - size_offset),  # Top point
                (position[0] - 40 - size_offset, position[1] + 40 + size_offset),  # Bottom left point
                (position[0] + 40 + size_offset, position[1] + 40 + size_offset)  # Bottom right point
            ])
        elif shape == "square":
            pygame.draw.rect(screen, color, (position[0] - 40 - size_offset, position[1] - 40 - size_offset, 80 + 2 * size_offset, 80 + 2 * size_offset))  # Centered larger square
        elif shape == "circle":
            pygame.draw.circle(screen, color, position, 40 + size_offset)  # Larger circle

    def drawButton(self, screen):
        """Draws the 'Run DoBot' button."""
        pygame.draw.rect(screen, (255, 0, 0), self.button_rect)  # Red button
        font = pygame.font.Font(None, 36)
        text = font.render('Run DoBot', True, (255, 255, 255))
        screen.blit(text, (self.button_rect.x + 10, self.button_rect.y + 5))

    def itemSelected(self, mouse_pos):
        """Handles item selection."""
        was_selected = False
        for shape, position, width, height, color in self.__shape_positions:
            if shape == "triangle":
                if self.isPointInTriangle(mouse_pos, position):
                    self.toggleSelection(shape, color)
                    was_selected = True
            elif shape == "square":
                if self.isPointInRect(mouse_pos, position, width, height):
                    self.toggleSelection(shape, color)
                    was_selected = True
            elif shape == "circle":
                if self.isPointInCircle(mouse_pos, position, 40):
                    self.toggleSelection(shape, color)
                    was_selected = True
        
        # Update coordinates if something was selected
        if was_selected:
            self.updateSelectedCoordinates()
            self.renderItems()

    def toggleSelection(self, shape, color):
        """Toggles the selection of a shape."""
        if (shape, color) in self.__selected_shapes:
            self.__selected_shapes.remove((shape, color))
        else:
            self.__selected_shapes.append((shape, color))
        self.updateSelectedCoordinates()
        self.renderItems()  # Re-render items to update the outline

    def updateSelectedCoordinates(self):
        """Updates the list of selected coordinates."""
        self.__selected_coordinates = []
        for shape, color in self.__selected_shapes:
            self.__selected_coordinates.extend([item.getInfo()[2] for item in self.__items if item.getInfo()[0] == shape and item.getInfo()[1] == color])
        # print(f"Selected coordinates: {self.__selected_coordinates}")

    def getSelectedCoordinates(self):
        """Returns the stored coordinates."""
        return self.__selected_coordinates

    def isPointInTriangle(self, point, position):
        # Barycentric technique to check if point is in triangle
        px, py = point
        x1, y1 = position[0], position[1] - 40
        x2, y2 = position[0] - 40, position[1] + 40
        x3, y3 = position[0] + 40, position[1] + 40

        denominator = ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))
        a = ((y2 - y3) * (px - x3) + (x3 - x2) * (py - y3)) / denominator
        b = ((y3 - y1) * (px - x3) + (x1 - x3) * (py - y3)) / denominator
        c = 1 - a - b

        return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1

    def isPointInRect(self, point, position, width, height):
        px, py = point
        rx, ry = position[0] - width // 2, position[1] - height // 2
        return rx <= px <= rx + width and ry <= py <= ry + height

    def isPointInCircle(self, point, position, radius):
        px, py = point
        cx, cy = position
        return (px - cx) ** 2 + (py - cy) ** 2 <= radius ** 2

    def initCamera(self):
        running = True
        if not self.screen:
            self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Camera Feed')

        while running:
            frame, gray_frame, edges, masks = self.camera.getImage()
            if frame is not None:
                detected_shapes, processed_frame = self.camera.processImage(frame, masks)
                items = [Item(shape, color, position) for shape, color, position in detected_shapes]
                self.setItems(items)
                self.renderItems()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.button_rect.collidepoint(mouse_pos):
                        self.updateSelectedCoordinates()  # Update before running
                        self.runDobot()
                    else:
                        self.itemSelected(mouse_pos)

            pygame.time.delay(100)  # Add a delay to prevent high CPU usage

        self.camera.release()
        pygame.quit()

    def runDobot(self):
        """Default runDobot implementation that can be overridden"""
        self.updateSelectedCoordinates()  # Ensure coordinates are up to date
        selected_coordinates = self.getSelectedCoordinates()
        print(f"Running DoBot with coordinates: {selected_coordinates}")

    def exit(self):
        """Exits the application and cleans up resources."""
        self.camera.release()
        if pygame.get_init():
            pygame.quit()
        if hasattr(self, 'runDobot'):
            self.runDobot = None

if __name__ == "__main__":
    gui = GUI(False, [], False, "")
    gui.initCamera()
