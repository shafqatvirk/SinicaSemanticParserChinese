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
	
	simplified_tradictional_dict = build_simplified_traditional_dict()
	tree_head_dict = build_tree_head_dict()
	word2semType_dict = word2semType()
	frameset_file_dict = frameset_dict() # verb_frame information
	e_hownet=EHowNetTree("../data/ehownet_ontology.txt")
    
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
		identif_file = open('../temp/identifier-features.txt','w')
		classif_file = open('../temp/classifier-features.txt','w')
		pred_file = open('../temp/pred.test','w')
		stats_file = open('../temp/stats.txt','w')
		stats_file.write(str(len(pred_trees))+'\n')
		for (predicate,pred_terNo) in pred_trees[:]:
			target = predicate.word
			pruned = pruning(parsed,pred_terNo,[])
			stats_file.write(str(len(pruned))+'\n')
			target_POS = predicate.data
			frameset = target
			#print frameset
			(verb_class,AllFrameSets) = find_verb_class(frameset,self.frameset_file_dict) # verb_frame information
			#print verb_class
			subcat = find_subcat(predicate.parent)
			#print subcat
			#print AllFrameSets
			for arg in pruned:
				#print arg.data
				features = []
				features.append('subcat='+subcat)
			 
				(t_word,t_word_pos,h_word,h_word_pos,all_words,pt,features) = find_features_without_traces_classifier(arg,arg.terNo,parsed,predicate,target,target_POS,self.tree_head_dict,features)
				if t_word == 0 and t_word_pos == 0 and h_word == 0 and h_word_pos == 0 and all_words == 0 and features == 0:
					continue
				
				if all_words != []:
					first_word = all_words[0]
					last_word = all_words[-1]
				else:
					first_word = 'no-first-word'
					last_word = 'no-last-word'
					
				############# simplified to traditional conversion
				#print 'before '+t_word
				if self.simplified_tradictional_dict.has_key(h_word.decode('utf-8-sig','ignore').encode('gb2312','ignore')):
					#print 'yes'
					h_word_trad = self.simplified_tradictional_dict[h_word.decode('utf-8-sig','ignore').encode('gb2312','ignore')]
				else:
					h_word_trad = h_word
				if self.simplified_tradictional_dict.has_key(t_word):
					t_word_trad = self.simplified_tradictional_dict[t_word]
					#print 'after '+t_word_trad 
				else:
					t_word_trad = t_word
				if self.simplified_tradictional_dict.has_key(first_word):
					first_word_trad = self.simplified_tradictional_dict[first_word]
				else:
					first_word_trad = first_word
				if self.simplified_tradictional_dict.has_key(last_word):
					last_word_trad = self.simplified_tradictional_dict[last_word]
				else: # if word is not found in dict, use the simplified version
					last_word_trad = last_word
				################################
				
				############################### use of ehownet
				
				if h_word != 'no-h-word' and h_word_pos != 'no-h-word-pos': 
					semType_h_word = find_semType(h_word_trad,h_word_pos,self.e_hownet,self.word2semType_dict)
					
				semType_t_word = find_semType(t_word_trad,target_POS,self.e_hownet,self.word2semType_dict)
				if first_word != 'no-first-word':
					semType_first_word = find_semType(first_word_trad,'',self.e_hownet,self.word2semType_dict)
				if last_word != 'no-last-word':
						semType_last_word = find_semType(last_word_trad,'',self.e_hownet,self.word2semType_dict)
			
				
				h_word = h_word.decode('utf-8-sig','ignore').encode('gb2312','ignore') # to make everything into once encoding
				features.append('t_word='+str(t_word))
				features.append('t_word_pls_pt='+str(t_word)+str(pt))
				features.append('t_word_pos='+str(t_word_pos))
				if h_word != 'no-h-word':
					features.append('h_word='+str(h_word))
					features.append('semType_h_word='+str(semType_h_word))
					features.append('t_word_pls_h_word='+t_word+h_word)
				if all_words != []:
					features.append('first_word='+first_word)
					features.append('last_word='+last_word)
					features.append('semType_first_word='+str(semType_first_word))
					features.append('semType_last_word='+str(semType_last_word))
					#features.append('semType_t_word_pls_l_word='semType_t_word+last_word)
					features.append('semType_t_pls_l_word='+str(semType_t_word+semType_last_word))
				features.append('h_word_pos='+str(h_word_pos))
				### verbclass information is not availeble in cpb2.0 # verb_frame information
				features.append('verbClass='+verb_class)
				features.append('verbClass_pls_pt='+verb_class+pt)
				features.append('verbClass_pls_h_word='+verb_class+h_word)
				features.append('allFrameSets='+str(AllFrameSets))
				features.append('verb_class_plus_allFrameSets='+str(verb_class+AllFrameSets))
				##############################
				features.append('semType_t_word='+str(semType_t_word))
				flat_argument = '_'.join([w.rstrip() for w in my_flatten(arg,[])])
				# features for identification
				identif_file.write(' '.join(features) + ' ?\n')
				#print 'h='+str(h)+' h_pos='+str(h_pos)+' path='+str(path)+' t_word_pls_pt='+t_word_pls_pt+' t_word_pls_h_word='+t_word_pls_h_word+' distance_pls_t_word='+distance_pls_t_word+ ' ?\n'
				# features for classification
				classif_file.write(' '.join(features) + ' ?\n')
				#print 'h='+str(h)+' h_pos='+str(h_pos)+' h_word='+str(h)+' h_word_pos='+str(h_pos)+' path='+str(path)+' t_word_pls_pt='+t_word_pls_pt+' t_word_pls_h_word='+t_word_pls_h_word+' subcat='+str(subcat)+ ' subcatAt='+str(subcatAt)+ ' subcatStar='+str(subcatStar)+ ' ?\n'
				pred_file.write(t_word+' '+flat_argument+'\n')
				#print t_word+' '+flat_argument+'\n'
		identif_file.close()
		classif_file.close()
		pred_file.close()
		#print ' '.join(features) + ' ?'
		#print ' '.join(features) + ' ' + label.rstrip() # for evaluation
				
				
	  
		
		
			
def my_flatten(node,flat_list):
	if node.data != None and node.data not in ['IN','TO'] and node.word != None and node.word != []:
		flat_list.append(node.word)
	for ch in node.children:
		my_flatten(ch,flat_list)
	return flat_list	 

if __name__ == "__main__":
    HOST, PORT = "localhost", 19997

    # Create the server, binding to localhost on port 19997
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	
	
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()