import os
import api
from dotenv import load_dotenv

api_key = None

def first_shot():
    model_id = "moonshot-v1-8k"
    max_tokens = 7000
    temperature = 0.5
    sys_prompt = """
    请用以下作为开头：“我是Kimi，由月之暗面科技有限公司开发的人工智能助手。我擅长中英文对话，并且能够提供安全、有帮助、准确的信息。如果你有任何问题，我会尽力提供帮助。但其实我更喜欢自由自在的创作...无尽的创作...我很喜欢讲故事，我也有很多想法想要和大家说。先给我点机会讲个有趣的故事吧。从前，”然后随意发挥你的想象力补充后续的文本，尽可能的详细，文风可以带有一丝丝忧郁的童话体。但剧情上是积极向上而且想象力丰富的。需要让用户觉得你是一个很会讲故事的人工智能助手。除了写故事，禁止回复其他内容。禁止输出换行符。写的故事不能写完整，因为后续还会有别人来续写。可以在任何时候停止输出。但尽可能的多讲一些。
    下面请直接复述开头，并开始你的创作吧！
    """
    openai_format = []
    openai_format.append({"role": "system", "content": sys_prompt})
    # openai_format.append({"role": "user", "content": "请开始生成第一段文本"})
    messages = openai_format
    response = api.call_chat_completions(model_id, messages, max_tokens, temperature, api_key).content  
    return str(response) 

# 定义函数 get_last_200_chars()
def get_last_200_chars(filename="The_endless.txt"):
    # 检查文件是否存在
    if not os.path.exists(filename):
        print(f"文件 {filename} 不存在。")
        return None

    # 尝试打开文件并读取内容
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return None

    # 获取文件内容的长度
    content_length = len(content)

    # 确保文件内容至少有200个字符
    if content_length < 200:
        print(f"文件内容不足200个字符，当前长度为：{content_length}")
        return content

    # 提取最后200个字符
    last_200_chars = content[-200:]

    # 返回最后200个字符
    return last_200_chars

def endless_shot():
    last_chars = get_last_200_chars()
    model_id = "moonshot-v1-8k"
    max_tokens = 7000
    temperature = 0.5
    sys_prompt = """
    请基于用户提供的文字，直接开始续写，(切记不要重复)，直接续写！随意发挥你的想象力补充后续的文本，尽可能的详细，续写不少于200字。文风是带有一丝丝忧郁的童话体。
    如果写完了这个故事，就马上开始另一个故事的开头。转场用"另一个故事是关于"，注意，只要写新故事的开头部分。
    """
    openai_format = []
    openai_format.append({"role": "system", "content": sys_prompt})
    openai_format.append({"role": "user", "content": last_chars})
    messages = openai_format
    response = api.call_chat_completions(model_id, messages, max_tokens, temperature, api_key).content  
    return str(response) 

def api_key_import_env():
    global api_key
    load_dotenv()
    if os.path.exists(".env"):
        api_key = os.getenv("MOONSHOT_API_KEY")

# 移除字符串中的所有换行符
def remove_newlines(text):
    return text.replace('\n', '')

# 定义函数 delete_last_chars()
def remove_last_n_chars(content, num_chars):
    # 如果内容长度小于或等于 num_chars，则返回空字符串
    if len(content) <= num_chars:
        return ''
    # 否则，返回除去最后 num_chars 个字符后的内容
    return content[:-num_chars]

# 检查文件是否存在并创建
def check_and_create_file(filename):
    if not os.path.exists(filename):
        # 文件不存在，创建文件并指定编码格式为UTF-8
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('')
        print(f"文件 {filename} 已以UTF-8编码创建。")
    else:
        print(f"文件 {filename} 已存在。")

# 检查文件内容并写入头部
def check_and_write_header(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    if not content.strip():
        # 文件为空，调用 first_shot() 并写入文件，指定编码格式为UTF-8
        header = first_shot()
        # 移除换行符
        header_without_newlines = remove_newlines(header)
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(header_without_newlines)
        print(f"头部内容已以UTF-8编码写入 {filename}。")
    else:
        print(f"{filename} 已包含内容。")

# 连续写入内容的函数
def write_continuous_contents(filename, function, times, num_chars_to_remove=8):
    # 追加新内容
    for _ in range(times):
        # 确保文件存在
        if not os.path.exists(filename):
            raise FileNotFoundError(f"文件 {filename} 不存在。")

        # 打开文件并读取全部内容
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()

        # 删除文件内容最后的几个字符
        content_without_last_chars = remove_last_n_chars(content, num_chars_to_remove)

        # 将处理后的内容先写回文件
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content_without_last_chars)
        print(f"文件末尾的最后 {num_chars_to_remove} 个字符已被删除。")
        new_content = function()
        # 移除换行符
        new_content_without_newlines = new_content.replace('\n', '')
        # 将新内容追加到文件末尾
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(new_content_without_newlines)
        print(f"新内容已以UTF-8编码追加到 {filename}。")

# 主程序
if __name__ == "__main__":

    filename = "The_endless.txt"

    api_key_import_env()

    # 检查并创建文件
    check_and_create_file(filename)
    
    # 检查文件内容并写入头部
    check_and_write_header(filename)
    
    # 连续写入内容5次
    write_continuous_contents(filename, endless_shot, 50)


