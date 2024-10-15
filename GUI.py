import pygame
from Camera import Camera
from DoBotArm import DoBotArm
from Item import Item



class GUI:
    def __init__(self,isItemSelected, itemOptions, isProcessLoading, errorMessage):
        self.__isItemSelected = isItemSelected
        self.__itemOptions = itemOptions
        self.__isProcessLoading = isProcessLoading
        self.__errorMessage = errorMessage

    def addItem(self,itemColor, itemShape,itemPosition):
        newItem = Item(itemColor, itemShape, itemPosition)
        self.itemColor = Item.getInfo()["color"]
        self.itemShape = Item.getInfo()["shape"]
        self.itemPosition = Item.getPosition()
        return [newItem]

    def renderItems(self):
        
        pass

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