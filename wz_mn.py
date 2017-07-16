from com.android.monkeyrunner import MonkeyDevice,MonkeyRunner

driver = MonkeyRunner.waitForConnection(30,'0123456789ABCDEF')
print type(driver)
w = driver.getProperty('display.width')
h = driver.getProperty('display.height')
print int(w)

cg_x = int(w)*1450/1920
cg_y = int(h)*920/1080

auto_x = int(w)*1790/1920
auto_y = int(h)*43/1080

pm_x = int(w)/2
pm_y = int(h)*1020/1080

zl_x = int(w)*1450/1920
zl_y = int(h)*990/1080

print 'cg(%d,%d),pm(%d,%d),zl(%d,%d)'%(cg_x,cg_y,pm_x,pm_y,zl_x,zl_y)
count = 1

driver.startActivity(component = "com.tencent.tmgp.sgame/com.tencent.tmgp.sgame.SGameActivity")
def wait(sec):
	for i in range(sec):
		print 'wait %dth seconds,count=%d'%(i,count)
		MonkeyRunner.sleep(1)
		driver.touch(pm_x,pm_y,MonkeyDevice.DOWN_AND_UP)

while True :
	print 'count:%d'%count
	driver.wake()
	print 'step1:press chuangguan'
	driver.touch(cg_x,cg_y,MonkeyDevice.DOWN_AND_UP)
	wait(20)
	driver.touch(auto_x,auto_y,MonkeyDevice.DOWN_AND_UP)
	
	
	print 'step2:wait for game over'
	wait(60)
	
	print 'step3:press screen'
	#driver.touch(pm_x,pm_y,MonkeyDevice.DOWN_AND_UP)
	#wait(7)
	#driver.touch(pm_x,pm_y,MonkeyDevice.DOWN_AND_UP)
	#wait(5)
	
	print 'step4:press play again'
	driver.touch(zl_x,zl_y,MonkeyDevice.DOWN_AND_UP)
	wait(8)
	count = count+1
