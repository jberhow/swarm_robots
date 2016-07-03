class Robot():
    def __init__(self,pos):
        self.pos=pos

class Swarm():
    def __init__(self,swarm_map={}):
        self.swarm_map=swarm_map
    def add_bot(self, robot):
        if robot not in self.swarm_map:
            self.swarm_map[robot]=[]

bot1 = Robot((50,50))
swarm = Swarm()

swarm.add_bot(bot1)
