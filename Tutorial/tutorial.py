class Pet:
    def __init__(self, name, species):
        self.name = name
        self.species = species


dog = Pet(name="Buddy", species="Dog")
print(dog)

dog = Pet("Buddy", "Dog")
print(dog)
cat = Pet("Whiskers", "Cat")
print(cat)
