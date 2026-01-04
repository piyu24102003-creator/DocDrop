# PyMySQL configuration - must be imported before Django models
import pymysql

# Patch PyMySQL to work with Django
pymysql.install_as_MySQLdb()

# Patch version info to satisfy Django's version check
pymysql.version_info = (2, 2, 1, "final", 0)

