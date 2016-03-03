import logging

_logging_configured=False

if not _logging_configured:
    logging.basicConfig(filemode='w', filename='jt3.log',level=logging.DEBUG, format='%(relativeCreated)-6d [%(name)-20s] %(levelname)-8s: %(message)s')
    _logging_configured=True

def build_module_logger(modulename):
    module_logger=logging.getLogger("jt3."+modulename)
    return {
        "debug":module_logger.debug,
        "info":module_logger.info,
        "warning":module_logger.warning,
        "error":module_logger.error,
        "critical":module_logger.critical
    }
