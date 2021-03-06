__author__ = '20093'

import wx
import os
import shutil
from multiprocessing.dummy import Pool as ThreadPool



def get_path(wildcard):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

def get_dir():
    app = wx.PySimpleApp()
    dialog = wx.DirDialog(
        None, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        mydir = dialog.GetPath()
    else:
        mydir = None
    dialog.Destroy()
    return mydir


def main():

    Sync_MAPS()
    # findWrong(folder_list)


def findWrong(folder_list):

    dest_folder = 'X:\REL_EFR\personals\Jinqiang\MAPS_Data\PTI_S3E_sorted'
    with open(folder_list, 'r') as fl:
        lines = fl.read().splitlines()
        line_num = 0
        for line in lines:
            line_num = line_num + 1

            rake_log = line + '/Process_TLV/rake.parse.log'

            if os.path.exists(rake_log):
                with open(rake_log, 'r') as rake_file:
                    for rake_line in rake_file:
                        if 'FAIL' in rake_line:
                            print 'decoding_failure ', rake_line
                load_log = line + '\Process_TLV\maps'
                if os.path.exists(load_log):
                    Pass_DUTs = []
                    for load_line in os.listdir(load_log):
                        if 'maps.log' in load_line:
                            FIM0_wrong = 0
                            FIM2_wrong = 0
                            FIM0_load_num = 0
                            FIM2_load_num = 0
                            maps_path = os.path.join(load_log, load_line)
                            with open(maps_path, 'r') as load_file:
                                for load_info in load_file:
                                    if '[LOAD]' in load_info:
                                        if load_info[-18:-14] == 'FIM0':
                                            FIM0_load_num = FIM0_load_num + 1
                                            if FIM0_load_num == 1 and load_info[-18:-1] <> 'Fim0_Ce0_Die0.csv':
                                                FIM0_wrong = 1
                                                print 'Wrong load ', load_info
                                        if load_info[-18:-14] == 'FIM2':
                                            FIM2_load_num = FIM2_load_num + 1
                                            if FIM2_load_num == 1 and load_info[-18:-1] <> 'Fim2_Ce0_Die0.csv':
                                                FIM2_wrong = 1
                                                print 'Wrong load ', load_info
                            if FIM0_wrong == 0 and FIM2_wrong == 0:

                                DUT = maps_path[
                                    maps_path.index('DUT') + 3:maps_path.index('DUT') + 5]
                                Pass_DUTs.append(DUT)

                    CNE = line[line.find('PC') - 5:line.find('PC') - 1]
                    PC = line[line.find('PC'):line.find('PC') + 3]
                    Folder_index = line.index('2FIM')
                    Folder = line[Folder_index + 5:Folder_index + 10]
                    DUT = line[-6:-1]
                    print CNE + '-' + PC + '-' + Folder + '-' + DUT
                    full_path = dest_folder + '/' + \
                        CNE + '-' + PC + '-' + Folder
                    if os.path.exists(full_path) == 0:
                        os.mkdir(full_path)
                    for path_file in os.listdir(load_log):
                        if path_file[-4:] == '.csv':
                            if path_file[8:10] in Pass_DUTs:
                                if 'MAPS_DUT' in path_file:
                                    shutil.copy(
                                        load_log + '/' + path_file, full_path)
                        if path_file[-4:] == '.log':
                            shutil.copy(load_log + '/' + path_file, full_path)

                else:
                    print 'load_log_not existing ', load_log
            else:
                print 'rake_log_not_existing ', rake_log,
                wrong = 1
    return wrong
    # for root, dirs, files in os.walk(line, topdown=True):
    #     for name in files:
    #
    #         if 'maps' in name and 'log' in name:
    #
    #             (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(os.path.join(root,name))
    #             if mtime<1433864233:
    #                 print root,name

    # if os.path.exists(line+'/temp'):
    #     for file in os.listdir(line+'/temp'):
    #         if file[-3:]=='log':
    #             with open(line+'/temp'+'/'+file) as logfile:
    #                 load_num=0
    #                 for log_line in logfile:
    #                     if log_line[:6]=='[LOAD]':
    #                         if load_num==0:
    # print line+'/temp'+'/'+file,log_line
    #                             if(log_line[log_line.find('Fim'):-1]=='Fim0_Ce0_Die0.csv'):
    #                                 (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(line+'/temp'+'/'+file)
    #                                 print "last modified: %s" % mtime,log_line
    #
    #                         load_num=load_num+1
    #


def Sync_MAPS():

    folder_list = get_path('*.txt')
    dest_folder = get_dir()

    with open(folder_list, 'r') as fl:
        lines = fl.read().splitlines()
        line_num = 0
        for line in lines:
            MAPS_sub = line + '/maps'
            CNE = line[line.find('PC')-5:line.find('PC')-1]
            PC = line[line.find('PC'):line.find('PC') + 3]
            Folder = line[line.rfind('_') + 1:]
            sync_path = os.path.join(dest_folder, Folder+'-'+CNE+'-'+PC)

            if os.path.exists(MAPS_sub):
                if os.path.exists(sync_path)==0:
                    shutil.copytree(MAPS_sub, sync_path)
                    print 'Sync of this folder finish', MAPS_sub, sync_path
                else:
                    print 'path alreday synced',MAPS_sub,sync_path
                csv_path=os.path.join(line,'ReadStamp.csv')
                if os.path.exists(csv_path):
                    shutil.copy(csv_path,sync_path)
                    print 'Sync of csv file finish',csv_path,sync_path
                else:
                    print csv_path,'Not generated yet'
            else:
                print line, 'Not processed'


if __name__ == '__main__':
    main()
