import time

from loguru import logger

from config import Config
from iqiyi import IQY


def main():
    logger.info("主程序启动了")
    config = Config.load_config()
    # tencent_video = TencentVideo('root', config)
    # tencent_video.tencent_video_get_vip_info()
    # tencent_video.tencent_video_auto_sign()

    iqy = IQY('root', config)

    iqy.get_rewards()
    # iqy.sign_in()
    time.sleep(3)
    iqy.get_user_info()

if __name__ == '__main__':
    main()
