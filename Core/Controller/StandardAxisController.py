from Services import StandardAxisService
def create_standard_structure(myproject, device):
    try:
        print('Creating standard structure')
        StandardAxisService.create_standard_structure(myproject, device)
    except Exception as e: 
        print('Error creating standard structure: ', e)
        return