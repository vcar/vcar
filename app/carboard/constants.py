import os
from config.config import DefaultConfig
# ------------------------------ Database constants ------------------------- #
STRING_LEN = 255
# ------------------------------ Default constants -------------------------- #
DEFAULT_AVATAR = "default.png"
DEFAULT_YEAR_ID = 1
DEFAULT_MODEL_ID = 1
# ------------------------------ User role ---------------------------------- #
USER = 0
ADMIN = 1
RESEARCHER = 2
USER_ROLES = [
    (0, 'Select an option ...'),
    (1, 'ADMIN'),
    (2, 'USER'),
    (3, 'Driver')
]
# ------------------------------ User status -------------------------------- #
DEFAULT_STATUS = 1
ACTIVE = 1
INACTIVE = 0
USER_STATUS = {
    INACTIVE: 'inactive',
    ACTIVE: 'active',
}
# ------------------------------ Form validation configuration -------------- #
USERNAME_LEN_MIN = 4
USERNAME_LEN_MAX = 25

FULLNAME_LEN_MIN = 4
FULLNAME_LEN_MAX = 25

PASSWORD_LEN_MIN = 4
PASSWORD_LEN_MAX = 16

AGE_MIN = 1
AGE_MAX = 100

MALE = 1
FEMALE = 2
SEX_TYPE = {
    MALE: 'Male',
    FEMALE: 'Female',
}
DRIVER_GENDER = [
    (0, 'Select a gender'),
    (1, 'Male'),
    (2, 'Female'),
    (3, 'Unknown')
]
# ------------------------------ View constants ----------------------------- #
PER_HOME_PAGE = 10
PER_PAGE = 20
USER_LOGO_DIR = 'static/uploads/avatars/'
BRAND_LOGO_DIR = 'static/uploads/brands/'
PLATFORM_LOGO_DIR = 'static/uploads/platforms/'
DRIVER_LOGO_DIR = 'static/uploads/drivers/'
VEHICLE_LOGO_DIR = 'static/uploads/vehicles/'
DRIVE_FILES_DIR = 'static/uploads/records/'

#
# ------------------------------ Trace upload  constants -------------------- #
UPLOAD_DATASET_DIR = os.path.join(DefaultConfig.UPLOAD_DIR, 'datasets')
ALLOWED_DATASET_EXTENSIONS = set(['txt', 'json', 'csv'])
# ------------------------------ File/Elastic constants --------------------- #
# file processed by elasicsearch
NOT_PROCESSED = 0
PROCESSED = 1
