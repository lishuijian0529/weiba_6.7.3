# -*- coding: GB2312 -*-
import os
import random
import time
import sys
import logging
import logger
class file():
        @staticmethod
        def readIpFile():                       #��ȡIP
                try:
                        f = open(r"ʹ�ù���IP.txt", 'r')
                        s=f.read()
                        return s.splitlines()
                except Exception, e:
                        print e.message

        @staticmethod
        def  writeIpFile(ip_list):          #д��IP
                try:
                        f = 'ʹ�ù���IP.txt'
                        with open(f, 'a') as f:
                                f.write(ip_list+'\n')
                except Exception, e:
                        print e.message

        @staticmethod
        def readOperationMode():#��ȡ����ģʽ
                try:
                        f = open(r"����ģʽ.txt", 'r')
                        s = f.read().decode("gb2312")
                        return s.splitlines()
                except Exception, e:
                    print e.message

        @staticmethod
        def deletefile():#�ж��ļ����޳���3��
                try:
                        if int(time.time()- os.path.getctime('ʹ�ù���IP.txt')) > int(259200):
                                os.remove('ʹ�ù���IP.txt')  # ɾ�����ļ�
                        else:
                                pass
                except :
                    pass

        @staticmethod
        def readuser():
                try:
                        f = open(r"ƽ̨�˺�.txt", 'r')
                        return f.readlines()
                except Exception, e:
                    print e.message

        @staticmethod
        def readwechatfile():
                try:
                        f = open(r"΢���˺�����.txt", 'r')
                        return f.read().splitlines()
                except Exception, e:
                    print e.message

        @staticmethod
        def writewechatfile(wechat_list,file_name):
                print wechat_list
                with open(file_name.decode('utf-8'), 'a') as f:
                                f.write(u''+wechat_list)

        @staticmethod
        def sh():
                try:
                        f = open(r"����Ȧ����.txt", 'r')
                        return f.readlines()[random.randint(0, 368)].decode("gb2312")
                except Exception, e:
                        print e.message

        @staticmethod
        def readphonenumber():
                try:
                        f = open(r"�ֻ�����.txt", 'r')
                        print f.readline()
                        return f.read().splitlines()
                except Exception, e:
                        print e.message

        @staticmethod
        def writephonenumber(Phonenumber):
                try:
                        wechatfile = "�ֻ�����.txt"
                        with open(wechatfile, 'w') as f:
                                for i in range(0,Phonenumber.__len__()):
                                        f.write(Phonenumber[i] + "\n")
                except Exception, e:
                    print e.message


        @staticmethod
        def readwxmc():
                try:
                        f = open(r"΢������.txt", 'r')
                        wxmc=f.readlines()
                        return wxmc[random.randint(0, wxmc.__len__())]
                except Exception, e:
                    print e.message

        @staticmethod
        def readerrorph():
                try:
                        f = open(r"�Ӻ��ѳɹ��б�.txt", 'r')
                        return f.read().splitlines()
                except Exception, e:
                    print e.message

        @staticmethod
        def writehy(sj):
                try:
                        wechatfile = "�Ӻ��ѳɹ��б�.txt"
                        with open(wechatfile, 'a') as f:
                                f.write(sj+'\n')
                except Exception, e:
                    print e.message

        @staticmethod
        def readtoken():
                try:
                        f = open(r"tcl85.ini", 'r')
                        return f.read().splitlines()
                except Exception, e:
                        print e.message

        @staticmethod
        def writetoken(token):
                try:
                        try:os.remove('tcl85.ini')
                        except:pass
                        f = open("tcl85.ini", 'w')  # �½����ļ�
                        f.write(token)
                except Exception, e:
                    print e.message

        @staticmethod
        def write_friend_fail(text):
                try:
                        file='�Ӻ����쳣.txt'
                        with open(file,'a') as file:
                            file.write(text+'\n')
                except Exception, e:
                    print e.message

        @staticmethod
        def write_pyq_fail(text):
                try:
                        file='������Ȧ�쳣.txt'
                        with open(file,'a') as file:
                            file.write(text+'\n')
                except Exception, e:
                    print e.message

        @staticmethod
        def write_pyq_succ(text):
                try:
                        file = '���ųɹ��б�.txt'
                        with open(file, 'a') as file:
                                file.write(text + '\n')
                except Exception, e:
                        print e.message

        @staticmethod
        def read_culture_list():
                try:
                        file = '�����б�.txt'
                        with open(file,'r') as file:
                                return file.readlines()
                except:pass

        @staticmethod
        def t62_write(list_data):
                try:
                        file = '��62�ɹ��б�.txt'
                        with open(file,'a') as file:
                                file.write(list_data+'\n')
                except:pass
        @staticmethod
        def writetmp(list):
                try:
                        try:
                                open('tmp.ini','r').read()
                                open('tmp.ini', 'w')
                        except:
                                open('tmp.ini', 'w')
                        with open('tmp.ini','a')as f:
                                for i in list:
                                        reload(sys)
                                        sys.setdefaultencoding("utf-8")
                                        f.write(i+'\n')
                except:pass

        @staticmethod
        def readtmp():
                try:
                        with open('tmp.ini','r') as f:
                                return f.readlines()
                except:return None


        @staticmethod
        def write_culture_list(list):
                file='����ָ��б�.txt'
                with open(file,'a') as f:
                        f.write(list+'\n')

        @staticmethod
        def wrtie_yh_list(list):
                file='�����б�.text'
                with open(file,'r')as f:
                        f.write(list+'\n')

        @staticmethod
        def read_TKT():
                with open('TKT����.txt', 'r')as f:
                       return f.readlines()

        @staticmethod
        def delete_TKT():
                os.remove('TKT����.txt')

        @staticmethod
        def write_TKT(data):
                with open('TKT����.txt', 'a') as f:
                        for i in range(0,data.__len__()):
                                f.write(data[i])

        @staticmethod
        def write_Tkt_NotReceived(data):
                with open('TKTδ�յ���֤��.txt','a')as f:
                        f.write(data+'\n')

        @staticmethod
        def wite_Tkt_NotHopCode(data):
                with open('TKTδ����.txt','a')as f:
                        f.write(data+'\n')

        @staticmethod
        def write_Tkt_gw(data):
            with open('����΢������.txt','a')as f:
                f.write(data+'\n')

        @staticmethod
        def read_lj():
                with open('�Ͼ�ר������.txt','r')as f:
                        return f.readlines()

        @staticmethod
        def delete_lj():
                os.remove('�Ͼ�ר������.txt')

        @staticmethod
        def write_lj(data):
                with open('�Ͼ�ר������.txt', 'a') as f:
                        for i in range(0,data.__len__()):
                                f.write(data[i])

        @staticmethod
        def wite_lj_NotHopCode(data):
                with open('�Ͼ�δ����.txt','a')as f:
                        f.write(data+'\n')

        @staticmethod
        def read_grsr():
                with open('����˽������.txt', 'r')as f:
                        return f.readlines()

        @staticmethod
        def delete_grsr():
                os.remove('����˽������.txt')

        @staticmethod
        def write_grsr(data):
                with open('����˽������.txt', 'a') as f:
                        for i in range(0, data.__len__()):
                                f.write(data[i])

        @staticmethod
        def read(file_name):
                with open(file_name.decode('utf-8'), 'r')as f:
                        return f.readlines()

        @staticmethod
        def delete(file_name):
                os.remove(file_name.decode('utf-8'))

        @staticmethod
        def write(data,file_name):
                with open(file_name.decode('utf-8'), 'a') as f:
                        for i in range(0, data.__len__()):
                                f.write(data[i])

        @staticmethod
        def write_NotHopCode(data,file_name):
                with open(file_name.decode('utf-8'), 'a')as f:
                        f.write(data + '\n')

        @staticmethod
        def read_all(file_name):
                with open(file_name.decode('utf-8'), 'r')as f:
                        return f.read()


