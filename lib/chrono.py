import time

seconds_limit: int = int(3e6)

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
        if (obj.seconds + secs) >= seconds_limit:
            # Normalize seconds to limit
            obj.seconds = seconds_limit
        elif (obj.seconds + secs) < seconds_limit:
            # Send seconsds to other object
            obj.seconds += secs
            self.seconds -= secs
        else:
            # Count seconsds until get limit in the other or secs to send in this object
            while self.seconds <= secs:
                if obj.seconds >= seconds_limit:
                    break
                elif self.ID != obj.ID:
                    obj.count()

    def count(self):
        '''
            Count one second more
            using the standard
            module time
        '''
        if self.seconds >= seconds_limit:            
            self.seconds = seconds_limit
        else:    
            self.seconds += time.gmtime().tm_sec            