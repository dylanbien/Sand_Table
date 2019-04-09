import Adafruit_PCA9685

HIGH = 4096
LOW = 0

class Adafruit_Ease_Lib():
    
    def __init__(self, **kwargs):
        self.adafruit = Adafruit_PCA9685.PCA9685()
        self.num_pins = 16
        print('Adafruit initialized')

    def change_frequency(self, freq):
        self.adafruit.set_pwm_freq(freq)

    def convert_freq_to_period(self, freq):
        return 1/freq

    def convert_period_to_freq(self, period):
        return 1/period

    def set_high(self, pin):
        if pin == 'all':
            self.set_all_pwm(HIGH, 0)
        elif isinstance(pin, list):
            for i in range(pin):
                self.adafruit.set_pwm(i, HIGH, 0)
        else:
            self.adafruit.set_pwm(pin, HIGH, 0)

    def set_low(self, pin):
        if pin == 'all':
            self.set_all_pwm(LOW, 0)
        elif isinstance(pin, list):
            for i in range(len(pin)):
                self.adafruit.set_pwm(i, LOW, 0)
        else:
            self.adafruit.set_pwm(pin, LOW, 0)

    def change_percentage(self, pin, percent):
        if percent == 100:
            self.set_high(pin)
            return
        elif percent == 0:
            self.set_low(pin)
            return
        percentage = int(4095 - (percent/100)*4095)
        if pin == 'all':
            self.adafruit.set_all_pwm(percentage, 0)

        elif isinstance(pin, list):
            for i in range(len(pin)):
                self.adafruit.set_pwm(i, percentage, 0)

        else:
            self.adafruit.set_pwm(pin, percentage, 0)

