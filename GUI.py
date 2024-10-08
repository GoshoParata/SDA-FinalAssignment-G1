import pygame
from Camera import Camera
from DoBotArm import DoBotArm
from Item import Item



class GUI:
    def __init__(self):
        self._isItemSelected = False
        self._itemOptions = []
        self._isProcessLoading = False
        self._errorMessage = ""

    def getItemList(self):
        """Returns a list of items."""
        return []

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