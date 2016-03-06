from framebase import frame
import framebase, logger
globals().update(logger.build_module_logger(__name__))

@frame.register_this("event_logger")
class EventLogger(framebase.Observer):
	def handle_event(s, e, *a, **k):
		pass#debug("Event '"+e+"' : "+str(a)+" "+str(k))
