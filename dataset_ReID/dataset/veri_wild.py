'''
@Author: Anys
@Date: 2023-01
@contact: anys@mail2.sysu.edu.cn
@github: https://github.com/sysu17363001
@Reference:
    Lou Y, Bai Y, Liu J, et al. A large-scale dataset for vehicle re-identification in the wild[C]//Proceedings of
    the IEEE Conference on Computer Vision and Pattern Recognition. 2019, 10.

@Dataset information:
    test scale:3000,5000,1000
    directory info:
    --VERI_Wild/
    ----images/: zipped file (.rar) of all images (containing train,query,and gallery).
    ----train_test_split/: contains train list,test list (query_3000/5000/10000、gallery_3000/5000/10000), and all
                            labels info (vhicle_info.txt)
    ----README: the introduction of VERI-Wild dataset
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os.path as osp
from base import BaseImageDataset
from tqdm import tqdm

class VeRiWild(BaseImageDataset):
    '''
    VeRI-Wild dataset
    '''
    def __init__(self, root='o:/',test_size=10000,verbose=True, **kwargs):
        super(VeRiWild, self).__init__(root)
        self.test_size = test_size
        self.path_init()
        self.check_dir()
        print("=================start load all info================")
        self.all_info = self.process_info()
        print("==============start load train dataset==============")
        self.train = self.process_dir_train()
        print("====================================================")
        print("==============start load test dataset===============")
        print("test size:", self.test_size)
        self.query,self.gallery=self.process_dir_test()
        print("===================================================")
    def path_init(self):
        dataset_dir = 'VeRI-Wild'
        scale = [3000, 5000, 10000]
        images = "images/images"
        train_test_split = "train_test_split"
        # root
        self.dataset_dir = osp.join(self.root, dataset_dir)
        # all images directory, unzipped folder of images
        self.image_dir = osp.join(self.dataset_dir, images)
        # train and test list
        self.train_test_dir =  osp.join(self.dataset_dir, train_test_split)
        # train dir
        self.train_dir = osp.join(self.train_test_dir,"train_list.txt")
        # test dir according to scale
        # gallery set
        assert self.test_size in scale, "test size not support,please try valid size: 3000,5000,or 10000"
        _dir = "test_{}_id.txt".format(self.test_size)
        _dir = osp.join(self.train_test_dir, _dir)
        self.test_gallery_dir = osp.join(self.train_test_dir,_dir)
        #  query set
        q_dir = "test_{}_id_query.txt".format(self.test_size)
        q_dir = osp.join(self.train_test_dir, q_dir)
        self.test_query_dir = osp.join(self.train_test_dir, q_dir)

        self.info_path = osp.join(self.train_test_dir, "vehicle_info.txt")

    def check_dir(self):
        """
            check if path exists.
            If Yes,return "File Path is Available!"
            or, return Error info.
        """
        if not osp.exists(self.dataset_dir):
            raise RuntimeError('"{}" is not available'.format(self.dataset_dir))
        if not osp.exists(self.image_dir):
            raise RuntimeError('"{}" is not available'.format(self.image_dir))
        if not osp.exists(self.dataset_dir):
            raise RuntimeError('"{}" is not available'.format(self.dataset_dir))
        if not osp.exists(self.train_test_dir):
            raise RuntimeError('"{}" is not available'.format(self.train_test_dir))
        if not osp.exists(self.train_dir):
            raise RuntimeError('"{}" is not available'.format(self.train_dir))
        if not osp.exists(self.info_path):
            raise RuntimeError('"{}" is not available'.format(self.info_path))
        if not osp.exists(self.test_query_dir):
            raise RuntimeError('"{}" is not available'.format(self.test_query_dir))
        if not osp.exists(self.test_gallery_dir):
            raise RuntimeError('"{}" is not available'.format(self.test_gallery_dir))
        print("File Path is Available!")

    def process_dir_train(self):
        '''
            read train data list from txt
            return: list->[],[i]->tuple: (image path, vehicle ids, camera ids, timestamp).
        '''
        train_list = []
        with open(self.train_dir) as f:
            for line in tqdm(f.readlines()):
                timestamp=''
                split_list = line.split(" ")
                img_path = split_list[0]
                for item in self.all_info:
                    if item[0] in img_path:
                        timestamp = item[2]
                vid = int(split_list[1])
                camid = int(split_list[2][:-1])
                img_path = osp.join(self.image_dir,img_path)
                if osp.exists(img_path):
                    # print((img_path,vid,camid,timestamp))
                    train_list.append((img_path,vid,camid,timestamp))
                # break
        return train_list

    def process_dir_test(self):
        '''
            read test data list from txt
            return: list->[],[i]->tuple: (image path, vehicle ids, camera ids, timestamp).
        '''
        query_list = []
        with open(self.test_query_dir) as f:
            for line in tqdm(f.readlines()):
                timestamp=''
                split_list = line.split(" ")
                img_path = split_list[0]
                for item in self.all_info:
                    if item[0] in img_path:
                        timestamp = item[2]
                vid = int(split_list[1])
                camid = int(split_list[2][:-1])
                img_path = osp.join(self.image_dir,img_path)
                if osp.exists(img_path):
                    # print((img_path,vid,camid,timestamp))
                    query_list.append((img_path,vid,camid,timestamp))
                # break
        gallery_list = []
        with open(self.test_gallery_dir) as f:

            for line in tqdm(f.readlines()):
                timestamp = ''
                split_list = line.split(" ")
                img_path = split_list[0]
                for item in self.all_info:
                    if item[0] in img_path:
                        timestamp = item[2]
                vid = int(split_list[1])
                camid = int(split_list[2][:-1])
                img_path = osp.join(self.image_dir, img_path)
                if osp.exists(img_path):
                    # print((img_path, vid, camid, timestamp))
                    gallery_list.append((img_path, vid, camid, timestamp))

        return query_list,gallery_list

    def process_info(self):
        '''
            read all vehicles information from txt
            return: list->[], [i]->list: the lines of txt,[image relative path (whose root is images/),camera id,
                                         timestamp, brand, model, color]
        '''
        all_info = []
        with open(self.info_path) as f:
            for line in tqdm(f.readlines()):
                split_list = line.split(";")
                split_list[-1]=split_list[-1][:-1]
                all_info.append(split_list)
                # print(split_list)
        return all_info

if __name__=="__main__":
    dataset = VeRiWild()
    print(dataset.train[0])
    print(dataset.query[0])
    print(dataset.gallery[0])
