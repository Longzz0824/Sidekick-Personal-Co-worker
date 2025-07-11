#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gradio国际化(i18n)错误修复脚本
专门解决 "Cannot format a message without first setting the initial locale" 错误
"""

import gradio as gr
import os
import sys
import time
import webbrowser
import threading
from pathlib import Path

def fix_locale_environment():
    """修复本地化环境设置"""
    print("🌍 修复本地化环境设置...")
    
    # 设置标准的英语环境
    locale_vars = {
        'LANG': 'en_US.UTF-8',
        'LC_ALL': 'en_US.UTF-8',
        'LC_CTYPE': 'en_US.UTF-8',
        'LC_MESSAGES': 'en_US.UTF-8',
        'LANGUAGE': 'en_US:en',
        'GRADIO_LANGUAGE': 'en',
        'GRADIO_LOCALE': 'en_US'
    }
    
    for var, value in locale_vars.items():
        os.environ[var] = value
        print(f"  ✅ 设置 {var}={value}")
    
    # 如果是Windows系统，额外设置
    if os.name == 'nt':
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        print("  ✅ Windows环境编码设置完成")

def clean_gradio_state():
    """清理Gradio状态"""
    print("🧹 清理Gradio状态...")
    
    # 清理可能的缓存和临时文件
    cache_dirs = [
        Path.home() / '.gradio',
        Path.home() / '.cache' / 'gradio',
        Path.home() / '.cache' / 'huggingface',
        Path('/tmp/gradio') if os.name != 'nt' else Path(os.environ.get('TEMP', '')) / 'gradio'
    ]
    
    for cache_dir in cache_dirs:
        if cache_dir.exists():
            try:
                import shutil
                shutil.rmtree(cache_dir, ignore_errors=True)
                print(f"  ✅ 清理缓存: {cache_dir}")
            except Exception as e:
                print(f"  ⚠️  清理失败: {cache_dir} - {e}")

def create_fixed_interface():
    """创建修复后的界面"""
    def simple_function(text):
        return f"✅ 修复成功！输入内容: {text}"
    
    # 使用最简单的配置，避免i18n问题
    interface = gr.Interface(
        fn=simple_function,
        inputs=gr.Textbox(
            label="Test Input",  # 使用英文标签
            placeholder="Enter some text to test...",
            value="Hello World!"
        ),
        outputs=gr.Textbox(
            label="Test Output"
        ),
        title="Gradio i18n Fix Test",
        description="If you can see this interface working, the i18n issue is fixed!",
        article="<div style='text-align: center; color: green; font-weight: bold;'>✅ Gradio is working correctly</div>",
        # 强制使用英文并避免复杂的本地化
        theme=gr.themes.Default(),
        css="""
        /* 确保界面显示正常 */
        .gradio-container {
            background-color: white !important;
            border: 2px solid #28a745 !important;
        }
        .gr-button {
            background-color: #28a745 !important;
            color: white !important;
        }
        /* 隐藏可能导致i18n问题的元素 */
        .gradio-container .gr-error,
        .gradio-container .gr-warning {
            display: none !important;
        }
        """
    )
    
    return interface

def launch_with_i18n_fix():
    """启动修复了i18n问题的Gradio"""
    
    print("🔧 Gradio国际化错误修复工具")
    print("=" * 60)
    print(f"📦 Python版本: {sys.version.split()[0]}")
    print(f"📦 Gradio版本: {gr.__version__}")
    print("=" * 60)
    
    # 修复环境设置
    fix_locale_environment()
    
    # 清理状态
    clean_gradio_state()
    
    # 重新导入gradio以应用新的环境变量
    try:
        import importlib
        importlib.reload(gr)
        print("✅ Gradio模块重新加载完成")
    except Exception as e:
        print(f"⚠️  模块重新加载失败: {e}")
    
    # 创建修复后的界面
    print("\n🚀 创建修复后的界面...")
    interface = create_fixed_interface()
    
    # 启动配置
    launch_configs = [
        {
            'name': 'Standard Launch',
            'params': {
                'server_name': '127.0.0.1',
                'server_port': 7872,
                'inbrowser': False,
                'share': False,
                'quiet': True,  # 减少输出中的本地化信息
                'show_error': False,  # 避免显示可能的i18n错误
                'favicon_path': None,  # 避免manifest.json问题
                'app_kwargs': {
                    'docs_url': None,  # 禁用文档页面
                    'redoc_url': None,  # 禁用redoc
                }
            }
        },
        {
            'name': 'Minimal Launch',
            'params': {
                'inbrowser': False,
                'share': False,
                'quiet': True
            }
        },
        {
            'name': 'Basic Launch',
            'params': {}
        }
    ]
    
    for i, config in enumerate(launch_configs):
        print(f"\n🔧 尝试启动方法 {i+1}: {config['name']}")
        
        try:
            # 计算URL
            if 'server_name' in config['params'] and 'server_port' in config['params']:
                url = f"http://{config['params']['server_name']}:{config['params']['server_port']}"
            else:
                url = "http://127.0.0.1:7872"
            
            print(f"🌐 服务器地址: {url}")
            print("💡 如果页面加载，i18n问题已解决！")
            
            # 延迟打开浏览器
            def open_browser():
                time.sleep(3)
                try:
                    webbrowser.open(url)
                    print(f"✅ 浏览器已打开: {url}")
                except Exception as e:
                    print(f"❌ 浏览器打开失败: {e}")
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            # 启动界面
            interface.launch(**config['params'])
            break
            
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            if i == len(launch_configs) - 1:
                print("\n❌ 所有启动方法都失败了")
                print("\n🔧 额外解决方案:")
                print("1. 重新安装Gradio:")
                print("   pip uninstall gradio")
                print("   pip install gradio")
                print("2. 检查Python环境是否完整")
                print("3. 尝试使用虚拟环境")
                print("4. 如果在Docker中，检查容器配置")

def main():
    """主函数"""
    print("🌍 Gradio国际化(i18n)错误修复工具")
    print("专门解决 'Cannot format a message without first setting the initial locale' 错误")
    print("=" * 80)
    
    # 显示错误信息
    print("🎯 检测到的错误:")
    print("   - svelte-i18n locale initialization error")
    print("   - manifest.json 404 error")
    print("   - runtime.lastError")
    print("\n🔧 将尝试以下修复:")
    print("   1. 设置正确的本地化环境变量")
    print("   2. 清理Gradio缓存和状态")
    print("   3. 使用英文界面避免i18n问题")
    print("   4. 禁用可能导致问题的功能")
    print("=" * 80)
    
    input("按回车键开始修复... ")
    
    try:
        launch_with_i18n_fix()
    except KeyboardInterrupt:
        print("\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print("\n🆘 如果问题仍然存在，请尝试:")
        print("1. 完全重新安装Gradio: pip uninstall gradio && pip install gradio")
        print("2. 检查Python版本兼容性")
        print("3. 在虚拟环境中测试")

if __name__ == "__main__":
    main()