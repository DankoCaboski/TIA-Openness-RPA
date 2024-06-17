from . import OpennessService
def create_robot_structure(device, robot_name, robot_type):
    group_name = robot_name + '_group'
    robot_group = OpennessService.create_group(device, group_name, None)
    import_robot_bk(robot_group.Blocks, robot_type)

def import_robot_bk(robot_group, robot_type : str):
    robot_type = robot_type.upper()
    if robot_type == 'ABB':
        print('Importing ABB robot block')
        OpennessService.import_block(robot_group, r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\robots\bk_abb.xml")
    elif robot_type == 'FANUC':
        print('Importing FANUC robot block')
        OpennessService.import_block(robot_group, 123, r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\robots\bk_fanuc.xml")