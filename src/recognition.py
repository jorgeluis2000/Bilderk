from src.interface import IClaseAdstrac

class FaceRecognition(IClaseAdstrac):
    def __init__(self):
        super(FaceRecognition, self).__init__()
        IClaseAdstrac.__init__(self)

    def who_are_you(self):
        print('''I'm a Face Recognition''' + '\ncasa')
