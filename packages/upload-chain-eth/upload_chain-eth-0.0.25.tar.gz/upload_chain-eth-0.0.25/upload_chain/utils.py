#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
工具类库
"""

import os.path
from upload_chain.exceptions import ValidationError
import random2
import json
import re
import ctypes
from ctypes import CDLL
from upload_chain import setting
from upload_chain.logger import logger

def create_machine_key(absfile):
    """
    生成唯一的机器标识符
    :param file: 文件的绝对路径
    :return:
    """
    if os.path.isdir(absfile):
        raise ValueError("%s must be a file", absfile)
    (path, file) = os.path.split(absfile)
    if not os.path.exists(path):
        os.makedirs(path, mode=0o777, exist_ok=False)
    with open(absfile, 'w', encoding='utf8') as f:
        rand = round(random2.SystemRandom().random() * 10000000000000000)
        f.write(str(rand))
    return rand


def get_machine_key(absfile):
    """
    获得本地的机器唯一标识符
    :param file: 文件的绝对路径
    :return: 机器标识符
    """
    if not os.path.exists(absfile):
        return create_machine_key(absfile)
    with open(absfile, 'r') as f:
        machine = f.read()
        if machine.strip().strip('\n').strip('\t') == '':
            machine = create_machine_key(absfile)
    return machine

def get_abi(abifile):
    """
    从文件中获得abi对象
    :param abifile: 本地的abi文件
    :return:
    """
    if not os.path.isfile(abifile):
        raise ValidationError("%s file is not exist" % abifile)
    with open(abifile) as f:
        json_str_data = f.read()
    json_obj = json.loads(json_str_data)
    return json_obj['abi']


def write_blocknum(cache_file, block_num):
    """
    将块号写入指定的文件
    :param cache_file:
    :param block_num:
    :return:
    """
    with open(cache_file, 'w') as f:
        f.write(str(block_num))


def get_cache_blocknum(cache_file):
    """
    获得缓存文件中的块号，如果不存在就返回0，并且新建文件
    :param cache_file:
    :return:
    """
    if os.path.isfile(cache_file):
        with open(cache_file) as f:
            block_num = f.read()
            num = block_num.strip().strip('\n').strip('\t')
            if re.match('^[0-9]+$', num):
                return int(num)
            else:
                raise ValueError('block number: %s is not number' % block_num)
    else:
        (path, file) = os.path.split(cache_file)
        if not os.path.exists(path):
            os.makedirs(path, mode=0o777, exist_ok=False)
        with open(cache_file, 'w', encoding='utf8') as f:
            f.write(str(0))
        return 0


def import_plugins():
    """ 用于加载`plugin` """
    import importlib
    here = os.path.abspath(os.path.dirname(__file__))
    path = '{}/plugins/'.format(here)
    for root, dirs, files in os.walk(path):
        if root == path:
            for file in files:
                if file != '__init__.py' and re.match(r'^(.*)\.py$', file):
                    name = file.split('.')[0]
                    importlib.import_module('upload_chain.plugins.{}'.format(name))
    # importlib.import_module('upload_chain.plugins')
    # importlib.import_module('upload_chain.plugins.events')
    # importlib.import_module('upload_chain.plugins.solider')


def DESEncrypt(txt):
    """
    加密数据
    :param txt: 明文
    :return:
    """
    DESEncrypt = CDLL('{}/../golang/crypto.so'.format(setting.PATH)).DESEncrypt  # 调用ｇｏ模块
    # 显式声明参数和返回的期望类型
    DESEncrypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    DESEncrypt.restype = ctypes.c_char_p
    pas = DESEncrypt(txt.encode(), setting.IV)
    return pas.decode()


def DESDecrypt(ciphertext):
    """
    解密数据
    :param ciphertext: 密文
    :return:
    """
    DESDecrypt = CDLL('{}/../golang/crypto.so'.format(setting.PATH)).DESDecrypt  # 调用ｇｏ模块
    # 显式声明参数和返回的期望类型
    DESDecrypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    DESDecrypt.restype = ctypes.c_char_p
    mw = DESDecrypt(ciphertext.encode(), setting.IV)
    return mw.decode()