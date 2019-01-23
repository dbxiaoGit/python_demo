#coding=utf-8
from com.android.monkeyrunner import MonkeyDevice,MonkeyRunner
import traceback

class AutoPlayer:
	def __init__(self):
		self.count = 1
		self.driver = MonkeyRunner.waitForConnection()
		print type(self.driver)
		self.screen_width = self.driver.getProperty('display.width')
		self.screen_height = self.driver.getProperty('display.height')
		print 'width:%s,height:%s'%(self.screen_width,self.screen_height)
		self.point_x1 = int(self.screen_width)*1520/1920
		self.point_y1 = int(self.screen_height)*1000/1080
		self.point_x2 = int(self.screen_width)*1520/1920
		self.point_y2 = int(self.screen_height)*880/1080
		print 'self.point_x1:%d,self.point_y1:%d'%(self.point_x1,self.point_y1)
		print 'self.point_x2:%d,self.point_y2:%d'%(self.point_x2,self.point_y2)
		self.driver.startActivity(component = "com.tencent.tmgp.sgame/com.tencent.tmgp.sgame.SGameActivity")
	def auto_play(self):
		while True :
			try:
				print 'touch count:%d ,touch postion x:%d ,y:%d'%(self.count,self.point_x1,self.point_y1 )
				#driver.wake()
				self.driver.touch(self.point_x1,self.point_y1,MonkeyDevice.DOWN_AND_UP)
				MonkeyRunner.sleep(1)
				print 'touch count:%d ,touch postion x1:%d ,y1:%d'%(self.count,self.point_x2,self.point_y2)
				self.driver.touch(self.point_x2,self.point_y2,MonkeyDevice.DOWN_AND_UP)
				MonkeyRunner.sleep(1)
				self.count = self.count+1
			except BaseException,e:
				print traceback.print_exc()
if __name__ == '__main__':
	auto_player_1 = ''
	while True:
		try:
			auto_player_1 = AutoPlayer()
			auto_player_1.auto_play()
		except BaseException,e:
			print traceback.print_exc()
			auto_player_1 = AutoPlayer()
			auto_player_1.auto_play()
		
