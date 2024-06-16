from Map import Map
from globals import Config
import pygame
from widgets import *


class MapEditor:
    actors = {
        "Wall": {"color": (0, 0, 0)},
        "Agent": {"color": (0, 150, 0)},
        "Goal": {"color": (255, 200, 0)},
        "Trail": {"color": (180, 0, 200)},
    }
    drag = False

    def __init__(self, map: Map, config: Config):
        self.map = map
        self.config = config
        self.drawmodes = ["Wall", "Agent", "Goal", "Clear"]
        self.mode = 0

        # Start window
        pygame.init()
        self.window = pygame.display.set_mode(config.window_size)
        pygame.time.Clock().tick(60)
        if config.font is not None and os.path.exists(config.font):
            self.font = pygame.font.Font(config.font, config.font_size)
        else:
            print(f"Warning: Font {config.font} not found, using default font")
            self.font = pygame.font.Font(None, config.font_size)
        self.running = True

        # Create Buttons
        self.mode_buttons: list[Button] = [
            ImageButton(10, self.config.window_height + 10, "images/wall.png", 30, 30),
            ImageButton(50, self.config.window_height + 10, "images/agent.png", 30, 30),
            ImageButton(90, self.config.window_height + 10, "images/goal.png", 30, 30),
            ImageButton(
                130, self.config.window_height + 10, "images/clear.png", 30, 30
            ),
        ]
        self.save_button = TextButton(
            self.config.window_width - 100 - 10,
            self.config.window_height + 10,
            100,
            30,
            (0, 255, 0),
            self.font,
            "Save",
        )

        self.clear_button = TextButton(
            self.config.window_width - 100 - 10 - 100 - 10,
            self.config.window_height + 10,
            100,
            30,
            (0, 255, 0),
            self.font,
            "Clear",
        )

        # Create draw mode status text
        self.status = self.font.render(
            f"Mode: {self.drawmodes[self.mode]}", True, (255, 255, 255)
        )
        self.status_rect = self.status.get_rect(
            center=(self.config.window_width / 2, self.config.window_height + 25)
        )

        # Grid hash
        self.grid: dict[tuple[int, int], str] = {}

    def create_grid(self):
        grid = {}
        grid[(self.map.agent[0], self.map.agent[1])] = "Agent"
        grid[(self.map.goal[0], self.map.goal[1])] = "Goal"
        for wall in self.map.walls:
            grid[(wall[0], wall[1])] = "Wall"
        return grid

    def draw(self):
        self.window.fill((0, 0, 0))

        # Draw the grid
        pygame.draw.rect(
            self.window,
            (255, 255, 255),
            (0, 0, self.config.window_width, self.config.window_height),
        )
        for x in range(self.config.grid_width):
            for y in range(self.config.grid_height):
                rect = pygame.Rect(
                    x * self.config.cell_size,
                    y * self.config.cell_size,
                    self.config.cell_size,
                    self.config.cell_size,
                )
                pygame.draw.rect(self.window, (200, 200, 200), rect, 1)

        # Draw the actors
        self.grid = self.create_grid()
        for pos, mode in self.grid.items():
            pygame.draw.rect(
                self.window,
                self.actors[mode]["color"],
                (
                    pos[0] * self.config.cell_size,
                    pos[1] * self.config.cell_size,
                    self.config.cell_size,
                    self.config.cell_size,
                ),
            )

        # Draw the buttons
        for button in self.mode_buttons:
            button.draw(self.window)

        # Draw the save button
        self.save_button.draw(self.window)

        # Draw the clear button
        self.clear_button.draw(self.window)

        # Draw the status
        self.window.blit(self.status, self.status_rect)

        # Update the display
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for i in range(len(self.mode_buttons)):
                    if self.mode_buttons[i].rect.collidepoint(x, y):
                        self.mode = i
                        return
                if self.save_button.rect.collidepoint(x, y):
                    self.map.save()
                    self.running = False
                    return
                if self.clear_button.rect.collidepoint(x, y):
                    self.map.walls.clear()
                    return

            if event.type == pygame.MOUSEBUTTONDOWN or self.drag:
                self.drag = True
                x, y = pygame.mouse.get_pos()
                grid_x = x // self.config.cell_size
                grid_y = y // self.config.cell_size

                if grid_x < self.config.grid_width or grid_y < self.config.grid_height:
                    coord = [grid_x, grid_y]
                    if self.drawmodes[self.mode] == "Wall":
                        self.map.walls.append(coord)
                    if self.drawmodes[self.mode] == "Agent":
                        if coord in self.map.walls:
                            self.map.walls.remove(coord)
                        self.map.agent = coord
                    if self.drawmodes[self.mode] == "Goal":
                        if coord in self.map.walls:
                            self.map.walls.remove(coord)
                        self.map.goal = coord
                    if self.drawmodes[self.mode] == "Clear":
                        if coord in self.map.walls:
                            self.map.walls.remove(coord)

            if event.type == pygame.MOUSEBUTTONUP:
                self.drag = False

            # Keys 1-4 to change mode
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.mode = 0
                elif event.key == pygame.K_2:
                    self.mode = 1
                elif event.key == pygame.K_3:
                    self.mode = 2
                elif event.key == pygame.K_4:
                    self.mode = 3
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

        self.status = self.font.render(
            f"Mode: {self.drawmodes[self.mode]}", True, (255, 255, 255)
        )

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
