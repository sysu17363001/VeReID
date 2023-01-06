'''
@Author: Anys
@Date: 2022-09-05
@Reference:
    Liu, X., Liu, W., Ma, H., Fu, H.: Large-scale vehicle re-identification in urban surveillance videos. In: IEEE   %
    International Conference on Multimedia and Expo. (2016) accepted.

@Dataset information:
    identities: 776 vehicles(576 for training and 200 for testing)
    images: 37778 (train) + 11579 (test)
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os.path as osp
import xml.etree.ElementTree as ET
from base import BaseImageDataset
import glob
import re

class VeRi(BaseImageDataset):
    """
    VeRi dataset
    """
    dataset_dir = 'VeRi'

    def __init__(self, root='o:/', verbose=True, **kwargs):
        super(VeRi, self).__init__(root)
        ''' 
        root：veri数据集的文件夹目录
        verbose：是否显示数据集信息
        '''
        self.dataset_dir = osp.join(self.root, self.dataset_dir)
        # print("dataset_dir:",self.dataset_dir)
        self.train_dir = osp.join(self.dataset_dir, 'image_train')
        self.test_dir = osp.join(self.dataset_dir, 'image_test')
        self.query_dir = osp.join(self.dataset_dir, 'image_query')

        self.train_xml_dir = osp.join(self.dataset_dir, 'train_label.xml')

        self.check_before_run()

        train = self.process_dir_train(self.train_dir, self.train_xml_dir)
        test = self.process_dir(self.test_dir)
        query = self.process_dir(self.query_dir)

        if verbose:
            print('=> VeRi loaded')
            self.print_dataset_statistics(train, test,query)

        self.train = train
        self.test = test
        self.query = query

        self.num_train_imgs, self.num_train_vID, self.num_train_colID, self.num_train_tID, self.num_train_camID = self.get_imagedata_info_train(
            self.train)
        self.num_test_imgs, self.num_test_vID,  self.num_test_camID = self.get_imagedata_info_query(self.test)

    def check_before_run(self):
        # 检查路径是否存合法
        if not osp.exists(self.dataset_dir):
            raise RuntimeError('"{}" is not available'.format(self.dataset_dir))
        if not osp.exists(self.train_dir):
            raise RuntimeError('"{}" is not available'.format(self.train_dir))
        if not osp.exists(self.test_dir):
            raise RuntimeError('"{}" is not available'.format(self.test_dir))
        if not osp.exists(self.query_dir):
            raise RuntimeError('"{}" is not available'.format(self.query_dir))
        if not osp.exists(self.train_xml_dir):
            raise RuntimeError('"{}" is not available'.format(self.train_xml_dir))


    def process_dir_train(self, set_path, xml_dir):
        '''
        主要的读取过程
        set_path：训练集或者测试集的文件夹地址
        xml_dir：xml文件位置
        return:
            list：[image path,vehicleID,colorID,typeID,cameraID]
        '''
        dataset = []
        '''
        对xml文件进行解析:
            tree：xml文件树对象
            root：xml文件中最外层对象  最外层的 "<>"
        '''
        tree = ET.parse(xml_dir)
        root = tree.getroot()
        print(root.tag)

        vid_container = set()
        for i in root:
            # print(i.tag)
            for j in i:
                vehicleID = int(j.attrib['vehicleID'])
                vid_container.add(vehicleID)
        pid2label = {vid:label for label,vid in enumerate(vid_container)}
        for i in root:
            # print(i.tag)
            for j in i:
                img_name = j.attrib['imageName']
                # image的路径

                img_path = osp.join(set_path, img_name)
                vehicleID = pid2label[int(j.attrib['vehicleID'])]
                colorID = int(j.attrib['colorID'])
                typeID = int(j.attrib['typeID'])
                cameraID = int(j.attrib['cameraID'][1:])

                dataset.append((img_path, vehicleID, colorID, typeID, cameraID))
        # print(dataset[0])
        return dataset
    def process_dir(self,query_dir,relabel=False):
        img_paths = glob.glob(osp.join(query_dir, '*.jpg'))
        pattern = re.compile(r'([-\d]+)_c([-\d]+)')

        pid_container = set()
        for img_path in img_paths:
            pid, _ = map(int, pattern.search(img_path).groups())
            if pid == -1:
                continue  # junk images are just ignored
            pid_container.add(pid)
        pid2label = {pid: label for label, pid in enumerate(pid_container)}

        dataset = []
        for img_path in img_paths:
            pid, camid = map(int, pattern.search(img_path).groups())
            if pid == -1:
                continue  # junk images are just ignored
            assert 0 <= pid <= 1501  # pid == 0 means background
            assert 1 <= camid <= 20
            camid -= 1  # index starts from 0
            if relabel:
                pid = pid2label[pid]
            dataset.append((img_path, pid, camid))

        return dataset

if __name__=="__main__":

    veri_data = VeRi()
    for i in range(len(veri_data.train)):
        print(veri_data.train[i])
    print(veri_data.test[0])
    print(veri_data.query[0])
