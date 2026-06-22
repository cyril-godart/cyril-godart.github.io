class Temperature:
    def __init__(self, celcius: float):
        if celcius < -273.15 :
            raise ValueError ("Sous le zéro absolue")
        self.celcius = celcius
    @property
    def celcius(self):
        return self._celcius
    @celcius.setter
    def celcius(self, value):
        if value < -273.15 :
            raise ValueError ("Sous le zéro absolue")
        self._celcius = value

    
if __name__ == "__main__":
    t = Temperature(37)
    print(t.celcius)
    t.celcius = -1000
    print(t.celcius)