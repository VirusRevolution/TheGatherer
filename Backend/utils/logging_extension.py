import logging
from logging import DEBUG, ERROR, getLogger, INFO, WARNING
from config.config import config

LOG = getLogger("Logging")

def add_logging_level(name: str, value: int, log_method: str | None = None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    log_method = log_method or name.lower()

    if hasattr(logging, name):
       raise AttributeError(f'{name} already defined in logging module')
    if hasattr(logging, log_method):
       raise AttributeError(f'{log_method} already defined in logging module')
    if hasattr(logging.getLoggerClass(), log_method):
       raise AttributeError(f'{log_method} already defined in logger class')

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(value):
            self._log(value, message, args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(value, message, *args, **kwargs)

    logging.addLevelName(value, name)
    setattr(logging, name, value)
    setattr(logging.getLoggerClass(), log_method, logForLevel)
    setattr(logging, log_method, logToRoot)


def setup_logging():
    """
    This iterates through every *target_name* defined under the *logging* key in config.yml
    and sets the log level for the respective logger to the value given in the config file.

    This allows to set
      - an underlying log level for everything
      - exceptions (i.e. more/less verbose logging) for specific modules

    Logging works as follows:
    Every module creates its own logger via `LOG = logging.getLogger('SearchModule')`.
    Every module then logs messages to its own logger via `LOG.trace(…)`, `LOG.debug(…)`, `LOG.info(…)`, `LOG.warn(…)`, `LOG.error(…)`.

    In the logs (i.e. on the console) you will only see messages of the _configured_ level or higher:

    So if the `root` loglevel is configured to be WARN, you will only see messages created with `LOG.warn(…)` or `LOG.error(…)`.
    If the `root` loglevel is configured to be DEBUG, you will only see DEBUG, INFO, WARNING and ERRORS, but not messages created with LOG.trace(…)
    :return:
    """
    logging.basicConfig(level=INFO, format="%(asctime)s %(levelname)5.5s %(name)10.10s: %(message)s") # Show messages during configuration. Overwritten at end of this method
    root_level      = WARNING
    root_level_name = 'WARNING'
    if not isinstance(config.logging, dict):
        return
    for module, level_name in config.logging.items():
        level = ERROR
        match level_name:
            case 'DEBUG':
                level = DEBUG
            case 'ERROR':
                level = ERROR
            case 'INFO':
                level = INFO
            case 'WARN'|'WARNING':
                level = WARNING
            case 'TRACE':
                # added by add_logging_level
                if hasattr(logging, 'TRACE'):
                    level = logging.TRACE
                else:
                    LOG.warning("LOG: Configuration contains invalid value (TRACE) for logging.%s – please fix config!", module)
                    level = DEBUG
            case _:
                raise ValueError(f'Configuration contains invalid value ({level_name}) for logging.{module} – please fix config!')

        if module == 'root':
            root_level      = level
            root_level_name = level_name
        else:
            logging.getLogger(module).setLevel(level)
            # the following message goes to the logger of the main module, hence __name__ is used as target
            LOG.info(f'"{module}" now logging at {level_name} level.')

    LOG.info(f"Setting root log level to {root_level_name}…")
    logging.basicConfig(level=root_level)

def _test_add_loglevel():
    add_logging_level('TRACE', logging.DEBUG - 5)
    logging.basicConfig(level=logging.TRACE)
    logging.debug(f"This is {__name__}")
    logging.getLogger(__name__).setLevel("TRACE")
    logging.getLogger(__name__).trace('that worked')
    logging.trace('so did this')
    print(logging.TRACE)

if __name__ == '__main__':
    _test_add_loglevel()
