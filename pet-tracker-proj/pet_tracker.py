class Pet:
    def __init__(self, name, animal):
        self.name = name
        self.animal = animal   
    def speak(self):
        return f"{self.name} the {self.animal} says hello!"
    

# Command-line interaction
name = input("Enter your pet's name: ")
animal = input("What kind of animal is it? ")

my_pet = Pet(name,animal)
print(my_pet.speak())