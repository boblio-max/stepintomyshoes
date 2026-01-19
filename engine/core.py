class SceneManager:

    def __init__(self):
        self.current_scene = None

    def change_scene(self, scene_func):
        """Switch to a new scene."""
        self.current_scene = scene_func

    def run(self):
        """Run the current scene in a loop."""
        while True:
            if self.current_scene:
                # Pass the SceneManager instance to the scene callable
                try:
                    self.current_scene(self)
                except TypeError:
                    # If the scene expects no arguments, call without
                    self.current_scene()
            else:
                break
