# trafficlight  
  
start and stop ec2 instances.  
  
### installation  
  
##### install with pip  
  
`pip install trafficlight`  
  
##### install from git repo  
  
https://bitbucket.org/rednap/trafficlight  
  
after cloning the repo to your machine. change directories into the repo.  
  
`$ cd trafficlight`  
   
`$ sudo cp trafficlight /usr/local/bin && sudo chmod a+x /usr/local/bin/trafficlight`  
  
confirm it's installed  
  
`$ which trafficlight`  
  
### dependencies   
  
-aws cli (installed and configured)  
-python3 (my env has python aliased to python3, if yours is different you'll need to change the shebang line)   
  
### usage  
  
show trafficlight help page, including usage and flags.  
`$ trafficlight -h`  
   
switch instance with tag Name:example. if instance is stopped it will start, if it's running it will stop.   
`$ trafficlight example`   
   
start all instances with tag Name:example. if instances are started already they will stay up.   
`$ trafficlight example -g`   
   
stop all instances tag Name:example. if instances are stopped already they will stay stopped.   
`$ trafficlight example -r`   
   
stop all instances with tag Products:example.    
`$ trafficlight example --key Products -r`   
   
list all ec2s and do nothing.  
`$ trafficlight -a`  
  
list all ec2s and stop them.  
`$ trafficlight -ar`  
