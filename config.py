import os


class Config(object):
    SECRET_KEY = (
        os.environ.get("SECRET_KEY")
        or b"@\xdau\x8f\x97\x1d\x19$L\x0e\x08\xd4F\xc5\xfe\xea"
    )

    MONGODB_SETTINGS = {"db": "UTA_Enrollment"}
