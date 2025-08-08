import time

class TimeWallet():
    def __init__(self, secs: int):
        '''
            Represent a seconds storage
            and data sender
        '''
        self.seconds: int = secs
        self.ID: str = hex(hash(self))

    def send(self, secs: int, obj):
        '''
            Send some seconds to other TimeWallet
            object when is possible
        '''
        if self.seconds >= int(3e6):
            # 1000(1k) hours limit
            self.seconds = int(3e6)
        elif self.seconds >= secs:
            obj.seconds += secs
            self.seconds -= secs
        else:
            while self.seconds <= secs:
                if self.ID != obj.ID:
                    self.count()
            self.send(secs, obj)

    def count(self):
        '''
            Count one second more
            using the standard
            module time
        '''            
        self.seconds += time.gmtime().tm_sec            