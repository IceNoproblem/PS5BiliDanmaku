#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面诊断 RTMP 监控问题
"""

import sys
import os

# 解决 Windows 控制台中文编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_file_exists(filepath, description):
    """检查文件是否存在"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description} 不存在: {filepath}")
        return False

def check_code_syntax(filepath):
    """检查 Python 代码语法"""
    try:
        import py_compile
        py_compile.compile(filepath, doraise=True)
        print(f"✓ {filepath} 语法正确")
        return True
    except py_compile.PyCompileError as e:
        print(f"✗ {filepath} 语法错误:")
        print(f"  {e}")
        return False
    except Exception as e:
        print(f"✗ 检查 {filepath} 时出错: {e}")
        return False

def check_imports(filepath):
    """检查代码导入"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()

        required_imports = ['requests', 'time', 'json', 'logging', 're', 'xml.etree.ElementTree']

        missing = []
        for imp in required_imports:
            if imp not in code:
                # ElementTree 特殊处理
                if 'ElementTree' not in code and imp == 'xml.etree.ElementTree':
                    missing.append(imp)
                elif imp != 'xml.etree.ElementTree':
                    missing.append(imp)

        if missing:
            print(f"✗ {filepath} 缺少导入: {', '.join(missing)}")
            return False
        else:
            print(f"✓ {filepath} 导入完整")
            return True

    except Exception as e:
        print(f"✗ 检查导入时出错: {e}")
        return False

def check_docker_compose(filepath):
    """检查 docker-compose.yml 配置"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        issues = []

        # 检查端口配置
        if 'RTMP_MONITOR_URL=http://playstation-server:80' in content:
            issues.append("端口配置错误: 应该是 8081 而不是 80")

        if 'RTMP_MONITOR_URL=http://playstation-server:8081' in content:
            print(f"✓ 端口配置正确: 8081")
        else:
            issues.append("未找到正确的端口配置")

        if issues:
            for issue in issues:
                print(f"✗ {issue}")
            return False
        else:
            print(f"✓ docker-compose.yml 配置正确")
            return True

    except Exception as e:
        print(f"✗ 检查配置时出错: {e}")
        return False

def main():
    """主诊断流程"""
    print("=" * 70)
    print("RTMP 监控问题诊断")
    print("=" * 70)
    print()

    project_dir = r"D:\PS5-Danmaku-Docker"

    print("[检查1] 项目目录")
    print("-" * 70)
    if not check_file_exists(project_dir, "项目目录"):
        print()
        print("请确保项目目录存在!")
        return

    print()

    print("[检查2] 关键文件")
    print("-" * 70)
    files_to_check = [
        (os.path.join(project_dir, "monitor_rtmp.py"), "monitor_rtmp.py"),
        (os.path.join(project_dir, "docker-compose.yml"), "docker-compose.yml"),
        (os.path.join(project_dir, "danmaku_forward.py"), "danmaku_forward.py"),
    ]

    for filepath, desc in files_to_check:
        check_file_exists(filepath, desc)

    print()

    print("[检查3] Python 代码语法")
    print("-" * 70)
    for filepath, desc in files_to_check:
        if filepath.endswith('.py'):
            check_code_syntax(filepath)

    print()

    print("[检查4] monitor_rtmp.py 导入")
    print("-" * 70)
    monitor_rtmp = os.path.join(project_dir, "monitor_rtmp.py")
    check_imports(monitor_rtmp)

    print()

    print("[检查5] docker-compose.yml 配置")
    print("-" * 70)
    docker_compose = os.path.join(project_dir, "docker-compose.yml")
    check_docker_compose(docker_compose)

    print()

    print("[检查6] XML 解析函数")
    print("-" * 70)
    try:
        with open(monitor_rtmp, 'r', encoding='utf-8') as f:
            code = f.read()

        # 检查关键函数和代码
        checks = [
            ('def _get_playstation_status', "_get_playstation_status 函数"),
            ('xml.etree.ElementTree', "XML 导入"),
            ('ET.fromstring', "XML 解析"),
            ('findtext', "XML 元素查找"),
            ('bw_video', "视频码率提取"),
            ('bw_audio', "音频码率提取"),
            ('bw_in', "总码率提取"),
        ]

        all_ok = True
        for pattern, desc in checks:
            if pattern in code:
                print(f"✓ {desc} 存在")
            else:
                print(f"✗ {desc} 缺失")
                all_ok = False

        if all_ok:
            print()
            print("✓ 所有必需的 XML 解析代码都存在")
        else:
            print()
            print("✗ 部分代码缺失")

    except Exception as e:
        print(f"✗ 检查代码时出错: {e}")

    print()
    print("=" * 70)
    print("诊断完成")
    print("=" * 70)
    print()
    print("如果所有检查都通过,请:")
    print("1. 运行 deploy_xml_fix_v2.bat 重新部署")
    print("2. 查看容器日志: docker logs ps5-danmaku-monitor -f")
    print("3. 访问 Web 界面: http://localhost:5000")
    print()
    print("如果 RTMP 部分仍然不显示:")
    print("1. 确认 PS5 正在推流")
    print("2. 检查 playstation-server 容器状态")
    print("3. 运行 python test_local_xml.py 测试 XML 访问")
    print()

if __name__ == '__main__':
    main()
    input("\n按回车键退出...")
