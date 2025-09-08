# @Date     : 2025/8/22 15:45
# @Author   : q275343119
# @File     : example.py
# @Description:
from common_utils.config.config_loader import config

if __name__ == "__main__":
    app_name = config.get("APP_NAME", default="default_app")
    app_port = config.get("APP_PORT", default=8080, cast=int)
    debug_mode = config.get("DEBUG", default=True, cast=bool)

    print(app_name, app_port, debug_mode)
