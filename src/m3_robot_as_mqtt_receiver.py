"""
Using a Brickman (robot) as the receiver of messages.
"""

# Same as m2_fake_robot_as_mqtt_sender,
# but have the robot really do the action.
# Implement just FORWARD at speeds X and Y is enough.
import ev3dev.ev3 as ev3
import time
import math

class SimpleRoseBot(object):
    def __init__(self):
        self.left_motor = Motor('B')
        self.right_motor = Motor('C')


    def go(self, left_speed, right_speed):
        self.left_motor.turn_on(left_speed)
        self.right_motor.turn_on(right_speed)

    def stop(self):
        self.left_motor.turn_off()
        self.right_motor.turn_off()

    def go_straight_for_seconds(self, seconds, speed):
        start_time = time.time()
        self.go(speed, speed)
        while True:
            current_time = time.time()
            if current_time - start_time >= seconds:
                break
        self.stop()

    def go_straight_for_inches(self, inches, speed):
        delta_s = (inches/self.left_motor.WheelCircumference)*360
        start_distance = self.left_motor.get_position()
        self.go(speed, speed)
        while True:
            current_distance = self.left_motor.get_position()
            if current_distance - start_distance >= delta_s:
                break
        self.stop()

class DelegateThatReceives(object):
    # self.bobob = SimpleRoseBot()
    def forward(self, left_speed, right_speed):
        bobob = SimpleRoseBot()
        bobob.go(left_speed, right_speed)



def main():
    name1 = input("Enter one name (subscriber): ")
    name2 = input("Enter another name (publisher): ")

    my_delegate = DelegateThatReceives()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect(name1, name2)
    time.sleep(1)  # Time to allow the MQTT setup.
    print()

    while True:
        time.sleep(0.01)  # Time to allow message processing







###############################################################################
# The  Motor   and   ColorSensor classes.  USE them, but do NOT modify them.
###############################################################################
class Motor(object):
    WheelCircumference = 1.3 * math.pi

    def __init__(self, port):  # port must be 'B' or 'C' for left/right wheels
        self._motor = ev3.LargeMotor('out' + port)

    def turn_on(self, speed):  # speed must be -100 to 100
        self._motor.run_direct(duty_cycle_sp=speed)

    def turn_off(self):
        self._motor.stop(stop_action="brake")

    def get_position(self):  # Units are degrees (that the motor has rotated).
        return self._motor.position

    def reset_position(self):
        self._motor.position = 0