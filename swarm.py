# class for each robot object
class Robot():
    def __init__(self,pos,id=0):
        self.pos=pos
        self.id = id
    def get_id(self):
        return self.id;
    def set_id(self,id):
        self.id=id;

# class for the swarm as a whole
class Swarm():
    def __init__(self,swarm_map={},ids=[],latest_id=0):
        self.swarm_map=swarm_map
        self.ids = ids
        self.latest_id=latest_id
    def add_bot(self, robot):
        if robot not in self.swarm_map:
            self.latest_id = self.latest_id + 1;
            robot.set_id(self.latest_id)
            self.swarm_map[robot]=[]
    def list_bots(self):
        for bot in self.swarm_map:
            print(bot)
    def list_paths(self):
        for bot in self.swarm_map:
            for neighbor in self.swarm_map[bot]:
                print(bot.get_id(), "->", neighbor.get_id())
    def connect_bots(self,bot1,bot2):
        self.swarm_map[bot1].append(bot2)

bot1 = Robot((50,50))
bot2 = Robot((75,50))
bot3 = Robot((50,150))
swarm = Swarm()

swarm.add_bot(bot1)
swarm.add_bot(bot2)
swarm.add_bot(bot3)

swarm.connect_bots(bot1,bot2)
swarm.connect_bots(bot1,bot3)

swarm.list_paths()
