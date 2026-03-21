#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RTMP推流监控脚本 - 调试增强版
增加了HTML内容输出和更详细的日志
"""

import sys
import os
import requests
import time
import json
import logging
from typing import Dict, Optional
import re

# ==================== 配置区 ====================

DANMAKU_API_URL = os.getenv('DANMAKU_API_URL', 'http://127.0.0.1:5000/api/rtmp/status/update')
RTMP_MONITOR_URL = os.getenv('RTMP_MONITOR_URL', 'http://playstation-server:80')
RTMP_SERVER_TYPE = os.getenv('RTMP_SERVER_TYPE', 'playstation')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '3'))

# 调试模式: 输出HTML内容到文件
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
HTML_OUTPUT_FILE = os.getenv('HTML_OUTPUT_FILE', '/app/debug_playstation.html')

# ==================== 日志配置 ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('monitor_rtmp_debug.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class RTMPMonitorDebug:
    """RTMP推流监控器 - 调试版"""

    def __init__(self, rtmp_url: str, danmaku_url: str, server_type: str = 'playstation'):
        self.rtmp_url = rtmp_url
        self.danmaku_url = danmaku_url
        self.server_type = server_type
        self.last_active = False

    def check_connection(self) -> bool:
        """检查RTMP服务器连接状态"""
        try:
            resp = requests.get(self.rtmp_url, timeout=5)
            logger.info(f"连接RTMP服务器: {resp.status_code}")
            return resp.status_code == 200
        except Exception as e:
            logger.error(f"连接RTMP服务器失败: {e}")
            return False

    def get_rtmp_status(self) -> Dict:
        """获取RTMP推流状态"""
        try:
            if self.server_type == 'playstation':
                return self._get_playstation_status()
            else:
                return {"active": False}
        except Exception as e:
            logger.error(f"获取RTMP状态失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return {"active": False}

    def _get_playstation_status(self) -> Dict:
        """
        获取bao3/playstation的状态 - 调试增强版
        HTML格式: 文本表格,每行一个字段,空格分隔
        """
        try:
            logger.info(f"正在访问 {self.rtmp_url}...")
            resp = requests.get(self.rtmp_url, timeout=5)
            logger.info(f"响应状态码: {resp.status_code}")

            if resp.status_code != 200:
                return {"active": False}

            html = resp.text
            logger.info(f"HTML内容长度: {len(html)} 字节")

            # 调试模式: 保存HTML到文件
            if DEBUG_MODE:
                try:
                    with open(HTML_OUTPUT_FILE, 'w', encoding='utf-8') as f:
                        f.write(html)
                    logger.info(f"HTML内容已保存到: {HTML_OUTPUT_FILE}")
                except Exception as e:
                    logger.warning(f"保存HTML文件失败: {e}")

            # 分析HTML结构
            logger.info("=== HTML结构分析 ===")
            lines = html.split('\n')
            live_lines = [line for line in lines if line.strip().startswith('live_')]
            logger.info(f"找到 {len(live_lines)} 个live流")

            if not live_lines:
                logger.info("未检测到活跃推流")
                return {"active": False}

            # 使用最后一个live流
            live_line = live_lines[-1].strip()
            logger.info(f"live流行前100字符: {live_line[:100]}")

            # 解析live流行
            # 注意: 使用制表符(\t)分隔,不是空格
            parts = live_line.split('\t')
            logger.info(f"分割后的字段数: {len(parts)}")

            if len(parts) < 16:
                logger.warning(f"live流行式不正确,字段数: {len(parts)}, 需要 >= 16")
                return {"active": False}

            # 显示关键字段
            logger.info("=== 关键字段 ===")
            logger.info(f"  [0] 流名: {parts[0] if len(parts) > 0 else 'N/A'}")
            logger.info(f"  [3] 视频码率: {parts[3] if len(parts) > 3 else 'N/A'}")
            logger.info(f"  [4] 分辨率: {parts[4] if len(parts) > 4 else 'N/A'}")
            logger.info(f"  [5] 帧率: {parts[5] if len(parts) > 5 else 'N/A'}")
            logger.info(f"  [13] 输出码率: {parts[13] if len(parts) > 13 else 'N/A'}")
            logger.info(f"  [14] 状态: {parts[14] if len(parts) > 14 else 'N/A'}")

            # 提取stream_key
            stream_key = parts[0]
            logger.info(f"检测到推流: {stream_key}")

            # 提取视频码率 (第4个字段,索引3)
            if len(parts) > 3:
                video_bitrate_str = parts[3]
                logger.info(f"视频码率原始值: {video_bitrate_str}")
                bitrate_match = re.search(r'(\d+\.?\d*)', video_bitrate_str)
                if bitrate_match:
                    bitrate_mbps = float(bitrate_match.group(1))
                    bitrate = int(bitrate_mbps * 1000)  # Mb/s -> kbps
                    logger.info(f"解析视频码率: {bitrate_mbps} Mb/s = {bitrate} kbps")
                else:
                    bitrate = 0
                    logger.warning("无法解析视频码率")
            else:
                bitrate = 0

            # 提取分辨率 (第5个字段,索引4)
            resolution = "1920x1080"
            if len(parts) > 4:
                resolution_str = parts[4]
                resolution_match = re.search(r'(\d{3,4})x(\d{3,4})', resolution_str)
                if resolution_match:
                    resolution = f"{resolution_match.group(1)}x{resolution_match.group(2)}"
                    logger.info(f"解析分辨率: {resolution}")
                else:
                    logger.warning(f"无法解析分辨率: {resolution_str}")

            # 提取帧率 (第6个字段,索引5)
            fps = 60
            if len(parts) > 5:
                fps_str = parts[5]
                logger.info(f"帧率原始值: {fps_str}")
                fps_match = re.search(r'(\d+)', fps_str)
                if fps_match:
                    fps = int(fps_match.group(1))
                    logger.info(f"解析帧率: {fps} fps")
                else:
                    logger.warning(f"无法解析帧率: {fps_str}")

            # 提取状态
            state = parts[-1] if len(parts) > 14 else "unknown"
            logger.info(f"解析状态: {state}")

            result = {
                "active": True,
                "stream_key": stream_key,
                "encoding": "H.264",
                "bitrate": bitrate,
                "resolution": resolution,
                "fps": fps
            }
            logger.info(f"最终结果: {result}")
            return result

        except Exception as e:
            logger.error(f"解析playstation状态失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
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
                    logger.info("✓ RTMP状态已更新到danmaku_forward.py")
                    return True
                else:
                    logger.warning(f"✗ 更新失败: {result.get('msg')}")
                    return False
            else:
                logger.error(f"✗ 更新失败，状态码: {resp.status_code}")
                return False

        except Exception as e:
            logger.error(f"更新状态时发生错误: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False

    def run(self):
        """运行监控循环"""
        logger.info("=" * 60)
        logger.info("RTMP推流监控服务启动 (调试增强版)")
        logger.info(f"  RTMP服务器: {self.rtmp_url}")
        logger.info(f"  RTMP类型: {self.server_type}")
        logger.info(f"  监控间隔: {CHECK_INTERVAL}秒")
        logger.info(f"  Danmaku API: {self.danmaku_url}")
        logger.info(f"  调试模式: {DEBUG_MODE}")
        if DEBUG_MODE:
            logger.info(f"  HTML输出文件: {HTML_OUTPUT_FILE}")
        logger.info("=" * 60)

        while True:
            try:
                # 获取RTMP状态
                rtmp_status = self.get_rtmp_status()

                if rtmp_status.get("active", False):
                    logger.info(
                        f"推流中 - {rtmp_status.get('stream_key')} | "
                        f"{rtmp_status.get('resolution')} | "
                        f"{rtmp_status.get('fps')}fps | "
                        f"{rtmp_status.get('bitrate')}kbps"
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


if __name__ == "__main__":
    monitor = RTMPMonitorDebug(RTMP_MONITOR_URL, DANMAKU_API_URL, RTMP_SERVER_TYPE)
    monitor.run()
