import serial

# X and Y are in terms of which direction are we moving in rather than which
# axis are we rotating around
DEGREE_PER_MS_Y = 0.000115195
DEGREE_PER_MS_X = 0.000305304
MS_PER_DEGREE_Y = 8680.968858
MS_PER_DEGREE_X = 3275.420875


def degrees_to_ms_x(deg: float):
    """
    Convert an angle in degrees to motor steps for the X axis (pan). 
    Input can be -180 to 180
    """
    # deg = max(min(deg, 180.0), -180.0)
    return int(round(deg * MS_PER_DEGREE_X))


def degrees_to_ms_y(deg: float):
    """
    Convert an angle in degrees to motor steps for the Y axis (tilt). 
    Input can be -180 to 180
    """
    # deg = max(min(deg, 180.0), -180.0)
    return int(round(deg * MS_PER_DEGREE_Y))


class ST4:
    def __init__(self, port: str, timeout=1):
        self._port = port
        self._ser = serial.Serial(self._port, 57600, timeout=timeout)

    def _send(self, command: str):
        command += '\n'
        self._ser.write(command.encode('utf-8'))

    def firmware_version(self):
        """Returns firmware version of the connected ST4"""
        self._send('G700')
        return self.readline()

    def readline(self):
        """
        Read a line (delimited by EOF) from the serial port. 
        If no newline is encountered, keeps reading bytes until the timeout
        specified in the class constructor.
        """
        return self._ser.readline().decode('utf-8')

    def go_rapid(self,
                 x: float = None,
                 y: float = None
                 ):
        """
        G0

        Goes to a particular position defined by absolute coordinates of all 
        axes. 
        Each motor moves independently to the position specified using 
        the currently set max velocities and acceleration for each axis. 

        - Virtual stops are not adhered to
        - If the value for an axis is None then no move command is given to
            that axis
        """
        cmd = 'G0 '
        if x is not None:
            cmd += f'X{degrees_to_ms_x(x)} '

        if y is not None:
            cmd += f'Y{degrees_to_ms_y(y)} '

        self._send(cmd)

    def go_coordinated(self,
                       time: float,
                       accel: float,
                       x: float = None,
                       y: float = None
                       ):
        """
        G1 

        Goes to a particular position defined by absolute coordinates for 
        each axis in the time given and with the given period of 
        acceleration (both measured in seconds).

        - Virtual stops are not adhered to
        - If the value for an axis is None then no move command is given to
            that axis
        - If the move cannot be achieved in the time requested it will move
            at the fasted speed possible with the current VMAX and AMAX
            settings
        """

        cmd = f'G1 T{time} A{accel}'

        if x is not None:
            cmd += f'X{degrees_to_ms_x(x)} '

        if y is not None:
            cmd += f'Y{degrees_to_ms_y(y)} '

        self._send(cmd)

    def jog(self,
            x: float = None,
            y: float = None
            ):
        """
        G2 

        Jogs the motor the specified number of steps

        - If you try to job over a stop, it will stop at `stop - expected`.
            If you are already over a stop, it will jog back to the limit  
        """

        cmd = 'G2 '
        if x is not None:
            cmd += f'X{degrees_to_ms_x(x)} '

        if y is not None:
            cmd += f'Y{degrees_to_ms_y(y)} '

        self._send(cmd)

    def set_motor_position(self, axis: int, position: float):
        """
        G200 

        Set the current position of the specified motor to be a particular 
        numerical value. This can be used for setting the zero position of a 
        particular axis.
        """
        if axis < 1 or axis > 4:
            raise ValueError(
                'set_motor_position axis must be 1 for pan, 2 for tilt, 3 for M3 or 4 for M4')

        if axis == 2:
            ms = degrees_to_ms_y(position)
        else:
            ms = degrees_to_ms_x(position)

        cmd = f'G200 M{axis} P{ms}'
        self._send(cmd)

    def zero_all_motors(self):
        """
        G201

        Set the current position of all motors to be the new zero position
        """

        self._send('G201')
