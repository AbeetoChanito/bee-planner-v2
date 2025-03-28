def main():
    import robot_interface

    robot = robot_interface.RobotInterface(width=15, height=17.5)

    robot.set_pose((0, -61.25, 0))
    robot.delay(500)
    robot.move_to_point((0, -48))
    robot.move_to_point((24, -48), reversed=True)
    robot.delay(500)
    robot.move_to_point((24, -24))
    robot.move_to_point((48, -24))
    robot.move_to_point((48, -60 - 7 / 2 + 17.5 / 2))
    robot.move_to_point((48, -48), reversed=True)
    robot.move_to_point((60, -48))
    robot.move_to_point((48, -48), reversed=True)
    robot.turn_to_heading(-45)
    robot.move_distance(-10)

    print(robot.get_commands())
    robot.render("v5rcskills.png", -90)

if __name__ == '__main__':
    main()