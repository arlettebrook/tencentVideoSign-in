
from loguru import logger

from tencent import tencent_video_auto_sign, tencent_video_get_vip_info


def main():
    logger.info("主程序启动了")
    # tencent_video_auto_sign()
    tencent_video_get_vip_info()

if __name__ == '__main__':
    main()