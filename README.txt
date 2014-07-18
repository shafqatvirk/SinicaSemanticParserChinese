INTRODUCTION
============
System for SenticNet Semantic analysis Challenge Task#2. The system is supposed to take input in the form of a text
file and produce "concepts" extracted from each of the sentence in the required format mentioned at the challenge website (http://sentic.net/challenge/).

DOWNLOADING and UNZIPPING
=========================
If you have downloaded it from github, you should have got 'SinicaSemanticParser-master.zip'. Please unzip it and rename the resulting directory to 'SinicaSemanticParser'. 

REQUIRMENTS
===========
The system requires at least Java, Python, Stanford Parser, and apache-opennlp. The system has been tested with the following configurations:

1. Windows 7
	- Java  version 1.7 update 45
	- Python 2.7.5
2. Windows 8
	- Java version 1.7 update 55
	- Python 2.7.5
	
3. Mac
	- Java version 1.8.0
	- Python 2.7.5

4. Linux (ubuntu 12.04)
	- Java 1.7 update 55
	- Python 2.7.3
	
FOLDER CONTENTS
===============
This directory 'SinicaSemanticParser' contains the following directries:

	1. classifier
	2. data
	3. headFinder
	4. input
	5. models
	6. output
	7. shared
	8. system
	9. temp
	10. tools
	
INSTRUCTIONS TO RUN THE SYSTEM
==============================
1. Please download Stanford Parser version 3.3.1 from this link (http://nlp.stanford.edu/software/lex-parser.shtml#Download), 
extract it and put the resulting 'stanford-parser-full-2014-01-04' directory in the 'SinicaSemanticParser' directory.

2. Please download 'apache-opennlp-1.5.3-bin.zip' from here (https://opennlp.apache.org/cgi-bin/download.cgi)
extract it and put the resulting 'apache-opennlp-1.5.3' directory in the 'SinicaSemanticParser' directory.

Note: Make sure after unzipping you get the directries named 'stanford-parser-full-2014-01-04' and 'apache-opennlp-1.5.3'. We have observed depening on
how to unzip it, you might get 'stanford-parser-full-2014-01-04/stanford-parser-full-2014-01-04' and 'apache-opennlp-1.5.3-bin/apache-opennlp-1.5.3'. 
In such cases just copy the 'stanford-parser-full-2014-01-04' and 'apache-opennlp-1.5.3' to 'SinicaSemanticParser' directory.

3. From the command prompt go into the 'SinicaSemanticParser/system' directory and compile java programs with the following command:

>javac -cp .;..\stanford-parser-full-2014-01-04\stanford-parser.jar;..\stanford-parser-full-2014-01-04\stanford-parser-3.3.1-models.jar;..\classifier\maxent\lib\trove-3.0.3.jar;..\apache-opennlp-1.5.3\lib\opennlp-maxent-3.0.3.jar *.java

4. Now run the 'ConceptExtractorServer' with the following command:

>java -cp .;..\stanford-parser-full-2014-01-04\stanford-parser.jar;..\stanford-parser-full-2014-01-04\stanford-parser-3.3.1-models.jar;..\classifier\maxent\lib\trove-3.0.3.jar;..\apache-opennlp-1.5.3\lib\opennlp-maxent-3.0.3.jar ConceptExtractorServer

You should see the following message:

"Loading parser from serialized file edu/stanford/nlp/models/lexparser/englishPCF
G.ser.gz ... done [2.4 sec].
Server Initialized, Waiting for input..."

Leave this server running.

5. Open another command line terminal, go into the 'SinicaSemanticParser/system/' directory and start 'featureExtractorServer' by using the following command:

>python featureExtractorServer.py

You should see the following message:

"Loading...
Ready!"

Leave this server running

6. Open another command line terminal, go into the 'SinicaSemanticParser/system/' directory and start 'featureExtractorServer' by using the following command:

>python featureExtractorServerLayer2.py

You should see the following message:

"Loading...
Ready!"

Leave this server running

7. Now place your input file in the 'SinicaSemanticParser/input/' directory and name it input.txt (the input.txt should have one tree (parsed Chinese sentence) per line). Currently it works on parsed sentences, but later the functionality of automatic parsing can be added as is in the english case

8. Open another command line terminal, go into the 'SinicaSemanticParser/system' directory and run the 'ConceptExtractorBatchClient' by issuing the following command:

>java -cp .;..\stanford-parser-full-2014-01-04\stanford-parser.jar;..\stanford-parser-full-2014-01-04\stanford-parser-3.3.1-models.jar;..\classifier\maxent\lib\trove-3.0.3.jar;..\apache-opennlp-1.5.3\lib\opennlp-maxent-3.0.3.jar ConceptExtractorBatchClient

If everything goes well, you should see the following message:

"SocketClient initialized
Processing......
Done!"

8. The output has been stored in the 'SinicaSemanticParser/output/output.txt'.





