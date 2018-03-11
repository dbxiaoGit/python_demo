from com.android.monkeyrunner import MonkeyDevice,MonkeyRunner
import traceback

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
				MonkeyRunner.sleep(1)
				count = count+1
	except BaseException,e:
		print traceback.print_exc()
	finally:
		auto_touch()
auto_touch()
