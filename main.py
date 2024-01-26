import time

from loguru import logger

from config import Config
from iqiyi import IQY
from tieba import Tieba


def main():
    logger.info("主程序启动了")
    config = Config.load_config()
    # tencent_video = TencentVideo('root', config)
    # tencent_video.tencent_video_get_vip_info()
    # tencent_video.tencent_video_auto_sign()

    iqy = IQY('root', config)

    checkInfo=iqy.check_in()

    checkInfo2=iqy.get_rewards()

    time.sleep(3)
    checkInfo3=iqy.get_user_info()
    logger.success(checkInfo+checkInfo2+checkInfo3)


    # tieBa = Tieba('root', config)
    # tieBa.check_in()


if __name__ == '__main__':
    main()
