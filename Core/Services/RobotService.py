from . import OpennessService
from . import UDTService
def create_robot_structure(device, robot_name, robot_type):
    group_name = robot_name + '_group'
    robot_group = OpennessService.create_group(device, group_name, None)
    import_robot_bk(device, robot_group.Blocks, robot_type)

def import_robot_bk(device, robot_group, robot_type : str):
    robot_type = robot_type.upper()
    if robot_type == 'ABB':
        print('Importing ABB robot block')
        #TODO: Trocar rota pelo caminho no servidor
        abb_bk_path = r"C:\Users\Willian\Desktop\exported_bk\bk_abb.xml"
        abb_dependencies = r"C:\Users\Willian\Desktop\exported_bk\bk_dp"
        udts = UDTService.list_udt_from_bk(abb_bk_path)
        print(udts)
        for udt in udts:
            udt_path = abb_dependencies + '\\' + udt + '.xml'
            OpennessService.import_data_type(device, udt_path)
        OpennessService.import_block(robot_group, abb_bk_path)
    elif robot_type == 'FANUC':
        print('Importing FANUC robot block')
        #TODO: Trocar rota pelo caminho no servidor
        OpennessService.import_block(robot_group, 123, r"C:\Users\Willian\Desktop\exported_bk\bk_fanuc.xml")