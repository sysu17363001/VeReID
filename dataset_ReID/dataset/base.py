'''
@Author: Anys
@Date: 2022-09-05

'''

from __future__ import absolute_import
from __future__ import print_function
import os.path as osp

class BaseDataset(object):
    """
    用于数据集的基本信息获取处理
    """
    def __init__(self, root):
        self.root = osp.expanduser(root)

    def get_imagedata_info_train(self, data):
        '''
        img_path,vehicleID,colorID,typeID,cameraID 值的个数 重复的不算 比如计算color的，就是计算颜色种类数

        return：
            个数
        '''
        vID,colID,tID,camID=[],[],[],[]

        for _,vid,coid,tid,camid in data:

            vID +=[vid]
            colID +=[coid]
            tID +=[tid]
            camID +=[camid]

        # 利用set计算值的个数
        vID = set(vID)
        colID = set(colID)
        tID = set(tID)
        camID = set(camID)

        num_vID = len(vID)
        num_colID = len(colID)
        num_tID = len(tID)
        num_camID = len(camID)
        num_imgs = len(data)

        return num_imgs,num_vID,num_colID,num_tID,num_camID

    def get_imagedata_info_query(self,data):
        vID,camID=[],[]

        for _,vid,camid in data:
            vID += [vid]
            camID += [camid]
        # 利用set计算值的个数
        vID = set(vID)
        camID = set(camID)

        num_vID = len(vID)
        num_camID = len(camID)
        num_imgs = len(data)

        return num_imgs, num_vID,  num_camID

    def print_dataset_statistics(self):
        raise NotImplementedError

class BaseImageDataset(BaseDataset):
    """
    用于数据集的基本信息输出
    """
    def print_dataset_statistics(self, train, test,query):
        num_train_imgs,num_train_vID,num_train_colID,num_train_tID,num_train_camID=self.get_imagedata_info_train(train)

        num_test_imgs,num_test_vID,num_test_camID=self.get_imagedata_info_query(test)

        num_query_imgs,num_query_vID,num_query_camID = self.get_imagedata_info_query(query)

        print('Image Dataset statistics:')
        print('  ----------------------------------------')
        print('  subset   | # IDs | # Images | # Colors| # Types| # Cameras')
        print('  ----------------------------------------')
        print('  train    | {:5d} | {:8d} | {:7d} | {:6d} |{:8d}'.format(num_train_vID,num_train_imgs,num_train_colID,num_train_tID,num_train_camID))
        print('  test     | {:5d} | {:8d} | {:>7} | {:>6} |{:8d}'.format(num_test_vID,num_test_imgs,"None","None",num_test_camID))
        print('  query    | {:5d} | {:8d} | {:>7} | {:>6} |{:8d}'.format(num_query_vID, num_query_imgs, "None","None", num_query_camID))
        print('  ----------------------------------------')