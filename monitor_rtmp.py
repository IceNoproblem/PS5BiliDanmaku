#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RTMP推流监控脚本
监控bao3/playstation (或类似的RTMP服务器) 状态，并更新到danmaku_forward.py

使用方法：
1. 启动bao3/playstation容器
2. 修改本脚本中的配置（RTMP服务器地址）
3. 运行本脚本：python monitor_rtmp.py
4. 在danmaku_forward.py的Web界面查看RTMP状态
"""

import sys
import os

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
    except:
        pass

import requests
import time
import json
import logging
import re
from typing import Dict, Optional

# ==================== 配置区 ====================

# 优先使用环境变量，否则使用默认值
DANMAKU_API_URL = os.getenv('DANMAKU_API_URL', 'http://127.0.0.1:5000/api/rtmp/status/update')
NGINX_RTMP_HOST = os.getenv('NGINX_RTMP_HOST', 'nginx-rtmp')
NGINX_RTMP_STAT_PORT = os.getenv('NGINX_RTMP_STAT_PORT', '80')

# RTMP服务器监控API地址（使用 Docker 容器名称）
# 优先使用环境变量，否则使用默认值
RTMP_MONITOR_URL = os.getenv('RTMP_MONITOR_URL', f"http://{NGINX_RTMP_HOST}:{NGINX_RTMP_STAT_PORT}")
RTMP_SERVER_TYPE = os.getenv('RTMP_SERVER_TYPE', 'nginx-rtmp')

# 监控间隔（秒）
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '2'))  # 改为2秒,更频繁采集

# 推流码前缀（PS5推流时通常会生成）
STREAM_KEY_PREFIX = "live_"

# ==================== 日志配置 ====================
_LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(_LOG_DIR, exist_ok=True)
_LOG_FILE = os.path.join(_LOG_DIR, 'monitor_rtmp.log')
logging.basicConfig(
    level=logging.DEBUG,  # 改为 DEBUG 以显示详细日志
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(_LOG_FILE, encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class RTMPMonitor:
    """RTMP推流监控器"""

    def __init__(self, rtmp_url: str, danmaku_url: str, server_type: str = 'playstation'):
        self.rtmp_url = rtmp_url
        self.danmaku_url = danmaku_url
        self.server_type = server_type
        self.last_active = False

    def check_connection(self) -> bool:
        """检查RTMP服务器连接状态"""
        try:
            resp = requests.get(self.rtmp_url, timeout=5)
            return resp.status_code == 200
        except Exception as e:
            logger.error(f"连接RTMP服务器失败: {e}")
            return False

    def get_rtmp_status(self) -> Dict:
        """
        获取RTMP推流状态
        根据不同的服务器类型解析不同的API响应格式
        """
        try:
            if self.server_type == 'srs':
                return self._get_srs_status()
            elif self.server_type == 'playstation':
                return self._get_playstation_status()
            elif self.server_type == 'nginx-rtmp':
                return self._get_nginx_status()
            elif self.server_type == 'custom':
                return self._get_custom_status()
            else:
                return {"active": False}
        except Exception as e:
            logger.error(f"获取RTMP状态失败: {e}")
            return {"active": False}

    def _get_playstation_status(self) -> Dict:
        """
        获取bao3/playstation的状态
        XML格式: nginx-rtmp XML统计数据
        """
        try:
            # 尝试访问根路径获取XML页面
            resp = requests.get(self.rtmp_url, timeout=5)
            if resp.status_code != 200:
                return {"active": False}

            html = resp.text

            # 使用 XML 解析
            import xml.etree.ElementTree as ET
            root = ET.fromstring(html)

            # 查找 live stream 中的码率信息
            # 路径: rtmp/server/application/live/stream
            server = root.find('server')
            if server is None:
                return {"active": False}

            application = server.find('application')
            if application is None:
                return {"active": False}

            live = application.find('live')
            if live is None:
                return {"active": False}

            stream = live.find('stream')
            if stream is None:
                return {"active": False}

            # 检查流是否活跃
            publishing_elem = stream.find('publishing')
            active_elem = stream.find('active')
            is_active = (publishing_elem is not None) or (active_elem is not None)

            if not is_active:
                logger.debug("流未活跃")
                return {"active": False}

            # 提取码率信息 (单位: bits per second)
            bw_video = stream.findtext('bw_video')
            bw_audio = stream.findtext('bw_audio')
            bw_in = stream.findtext('bw_in')

            # 提取流名称
            stream_key = stream.findtext('name') or ''
            logger.info(f"检测到推流: {stream_key}")

            # 提取客户端信息
            nclients = stream.findtext('nclients') or '0'
            logger.debug(f"客户端数: {nclients}")

            # 提取视频信息
            meta = stream.find('meta')
            video_info = {'width': '1920', 'height': '1080', 'frame_rate': '60', 'codec': 'H264'}
            if meta is not None:
                video = meta.find('video')
                if video is not None:
                    width_text = video.findtext('width')
                    height_text = video.findtext('height')
                    fps_text = video.findtext('frame_rate')
                    codec_text = video.findtext('codec')

                    if width_text:
                        video_info['width'] = width_text
                    if height_text:
                        video_info['height'] = height_text
                    if fps_text:
                        video_info['frame_rate'] = fps_text
                    if codec_text:
                        video_info['codec'] = codec_text

            # 计算总码率 (单位: kbps)
            total_bitrate_bps = int(bw_in) if bw_in and bw_in.isdigit() else 0
            video_bitrate_bps = int(bw_video) if bw_video and bw_video.isdigit() else 0
            audio_bitrate_bps = int(bw_audio) if bw_audio and bw_audio.isdigit() else 0

            bitrate = total_bitrate_bps // 1000  # 转换为 kbps
            mbps = total_bitrate_bps / 1000000  # 转换为 Mb/s

            # 提取分辨率和帧率
            width = video_info.get('width', '1920')
            height = video_info.get('height', '1080')
            resolution = f"{width}x{height}"
            fps = int(video_info.get('frame_rate', '60')) if video_info.get('frame_rate') else 60
            codec = video_info.get('codec', 'H.264')

            logger.info(
                f"检测到视频码率: {mbps:.2f} Mb/s ({bitrate} kbps) | "
                f"{resolution} | {fps}fps | {codec}"
            )

            return {
                "active": True,
                "stream_key": stream_key,
                "encoding": codec,
                "bitrate": bitrate,
                "resolution": resolution,
                "fps": fps
            }

        except ET.ParseError as e:
            logger.error(f"XML 解析失败: {e}")
            return {"active": False}
        except Exception as e:
            logger.error(f"解析playstation状态失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return {"active": False}

    def _get_nginx_status(self) -> Dict:
        """
        获取nginx-rtmp-module的状态
        需要nginx配置中开启stats
        """
        try:
            resp = requests.get(self.rtmp_url, timeout=5)
            if resp.status_code != 200:
                return {"active": False}

            data = resp.text

            # nginx-rtmp stats通常是XML格式
            # 需要解析XML查找活跃的流
            import xml.etree.ElementTree as ET
            import re
            root = ET.fromstring(data)

            # 查找live流
            for stream in root.findall('.//stream'):
                # name是子元素，不是属性
                name_elem = stream.find('name')
                name = name_elem.text if name_elem is not None else ''

                # 检查是否有active元素（自闭合标签表示活跃）
                active_elem = stream.find('active')
                is_active = active_elem is not None  # 如果存在active元素，说明流是活跃的

                if name and is_active:
                    # 使用正则表达式从原始XML中提取所有信息
                    bw_in_match = re.search(r'<bw_in>(\d+)</bw_in>', data)
                    width_match = re.search(r'<width>(\d+)</width>', data)
                    height_match = re.search(r'<height>(\d+)</height>', data)
                    fps_match = re.search(r'<frame_rate>(\d+)</frame_rate>', data)
                    codec_match = re.search(r'<codec>(\w+)</codec>', data)

                    # 提取并转换数据
                    bw_in = bw_in_match.group(1) if bw_in_match else '0'
                    bitrate = int(bw_in) // 1000 if bw_in.isdigit() else 0

                    width = width_match.group(1) if width_match else '1920'
                    height = height_match.group(1) if height_match else '1080'
                    resolution = f"{width}x{height}"

                    fps = fps_match.group(1) if fps_match else '60'

                    encoding = codec_match.group(1) if codec_match else 'H.264'

                    return {
                        "active": True,
                        "stream_key": name,
                        "encoding": encoding,
                        "bitrate": bitrate,
                        "resolution": resolution,
                        "fps": int(fps) if fps.isdigit() else 60
                    }

            return {"active": False}

        except Exception as e:
            logger.error(f"解析nginx-rtmp状态失败: {e}")
            return {"active": False}

    def _get_srs_status(self) -> Dict:
        """
        获取 SRS 状态
        SRS 提供 JSON 格式的 API
        """
        try:
            resp = requests.get(self.rtmp_url, timeout=5, proxies={})
            if resp.status_code != 200:
                return {"active": False}

            data = resp.json()

            # SRS API 返回格式
            if data.get("code") == 0:
                streams = data.get("data", {}).get("streams", [])

                if streams:
                    # 取第一个流
                    s = streams[0]

                    # 提取信息
                    stream_key = s.get("name", "")

                    # 视频信息
                    video = s.get("video", {})
                    width = video.get("width", 1920)
                    height = video.get("height", 1080)
                    codec = video.get("codec", "H.264")
                    resolution = f"{width}x{height}"

                    # 帧率
                    fps = s.get("fps", 60)

                    # 码率
                    kbps = s.get("kbps", {})
                    bitrate = kbps.get("total", 0)

                    logger.debug(f"SRS 流信息: {stream_key} | {resolution} | {fps}fps | {bitrate}kbps")

                    return {
                        "active": True,
                        "stream_key": stream_key,
                        "encoding": codec,
                        "bitrate": bitrate,
                        "resolution": resolution,
                        "fps": fps
                    }

            return {"active": False}

        except Exception as e:
            logger.error(f"解析 SRS 状态失败: {e}")
            return {"active": False}

    def _get_custom_status(self) -> Dict:
        """
        获取自定义API的状态
        假设API返回JSON格式
        """
        try:
            resp = requests.get(self.rtmp_url, timeout=5)
            if resp.status_code != 200:
                return {"active": False}

            data = resp.json()

            # 根据实际API响应格式解析
            # 示例格式（需要根据实际调整）:
            # {
            #   "live": true,
            #   "stream_key": "live_abc123",
            #   "bitrate": 4500,
            #   "resolution": "1920x1080",
            #   "fps": 60
            # }

            if data.get("live", False):
                return {
                    "active": True,
                    "stream_key": data.get("stream_key", ""),
                    "encoding": data.get("encoding", "H.264"),
                    "bitrate": data.get("bitrate", 0),
                    "resolution": data.get("resolution", ""),
                    "fps": data.get("fps", 0)
                }

            return {"active": False}

        except Exception as e:
            logger.error(f"解析自定义API状态失败: {e}")
            return {"active": False}

    def update_danmaku_status(self, status: Dict) -> bool:
        """更新到danmaku_forward.py的状态"""
        try:
            logger.debug(f'update_danmaku_status: 发送数据 = {status}')
            resp = requests.post(
                self.danmaku_url,
                json=status,
                timeout=5,
                headers={'Content-Type': 'application/json'}
            )

            if resp.status_code == 200:
                result = resp.json()
                logger.debug(f'update_danmaku_status: 响应 = {result}')
                if result.get('code') == 0:
                    logger.debug("RTMP状态已更新到danmaku_forward.py")
                    return True
                else:
                    logger.warning(f"更新失败: {result.get('msg')}")
                    return False
            else:
                logger.error(f"更新失败，状态码: {resp.status_code}")
                return False

        except Exception as e:
            logger.error(f"更新状态时发生错误: {e}")
            return False

    def run(self):
        """运行监控循环"""
        logger.info("=" * 60)
        logger.info("RTMP推流监控服务启动")
        logger.info(f"  RTMP服务器: {self.rtmp_url}")
        logger.info(f"  RTMP类型: {self.server_type}")
        logger.info(f"  监控间隔: {CHECK_INTERVAL}秒")
        logger.info(f"  Danmaku API: {self.danmaku_url}")
        logger.info("=" * 60)

        while True:
            try:
                # 获取RTMP状态
                rtmp_status = self.get_rtmp_status()

                if rtmp_status.get("active", False):
                    current_bitrate = rtmp_status.get('bitrate', 0)
                    current_stream = rtmp_status.get('stream_key', '')

                    # 格式化显示Mb/s
                    mbps = current_bitrate / 1000 if current_bitrate > 0 else 0

                    logger.info(
                        f"[实时] {current_stream} | "
                        f"{rtmp_status.get('resolution')} | "
                        f"{rtmp_status.get('fps')}fps | "
                        f"{mbps:.2f} Mb/s ({current_bitrate} kbps)"
                    )

                    # 更新到danmaku_forward.py
                    self.update_danmaku_status(rtmp_status)
                else:
                    if self.last_active:
                        logger.info("推流已停止")

                    # 更新为非活跃状态
                    self.update_danmaku_status({"active": False})

                self.last_active = rtmp_status.get("active", False)

            except KeyboardInterrupt:
                logger.info("收到停止信号，退出监控")
                break
            except Exception as e:
                logger.error(f"监控循环错误: {e}", exc_info=True)

            # 等待下一次检查
            time.sleep(CHECK_INTERVAL)


def test_connection():
    """测试配置是否正确"""
    logger.info("测试RTMP服务器连接...")
    monitor = RTMPMonitor(RTMP_MONITOR_URL, DANMAKU_API_URL, RTMP_SERVER_TYPE)

    if monitor.check_connection():
        logger.info("✓ RTMP服务器连接成功")
    else:
        logger.error("✗ RTMP服务器连接失败，请检查配置")
        return False

    logger.info("测试Danmaku API连接...")
    try:
        resp = requests.post(
            DANMAKU_API_URL,
            json={"active": False},
            timeout=5
        )
        if resp.status_code == 200:
            logger.info("✓ Danmaku API连接成功")
        else:
            logger.error(f"✗ Danmaku API返回错误: {resp.status_code}")
            return False
    except Exception as e:
        logger.error(f"✗ Danmaku API连接失败: {e}")
        return False

    return True



if __name__ == "__main__":
    # 在 Docker 环境中，等待依赖容器完全启动（服务就绪，不只是容器起来了）
    if os.getenv('DOCKER_ENV'):
        logger.info("Docker 环境：等待 playstation-server / danmaku-system 服务就绪...")
        # 手动重启场景：playstation-server 的 nginx 可能需要 10-30 秒才真正响应
        # 用更长的总等待时间（120 秒 = 40次 × 3秒），超时后不 exit 而是继续运行
        max_retries = 40
        retry_interval = 3

        connected = False
        for attempt in range(1, max_retries + 1):
            logger.info(f"尝试连接 ({attempt}/{max_retries})...")
            if test_connection():
                logger.info("✓ 连接测试成功，开始监控")
                connected = True
                break
            else:
                if attempt < max_retries:
                    logger.warning(f"连接失败，{retry_interval} 秒后重试...")
                    time.sleep(retry_interval)

        if not connected:
            # 超时仍未连上：不退出，进入监控循环（循环内部会不断重试）
            # 这样容器不会因为 exit(1) 被反复重启，日志也更干净
            logger.warning("=" * 60)
            logger.warning("初始连接测试超时，但仍将进入监控循环持续重试。")
            logger.warning("如果 playstation-server 稍后启动，监控会自动生效。")
            logger.warning("=" * 60)
    else:
        # 本地环境：测试一次，失败则提示
        if not test_connection():
            logger.error("连接测试失败，请检查配置")
            input("按回车键退出...")
            exit(1)

    # 启动监控
    monitor = RTMPMonitor(RTMP_MONITOR_URL, DANMAKU_API_URL, RTMP_SERVER_TYPE)
    monitor.run()

