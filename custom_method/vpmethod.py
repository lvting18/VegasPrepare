import os
import shutil
import random
import sqlite3
import time
import yaml
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import win32gui
import sys
from selenium.webdriver.support import expected_conditions as EC
import logging
import glob


# 先获取日志name
logger = logging.getLogger(__name__)
# 全局定义最低级别
logger.setLevel(level=logging.DEBUG)
# 文件输出信息级别
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.DEBUG)
# 屏幕输出信息级别
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# add formatter
formatter = logging.Formatter('%(asctime)s - %(module)s:%(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console.setFormatter(formatter)
# add to logger
logger.addHandler(handler)
logger.addHandler(console)


# compare if files in two folders are same
def compare_files(source_path, target_path):
    source_files = []
    target_files = []
    for a in os.walk(source_path):
        source_files = source_files + a[2]
    for b in os.walk(target_path):
        target_files = target_files + b[2]
    source_files.sort()
    target_files.sort()
    if source_files == target_files:
        logger.info('FILES ARE SAME')
        return True
    else:
        logger.info('FILES ARE DIFFERENT!')
        return False


def get_file_number(path):
    ini_path = path + r'\*'
    n = len(glob.glob(ini_path))
    logger.debug(n)
    return n


if __name__ == '__main__':
    get_file_number(r'F:\AutoTarget_Build#239_20200610_145136\target_20200610_144352')


def read_yml(key):
    # get parent folder of current folder, then join folder with folder "data" and file "data.yml"
    # yml_path = os.path.join(os.path.dirname(os.getcwd()), 'data', 'data.yml')
    yml_path = r'D:\Python\mama\data\data.yml'
    f = open(yml_path, encoding="utf-8")
    yml_data = yaml.load(f, Loader=yaml.FullLoader)
    return yml_data[key]


def load_param(class_name, case_name):
    old = list(read_yml(class_name)[case_name].values())
    x = len(old)
    y = len(old[0])
    new = []
    n = []
    i = 0
    j = 0
    while i < y:
        while j < x:
            n.append(old[j][i])
            j = j + 1
        j = 0
        new.append(n)
        i = i + 1
        n = []
    return new


# init Vegas Prepare when start automation testing
def ini_vp():
    from ruamel import yaml
    # get yaml
    # yml_path = os.path.join(os.path.dirname(os.getcwd()), 'data', 'data.yml')
    yml_path = r'D:\Python\mama\data\data.yml'
    f = open(yml_path, encoding="utf-8")
    yml_data = yaml.load(f, Loader=yaml.RoundTripLoader)
    # init config.ini and database
    configure_ini = yml_data['configure_ini']
    database = yml_data['database']
    shutil.copyfile(configure_ini[1], configure_ini[0])
    shutil.copyfile(database[1], database[0])
    # get build version
    version = yml_data['build'].__str__().split('[')[1].split(']')[0]
    # get automation target folder to create 'existing' target folder
    t = yml_data['target_partition']
    dir_path = t + 'AutoTarget_' + version
    if os.path.exists(dir_path):
        shutil.move(dir_path, dir_path + time.strftime('_%Y%m%d_%H%M%S', time.localtime(time.time())))
    os.makedirs(dir_path, exist_ok=True)
    t1 = dir_path + '\\target1'
    t2 = dir_path + '\\target2'
    os.makedirs(t1, exist_ok=True)
    os.makedirs(t2, exist_ok=True)
    # for i in os.listdir(t1):
    #     f_path = os.path.join(t1, i)
    #     os.remove(f_path)
    # for i in os.listdir(t2):
    #     f_path = os.path.join(t2, i)
    #     os.remove(f_path)
    # update "import_target" in data.yml
    yml_data['import_target'] = dir_path
    # update target for test case "test_import_to_existing_target" in data.yml
    yml_data['TestImport']['test_import_to_existing_target']['target'][0] = t1
    yml_data['TestImport']['test_import_to_existing_target']['target'][1] = t2
    with open(yml_path, 'w', encoding="utf-8") as nf:
        yaml.dump(yml_data, nf, Dumper=yaml.RoundTripDumper, allow_unicode=True)


# according keyword name, find its id
def db_assigned_keyword_id(n):
    current_database = read_yml('database')[0]
    mydb = sqlite3.connect(current_database)
    cursor = mydb.cursor()
    # excute_sen = "select id from tag where name is '%s';" % n
    excute_sen = "select Id from Keyword where Name is '%s';" % n
    cursor.execute(excute_sen)
    tables = cursor.fetchall()
    keyword_id = tables[0][0]
    return keyword_id


# 根据需求的类型，从数据库里随机获取，返回路径
def db_random(s_type, n='random'):
    # according s_type, get all from tables:
    # collection-->all collections
    # collection_set-->all collection sets
    # collection_file-->all collections and collection sets
    # library, library_file-->all folders
    t_db = ''
    if s_type == 'collection' or s_type == 'collection_set' or s_type == 'collection&set' or s_type == 'collection_file':
        t_db = 'collection'
    elif s_type == 'library' or s_type == 'library_file':
        t_db = 'dir'
    current_database = read_yml('database')[0]
    mydb = sqlite3.connect(current_database)
    cursor = mydb.cursor()
    excute_sen = "select * from %s;" % t_db
    if s_type == 'collection':
        excute_sen = "select * from %s where isset=0;" % t_db
    elif s_type == 'collection_set':
        excute_sen = "select * from %s where isset=1;" % t_db
    cursor.execute(excute_sen)
    # 读取collection或者dir两张数据库表，满足条件的所有数据，放到tables里，列表嵌套列表的形式
    tables = cursor.fetchall()
    logger.info(tables)
    # 如果数据库的collection或者dir里没有数据，返回False
    if not tables:
        logger.info('no data')
        return False
    # 有数据的话，取collection/collection set/folder, and its path
    else:
        # 如果传入的n是random，从数据库里随机取一个
        if n == 'random':
            # 从tables里随机选出一个值
            random_c = random.choice(tables)
            logger.info(random_c)
        else:
            # 如果变量传入了值，根据需要第几个item来pop
            random_c = tables.pop(int(n) - 1)
        # 获取选中的item的id
        random_id = random_c[0]
        # 获取该item的name，并创造一个random_path的列表
        random_path = [random_c[1]]
        # 如果选中的item的parent id不是0，继续下面的循环
        while random_c[2] != 0:
            # 根据random_c[2]，也就是parent id找到parent那一行
            cursor.execute("select * from %s where id='%s';" % (t_db, random_c[2]))
            tables = cursor.fetchall()
            # 因为是列表嵌套列表的形式，所以需要读取第一个列表
            random_c = tables[0]
            # 读取parent的name，加到random_path里
            random_path.append(random_c[1])
        # 循环完所有的parent，把random_path整个列表翻转一下
        random_path.reverse()
        # 在random_path列表里加上选中的item的id
        random_path.append(random_id)
        logger.info(random_path)
        return random_path


# 根据需求的类型，从数据库里随机获取，返回路径
def new_db_random(s_type, n='random'):
    # according s_type, get all from tables:
    if s_type == 'collection':
        t_db = 'Collections'
        excute_sen = "select * from %s;" % t_db
    elif s_type == 'collection_set':
        t_db = 'CollectionSets'
        excute_sen = "select * from %s;" % t_db
    elif s_type == 'collection&set':
        t_db = random.choice(['Collections', 'CollectionSets'])
        excute_sen = "select * from %s;" % t_db
    # 文件夹的数据库表里会多写入父文件夹，所以要多加一个过滤条件
    elif s_type == 'library':
        t_db = 'AssetFolder'
        excute_sen = "select * from %s WHERE IsImportedFolder=1;" % t_db
    else:
        logger.warning('DONT KNOW TYPE!!')
        return False
    current_database = r'C:\Users\Blair\AppData\Roaming\MxHUBData\mxlocalhub.db'
    mydb = sqlite3.connect(current_database)
    cursor = mydb.cursor()
    cursor.execute(excute_sen)
    # 读取collection或者dir两张数据库表，满足条件的所有数据，放到tables里，列表嵌套列表的形式
    tables = cursor.fetchall()
    logger.debug(tables)
    # 如果数据库的collection或者dir里没有数据，返回False
    if not tables:
        logger.warning('NO DATA IN THIS TABLE!!')
        return False
    # 有数据的话，取collection/collection set/folder, and its path
    else:
        # 如果传入的n是random，从数据库里随机取一个
        if n == 'random':
            random_c = random.choice(tables)
            tables.remove(random_c)
        else:
            # 如果变量传入了值，根据需要第几个item来pop
            random_c = tables.pop(int(n) - 1)
        logger.debug(random_c)
        logger.debug(tables)
        # 获取选中的item的id
        random_id = random_c[0]
        # 获取该item的name，并创造一个random_path的列表
        random_path = [random_c[1]]
        # folder, collection, collection set判断parent的方法都不一样，分开写
        cursor.execute("select * from JoinCollectionSetAndCollectionSet;")
        tables_join_sets = cursor.fetchall()
        logger.debug(tables_join_sets)
        cursor.execute("select * from CollectionSets;")
        tables_sets = cursor.fetchall()
        logger.debug(tables_sets)
        if t_db == 'Collections':
            cursor.execute("select * from JoinCollectionAndCollectionSet;")
            tables = cursor.fetchall()
            for i in tables:
                if random_id == i[0]:
                    p_id = i[1]
                    cursor.execute("select Name from CollectionSets WHERE Id=%d;" % i[1])
                    p_name = cursor.fetchall()[0][0]
                    logger.debug(p_name)
                    random_path.append(p_name)
                    n = len(tables_join_sets)
                    while n > 0:
                        for j in tables_join_sets:
                            if p_id == j[0]:
                                cursor.execute("select Name from CollectionSets WHERE Id=%d;"%j[1])
                                p_name = cursor.fetchall()[0][0]
                                logger.debug(p_name)
                                random_path.append(p_name)
                                p_id = j[1]
                                tables_join_sets.remove(j)
                                n = len(tables_join_sets)
                                logger.debug(tables_join_sets)
                                logger.debug(random_path)
                                break
                            else:
                                n = n - 1
                                continue
                    break
                else:
                    continue
        elif t_db == 'CollectionSets':
            n = len(tables_join_sets)
            p_id = random_id
            while n > 0:
                for i in tables_join_sets:
                    if p_id == i[0]:
                        cursor.execute("select Name from CollectionSets WHERE Id=%d;" % i[1])
                        p_name = cursor.fetchall()[0][0]
                        logger.debug(p_name)
                        random_path.append(p_name)
                        p_id = i[1]
                        tables_join_sets.remove(i)
                        n = len(tables_join_sets)
                        logger.debug(tables_join_sets)
                        logger.debug(random_path)
                        break
                    else:
                        n = n - 1
                        continue
        elif t_db == 'AssetFolder':
            p_id = random_c[2]
            n = len(tables)
            while n > 0:
                for i in tables:
                    if p_id == i[0]:
                        random_path.append(i[1])
                        p_id = i[2]
                        tables.remove(i)
                        n = len(tables)
                        logger.debug(tables)
                        logger.debug(random_path)
                        break
                    else:
                        n = n - 1
                        continue
        logger.debug(random_path)
        # 循环完所有的parent，把random_path整个列表翻转一下
        random_path.reverse()
        # 在random_path列表里加上选中的item的id
        random_path.append(random_id)
        logger.debug(random_path)
        return random_path


# move collection set
def db_selected_set_when_move_collection_set(set_id):
    current_database = read_yml('database')[0]
    mydb = sqlite3.connect(current_database)
    cursor = mydb.cursor()
    excute_sen = "select id, pid from collection where isset=1;"
    cursor.execute(excute_sen)
    # 读取collection或者dir两张数据库表，满足条件的所有数据，放到tables里，列表嵌套列表的形式
    tables = cursor.fetchall()
    for i in tables:
        if i[0] == set_id:
            tables.remove(i)
    tables_bak = tables[:]
    print(tables)
    for i in tables:
        if i[1] == set_id:
            set_id = i[0]
            tables_bak.remove(i)
    selected_set_id = tables_bak[0][0]
    return selected_set_id


# add to collection/move to collection
def db_selected_collection():
    # todo: 点击collection set，选择除All的第一个collection set，点击collection，选择第二个collection，根据新的数据库，返回id
    selected_collection_id = ''
    return selected_collection_id


# move to folder
def db_selected_folder():
    # todo: 选择第二个folder
    selected_folder_id = '3'
    return selected_folder_id


# create collection for files
def db_selected_collection_set():
    # todo: 点击collection set，选择除All的第一个collection set
    selected_collection_set_id = ''
    return selected_collection_set_id


def db_full_path(item_id):
    # todo: 根据id拼接full path，目前只需要folder的
    full_path = ''
    return full_path


def get_screenshot(current_def):
    version = read_yml('build').__str__().split('[')[1].split(']')[0]
    dir_path = read_yml('screenshot_path') + '\\Screenshot_' + version
    # dir_path = 'F:\\Screenshot\\Screenshot_' + time.strftime('%m%d', time.localtime(time.time()))
    os.makedirs(dir_path, exist_ok=True)
    hwnd = win32gui.FindWindow(None, 'VEGAS Prepare')
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    file_name = '%s' % current_def + time.strftime('_%Y%m%d_%H%M%S', time.localtime(time.time())) + '.jpg'
    imgPath = dir_path + '\\' + file_name
    img.save(imgPath)
    return imgPath


# get target collection id from config.ini
def get_target_id():
    config_file = open(read_yml('configure_ini')[0])
    try:
        config_list = config_file.read().splitlines()
    finally:
        config_file.close()
    t = ''
    for t in config_list:
        if 'targetid' in t:
            break
    target_id = t.split('=')[1]
    try:
        float(target_id)
        if target_id == '0':
            return False
        else:
            return target_id
    except ValueError:
        return False
