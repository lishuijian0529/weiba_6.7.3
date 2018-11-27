# -*- coding: utf-8 -*-
import os
import re
from File import file
from appium.webdriver.common.touch_action import TouchAction
import datetime
from OpenPhone import Open
from PhoneNumber import PhoneNumber
from Analysis import analysis
from SubmissionOrder import submissionorder
import logging
import TokenYZ
import random
import duoduo_api
from Token import token
from weiba_api import WB
import time
import json
import base64
import requests
import zipfile
import traceback

class newenvironment():
    def __init__(self, uid, password, pid, deviceid, port, o_username, o_password, wxmm, phmode, wxmc, phonenumber, gj_mode, tm=None, cooperator=None, country=None,gj=None,qh=None,ip=None):
        self.uid = uid
        self.cooperator = cooperator
        self.password = password
        self.pid = pid
        self.deviceid = deviceid
        self.port = port
        self.o_username = o_username
        self.o_password = o_password
        self.wxmm = wxmm
        self.phmode = phmode
        self.ph = PhoneNumber(self.uid, self.password, self.pid, self.deviceid, phmode)
        self.wxmc = wxmc
        self.gj_mode = gj_mode
        self.phonenumber = phonenumber
        self.tm = tm
        self.country = country
        self.gj = gj
        self.qh = qh
        self.ip = ip
        self.w = WB(deviceid)
        self.element_json = json.loads(file.read_all('6.7.3.json'))


    #微霸新机
    def wb_new(self):
        #api调用一键新机
        status = self.w.newDevice()
        if status == True:
            logging.info(self.deviceid+u'-一键新机成功')
            self.visualization('一键新机成功')
            logging.info(self.deviceid + u'-准备打开WX')
            self.visualization('准备打开WX')
            self.driver = Open().Phone('com.tencent.mm','.ui.LauncherUI', self.deviceid, self.port)
            self.driver.implicitly_wait(180)
            size = self.driver.get_window_size()
            self.wb = int(size.values()[0]) / 1080
            self.hb = int(size.values()[1]) / 1920

    #多多新机
    def dd_new(self):
        time.sleep(2)
        self.device_token = duoduo_api.newPhone(self.deviceid)
        logging.info(self.deviceid+'-token:%s'%self.device_token)
        time.sleep(2)
        logging.info(self.deviceid + u'-一键新建成功')
        self.visualization('一键新建成功')
        logging.info(self.deviceid + u'-启动WX')
        self.visualization('启动WX')
        self.driver = Open().Phone('com.tencent.mm', '.ui.LauncherUI', self.deviceid, self.port)
        self.driver.implicitly_wait(180)
        size = self.driver.get_window_size()
        self.wb = int(size.values()[0]) / 1080
        self.hb = int(size.values()[1]) / 1920


    #国内注册
    def register(self):
        self.driver.implicitly_wait(7)
        if self.driver.find_elements_by_name(self.element_json['allow'])!=[]:
            self.driver.find_element_by_name(self.element_json['allow']).click()
            time.sleep(2)
            self.driver.find_element_by_name(self.element_json['allow']).click()
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_id(self.element_json[u'首页注册ID']).click()
        time.sleep(1)
        self.visualization('点击注册')
        logging.info(self.deviceid + u'-点击注册')
    def visualization(self, message):
        try:
            requests.get('http://127.0.0.1:666/query?time=%s&number=%s&state=%s' % (int(time.time()), self.deviceid, message))
        except:
            pass

    #国内输入账号信息
    def input_text(self):
        if self.driver.find_element_by_id(self.element_json[u'选择国家ID']).get_attribute(("text")) ==u'中国（+86）':
            pass
        else:
            self.driver.find_element_by_id(self.element_json[u'选择国家ID']).click()
            self.driver.find_element_by_id(self.element_json[u'选择国家搜索按钮ID']).click()
            self.driver.find_element_by_id(self.element_json[u'输入框ID']).clear()
            self.driver.find_element_by_id(self.element_json[u'输入框ID']).send_keys(u'中国')
            self.driver.find_element_by_name('Z').click()
        self.driver.find_elements_by_id(self.element_json[u'输入框ID'])[0].click()
        for i in list(self.wxmc):
            time.sleep(0.3)
            os.system('adb -s %s shell input text %s' % (self.deviceid, i))
        #self.driver.find_elements_by_id(self.element_json[u'输入框ID'])[0].send_keys(self.wxmc)
        self.visualization('输入昵称')
        logging.info(self.deviceid + u'-输入昵称')
        self.driver.find_elements_by_id(self.element_json[u'输入框ID'])[1].clear()
        self.visualization('清空手机号码')
        logging.info(self.deviceid + u'-清空手机号码')
        #os.system('adb -s %s shell input text %s' % (self.deviceid, self.phonenumber[0]))
        for i in  list(self.phonenumber[0]):
            time.sleep(0.3)
            os.system('adb -s %s shell input text %s'%(self.deviceid,i))
        logging.info(self.deviceid + u'-输入手机号码:' + self.phonenumber[0])
        self.driver.find_elements_by_id(self.element_json[u'输入框ID'])[2].click()
        for i in  list(self.wxmm):
            time.sleep(0.3)
            os.system('adb -s %s shell input text %s'%(self.deviceid,i))
        #os.system('adb -s %s shell input text %s' % (self.deviceid, self.wxmm))
        logging.info(self.deviceid + u'-输入密码:' + self.wxmm)
        self.visualization('输入密码:%s' % self.wxmm)
        self.driver.implicitly_wait(180)
        self.driver.find_element_by_id(self.element_json[u'手机号注册页面注册按钮ID']).click()
        logging.info(self.deviceid + u'-点击注册')
        self.visualization('点击注册')
        self.driver.implicitly_wait(1)
        while True:
            if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("下一步 ")')!=[]:
                self.driver.find_elements_by_class_name(self.element_json['CheckBox'])[0].click()
                logging.info(self.deviceid + u'-同意协议')
                self.visualization('同意协议')
                time.sleep(2)
                self.driver.find_element_by_android_uiautomator('new UiSelector().description("下一步 ")').click()
                time.sleep(5)
                break
            if self.driver.find_elements_by_id(self.element_json[u'手机号注册页面注册按钮ID'])!=[]:
                self.driver.find_element_by_id(self.element_json[u'手机号注册页面注册按钮ID']).click()
            if self.driver.find_elements_by_name('网页无法打开') != []:
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                self.driver.quit()
                raise Exception, "not find page"
            if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("网页无法打开")') != []:
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                self.driver.quit()
                raise Exception, "not find page"
            if self.driver.find_elements_by_name('找不到网页') != []:
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                self.driver.quit()
                raise Exception, "not find page"

        while True:
            if  self.driver.find_elements_by_android_uiautomator('new UiSelector().description("下一步 ")')!=[]:
                self.driver.find_elements_by_class_name(self.element_json['CheckBox'])[0].click()
                logging.info(self.deviceid + u'-同意协议')
                self.visualization('同意协议')
                time.sleep(2)
                self.driver.find_element_by_android_uiautomator('new UiSelector().description("下一步 ")').click()
            if self.driver.find_elements_by_id(self.element_json[u'错误弹窗确定ID'])!=[]:
                self.driver.find_element_by_id(self.element_json[u'错误弹窗确定ID']).click()
            if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("拖动下方滑块完成拼图")')!=[]:
                self.visualization('进入滑图页面')
                logging.info(self.deviceid+u'-进入滑图页面')
                break
            if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("返回 ")')!=[]:
                raise Exception(logging.info(self.deviceid + u'-出现三个月或者系统繁忙'))
            if self.driver.find_elements_by_name('网页无法打开') != []:
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                self.driver.quit()
                raise Exception, "not find page"
            if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("网页无法打开")') != []:
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                self.driver.quit()
                raise Exception, "not find page"
            if self.driver.find_elements_by_name('找不到网页') != []:
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                self.driver.quit()
                raise Exception, "not find page"
            TouchAction(self.driver).tap(element=None, x=int(500 / self.wb), y=int(1080 / self.hb)).perform()
        time.sleep(5)

    # 小蚂蚁

    def gw_yztp_1280(self):
       pass
    #滑图错误
    def error_Three_Months(self):
        if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("返回 ")')!=[]:
            self.visualization('出现三个月,重新返回')
            logging.info(self.deviceid + u'-出现三个月,重新返回')
            if self.phmode == '14.玉米平台'.decode("utf-8"):
                self.ph.yumi_cancelSMSRecv(self.phonenumber[0], self.phonenumber[1])
            return '1'

    #成功跳码
    def successful_Skip_Code(self):
        if self.driver.find_elements_by_id(self.element_json['czl'])!=[]:
            self.visualization('跳码成功')
            logging.info(self.deviceid + u'-跳码成功')
            return True

    #跳码失败直接退出
    def skip_Code_fail(self,error_type=None):
        if self.driver.find_elements_by_android_uiautomator(
                'new UiSelector().description("让用户用微信扫描下面的二维码")')!=[]:
            if error_type == 'Continue':
                time.sleep(10)
                self.visualization('跳转到二维码页面')
                logging.info(self.deviceid + u'-跳转到二维码页面')
                os.popen('adb -s ' + self.deviceid + ' shell mkdir /sdcard/Pictures')
                os.popen('adb -s ' + self.deviceid + ' shell /system/bin/screencap -p /sdcard/Pictures/succ.png')
                time.sleep(6)
            return False
    # 国内图片验证
    def yztp(self):
        """
        验证图片 
        """
        time.sleep(2)
        if self.tm == '9':
            while True:
                if self.driver.find_elements_by_name(self.element_json[u'Safety_Check'])!=[]:
                    if self.skip_Code_fail()== False:
                        return False
                    if self.error_Three_Months() == '1':
                        return '1'
                if self.driver.find_elements_by_id(self.element_json[u'短信内容ID']) != []:
                    return True
                if self.driver.find_elements_by_name('网页无法打开') != []:
                    logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                    self.driver.quit()
                    raise Exception, "not find page"
                if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("网页无法打开")') != []:
                    logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                    self.driver.quit()
                    raise Exception, "not find page"
                if self.driver.find_elements_by_name('找不到网页') != []:
                    logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                    self.driver.quit()
                    raise Exception, "not find page"
        if self.tm == "7":
                while True:
                    try:
                        for j in range(100, 200, 30):
                            a = TouchAction(self.driver)
                            a.press(x=250, y=1000)
                            for i in range(0, 5):
                                a.move_to(x=50, y=(random.randint(-500, 0))).wait(0)
                                a.move_to(x=50, y=(random.randint(0, 500))).wait(0)
                            for i in range(0, j / 10):
                                a.move_to(x=10, y=0).wait(100)
                            a.release().perform()
                            if self.driver.find_elements_by_name(self.element_json[u'Safety_Check']) != []:
                                if self.skip_Code_fail('Continue')==False:
                                    return False
                                if self.error_Three_Months() == '1':
                                    return '1'
                            if self.driver.find_elements_by_id(self.element_json[u'短信内容ID']) != []:
                                return True
                            if self.driver.find_elements_by_name('网页无法打开') != []:
                                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                                self.driver.quit()
                                raise Exception, "not find page"
                            if self.driver.find_elements_by_android_uiautomator(
                                    'new UiSelector().description("网页无法打开")') != []:
                                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                                self.driver.quit()
                                raise Exception, "not find page"
                            if self.driver.find_elements_by_name('找不到网页') != []:
                                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                                self.driver.quit()
                                raise Exception, "not find page"
                    except:pass
        if self.tm == "6":
            while True:
                try:
                    for j in range(100, 200, 30):
                        a = TouchAction(self.driver)
                        a.press(x=250, y=1000)
                        for i in range(0, 5):
                            a.move_to(x=50, y=(random.randint(-500, 0))).wait(0)
                            a.move_to(x=50, y=(random.randint(0, 500))).wait(0)
                        for i in range(0, j / 10):
                            a.move_to(x=10, y=0).wait(100)
                        a.release().perform()
                        if self.driver.find_elements_by_name(self.element_json[u'Safety_Check']) != []:
                            if self.skip_Code_fail() == False:
                                return False
                            if self.error_Three_Months()== '1':
                                return '1'
                        if self.driver.find_elements_by_id(self.element_json[u'短信内容ID']) != []:
                            return True
                        if self.driver.find_elements_by_name('网页无法打开') != []:
                            logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                            self.driver.quit()
                            raise Exception, "not find page"
                        if self.driver.find_elements_by_android_uiautomator(
                                'new UiSelector().description("网页无法打开")') != []:
                            logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                            self.driver.quit()
                            raise Exception, "not find page"
                        if self.driver.find_elements_by_name('找不到网页') != []:
                            logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                            self.driver.quit()
                            raise Exception, "not find page"
                except:pass
        else:
            while True:
                try:
                    for j in range(100, 200, 30):
                        a = TouchAction(self.driver)
                        a.press(x=250, y=1000)
                        for i in range(0, 5):
                            a.move_to(x=50, y=(random.randint(-500, 0))).wait(0)
                            a.move_to(x=50, y=(random.randint(0, 500))).wait(0)
                        for i in range(0, j / 10):
                            a.move_to(x=10, y=0).wait(100)
                        a.release().perform()
                        self.visualization('验证中')
                        logging.info(self.deviceid + u'-验证中')
                        if self.driver.find_elements_by_name(self.element_json['Safety_Check']) != []:
                            if self.skip_Code_fail('Continue')==False:
                                return False
                            if self.error_Three_Months()==False:
                                return False
                        if self.driver.find_elements_by_id(self.element_json['czl'])!=[]:
                            return True
                        if self.driver.find_elements_by_name('网页无法打开') != []:
                            logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                            self.driver.quit()
                            raise Exception, "not find page"
                        if self.driver.find_elements_by_android_uiautomator(
                                'new UiSelector().description("网页无法打开")') != []:
                            logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                            self.driver.quit()
                            raise Exception, "not find page"
                        if self.driver.find_elements_by_name('找不到网页') != []:
                            logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                            self.driver.quit()
                            raise Exception, "not find page"
                except:pass
    #任务确认
    def task_validation(self):
        """
        任务确认 
        """
        time.sleep(5)
        token = TokenYZ.pdtoken()
        status = submissionorder().confirm(self.deviceid, self.taskid, token)
        if status == '成功':
            self.visualization('任务已确认完成')
            logging.info(self.deviceid+u'-任务已确认完成')
        else:
            token = TokenYZ.pdtoken()
            status = submissionorder().confirm(self.deviceid, self.taskid, token)
            if status == '成功':
                self.visualization('任务已确认完成')
                logging.info(self.deviceid+u'-任务已确认完成')
        logging.info(self.deviceid + u'-正在发送短信')
        self.visualization('正在发送短信')
    #等待扫码
    def waiting_code(self, end_time):
        self.driver.implicitly_wait(5)
        for self.i in range(1, int(end_time)):
            TouchAction(self.driver).tap(element=None, x=int(500 / self.wb), y=int(900/ self.hb)).perform()
            if self.driver.find_elements_by_id(self.element_json[u'短信内容ID']) != []:
                self.dx = re.findall('[a-z0-9]{1,10}', self.driver.find_element_by_id(self.element_json[u'短信内容ID']).get_attribute(("text")))[0]
                logging.info(self.deviceid + u'-提取的发送内容为' + self.dx)
                self.task_validation()
                return True
            else:
                logging.info(self.deviceid + u'-扫码剩余时长' + str(end_time * 5 - self.i * 5))
                if self.i == end_time - 1:
                    token = TokenYZ.pdtoken()
                    submissionorder().fail(self.deviceid, self.taskid, token)
                    self.visualization('辅助并未扫描成功,等待时间已过,重新注册!')
                    logging.info(self.deviceid + u'-辅助并未扫描成功,等待时间已过,重新注册!')
                    if self.tm == '7':
                        if self.phmode == '14.玉米平台'.decode("utf-8"):
                            self.ph.yumi_cancelSMSRecv(self.phonenumber[0], self.phonenumber[1])
                    if self.phmode == '3.火箭API'.decode("utf-8"):
                        return self.ph.hj_fail(TokenYZ.pdtoken(), self.phonenumber[1])
                    self.driver.quit()
                    return False
    #切换VPN
    def switching_VPN(self):
        os.system('adb -s ' + self.deviceid + ' shell am force-stop org.proxydroid')
        os.system('adb -s ' + self.deviceid + ' shell am force-stop it.colucciweb.sstpvpnclient')

    #打开影子科技
    def start_yz(self):
        os.popen('adb -s ' + self.deviceid + ' shell am force-stop wechatscancoder.jionego.com.wechatscancoder')
        os.popen('adb -s %s shell am start -n wechatscancoder.jionego.com.wechatscancoder/.MainActivity' % self.deviceid).read()
        time.sleep(3)
        os.popen('adb -s %s shell am start -n com.tencent.mm/.ui.LauncherUI' % self.deviceid).read()

     #获取二维码图片
    def get_qr_image(self):
        folder = os.path.exists('./%s' % self.deviceid)
        if not folder:
            os.makedirs('./%s' % self.deviceid)
        else:
            pass
        res = requests.get('http://193.112.218.104:89/api?str=Initialize').text
        image = json.loads(res)['qrcode']
        data_62 = json.loads(res)['data']
        h = open("./%s/%s.jpg" % (self.deviceid, self.deviceid), "wb")
        h.write(base64.b64decode(image))
        h.close()
        os.popen('adb -s %s push ./%s/%s.jpg  /sdcard/myData/%s.jpg' % (self.deviceid, self.deviceid, self.deviceid,self.deviceid)).read()
        time.sleep(2)
        os.popen('adb -s %s shell mv /sdcard/myData/%s.jpg /sdcard/myData/scan.jpg' % (self.deviceid, self.deviceid)).read()
        time.sleep(2)
        os.system('adb -s %s shell curl http://127.0.0.1:8089?api=scandCode' % self.deviceid)
        return data_62



    #国内判断跳码
    def qr_validation(self, status):
        """
        判断是否跳码成功
        """
        if status == '1':
            self.driver.quit()
        if status == False:
            if self.tm == '9' or self.tm == '6':
                logging.info(self.deviceid + u'-未跳码成功,重新注册!')
                if self.phmode == '3.火箭API'.decode("utf-8"):
                    self.ph.hj_fail(TokenYZ.pdtoken(), self.phonenumber[1])
                if self.phmode == '9.老九专属API'.decode("utf-8"):
                    file().wite_lj_NotHopCode(self.phonenumber[0])
                if self.phmode == '2.菜鸟平台'.decode('utf-8'):
                    self.ph.cn_lh(self.phonenumber[0], self.phonenumber[1])
                if self.phmode == '12.国内私人3'.decode('utf-8'):
                    self.ph.grsr3_lh(self.phonenumber[1])
                if self.phmode == '13.国内私人4'.decode('utf-8'):
                    self.ph.grsr4_lh(self.phonenumber[1])
                self.driver.quit()
            else:
                self.Submission_Task()
                if self.cooperator == '1.火箭辅助'.decode("utf-8"):
                    if self.waiting_code(72) == True:
                        if self.phmode == '14.玉米平台'.decode("utf-8"):
                            return self.yumi_sendmsg(self.dx)
                        if self.phmode == '3.火箭API'.decode("utf-8"):
                            if self.ph.send_text(TokenYZ.pdtoken(), self.phonenumber[1], self.dx) == True:
                                return 'succ'
                            else:
                                return None
                        if self.phmode == '1.小鱼平台'.decode('utf-8'):
                            return self.ph.xiaoyu_send_message(self.phonenumber[0], self.dx)
                        if self.phmode == '13.国内私人4'.decode('utf-8'):
                            return self.ph.grsr4_send(self.phonenumber[1], self.dx)
                        if self.phmode == '12.国内私人3'.decode('utf-8'):
                            return self.ph.grsr3_send(self.phonenumber[1], self.dx)
                    else:
                        return False
        if status == True:
            dx = re.findall('[a-z0-9]{1,10}', self.driver.find_element_by_id(self.element_json[u'短信内容ID']).get_attribute(("text")))[0]
            self.visualization('正在发送信息:%s' % dx)
            logging.info(self.deviceid + u'-正在发送信息')
            logging.info(self.deviceid + u'-读取的短信内容为:' + dx)
            if self.phmode == '14.玉米平台'.decode("utf-8"):
                return self.yumi_sendmsg(dx)
            if self.phmode == '2.菜鸟平台'.decode('utf-8'):
                return self.ph.cn_send(self.phonenumber[1], dx)
            if self.phmode == '3.火箭API'.decode("utf-8"):
                #如果火箭平台返回True代表发送成功
                hj_status = self.ph.send_text(TokenYZ.pdtoken(), self.phonenumber[1], dx)
                if hj_status == True:
                    # 如果火箭平台返回True则返回一个succ
                    self.ph.hj_success(TokenYZ.pdtoken(), self.phonenumber[1])
                    return 'succ'
            if self.phmode == '7.辽宁API'.decode("utf-8"):
                ln_status=self.ph.ln_send(self.phonenumber[0], dx)
                if ln_status == True:
                    return 'succ'
            if self.phmode == '8.国内私人1'.decode("utf-8"):
                return self.ph.gnsr_send_text(self.phonenumber[0], dx)
            if self.phmode == '9.老九专属API'.decode("utf-8"):
                return self.ph.lj_send_text(self.phonenumber[0], dx)
            if self.phmode == '10.国内私人2'.decode('utf-8'):
                return self.ph.gnsr2_send(self.phonenumber[0], dx)
            if self.phmode == '12.国内私人3'.decode('utf-8'):
                return self.ph.grsr3_send(self.phonenumber[1], dx)
            if self.phmode == '13.国内私人4'.decode('utf-8'):
                return self.ph.grsr4_send(self.phonenumber[1], dx)
            if self.phmode == '1.小鱼平台'.decode('utf-8'):
                return self.ph.xiaoyu_send_message(self.phonenumber[0], dx)
    #提交任务
    def Submission_Task(self):
        """
        提交任务订单
        """
        self.driver.implicitly_wait(180)
        self.visualization('获取二维码')
        logging.info(self.deviceid + u'-获取二维码')
        self.visualization('正在解析二维码')
        logging.info(self.deviceid + u'-正在解析二维码')
        token = TokenYZ.pdtoken()
        url = analysis().get(self.deviceid)
        self.visualization('二维码解析地址:%s' % url)
        logging.info(self.deviceid + u'-二维码解析地址:%s' % url)
        if self.phmode == '3.火箭API'.decode("utf-8"):
            self.taskid = submissionorder().submission_hj(url, self.phonenumber[0], token, '360', self.phonenumber[1])
        else:
            self.taskid = submissionorder().submission(url, self.phonenumber[0], token, '360')
        self.visualization('订单提交成功')
        self.visualization('订单号:%s' % self.taskid)
        logging.info(self.deviceid + u'-订单提交成功')
        logging.info(self.deviceid + u'-订单号:' + self.taskid)
        self.driver.implicitly_wait(5)
    #玉米发短信
    def yumi_sendmsg(self, dx):
        try:
            yz = self.ph.yumi_sendmessages(dx, self.phonenumber[0], self.phonenumber[1])
            return yz
        except:
            logging.info(self.deviceid + u'-短信发送失败,卡商已下卡')
            self.visualization('短信发送失败,卡商已下卡')


    #提62
    def check_62(self):
        try:
            data = open('config.ini', 'r').read()
            return json.loads(data)['62'], json.loads(data)['A16']
        except:
            with open('config.ini', 'w') as f:
                f.write('{"62":"False","A16":"False"}')
            return "False", "False"

    def T_A16(self):
        os.system('adb -s %s shell input keyevent 3' % self.deviceid)
        A16_list = []
        file_list = os.popen('adb shell ls /data/data/com.tencent.mm/files/kvcomm/').readlines()
        try:
            for _file in file_list:
                if _file in _file:
                    os.system('adb shell su root chmod a+rw /data/data/com.tencent.mm/files/kvcomm/%s' % file)
                    file_data = os.popen(
                        'adb shell su root cat -v /data/data/com.tencent.mm/files/kvcomm/%s' % file).read()
                    A16 = re.findall(',(A[0-9a-z]{15})', file_data)
                    if A16 != []:
                        A16_list.append(A16[0])
            data = json.loads(
                os.popen('adb shell curl "http://127.0.0.1:8888/cmd?group=AppTool\&action=getHookDevice').read())['data']
            file().write('%s|%s|%s|%s|%s|%s|%s|%s' % (self.phonenumber[0], self.wxmm, A16_list[0], data['phone']['Imei'], data['build']['ANDROIDID'],data['phone']['BSSID'], data['build']['CPU_ABI'], data['build']['BRAND']), 'A16数据.txt')
            self.visualization('提A16数据成功')
            token().huojian_t62(self.deviceid, TokenYZ.pdtoken())
            logging.info(u'%s-提A16数据成功' % self.deviceid)
        except:
            self.visualization('提A16数据失败')
            logging.info(u'%s-提A16数据失败' % self.deviceid)


    def scanCode(self):
        config_data = self.check_62()
        if config_data[0] == "True":
            self.start_yz()
            if token().get_jurisdiction(TokenYZ.pdtoken(),self.deviceid) != None:
                for i in range(0, 2):
                    logging.info(self.deviceid + u'-开始提62')
                    data_62 = self.get_qr_image()
                    for j in range(0, 10):
                        os.system('adb -s %s shell input swipe 500 1200 500 1600' % self.deviceid)
                        self.driver.implicitly_wait(5)
                        if self.driver.find_elements_by_name('iPad 微信已登录') != []:
                            self.visualization('提62成功')
                            logging.info(self.deviceid + u'-提62成功')
                            file().write('%s----%s----%s----%s----%s\n' % (self.phonenumber[0], self.wxmm, data_62, self.wxid, datetime.datetime.now().strftime('%Y-%m-%d')), '提62成功列表.txt')
                            token().huojian_t62(self.deviceid, TokenYZ.pdtoken())
                            return data_62
                        if j == 9:
                            logging.info(u'%s-提取62失败' % self.deviceid)
                            self.visualization('提取62失败')
                            file().write('%s|\n' % self.phonenumber[0], '提62失败列表.txt')
                    if i == 1:
                        break
        if config_data[1] == "True":
            os.system('adb -s %s shell input keyevent 3' % self.deviceid)
            if token().huojian_t62(self.deviceid, TokenYZ.pdtoken()) == True:
                self.T_A16()

    #写入文件
    def xr_wechat(self,wxid=None):
        self.visualization('准备写入微信数据')
        logging.info(self.deviceid+u'-准备写入微信数据')
        if self.gj_mode == '1.微霸改机'.decode("utf-8"):
            wechat_list = '%s_%s  %s  %s  %s  %s  \n' % (self.phonenumber[0], self.wxmm, self.ip, self.deviceid, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), wxid)
            file().write(wechat_list, '微信账号数据.txt')

    def cloud_wechat(self,wxid=None,cloudCode=None):
        self.visualization('准备写入微信数据')
        logging.info(self.deviceid + u'-准备写入微信数据')
        if self.gj_mode == '1.微霸改机'.decode("utf-8"):
            wechat_list = '%s_%s  %s  %s  %s  %s  %s\n' % (self.phonenumber[0], self.wxmm, self.ip, self.deviceid, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), wxid,cloudCode)
            file().write(wechat_list, '微信账号数据(带云码).txt')

    def send_login(self):
            self.visualization('短信发送成功')
            logging.info(self.deviceid + u'-短信发送成功')
            if self.phmode == '8.国内私人1'.decode("utf-8"):
                self.ph.qg_card_add(TokenYZ.pdtoken(), self.phonenumber[0])
            if self.phmode == '1.小鱼平台'.decode('utf-8'):
                time.sleep(32)
            time.sleep(8)
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_name(self.element_json['Next_Step']).click()
            # 判断是否发送短信失败,点击下一步
            self.driver.implicitly_wait(2)
            while True:
                os.system('adb -s %s shell input tap 600 1098' % self.deviceid)
                if self.driver.find_elements_by_id(self.element_json[u'输入框ID'])!=[]:
                    self.driver.quit()
                if self.driver.find_elements_by_id(self.element_json[u'错误弹窗确定ID']) != []:
                    self.cw = self.driver.find_element_by_id(self.element_json[u'错误弹窗内容ID']).get_attribute(('text'))
                    if '短信' in self.cw.encode('utf-8'):
                        self.driver.find_element_by_id(self.element_json[u'错误弹窗确定ID']).click()
                        if self.phmode == '1.小鱼平台'.decode('utf-8'):
                            time.sleep(75)
                        time.sleep(25)
                        self.driver.find_element_by_name(self.element_json['Next_Step']).click()
                        time.sleep(20)
                        if self.driver.find_elements_by_id(self.element_json[u'错误弹窗确定ID'])!=[]:
                            self.cw = self.driver.find_element_by_id(self.element_json[u'错误弹窗内容ID']).get_attribute(('text'))
                            if '短信' in self.cw.encode('utf-8'):
                                self.visualization('已点击过"已发送短信，下一步"两次,还是未注册成功,进入重新注册流程')
                                logging.info(self.deviceid + u'-已点击过"已发送短信，下一步"两次,还是未注册成功,进入重新注册流程')
                                self.driver.quit()
                            if '逻辑' in self.cw.encode('utf-8'):
                                self.driver.find_element_by_id(self.element_json[u'错误弹窗确定ID']).click()
                                self.visualization('已进入到微信页面,等待5秒判断是否出现秒封状况')
                                logging.info(self.deviceid + u'-已进入到微信页面,等待5秒判断是否出现秒封状况')
                                if self.driver.find_elements_by_id(self.element_json[u'错误弹窗确定ID']) != []:
                                    self.cw = self.driver.find_element_by_id(self.element_json[u'错误弹窗内容ID']).get_attribute(('text'))
                                    if '表情' in self.cw.encode('utf-8'):
                                        self.driver.find_element_by_name('取消').click()
                                        self.wxid = self.w.get_wxid()
                                        self.xr_wechat(self.wxid)
                                        if self.w.save_wechat_data(self.phonenumber[0], self.wxid, self.wxmc) == True:
                                            break
                                    else:
                                        self.visualization('账号秒封')
                                        logging.info(self.deviceid + u'-账号秒封,重新注册')
                                else:
                                    self.wxid = self.w.get_wxid()
                                    self.xr_wechat(self.wxid)
                                    if self.w.save_wechat_data(self.phonenumber[0], self.wxid, self.wxmc) == True:
                                        break
                    if '异常' in self.cw.encode('utf-8'):
                        self.visualization('该账号被秒封')
                        logging.info(self.deviceid + u'-该账号被秒封')
                        if self.gj_mode == '1.微霸改机'.decode("utf-8"):
                            self.wxid = self.w.get_wxid()
                            self.xr_wechat(self.wxid)
                            if self.w.save_wechat_data(self.phonenumber[0], self.wxid, self.wxmc) == True:
                                break
                    if '逻辑' in self.cw.encode('utf-8'):
                        self.driver.find_element_by_id(self.element_json[u'错误弹窗确定ID']).click()
                        self.visualization('已进入到微信页面,等待10秒判断是否出现秒封状况')
                        logging.info(self.deviceid + u'-已进入到微信页面,等待10秒判断是否出现秒封状况')
                        self.driver.implicitly_wait(10)
                        if self.driver.find_elements_by_id(self.element_json[u'错误弹窗确定ID']) != []:
                            self.cw = self.driver.find_element_by_id(self.element_json[u'错误弹窗内容ID']).get_attribute(('text'))
                            if '表情' in self.cw.encode('utf-8'):
                                self.driver.find_element_by_name('取消').click()
                                self.wxid = self.w.get_wxid()
                                self.xr_wechat(self.wxid)
                                if self.w.save_wechat_data(self.phonenumber[0], self.wxid, self.wxmc) == True:
                                    break
                            else:
                                self.visualization('账号秒封')
                                logging.info(self.deviceid + u'-账号秒封,重新注册')
                        else:
                            self.wxid = self.w.get_wxid()
                            self.xr_wechat(self.wxid)
                            if self.w.save_wechat_data(self.phonenumber[0], self.wxid, self.wxmc) == True:
                                break
                    if '一个月' in self.cw.encode('utf-8'):
                        self.visualization('该手机号码一个月之内不能重复注册')
                        logging.info(self.deviceid + u'-该手机号码一个月之内不能重复注册')
                        self.driver.quit()
                    if '当天' in self.cw.encode('utf-8'):
                        self.visualization('该手机号码当天不能重复注册')
                        logging.info(self.deviceid + u'-该手机号码当天不能重复注册')
                        os.popen('adb -s %s shell input keyevent 4' % self.deviceid).read()
                        time.sleep(3)
                        os.popen('adb -s %s shell input keyevent 4' % self.deviceid).read()
                        self.driver.implicitly_wait(60)
                        if self.driver.find_elements_by_id(self.element_json[u'输入框ID'])!=[]:
                            os.popen('adb -s %s shell input keyevent 4' % self.deviceid).read()
                            if self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID'])!=[]:
                                pass
                    if '不正确' in self.cw.encode('utf-8'):
                        self.visualization('发送的验证码不正确')
                        logging.info(self.deviceid + u'-发送的验证码不正确')
                        self.driver.quit()
                    if '表情' in self.cw.encode('utf-8'):
                        self.driver.find_element_by_name('　取消　').click()
                if self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID']) != []:
                    self.visualization('已进入到微信页面,等待10秒判断是否出现秒封状况')
                    logging.info(self.deviceid + u'-已进入到微信页面,等待10秒判断是否出现秒封状况')
                    self.driver.implicitly_wait(10)
                    if self.driver.find_elements_by_id(self.element_json[u'错误弹窗确定ID']) != []:
                        self.cw = self.driver.find_element_by_id(self.element_json[u'错误弹窗内容ID']).get_attribute(('text'))
                        if '表情' in self.cw.encode('utf-8'):
                            self.driver.find_element_by_name('　取消　').click()
                            self.wxid = self.w.get_wxid()
                            self.xr_wechat(self.wxid)
                        if self.w.save_wechat_data(self.phonenumber[0], self.wxid, self.wxmc) == True:
                            break
                        else:
                            self.visualization('账号秒封')
                            logging.info(self.deviceid + u'-账号秒封,重新注册')
                            self.driver.quit()
                    else:
                        self.wxid = self.w.get_wxid()
                        self.xr_wechat(self.wxid)
                        if self.w.save_wechat_data(self.phonenumber[0], self.wxid, self.wxmc) == True:
                            break

    def judge_Expression(self):
        self.driver.implicitly_wait(2)
        if self.driver.find_elements_by_id(self.element_json[u'错误弹窗确定ID']) != []:
            self.cw = self.driver.find_element_by_id(self.element_json[u'错误弹窗内容ID']).get_attribute(('text'))
            if '表情' in self.cw.encode('utf-8'):
                self.driver.find_element_by_name('　取消　').click()
        self.driver.implicitly_wait(60)



    def save_wechat_data(self):
        self.xr_wechat(self.wxid)
        self.visualization('注册数据已写入文件')
        logging.info(self.deviceid + u'-注册数据已写入文件')
        self.visualization('正在保存微霸数据请稍等')
        logging.info(self.deviceid + u'-正在保存微霸数据请稍等')
    # 国内登录
    def login_validation(self, yz):
        if yz == None:
            self.driver.quit()
        if yz == 'succ':
            self.send_login()

    #国内发圈
    def fpyq(self, yz):
        if yz == None:
            self.driver.quit()
        if yz == 'succ':
            self.send_login()
            self.visualization('重新打开WX')
            logging.info(self.deviceid + u'-重新打开WX')
            self.driver = Open().Phone('com.tencent.mm', '.ui.LauncherUI', self.deviceid, self.port)
            time.sleep(10)
            self.judge_Expression()
            self.driver.implicitly_wait(2)
            while True:
                if self.driver.find_elements_by_id(self.element_json[u'错误弹窗确定ID'])!=[]:
                    self.driver.quit()
                    break
                if self.driver.find_elements_by_id(self.element_json[u'首页注册ID'])!=[]:
                    self.visualization('账号被秒封')
                    logging.info(self.deviceid + u'-账号被秒封')
                    self.driver.quit()
                    break
                if self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID'])!=[]:
                    self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID'])[2].click()
                    self.visualization('点击发现')
                    logging.info(self.deviceid + u'-点击发现')
                    break
                if  self.driver.find_elements_by_id(self.element_json[u'输入框ID'])!=[]:
                    self.visualization('账号被秒封')
                    logging.info(self.deviceid + u'-账号被秒封')
                    self.driver.quit()
            self.driver.implicitly_wait(2)
            self.judge_Expression()
            if self.driver.find_elements_by_id(self.element_json[u'发现页面朋友圈ID'])!=[]:
                self.driver.find_elements_by_id(self.element_json[u'发现页面朋友圈ID'])[0].click()
                time.sleep(random.randint(1, 3))
            else:
                self.visualization('点击发现失败,重新点击')
                logging.info(self.deviceid + u'-点击发现失败,重新点击')
                self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID'])[2].click()
                self.driver.find_elements_by_id(self.element_json[u'发现页面朋友圈ID'])[0].click()
            self.judge_Expression()
            if self.driver.find_elements_by_id(self.element_json[u'朋友圈相机ID'])!=[]:
                TouchAction(self.driver).long_press(self.driver.find_element_by_id(self.element_json[u'朋友圈相机ID']), 2000).release().perform()
            self.judge_Expression()
            self.driver.implicitly_wait(5)
            #检测有没有朋友圈
            if self.driver.find_elements_by_id(self.element_json[u'发表按钮ID'])!=[]:
                self.input_pyq_message()
            else:
                time.sleep(random.randint(1, 2))
                self.driver.find_element_by_id(self.element_json[u'我知道了ID']).click()
                self.input_pyq_message()
            logging.info(self.deviceid + u'-点击发表')
            self.visualization('点击发表')
            self.judge_Expression()
            self.driver.find_element_by_android_uiautomator(
                'new UiSelector().description("返回")').click()
            self.judge_Expression()
            self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID'])[0].click()
            time.sleep(3)
            self.cloudCode = self.w.getCloudCode(self.phonenumber[0])
            self.cloud_wechat(self.wxid,self.cloudCode)

        else:
            self.visualization('未接收到卡商反馈，注册失败')
            logging.info(self.deviceid + u'-未接收到卡商反馈，注册失败')

    def input_pyq_message(self):
        time.sleep(random.randint(1, 2))
        self.driver.find_element_by_id(self.element_json[u'朋友圈内容输入框ID']).click()
        self.driver.find_element_by_id(self.element_json[u'朋友圈内容输入框ID']).send_keys(file().sh())
        logging.info(self.deviceid + u'-输入文字')
        self.visualization('输入文字')
        time.sleep(random.randint(1, 2))
        self.driver.find_element_by_id(self.element_json[u'发表按钮ID']).click()

    def pd_gj(self):
        if self.gj_mode == '1.微霸改机'.decode("utf-8"):
            self.wb_new()
        if self.gj_mode == '2.神奇改机'.decode("utf-8"):
            self.dd_new()

    def new_zh(self):
        try:
            self.pd_gj()
            self.register()
            self.input_text()
            self.login_validation(self.qr_validation(self.yztp()))
        except:
            traceback.print_exc()
            self.visualization('账号注册失败')
            logging.info(self.deviceid + u'-账号注册失败')

    def new_zhpyq(self):
        try:
            self.pd_gj()
            self.register()
            self.input_text()
            self.fpyq(self.qr_validation(self.yztp()))
        except:
            self.visualization('账号注册失败')
            logging.info(self.deviceid + u'-账号注册失败')

    def zc_pyq_t62(self):
        try:
            self.pd_gj()
            if self.country == '1.国内'.decode("utf-8"):
                self.register()
                self.input_text()
                self.fpyq(self.qr_validation(self.yztp()))
                self.scanCode()
        except:
            traceback.print_exc()
            self.visualization('账号注册失败')
            logging.info(self.deviceid + u'-账号注册失败')
            try:
                if self.phmode == '3.火箭API'.decode("utf-8"):
                    self.ph.hj_fail(TokenYZ.pdtoken(), self.phonenumber[1])
            except:pass
