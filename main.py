from tencent import  tencent_video_sign
from loguru import logger

def main():
    logger.info("主程序启动了")
    tencent_video_sign()


if __name__ == '__main__':
    main()