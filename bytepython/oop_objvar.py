class Robot:
    population = 0

    def __init__(self, name):
        self.name = name
        print("Initializing {}".format(self.name))
        Robot.population += 1

    def die(self):
        print("{} is being destroyed!".format(self.name))
        Robot.population -= 1
        if Robot.population == 0:
            print("{} was the last one!".format(self.name))
        else:
            print("There are still {:d} robots working!".format(self.__class__.population))

    def say_hi(self):
        print("Hello, my name is {}".format(self.name))
        return self

    @classmethod
    def how_many(cls):
        print("We have {:d} robots!".format(Robot.population))


r1 = Robot('R1').say_hi()
Robot.how_many()
r2 = Robot('R2').say_hi()
Robot.how_many()

r1.die()
Robot.how_many()

print("self.population =", r1.population)


