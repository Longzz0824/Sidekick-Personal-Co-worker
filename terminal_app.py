import asyncio
from sidekick import Sidekick


class TerminalSidekick:
    def __init__(self):
        self.sidekick = None
        self.history = []
        
    async def setup(self):
        """初始化 Sidekick"""
        print("🚀 正在初始化 Sidekick...")
        self.sidekick = Sidekick()
        await self.sidekick.setup()
        print("✅ Sidekick 已准备就绪！")
        
    async def process_message(self, message, success_criteria):
        """处理用户消息"""
        if not self.sidekick:
            print("❌ Sidekick 尚未初始化")
            return
            
        try:
            print(f"🤖 正在处理: {message}")
            if success_criteria:
                print(f"🎯 成功标准: {success_criteria}")
            
            results = await self.sidekick.run_superstep(message, success_criteria, self.history)
            
            # 提取主要回答内容
            main_answer = self.extract_main_answer(results)
            
            # 更新历史记录
            self.history.append({"role": "user", "content": message})
            self.history.append({"role": "assistant", "content": main_answer})
            
            print(f"\n📋 结果:\n{main_answer}")
            return main_answer
            
        except Exception as e:
            print(f"❌ 处理消息时出错: {e}")
            return None
    
    def extract_main_answer(self, results):
        """提取主要答案内容"""
        if not results:
            return "无结果"
            
        # 如果结果是列表，查找助手的回答
        if isinstance(results, list):
            for item in results:
                if isinstance(item, dict) and item.get('role') == 'assistant':
                    content = item.get('content', '')
                    # 如果内容不是评估反馈，则返回
                    if not content.startswith('Evaluator Feedback'):
                        return content
        
        # 如果结果是字符串，直接返回
        if isinstance(results, str):
            return results
            
        # 如果结果是字典，尝试提取content
        if isinstance(results, dict):
            return results.get('content', str(results))
        
        # 其他情况，转换为字符串
        return str(results)
    
    async def reset(self):
        """重置 Sidekick"""
        print("🔄 正在重置 Sidekick...")
        self.cleanup()
        self.history = []
        await self.setup()
        
    def cleanup(self):
        """清理资源"""
        print("🧹 正在清理资源...")
        try:
            if self.sidekick:
                self.sidekick.cleanup()
                self.sidekick = None
        except Exception as e:
            print(f"⚠️ 清理过程中出现异常: {e}")
    
    def print_help(self):
        """打印帮助信息"""
        print("\n" + "="*50)
        print("📖 Sidekick 终端版使用说明")
        print("="*50)
        print("命令:")
        print("  help    - 显示此帮助信息")
        print("  reset   - 重置 Sidekick")
        print("  history - 显示对话历史")
        print("  clear   - 清空屏幕")
        print("  quit    - 退出程序")
        print("\n使用方法:")
        print("1. 输入您的请求")
        print("2. 系统会询问成功标准（可选，直接回车跳过）")
        print("3. Sidekick 会处理您的请求并返回结果")
        print("="*50 + "\n")
    
    def print_history(self):
        """打印对话历史"""
        if not self.history:
            print("📭 暂无对话历史")
            return
            
        print("\n" + "="*30 + " 对话历史 " + "="*30)
        for i, msg in enumerate(self.history, 1):
            role = "🧑 用户" if msg["role"] == "user" else "🤖 助手"
            print(f"{i}. {role}: {msg['content']}")
        print("="*71 + "\n")
    
    def is_special_command(self, user_input):
        """检查是否是特殊命令"""
        special_commands = ['quit', 'help', 'reset', 'history', 'clear', 'exit']
        return user_input.lower() in special_commands
    
    async def handle_special_command(self, command):
        """处理特殊命令"""
        command = command.lower()
        
        if command == 'quit' or command == 'exit':
            print("👋 再见！")
            return True  # 表示需要退出
        elif command == 'help':
            self.print_help()
            return False
        elif command == 'reset':
            await self.reset()
            return False
        elif command == 'history':
            self.print_history()
            return False
        elif command == 'clear':
            import os
            os.system('cls' if os.name == 'nt' else 'clear')
            return False
        
        return False
    
    async def run(self):
        """运行主循环"""
        print("🎉 欢迎使用 Sidekick 终端版！")
        print("输入 'help' 查看使用说明，输入 'quit' 或 'exit' 退出程序")
        
        await self.setup()
        
        try:
            while True:
                print("\n" + "-"*50)
                user_input = input("💬 请输入您的请求 (或输入命令): ").strip()
                
                if not user_input:
                    continue
                
                # 检查并处理特殊命令
                if self.is_special_command(user_input):
                    should_quit = await self.handle_special_command(user_input)
                    if should_quit:
                        break
                    continue
                
                # 获取成功标准
                success_criteria = input("🎯 请输入成功标准 (可选，直接回车跳过): ").strip()
                if not success_criteria:
                    success_criteria = None
                
                # 处理消息
                await self.process_message(user_input, success_criteria)
                
        except KeyboardInterrupt:
            print("\n\n👋 程序被用户中断，正在退出...")
        except Exception as e:
            print(f"\n❌程序运行出错: {e}")
        finally:
            self.cleanup()


async def main():
    """主函数"""
    terminal_sidekick = TerminalSidekick()
    await terminal_sidekick.run()


if __name__ == "__main__":
    asyncio.run(main())