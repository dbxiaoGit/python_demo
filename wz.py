from com.android.monkeyrunner import MonkeyDevice,MonkeyRunner

driver = MonkeyRunner.waitForConnection(30,'0123456789ABCDEF')
print type(driver)
w = driver.getProperty('display.width')
h = driver.getProperty('display.height')
print int(w)

cg_x = int(w)*1450/1920
cg_y = int(h)*920/1080

pm_x = int(w)/2
pm_y = int(h)*1020/1080

zl_x = int(w)*1450/1920
zl_y = int(h)*990/1080

print 'cg(%d,%d),pm(%d,%d),zl(%d,%d)'%(cg_x,cg_y,pm_x,pm_y,zl_x,zl_y)


driver.startActivity(component = "com.tencent.tmgp.sgame/com.tencent.tmgp.sgame.SGameActivity")
#MonkeyRunner.sleep(5)
while True :
	driver.wake()
	print 'step1:press chuangguan'
	driver.touch(cg_x,cg_y,MonkeyDevice.DOWN_AND_UP)
	MonkeyRunner.sleep(5)
	
	print 'step2:sleep 100s'
	MonkeyRunner.sleep(100)
	
	print 'step3:press screen'
	driver.touch(pm_x,pm_y,MonkeyDevice.DOWN_AND_UP)
	MonkeyRunner.sleep(1)
	driver.touch(pm_x,pm_y,MonkeyDevice.DOWN_AND_UP)
	MonkeyRunner.sleep(5)
	
	print 'step4:press play again'
	driver.touch(zl_x,zl_y,MonkeyDevice.DOWN_AND_UP)
	MonkeyRunner.sleep(5)
