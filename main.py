from loguru import logger

from tencent import tencent_video_get_vip_info, tencent_video_auto_sign


def main():
    logger.info("主程序启动了")
    # tencent_video_auto_sign("root")
    tencent_video_get_vip_info("root")


if __name__ == '__main__':
    main()
