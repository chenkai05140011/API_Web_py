import json
import os


def readyml(Path):
    '''读取yml文件内容
    realPath: 文件的真实绝对路径 '''
    if not os.path.isfile(Path):
        raise FileNotFoundError("文件路径不存在，请检查路径是否正确：%s" % Path)
    # open方法打开直接读出来
    f = open(Path, 'r', encoding='utf-8')
    cfg = f.read()
    d = json.load(cfg)
    # 用load方法转字典
    print("读取的测试文件数据：%s"%d)
    return d

if __name__ == '__main__':
    data = readyml("test_data.yml")