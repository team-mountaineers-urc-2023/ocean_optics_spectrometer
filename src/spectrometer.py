#!/usr/bin/env python3

from typing import Tuple, List
from math import sin, cos
from random import Random

import rospy

from ocean_optics_spectrometer.srv import CaptureSpectrometer, CaptureSpectrometerRequest, CaptureSpectrometerResponse
from seabreeze.spectrometers import Spectrometer as SeabreezeSpectrometer

### main #####################################################################

def main():
	Spectrometer().loop()

class Spectrometer:
	def __init__(self):

		rospy.init_node("spectrometer")

		### connect to ROS ###################################################

		self.device_sn = rospy.get_param("~device_sn")

		spectrometer_service = rospy.get_param("~spectrometer_service")

		self.spectrometer_srv = rospy.Service(spectrometer_service, CaptureSpectrometer, self.capture_callback)

		### end init #########################################################

	### local functions ######################################################

	def fake_data(self) -> Tuple[List[float], List[float]]:
		wavelengths = list(range(330, 850))
		intensities = []

		r = Random()

		a = r.randint(600, 1000)
		b = r.randint(600, 1000)
		c = r.randint(50, 100)
		d = r.randint(50, 100)
		e = r.randint(5, 20)
		f = r.randint(500, 4000)

		for w in wavelengths:
			i = 5*a*sin(w/a) + 5*b*cos(w/b) + 30*c*sin(w/c) + 10*d*cos(w/d) + 10*e*sin(w/e) + f
			intensities.append(i)

		return wavelengths, intensities

	### callbacks ############################################################

	def capture_callback(self, req: CaptureSpectrometerRequest) -> CaptureSpectrometerResponse:
		response = CaptureSpectrometerResponse()

		spec = SeabreezeSpectrometer.from_serial_number(self.device_sn)
		spec.integration_time_micros(req.integration_time)

		response.wavelengths = spec.wavelengths()
		response.intensities = spec.intensities()

		# fake data for testing
		# response.wavelengths, response.intensities = self.fake_data()

		return response

	### loop #################################################################

	def loop(self):
		rospy.spin()

if __name__ == "__main__":
	main()
