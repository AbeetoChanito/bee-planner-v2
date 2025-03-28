import math
from abc import ABC, abstractmethod
from copy import deepcopy

from util import *


class FunctionNames:
    MOVE_TO_POINT = "MoveToPoint"
    MOVE_DISTANCE = "MoveDistance"
    TURN_TO_POINT = "TurnToPoint"
    TURN_TO_HEADING = "TurnToHeading"
    SET_POSE = "SetPose"
    DELAY = "pros::delay"


class BaseCommand(ABC):
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_updated_robot_state(self) -> 'RobotInterface':
        raise NotImplementedError

    @property
    def past_robot(self) -> 'RobotInterface':
        raise NotImplementedError


class TextCommand(BaseCommand):
    def __init__(self, robot: 'RobotInterface', code: str):
        self.robot = robot
        self.code = code

    def __str__(self):
        return self.code

    def get_updated_robot_state(self) -> 'RobotInterface':
        return deepcopy(self.robot)

    @property
    def past_robot(self) -> 'RobotInterface':
        return self.robot


class TurnToHeading(BaseCommand):
    def __init__(self, robot: 'RobotInterface', heading: float, **kwargs):
        self.robot = robot
        self.heading = heading
        self.kwargs = kwargs

    def __str__(self) -> str:
        return f"{FunctionNames.TURN_TO_HEADING}({self.heading}, {build_args(self.kwargs)});\n"

    def get_updated_robot_state(self) -> 'RobotInterface':
        modified_robot = deepcopy(self.robot)
        modified_robot.theta = self.heading
        return modified_robot

    @property
    def past_robot(self) -> 'RobotInterface':
        return self.robot


class TurnToPoint(BaseCommand):
    def __init__(self, robot: 'RobotInterface', point: tuple[float, float], **kwargs):
        self.robot = robot
        self.point = point
        self.kwargs = kwargs

    def __str__(self):
        x, y = self.point
        return f"{FunctionNames.TURN_TO_POINT}({x}, {y}, {build_args(self.kwargs)});\n"

    def get_updated_robot_state(self) -> 'RobotInterface':
        x, y = self.point
        modified_robot = deepcopy(self.robot)
        reversed_status = self.kwargs.get('reversed', False)
        modified_robot.theta = radians_to_degrees(math.atan2(x - self.robot.x, y - self.robot.y)) + (
            180 if reversed_status else 0)
        return modified_robot

    @property
    def past_robot(self) -> 'RobotInterface':
        return self.robot


class MoveDistance(BaseCommand):
    def __init__(self, robot: 'RobotInterface', distance: float, **kwargs):
        self.robot = robot
        if kwargs.get('reversed', False):
            distance = -distance
        self.distance = distance
        heading_radians = degrees_to_radians(self.robot.theta)
        self.target_x = self.robot.x + self.distance * math.sin(heading_radians)
        self.target_y = self.robot.y + self.distance * math.cos(heading_radians)
        self.kwargs = kwargs

    def __str__(self) -> str:
        return f"{FunctionNames.MOVE_DISTANCE}({self.distance}, {build_args(self.kwargs)});\n"

    def get_updated_robot_state(self) -> 'RobotInterface':
        modified_robot = deepcopy(self.robot)
        modified_robot.x = self.target_x
        modified_robot.y = self.target_y
        return modified_robot

    @property
    def past_robot(self) -> 'RobotInterface':
        return self.robot


class MoveToPoint(BaseCommand):
    def __init__(self, robot: 'RobotInterface', point: tuple[float, float], **kwargs):
        self.robot = robot
        self.x, self.y = point
        self.distance = math.hypot(self.x - self.robot.x, self.y - self.robot.y)
        self.kwargs = kwargs

    def __str__(self) -> str:
        return f"{FunctionNames.MOVE_TO_POINT}({self.x}, {self.y}, {build_args(self.kwargs)});\n"

    def get_updated_robot_state(self) -> 'RobotInterface':
        reversed_status = self.kwargs.get('reversed', False)
        modified_robot = deepcopy(self.robot)
        modified_robot = TurnToPoint(modified_robot, (self.x, self.y),
                                     reversed=reversed_status).get_updated_robot_state()
        modified_robot = MoveDistance(modified_robot, self.distance, reversed=reversed_status).get_updated_robot_state()
        return modified_robot

    @property
    def past_robot(self) -> 'RobotInterface':
        return self.robot


class SetPose(BaseCommand):
    def __init__(self, robot: 'RobotInterface', pose: tuple[float, float, float]):
        self.robot = robot
        self.pose = pose

    def __str__(self) -> str:
        x, y, theta = self.pose
        return f"{FunctionNames.SET_POSE}({x}, {y}, {theta});\n"

    def get_updated_robot_state(self) -> 'RobotInterface':
        x, y, theta = self.pose
        modified_robot = deepcopy(self.robot)
        modified_robot.x = x
        modified_robot.y = y
        modified_robot.theta = theta
        return modified_robot

    @property
    def past_robot(self) -> 'RobotInterface':
        return self.robot


class Delay(TextCommand):
    def __init__(self, robot: 'RobotInterface', delay_time: int):
        super().__init__(robot, f"{FunctionNames.DELAY}({delay_time});\n")


from robot_interface import RobotInterface
