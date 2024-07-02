from Services import IHMService
def create_IHM_structure(myproject, device):
    try:
        print('Creating screens structure')
        IHMService.create_IHM_structure(myproject, device)
    except Exception as e: 
        print('Error creating screens structure: ', e)
        return