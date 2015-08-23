Hadoop MapReduce LogParser
====

This is a simple log parser for Hadoop MapReduce standard log, developed with [@jaquejbrito](http://github.com/jaquejbrito). The script will parse the whole log file into a rather simple list of dictionaries, following a simple logic. It is considered that in each logfile there are several executions of each algorithm/program (intended, for instance, to further analyses). Each execution is then divided in several different jobs, or map-reduce cycles. This script will parse all relevant information seperately for each job, then for each execution time. See example below.


Example of usage
----

For instance, suppose you have a logfile called [Example1.log](https://github.com/thmosqueiro/RandomPy/blob/master/Hadoop_MapReduce_LogParser/Exemplo1.log) with three executions with three jobs each, then you can run:
```
import HMRLogParser as lib
ExecMeasures = lib.HMRlogParser('Example1.log')
```
Then, *ExecMeasures* object will have all data you need. The information of all jobs regarding the first execution will be the first element: *ExecMeasures[0]*. To access information about j-th job during i-th execution, simply use *ExecMeasures[i][j]*.

The information is stored in dictionaries. There are a total of 6 dictionaries:
```
>>>  print ExecMeasures[0][0].keys()
['File Output Format Counters', 'File Input Format Counters', 'Map-Reduce Framework', 
'File System Counters', 'Job Counters', 'Shuffle Errors']
```
Each of the above dictionary names are tagged according to the standard logfile from Hadoop MapReduce. In each of these dictionaries, you will find the actual measures:
```
>>> print ExecMeasures[0][0]['File System Counters']
{'FILE: Number of write operations': 0.0, 'HDFS: Number of write operations': 560.0, 
'FILE: Number of read operations': 0.0, 'HDFS: Number of bytes read': 63658132005.0, 
'HDFS: Number of read operations': 2271.0, 'FILE: Number of bytes written': 42339241102.0, 
'HDFS: Number of large read operations': 0.0, 'HDFS: Number of bytes written': 598406528.0, 
'FILE: Number of large read operations': 0.0, 'FILE: Number of bytes read': 21205204191.0}
```
If you need a list of all measures inside any given dictionary, just use *.keys()* method.
```
>>> print ExecMeasures[0][0]['File System Counters'].keys()
['FILE: Number of write operations', 'HDFS: Number of write operations', 
'FILE: Number of read operations', 'HDFS: Number of bytes read', 
'HDFS: Number of read operations', 'FILE: Number of bytes written', 
'HDFS: Number of large read operations', 'HDFS: Number of bytes written', 
'FILE: Number of large read operations', 'FILE: Number of bytes read']
```
Thus, you don't need to go dig the logfiles to file what each item means.

This data organization makes it easy to run averages or any kind of statistics throughout a set of logfiles. At the end of **HMRLogParser.py** file you can find a small example evaluating averages over time.


Example of batch analysis
---

You can simply run the following to see how the parser works.
```
python HMRLogParser.py
```
This should prompt the following graph.

<img src="https://raw.githubusercontent.com/thmosqueiro/RandomPy/master/Hadoop_MapReduce_LogParser/ExampleGraph.png" width=350px />




# License
------

This is under the WTFPL, use it as you want. Stars are welcome thou.


```
	     DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
                    Version 2, December 2004 

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net> 

 Everyone is permitted to copy and distribute verbatim or modified 
 copies of this license document, and changing it is allowed as long 
 as the name is changed. 

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 

  0. You just DO WHAT THE FUCK YOU WANT TO.
```

**tl;dr** version: use it as you please, just don't sue me.
