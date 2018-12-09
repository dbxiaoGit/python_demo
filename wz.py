from com.android.monkeyrunner import MonkeyDevice,MonkeyRunner
import traceback

class AutoPlayer:
	def __init__(self):
		self.count = 1
		self.driver = MonkeyRunner.waitForConnection("MKJNW17C19000245",30)
		print type(self.driver)
		self.screen_width = self.driver.getProperty('display.width')
		self.screen_height = self.driver.getProperty('display.height')
		print int(self.screen_width )
		print int(self.screen_height)
		self.point_x = int(self.screen_width)*1600/1920
		self.point_y = int(self.screen_height)*960/1080
		print 'cg(%d,%d)'%(self.point_x,self.point_y)
		self.driver.startActivity(component = "com.tencent.tmgp.sgame/com.tencent.tmgp.sgame.SGameActivity")
	def auto_play(self):
		while True :
			try:
				#self.driver = MonkeyRunner.waitForConnection()
				print 'touch count:%d ,touch postion x:%d ,y:%d'%(self.count,self.point_x,self.point_y)
				self.driver.touch(self.point_x,self.point_y,MonkeyDevice.DOWN_AND_UP)
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
		finally:
			auto_player_1 = AutoPlayer()
			auto_player_1.auto_play()
