class Loger:

    def __init__(self):
        
        print("Welcome to logging system")

    def welcome(self):
        
        print("Starting PhotoDataChanger")

    def loaded(self, filename):

        print(f"Image {filename} have been loaded to system")
    
    def start_edit(self, filename):

        print(f"Starting editing {filename}")
    
    def no_arg(self, filename):

        print(f"Editing image {filename} was aborted")
        print("No arguments to edit were given")