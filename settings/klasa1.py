from kivy.clock import Clock

class FPSmeter():
    def __init__(self):
        print("init")

    def start(self):
        self.event=Clock.schedule_interval(self.pri, 1)

    def pri(self, dt):
        print(f"Czas: {Clock.get_rfps():.2f}")
    
    
    




