import logging,logging.handlers



log01 = logging.getLogger("LauncherLog")
log02 = logging.getLogger("LauncherLog.fileManager")

hndl01 = logging.handlers.RotatingFileHandler(filename="Launcher.log",maxBytes=2 * 1024 * 1024,backupCount=2)
form01 = logging.Formatter(fmt = "%(levelname)s in %(processName)s:%(message)s")
hndl01.setFormatter(form01)
log01.addHandler(hndl01)


log01.setLevel("DEBUG")
log02.setLevel("DEBUG")