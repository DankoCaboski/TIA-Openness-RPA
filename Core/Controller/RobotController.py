from Services import RobotService
def create_robot_structure(device, robot_name, robot_type):
    try:
        print('Creating robot structure')
        RobotService.create_robot_structure(device, robot_name, robot_type)
    except Exception as e: 
        print('Error creating robot structure: ', e)
        return