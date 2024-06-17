from Services import RobotService
def create_robot_structure(robot_name, robot_type):
    group_name = robot_name + '_group'
    RobotService.create_robot_structure(group_name)