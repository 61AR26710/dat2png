import os

OLD_HEADER = b'\x89\x44\x41\x54'   # 原文件头
NEW_HEADER = b'\x89\x50\x4E\x47'   # PNG 文件头前 4 字节

def process_one(dat_path, png_path):
    """把单个 dat 文件改名并修正文件头"""
    # 0) 目标已存在则跳过
    if os.path.exists(png_path):
        print(f'跳过已存在：{png_path}')
        return

    # 1) 改名
    os.rename(dat_path, png_path)

    # 2) 修正文件头（以下不变）
    with open(png_path, 'r+b') as f:
        header = f.read(4)
        if header == OLD_HEADER:
            f.seek(0)
            f.write(NEW_HEADER)
            print(f'已处理：{png_path}')
        else:
            print(f'跳过：{png_path}（头不匹配）')

def batch_convert(folder):
    """遍历文件夹，批量处理（含子目录）"""
    if not os.path.isdir(folder):
        print('路径不存在或不是文件夹')
        return

    for dirpath, _, filenames in os.walk(folder):      # ← 只改这里
        for name in filenames:
            if name.lower().endswith('.dat'):
                dat_path = os.path.join(dirpath, name)
                png_path = os.path.join(dirpath, os.path.splitext(name)[0] + '.png')
                try:
                    process_one(dat_path, png_path)
                except PermissionError:
                    print(f'无权限：{dat_path}')

if __name__ == '__main__':
    target_folder = r'C:\dattopng\convert'
    batch_convert(target_folder)
