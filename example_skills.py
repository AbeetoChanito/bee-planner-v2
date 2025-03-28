def main():
    from robot_interface import RobotInterface

    robot = RobotInterface(width=10, height=10)
    
    t = RobotInterface.TILE_SIZE

    robot.set_pose((0, -2 * t, 0))
    robot.move_to_point((t, -2 * t), reversed=True)
    robot.delay(500)
    robot.move_to_point((t, -2 * t))
    robot.move_to_point((2 * t, -t))
    robot.move_to_point((2 * t, -2.5 * t - 7 / 2 + 17.5 / 2))
    robot.move_to_point((2 * t, -2 * t), reversed=True)
    robot.move_to_point((2.5 * t, -2 * t))
    robot.move_to_point((2 * t, -2 * t), reversed=True)
    robot.turn_to_heading(-45)
    robot.move_distance(-15)

    print(robot.get_commands())
    robot.render("v5rcskills.png", -90)

if __name__ == '__main__':
    main()