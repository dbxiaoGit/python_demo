from com.android.monkeyrunner import MonkeyDevice,MonkeyRunner
import traceback

class AutoPlayer:
	driver = ''
	point_x = ''
	point_y = ''
	point_x1 = ''
	point_y1 = ''
	count = 1
	def __init__(self):
		AutoPlayer.driver = MonkeyRunner.waitForConnection()
		print type(AutoPlayer.driver)
		self.screen_width = AutoPlayer.driver.getProperty('display.width')
		self.screen_height = AutoPlayer.driver.getProperty('display.height')
		print int(self.screen_width )
		AutoPlayer.point_x = int(self.screen_width)*1600/1920
		AutoPlayer.point_y = int(self.screen_height)*960/1080
		AutoPlayer.point_x1 = int(self.screen_width)*1710/1920
		AutoPlayer.point_y1 = int(self.screen_height)*100/1080
		print 'cg(%d,%d)'%(AutoPlayer.point_x,AutoPlayer.point_y)
		AutoPlayer.driver.startActivity(component = "com.tencent.tmgp.sgame/com.tencent.tmgp.sgame.SGameActivity")
	def auto_play(self):
		while True :
			try:
				print 'touch count:%d ,touch postion x:%d ,y:%d'%(AutoPlayer.count,AutoPlayer.point_x,AutoPlayer.point_y)
				#driver.wake()
				AutoPlayer.driver.touch(AutoPlayer.point_x,AutoPlayer.point_y,MonkeyDevice.DOWN_AND_UP)
				MonkeyRunner.sleep(1)
				AutoPlayer.driver.touch(AutoPlayer.point_x1,AutoPlayer.point_y1,MonkeyDevice.DOWN_AND_UP)
				MonkeyRunner.sleep(3)
				AutoPlayer.count = AutoPlayer.count+1
			except BaseException,e:
				print traceback.print_exc()
if __name__ == '__main__':
	switch_flag = False
	auto_player_1 = ''
	while True:
		try:
			auto_player_1 = AutoPlayer()
			switch_flag = True
		except BaseException,e:
			print traceback.print_exc()
		finally:
			if switch_flag :
				break
	auto_player_1.auto_play()
