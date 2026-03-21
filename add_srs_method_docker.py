# -*- coding: utf-8 -*-
"""添加 SRS 状态方法到 Docker 版本 monitor_rtmp.py"""

# 读取文件
with open('monitor_rtmp.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 在 _get_custom_status 之前插入 SRS 方法
srs_method = '''    def _get_srs_status(self) -> Dict:
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

'''

# 查找插入位置
insert_before = '    def _get_custom_status(self) -> Dict:'

if insert_before in content:
    content = content.replace(insert_before, srs_method + insert_before)
    # 写回文件
    with open('monitor_rtmp.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('SRS 方法已添加到 Docker 版本')
else:
    print('未找到插入位置')
