from . import OpennessService
def create_robot_structure(robot_name, robot_type):
    group_name = robot_name + '_group'
    robot_group = OpennessService.create_group(group_name)
    import_robot_bk(robot_group.Blocks, robot_type)

def import_robot_bk(robot_group, robot_type):
    if robot_type == 'ABB':
        OpennessService.import_block(robot_group, r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\robots\ABB.xml")
    elif robot_type == 'Fanuc':
        OpennessService.import_block(robot_group, r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\robots\Fanuc.xml")