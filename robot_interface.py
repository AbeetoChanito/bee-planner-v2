import os
from copy import deepcopy

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import sys


class RobotInterface:
    WINDOW_SIZE: int = 700
    FIELD_WIDTH: float = 3600 / 25.6 + 4
    TILE_SIZE = 3600 / 6 / 25.4
    PX_TO_IN = WINDOW_SIZE / FIELD_WIDTH
    BEFORE_TRANS: int = 128
    AFTER_TRANS: int = 156

    def __init__(self, width: float, height: float):
        self.x: float = 0
        self.y: float = 0
        self.theta: float = 0
        self.command_list: list[command.BaseCommand] = []
        self.width = width
        self.height = height

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}, Theta: {self.theta}"

    def get_states(self, state: int) -> tuple[list['RobotInterface'], 'command.BaseCommand | None']:
        if state == 0:
            return [deepcopy(self)], None
        latest_command = self.command_list[state - 1]
        return [latest_command.past_robot, latest_command.get_updated_robot_state()], latest_command

    def get_new_robot_state(self) -> 'RobotInterface':
        if len(self.command_list) == 0:
            return deepcopy(self)
        return self.command_list[-1].get_updated_robot_state()

    def get_commands(self):
        return "".join([str(c) for c in self.command_list])

    def move_to_point(self, point: tuple[float, float], **kwargs) -> None:
        self.command_list.append(command.MoveToPoint(self.get_new_robot_state(), point, **kwargs))

    def turn_to_point(self, point: tuple[float, float], **kwargs) -> None:
        self.command_list.append(command.TurnToPoint(self.get_new_robot_state(), point, **kwargs))

    def turn_to_heading(self, heading: float, **kwargs) -> None:
        self.command_list.append(command.TurnToHeading(self.get_new_robot_state(), heading, **kwargs))

    def move_distance(self, distance: float, **kwargs) -> None:
        self.command_list.append(command.MoveDistance(self.get_new_robot_state(), distance, **kwargs))

    def add_text(self, text: str):
        self.command_list.append(command.TextCommand(self.get_new_robot_state(), text))

    def set_pose(self, pose: tuple[float, float, float]) -> None:
        self.command_list.append(command.SetPose(self.get_new_robot_state(), pose))

    def delay(self, time: int):
        self.command_list.append(command.Delay(self.get_new_robot_state(), time))

    @staticmethod
    def convert_to_field(x: float, y: float) -> tuple[int, int]:
        x *= RobotInterface.PX_TO_IN
        y *= RobotInterface.PX_TO_IN * -1
        x += RobotInterface.WINDOW_SIZE / 2
        y += RobotInterface.WINDOW_SIZE / 2
        return int(x), int(y)

    @staticmethod
    def render_robot(robot: 'RobotInterface', window: pygame.Surface, trans: int) -> None:
        width = robot.width * RobotInterface.PX_TO_IN
        height = robot.height * RobotInterface.PX_TO_IN
        rect = pygame.Surface((width, height), pygame.SRCALPHA)
        rect.fill((0, 0, 0, trans))
        pygame.draw.line(rect, (255, 0, 0), (width / 2, 0), (width / 2, height / 2), 5)
        rotated_surface = pygame.transform.rotate(rect, -robot.theta)  # Counterclockwise
        rotated_rect = rotated_surface.get_rect(center=RobotInterface.convert_to_field(robot.x, robot.y))
        window.blit(rotated_surface, rotated_rect.topleft)

    def render(self, image_path: str, field_transform: int) -> None:
        pygame.init()

        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (self.WINDOW_SIZE, self.WINDOW_SIZE))
        image = pygame.transform.rotate(image, -field_transform)

        window = pygame.display.set_mode(image.get_size())
        pygame.display.set_caption(f"Field image: {image_path}")

        clock = pygame.time.Clock()

        running = True
        current_state = 0
        total_states = len(self.command_list) + 1

        pygame.font.init()
        font = pygame.font.Font("font.ttf", 20)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_state = (current_state - 1) % total_states
                    elif event.key == pygame.K_RIGHT:
                        current_state = (current_state + 1) % total_states

            window.blit(image, (0, 0))

            states, c = self.get_states(current_state)
            if len(states) == 1:
                RobotInterface.render_robot(states[0], window, self.BEFORE_TRANS)
            elif isinstance(c, command.TextCommand):
                RobotInterface.render_robot(states[1], window, self.AFTER_TRANS)
            else:
                RobotInterface.render_robot(states[0], window, self.BEFORE_TRANS)
                RobotInterface.render_robot(states[1], window, self.AFTER_TRANS)

            current_state_str = "Start" if current_state == 0 else str(c)
            lines = current_state_str.split("\n")
            for i, line in enumerate(lines):
                text = font.render(line, True, (255, 255, 255))
                window.blit(text, (30, 20 + i * 20))

            pygame.display.update()

            clock.tick(60)

        pygame.quit()
        sys.exit()


import command
