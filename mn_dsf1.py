from com.android.monkeyrunner import MonkeyDevice,MonkeyRunner
import traceback
'''
def auto_touch():
	try:
		driver = MonkeyRunner.waitForConnection(30,'0123456789ABCDEF')
		print type(driver)
		w = driver.getProperty('display.width')
		h = driver.getProperty('display.height')
		print int(w)
		cg_x = int(w)*1600/1920
		cg_y = int(h)*960/1080
		print 'cg(%d,%d)'%(cg_x,cg_y)
		count = 1
		driver.startActivity(component = "com.tencent.tmgp.sgame/com.tencent.tmgp.sgame.SGameActivity")
		while True :
				print 'touch count:%d ,touch postion x:%d ,y:%d'%(count,cg_x,cg_y)
				driver.wake()
				driver.touch(cg_x,cg_y,MonkeyDevice.DOWN_AND_UP)
				MonkeyRunner.sleep(2)
				count = count+1
	except BaseException,e:
		print traceback.print_exc()
	finally:
		auto_touch()
auto_touch()
'''
class AutoPlayer:
	driver = ''
	point_x = ''
	point_y = ''
	count = 1
	def __init__(self):
		AutoPlayer.driver = MonkeyRunner.waitForConnection(30,'0123456789ABCDEF')
		print type(AutoPlayer.driver)
		self.screen_width = AutoPlayer.driver.getProperty('display.width')
		self.screen_height = AutoPlayer.driver.getProperty('display.height')
		print int(self.screen_width )
		AutoPlayer.point_x = int(self.screen_width)*1600/1920
		AutoPlayer.point_y = int(self.screen_height)*960/1080
		print 'cg(%d,%d)'%(AutoPlayer.point_x,AutoPlayer.point_y)
		AutoPlayer.driver.startActivity(component = "com.tencent.tmgp.sgame/com.tencent.tmgp.sgame.SGameActivity")
	def auto_play(self):
		while True :
			try:
				print 'touch count:%d ,touch postion x:%d ,y:%d'%(AutoPlayer.count,AutoPlayer.point_x,AutoPlayer.point_y)
				#driver.wake()
				AutoPlayer.driver.touch(AutoPlayer.point_x,AutoPlayer.point_y,MonkeyDevice.DOWN_AND_UP)
				MonkeyRunner.sleep(2)
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
	
