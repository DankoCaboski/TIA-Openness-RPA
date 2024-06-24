from Services import MesaGiratoriaService
def create_mesa_structure(myproject, device, mesa_name, mesa_type, mg_blocks_value):
    try:
        print('Creating mesa structure')
        MesaGiratoriaService.create_mesa_structure(myproject, device, mesa_name, mesa_type, mg_blocks_value)
    except Exception as e: 
        print('Error creating mesa structure: ', e)
        return