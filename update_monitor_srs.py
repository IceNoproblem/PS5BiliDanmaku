# -*- coding: utf-8 -*-
"""更新 Docker 版本 monitor_rtmp.py 以支持环境变量和 SRS"""

# 读取文件
with open('monitor_rtmp.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 更新配置区域，支持环境变量
old_config = '''# ==================== 配置区 ====================

# danmaku_forward.py的API地址
DANMAKU_API_URL = "http://127.0.0.1:5000/api/rtmp/status/update"

# RTMP服务器监控API地址（根据实际使用的服务调整）
# 方式1: 如果使用本地nginx-rtmp（推荐）
RTMP_MONITOR_URL = "http://127.0.0.1:8080/stat"'''

new_config = '''# ==================== 配置区 ====================

# danmaku_forward.py的API地址
DANMAKU_API_URL = os.getenv('DANMAKU_API_URL', "http://127.0.0.1:5000/api/rtmp/status/update")

# RTMP服务器监控API地址（根据实际使用的服务调整）
# 方式1: 如果使用 SRS (推荐，Docker环境默认)
RTMP_MONITOR_URL = os.getenv('RTMP_MONITOR_URL', "http://127.0.0.1:1985/api/v1/streams/")

# 方式2: 如果使用本地nginx-rtmp
# RTMP_MONITOR_URL = "http://127.0.0.1:8080/stat"'''

if old_config in content:
    content = content.replace(old_config, new_config)
    print('配置区域已更新')
else:
    print('未找到配置区域')

# 更新 RTMP_SERVER_TYPE，支持环境变量
old_server_type = '''# RTMP服务器类型：'playstation', 'nginx-rtmp', 'custom'
RTMP_SERVER_TYPE = 'nginx-rtmp''

# 推流码前缀（PS5推流时通常会生成）'''

new_server_type = '''# RTMP服务器类型：'srs', 'nginx-rtmp', 'playstation', 'custom'
RTMP_SERVER_TYPE = os.getenv('RTMP_SERVER_TYPE', 'srs')

# 推流码前缀（PS5推流时通常会生成）'''

if old_server_type in content:
    content = content.replace(old_server_type, new_server_type)
    print('RTMP_SERVER_TYPE 已更新')
else:
    print('未找到 RTMP_SERVER_TYPE')

# 在 get_rtmp_status 中添加 SRS 支持
old_method_check = '''        try:
            if self.server_type == 'playstation':
                return self._get_playstation_status()
            elif self.server_type == 'nginx-rtmp':
                return self._get_nginx_status()
            elif self.server_type == 'custom':'''

new_method_check = '''        try:
            if self.server_type == 'srs':
                return self._get_srs_status()
            elif self.server_type == 'playstation':
                return self._get_playstation_status()
            elif self.server_type == 'nginx-rtmp':
                return self._get_nginx_status()
            elif self.server_type == 'custom':'''

if old_method_check in content:
    content = content.replace(old_method_check, new_method_check)
    print('get_rtmp_status 已添加 SRS 支持')
else:
    print('未找到 get_rtmp_status 方法或已更新')

# 写回文件
with open('monitor_rtmp.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('\\nDocker 版本 monitor_rtmp.py 已更新完成')
