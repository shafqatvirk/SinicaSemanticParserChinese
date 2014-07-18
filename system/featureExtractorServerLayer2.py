import SocketServer
import sys
sys.path.append("../shared")
from prepareData import *
from buildModelAuxiliaries3 import *
from ehownet import *
from auxiliaryFuns import *
import os
import itertools

class MyTCPHandler(SocketServer.BaseRequestHandler):
	"""
	The RequestHandler class for our server.

	It is instantiated once per connection to the server, and must
	override the handle() method to implement communication to the
	client.
	"""
	
	
	print "Loading..."
	
	#simplified_tradictional_dict = build_simplified_traditional_dict()
	#tree_head_dict = build_tree_head_dict()
	#word2semType_dict = word2semType()
	#frameset_file_dict = frameset_dict() # verb_frame information
	#e_hownet=EHowNetTree("../data/ehownet_ontology.txt")
    
	print "Ready!"
	def handle(self):
		# self.request is the TCP socket connected to the client
		self.data = self.request.recv(1024).strip()
		#print self.data
		self.extractor(self.data)
		#print "{} wrote:".format(self.client_address[0])
		# just send back the same data, but upper-cased
		self.request.sendall('Done')
		#print "Successfully served the request!"
	def extractor(self,tree):
		#print tree
		(parsed,r) = parseExpr(str(tree),0,0)
		#print parsed.data
		pred_trees =  find_pred_trees(parsed,[])
		#print pred_trees
		classif_features_layer1 = open('../temp/classifier-features.txt','r').readlines()
		classif_features_layer2 = open('../temp/classifier-features-layer2.txt','w')
		classif_file_lines = open('../temp/classifier-output.txt','r').readlines()
		identifier_file_lines = open('../temp/identifier-output.txt','r').readlines()
		#classif_file_lines = [l for l in classif_file if l != '\n']
		#pred_file = open('../temp/pred.test','w')
		stats_file = open('../temp/stats.txt','r').readlines()
		fr = 0
		to = 0
		idx = 1
		no_of_preds = int(stats_file[0].rstrip())
		for i in range(0,no_of_preds):
			to = to + int(stats_file[idx].rstrip())
			idx = idx + 1
			#print fr
			#print to
			required_classif_output = classif_file_lines[fr:to]
			required_identi_output = identifier_file_lines[fr:to]
			required_classif_lables = []
			for (clasi,ident) in zip(required_classif_output,required_identi_output):
				if ident.split(' ')[0] == 'yes':
					required_classif_lables.append(clasi.split(' ')[2])
			#print required_classif_lables
			required_classif_features = classif_features_layer1[fr:to]
			d = 0
			for f in required_classif_features:
				temp2 = [] #!
				ln = 0
				rn = 0
				for n in range(0,len(required_classif_lables)):
				#ln = 0 #<
				#rn = 0
					if n != d: 
						if n < d: #<
							temp2.append((required_classif_lables[n].rstrip(),'l',ln))
							ln = ln + 1
						else:
							temp2.append((required_classif_lables[n].rstrip(),'r',rn))
							rn = rn + 1
				d = d + 1
				fr = to
				context_features = []
				for (l,pos,no) in temp2: #<
						context_features.append('label_context_'+str(pos)+'_'+str(no)+'='+l) #<
				context_label = ' '.join(context_features)
				classif_features_layer2.write(f.split('?')[0] + ' ' + context_label + ' ?\n' )  
			
		#identif_file.close()
		#classif_file.close()
		#pred_file.close()
		#print ' '.join(features) + ' ?'
		#print ' '.join(features) + ' ' + label.rstrip() # for evaluation
				
				
	  
		
		
			
def my_flatten(node,flat_list):
	if node.data != None and node.data not in ['IN','TO'] and node.word != None and node.word != []:
		flat_list.append(node.word)
	for ch in node.children:
		my_flatten(ch,flat_list)
	return flat_list	 

if __name__ == "__main__":
    HOST, PORT = "localhost", 19999

    # Create the server, binding to localhost on port 19997
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	
	
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()