
DATA = {
    'fuel_level': 0,
    'transmission_gear_position': 0,
    'vehicle_speed': 0,
    'engine_speed': 0,
    'torque_at_transmission': 0,
}
# 'accelerator_pedal_position': 0,
# 'steering_wheel_angle': 0,
# 'brake_pedal_status': 0,

WEIGHT = 1

# For key in range d
    # if d[key][0] <= value <= d[key][1]:
    # if d[key][0] <= value < d[key][1]:
# End For

class DefaultSettings(object):
    # 1 - fuel_level [ 0 => 120] (%)
    FUEL_EFFICIENCY = {
        1: [0, 20],
        2: [20, 40],
        3: [40, 60],
        4: [60, 80],
        5: [80, 100],
        6: [100, 120]
    }
    # 2 - transmission gear position [ -1 => 7 ]
    GEAR_POSITION = {
        -1: "reverse",
        0: "neutral",
        1: "first",
        2: "second",
        3: "third",
        4: "fourth",
        5: "fifth",
        6: "sixth",
        7: "seventh"
    }
    # 3 - vehicle speed [ 0 => 800] (km/h)
    VEHICLE_SPEED = {
        1: [0, 10],
        2: [10, 20],
        3: [20, 30],
        4: [30, 40],
        5: [40, 50],
        6: [50, 60],
        7: [60, 655],
		8: [655, 800]
    }
    # 4 - engine speed [ 0 => 20000] (RPM)
    ENGINE_SPEED = {
        1: [0, 500],
        2: [500, 1000],
        3: [1000, 1500],
        4: [1500, 2000],
        5: [2000, 2500],
        6: [2500, 3000],
        7: [3000, 4000],
        8: [4000, 16382],
		9: [16382, 20000]
    }
    # 5 - torque at transmission [ -500 => 2000] (Nm)
    TORQUE = {
        1: [-500, -100],
        2: [-100, 0],
        3: [0, 50],
        4: [50, 100],
        5: [100, 150],
        6: [150, 200],
        7: [200, 500],
        8: [500, 1500],
		9: [1500, 2000]
    }
    # 6 - accelerator pedal position [ 0 => 100] (%)
    ACCEL_PEDAL = {
        1: [0, 10],
        2: [10, 20],
        3: [20, 30],
        4: [30, 40],
        5: [40, 50],
        6: [50, 60],
        7: [60, 100]
    }
    # 7 - steering wheel angle [ -600 => +600] (Degrees)
    STEERING = {
        1: [-600, -300],
        2: [-300, 100],
        3: [100, 300],
        4: [300, 600]
    }
    # 8 - parking brake status [ True or False]
    PARKING_BRAKE = {
        1: "true",
        2: "false"
    }
    # 9 - parking pedal status [ True or False]
    PARKING_PEDAL = {
        1: "true",
        2: "false"
    }

COLORS = [
    '#FFFF00',
    '#FB7E81',
    '#7BE141',
    '#6E6EFD',
    '#C2FABC',
    '#FFA807',
    '#FFEB3B',
    '#9C27B0',
    '#FF5722',
    '#673AB7',
    '#00BCD4',
    '#8BC34A',
    '#FF5722',
    '#6E6EFD',
    '#607D8B',
]

# All openxc data
# DATA = {
#     'accelerator_pedal_position': 0,
#     'brake_pedal_status': 0,
#     'button_state': 0,
#     'door_status': 0,
#     'engine_speed': 0,
#     'fuel_consumed_since_restart': 0,
#     'fuel_level': 0,
#     'headlamp_status': 0,
#     'ignition_status': 0,
#     'latitude': 0,
#     'longitude': 0,
#     'odometer': 0,
#     'steering_wheel_angle': 0,
#     'torque_at_transmission': 0,
#     'transmission_gear_position': 0,
#     'vehicle_speed': 0,
#     'windshield_wiper_status': 0
# }
