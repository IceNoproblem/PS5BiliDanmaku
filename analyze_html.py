#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析RTMP服务器HTML内容并更新解析逻辑
"""

import re

# 用户提供的实际HTML内容
html_content = """RTMP	#clients	Video	Audio	In bytes	Out bytes	In bits/s	Out bits/s	State	Time
Accepted: 2	codec	bits/s	size	fps	codec	bits/s	freq	chan	11.74 MB	11.72 MB	6.39 Mb/s	6.37 Mb/s		37s
app
live streams	2
live_1348515979_DGbH2broJeGMhclrsyQ3zRu3TzZvw8	2	H264 Main 4.2	6.33 Mb/s	1920x1080	59	AAC LC	69 Kb/s	48000	2	11.71 MB	11.71 MB	6.39 Mb/s	6.39 Mb/s	active	35s"""

print("=" * 70)
print("RTMP HTML内容分析")
print("=" * 70)
print()

lines = html_content.split('\n')

# 分析HTML结构
print("[HTML结构分析]")
for i, line in enumerate(lines):
    print(f"行{i}: {line[:80]}")
print()

# 提取关键信息
print("=" * 70)
print("关键信息提取")
print("=" * 70)
print()

# 1. 查找 live_ 开头的行(包含完整信息)
print("[1] 查找 live_ 开头的行...")
live_lines = [line for line in lines if line.strip().startswith('live_')]
if live_lines:
    live_line = live_lines[-1]  # 使用最后一个live流
    print(f"✓ 找到live流行: {live_line[:100]}...")
    print()

    # 2. 从live行中提取信息
    print("[2] 从live行中提取信息...")

    # 按空白分割
    parts = live_line.split()
    print(f"分割后的部分数: {len(parts)}")
    for i, part in enumerate(parts[:15]):  # 只显示前15个
        print(f"  [{i:2d}] {part}")

    # 3. 分析数据结构
    print()
    print("[3] 数据结构分析:")
    print(f"  [0] 流名: {parts[0] if len(parts) > 0 else 'N/A'}")
    print(f"  [1] 客户数: {parts[1] if len(parts) > 1 else 'N/A'}")
    print(f"  [2] 视频编码: {parts[2] if len(parts) > 2 else 'N/A'}")
    print(f"  [3] 视频码率: {parts[3] if len(parts) > 3 else 'N/A'}")
    print(f"  [4] 分辨率: {parts[4] if len(parts) > 4 else 'N/A'}")
    print(f"  [5] 帧率: {parts[5] if len(parts) > 5 else 'N/A'}")
    print(f"  [6] 音频编码: {parts[6] if len(parts) > 6 else 'N/A'}")
    print(f"  [7] 音频码率: {parts[7] if len(parts) > 7 else 'N/A'}")
    print(f"  [8] 采样率: {parts[8] if len(parts) > 8 else 'N/A'}")
    print(f"  [9] 声道: {parts[9] if len(parts) > 9 else 'N/A'}")
    print(f"  [10] In bytes: {parts[10] if len(parts) > 10 else 'N/A'}")
    print(f"  [11] Out bytes: {parts[11] if len(parts) > 11 else 'N/A'}")
    print(f"  [12] In bits/s: {parts[12] if len(parts) > 12 else 'N/A'}")
    print(f"  [13] Out bits/s: {parts[13] if len(parts) > 13 else 'N/A'}")
    print(f"  [14] State: {parts[14] if len(parts) > 14 else 'N/A'}")
    print(f"  [15] Time: {parts[15] if len(parts) > 15 else 'N/A'}")
    print()

    # 4. 提取具体值
    print("[4] 提取并转换数值:")

    # 流名
    if len(parts) > 0:
        stream_key = parts[0].replace('live_', '')
        print(f"  ✓ Stream Key: live_{stream_key}")

    # 视频码率 (Mb/s)
    if len(parts) > 3:
        video_bitrate_str = parts[3]
        # 提取数字部分
        bitrate_match = re.search(r'(\d+\.?\d*)', video_bitrate_str)
        if bitrate_match:
            video_bitrate_mbps = float(bitrate_match.group(1))
            video_bitrate_kbps = int(video_bitrate_mbps * 1000)
            print(f"  ✓ 视频码率: {video_bitrate_mbps} Mb/s = {video_bitrate_kbps} kbps")

    # 分辨率
    if len(parts) > 4:
        resolution = parts[4]
        resolution_match = re.search(r'(\d{3,4})x(\d{3,4})', resolution)
        if resolution_match:
            width = resolution_match.group(1)
            height = resolution_match.group(2)
            full_resolution = f"{width}x{height}"
            print(f"  ✓ 分辨率: {full_resolution}")
        else:
            print(f"  ✓ 分辨率: {resolution}")

    # 帧率
    if len(parts) > 5:
        fps_str = parts[5]
        fps_match = re.search(r'(\d+)', fps_str)
        if fps_match:
            fps = int(fps_match.group(1))
            print(f"  ✓ 帧率: {fps} fps")

    # 输出码率 (Out bits/s)
    if len(parts) > 13:
        out_bitrate_str = parts[13]
        bitrate_match = re.search(r'(\d+\.?\d*)', out_bitrate_str)
        if bitrate_match:
            out_bitrate_mbps = float(bitrate_match.group(1))
            out_bitrate_kbps = int(out_bitrate_mbps * 1000)
            print(f"  ✓ 输出码率: {out_bitrate_mbps} Mb/s = {out_bitrate_kbps} kbps")

    # 状态
    if len(parts) > 14:
        state = parts[14]
        print(f"  ✓ 状态: {state}")

    print()

    # 5. 生成解析函数
    print("[5] 生成解析函数代码:")
    print("""
def parse_live_line(line):
    '''解析live流行'''
    parts = line.split()

    if len(parts) < 16:
        return None

    result = {
        'stream_key': parts[0],
        'clients': parts[1],
        'video_codec': parts[2],
        'video_bitrate_str': parts[3],
        'resolution': parts[4],
        'fps_str': parts[5],
        'audio_codec': parts[6],
        'audio_bitrate_str': parts[7],
        'sample_rate': parts[8],
        'channels': parts[9],
        'in_bytes': parts[10],
        'out_bytes': parts[11],
        'in_bitrate_str': parts[12],
        'out_bitrate_str': parts[13],
        'state': parts[14],
        'time': parts[15]
    }

    # 提取码率
    video_bitrate_match = re.search(r'(\d+\.?\d*)', parts[3])
    if video_bitrate_match:
        video_bitrate_mbps = float(video_bitrate_match.group(1))
        result['bitrate'] = int(video_bitrate_mbps * 1000)

    # 提取分辨率
    resolution_match = re.search(r'(\d{3,4})x(\d{3,4})', parts[4])
    if resolution_match:
        result['resolution'] = f"{resolution_match.group(1)}x{resolution_match.group(2)}"

    # 提取帧率
    fps_match = re.search(r'(\d+)', parts[5])
    if fps_match:
        result['fps'] = int(fps_match.group(1))

    return result

# 使用示例:
live_lines = [line for line in html.split('\\n') if line.strip().startswith('live_')]
if live_lines:
    data = parse_live_line(live_lines[-1])
    print(f"码率: {data['bitrate']} kbps")
    print(f"分辨率: {data['resolution']}")
    print(f"帧率: {data['fps']} fps")
""")

print("=" * 70)
print("分析完成!")
print("=" * 70)
