import logging

_logging_configured=False

fmt="%(relativeCreated)-6d [%(name)-20s] %(levelname)-8s: %(message)s"

if not _logging_configured:
    logging.basicConfig(format=fmt, level=logging.DEBUG)
    filehandler=logging.FileHandler("jt3.log", 'w')
    filehandler.setFormatter(logging.Formatter(fmt))
    filehandler.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(filehandler)
    _logging_configured=True

def build_module_logger(modulename):
    module_logger=logging.getLogger("jt3."+modulename)
    return {
        "debug":module_logger.debug,
        "info":module_logger.info,
        "warning":module_logger.warning,
        "error":module_logger.error,
        "critical":module_logger.critical,
        "exception":module_logger.exception
    }
