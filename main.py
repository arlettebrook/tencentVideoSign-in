import time

from loguru import logger

from config import Config
from iqiyi import IQY
from iqiyi2 import IQY2
from tieba import Tieba


def main():
    logger.info("主程序启动了")
    config = Config.load_config()
    # tencent_video = TencentVideo('root', config)
    # tencent_video.tencent_video_get_vip_info()
    # tencent_video.tencent_video_auto_sign()

    iqy = IQY2('root', config)
    logger.success(iqy.main())


    # tieBa = Tieba('root', config)
    # tieBa.check_in()


if __name__ == '__main__':
    main()
