import machine

def deep_sleep_seconds(seconds):
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, seconds * 1000)
    print('Entering deep sleep for %s seconds' % seconds)
    machine.deepsleep()