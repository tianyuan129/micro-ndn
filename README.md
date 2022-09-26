# micro-ndn
A Docker-based NDN Emulation Tool.
This tool is not another [Mini-NDN](https://github.com/named-data/mini-ndn), but a docker-based tool for people who want to have NDN environment in containers with basic topology settings.

It only brings up few container instances with some help on security bootstrapping and connectivity/reachability setup.
By default, this tool pulls image ``tianyuan129/ndn-basic:latest``.

The code is simple and please look at ``example.py`` for tool usage. 

Prerequistes
------------
Have Docker installed and its daemon is running.

Install
---------
```
pip3 install  .
```

Try Example
------------
```
python3 example.py 
```
