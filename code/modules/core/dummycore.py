from framebase import frame
import logger
globals().update(logger.build_module_logger("dummycore"))

@frame.register_this("dummycore")
class DummyCore:
	def run_main(self):
		print ("DummyCore Invoked")
		info("DummyCore started!")
		frame.send_event("core_loaded")
		while 1:
			try:
				frame.send_event("render", 0)
			except BaseException as e:
				exception("Error in render call")
