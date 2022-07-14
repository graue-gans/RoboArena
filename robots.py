# robots.py contains all robot classes

# use this like an abstract class or even interface in java
# so just give it the most basic things a robot needs
class Robot():
    """
    'Abstract' Robot class 
    Contains the basic fields and methods for every robot
    """
    
    def __init__(self, posx, posy, radius, alpha, color, a, a_alpha, a_max, a_alpha_max, v, v_alpha):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.alpha = alpha
        self.color = color
        self.a = a
        self.a_alpha = a_alpha
        self.a_max = a_max
        self.a_alpha_max = a_alpha_max
        self.v = v
        self.v_alpha = v_alpha

    # ...


# examplary classes that extend the 'abstract' Robot class
class BasicRobot(Robot):
    pass

class PlayerRobot(Robot):
    pass

class EnemyRobot(Robot):
    pass
