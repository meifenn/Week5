import random
class MarbleBag:

    def __init__(self,oriBag):
        self.bag=[]
        self.Oribag=oriBag

    def draw(self):
        if not self.bag:
            self.bag=self.Oribag.copy()
            random.shuffle(self.bag)
        return self.bag.pop()
    
class Success:
    
    def attempt(success_rate=50):
        assert success_rate>=0 and success_rate<=100,"success rate must be between 0-100"
        p=random.uniform(0,100)
        base_probability=success_rate
        if p< base_probability:
            print("successful")
            return True
        else:
            print("failed")
            return False
        
class Progressive:

    def __init__(self,success_rate,increment) -> None:
        self.base_success=success_rate
        self.current_success=self.base_success
        self.increment=increment

    def reset_prob(self):
        self.current_success=self.base_success

    def attempt(self):

        p=random.uniform(0,100)
        if p< self.current_success:
            print("successful"+ str(self.current_success))
            self.reset_prob()
            return True
        else:
            print("failed"+ str(self.current_success))
            self.current_success += self.increment
            return False
        
class FixRateProb:
    
    def __init__(self,prob,fixed_rate) -> None:
        self.attempt_count=0
        self.fixed_success=fixed_rate
        self.base_prob=prob
    
    def attempt(self):
        self.attempt_count+=1
        if self.attempt_count >= self.fixed_success:
            self.attempt_count=0
            return True
        roll = random.uniform(0,100)
        if roll<self.base_prob:
            self.attempt_count=0
            return True
        else:
            return False
        
class Predetermination():
    def __init__(self,max_attempts) -> None:
        self.attempts=0
        self.max_attempts=max_attempts

    def attempt(self):
        self.attempts=+ 1
        if self.attempts >= self.max_attempts:
            self.attempts=0
            return True
        return False