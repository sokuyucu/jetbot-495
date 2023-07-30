from jetbot import Robot
robot = Robot()
robot.left(speed=0.3)
robot.stop()

import time
robot.left(0.3)
time.sleep(0.5) # delay
robot.stop() # stops wheels

robot.set_motors(0.3, 0.6) # left motor at %30 and right motor at %60 speed
time.sleep(1.0)
robot.stop()

robot.left_motor.value = 0.3 # left motor at %30
robot.right_motor.value = 0.6 # right motor at %60
time.sleep(1.0)
robot.left_motor.value = 0.0 # left motor at %0
robot.right_motor.value = 0.0 # right motor at %0

# MAIN CONTROL FUNCTIONS
def stop(change):
    robot.stop()
    
def step_forward(change):
    robot.forward(0.4)
    time.sleep(0.5)
    robot.stop()

def step_backward(change):
    robot.backward(0.4)
    time.sleep(0.5)
    robot.stop()

def step_left(change):
    robot.left(0.3)
    time.sleep(0.5)
    robot.stop()

def step_right(change):
    robot.right(0.3)
    time.sleep(0.5)
    robot.stop()
    


from jetbot import Heartbeat

heartbeat = Heartbeat()

# this function will be called when heartbeat 'alive' status changes
def handle_heartbeat_status(change):
    if change['new'] == Heartbeat.Status.dead:
        robot.stop()
        
heartbeat.observe(handle_heartbeat_status, names='status')

period_slider = widgets.FloatSlider(description='period', min=0.001, max=0.5, step=0.01, value=0.5)
traitlets.dlink((period_slider, 'value'), (heartbeat, 'period'))

display(period_slider, heartbeat.pulseout)

robot.left(0.2) 

# now lower the `period` slider above until the network heartbeat can't be satisfied