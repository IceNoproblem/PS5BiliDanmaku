#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地测试 XML 解析 - 模拟 RTMP 监控
"""

import sys
import requests
import xml.etree.ElementTree as ET

# 解决 Windows 控制台中文编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_local_xml():
    """测试本地访问 XML"""
    print("=" * 70)
    print("测试本地 RTMP XML 访问")
    print("=" * 70)
    print()

    # 测试 URL
    url = "http://localhost:8081/"
    print(f"访问 URL: {url}")
    print()

    try:
        # 请求 XML
        resp = requests.get(url, timeout=5)

        if resp.status_code != 200:
            print(f"✗ 请求失败,状态码: {resp.status_code}")
            return False

        print(f"✓ 请求成功,状态码: {resp.status_code}")
        print()

        # 显示前 500 字符
        content = resp.text
        print("响应内容 (前 500 字符):")
        print("-" * 70)
        print(content[:500])
        print("-" * 70)
        print()

        # 尝试解析 XML
        try:
            root = ET.fromstring(content)
            print("✓ XML 解析成功")
            print()

            # 查找 stream
            server = root.find('server')
            if server is None:
                print("✗ 未找到 server 元素")
                return False

            application = server.find('application')
            if application is None:
                print("✗ 未找到 application 元素")
                return False

            live = application.find('live')
            if live is None:
                print("✗ 未找到 live 元素")
                return False

            stream = live.find('stream')
            if stream is None:
                print("✗ 未找到 stream 元素")
                print("这可能表示当前没有推流")
                return False

            print("✓ 找到 stream 元素")
            print()

            # 检查流状态
            publishing_elem = stream.find('publishing')
            active_elem = stream.find('active')
            is_active = (publishing_elem is not None) or (active_elem is not None)

            if is_active:
                print("✓ 流状态: 活跃")
            else:
                print("✗ 流状态: 未活跃")
                return False

            print()

            # 提取码率
            bw_video = stream.findtext('bw_video')
            bw_audio = stream.findtext('bw_audio')
            bw_in = stream.findtext('bw_in')

            if bw_video:
                video_bitrate_bps = int(bw_video)
                video_kbps = video_bitrate_bps / 1000
                video_mbps = video_bitrate_bps / 1000000
                print(f"视频码率: {video_mbps:.2f} Mb/s ({video_kbps:.0f} kbps)")

            if bw_audio:
                audio_bitrate_bps = int(bw_audio)
                audio_kbps = audio_bitrate_bps / 1000
                audio_mbps = audio_bitrate_bps / 1000000
                print(f"音频码率: {audio_mbps:.2f} Mb/s ({audio_kbps:.0f} kbps)")

            if bw_in:
                total_bitrate_bps = int(bw_in)
                total_kbps = total_bitrate_bps / 1000
                total_mbps = total_bitrate_bps / 1000000
                print(f"总码率:   {total_mbps:.2f} Mb/s ({total_kbps:.0f} kbps)")

            print()
            print("=" * 70)
            print("✓ 测试成功!")
            print("=" * 70)
            return True

        except ET.ParseError as e:
            print(f"✗ XML 解析失败: {e}")
            return False

    except requests.exceptions.ConnectionError:
        print("✗ 连接失败: 无法连接到 RTMP 服务器")
        print("  请确保:")
        print("  1. PS5 正在推流")
        print("  2. bao3/playstation 容器正在运行")
        print("  3. 端口 8081 可访问")
        return False

    except Exception as e:
        print(f"✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_local_xml()
    input("\n按回车键退出...")
