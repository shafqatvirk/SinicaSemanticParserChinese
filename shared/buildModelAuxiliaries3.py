from prepareData import *
import re
import os
def find_features_without_traces_classifier(arg,trNo,parsed,predicate,target,target_POS,tree_head_dict,features):

	if arg != 0 and arg != None:
		if len(arg.children) == 1 and (arg.children[0].data == '-NONE-'):
			return (0,0,0,0,0,0,0)
		
		#gov = find_gov(parsed,terNo,height)
		gov = find_gov_arg(parsed,arg)
		if gov != None:
			features.append('gov='+gov)
		(p,path_to_BA,path_to_BEI,voice,BA_terNo,BEI_terNo) = path_arg(parsed,arg,predicate)
		if BA_terNo < arg.terNo or BEI_terNo < arg.terNo:
			#voice_position = 'before'
			features.append('voice_position=before')
		else:
			#voice_position = 'after'
			features.append('voice_position=after')
		if arg.parent != None:
			subcatStar = find_subcat(arg.parent)
			(l_sib_pt,r_sib_pt) = find_left_right_child_pt(arg.parent,arg)
			features.append('l_sib_pt='+l_sib_pt)
			features.append('r_sib_pt='+r_sib_pt)
			features.append('subcatStar='+subcatStar)
		#else:
			#subcatStar = 'None'
			#l_sib_pt = 'None'
			#r_sib_pt = 'None'
		subcatAt = find_subcat(arg)
		#print p
		#if path_to_BA != 'no-BA' or path_to_BEI != 'no-BEI': 
			#print path_to_BA
			#print path_to_BEI
		features.append('subcatAt='+subcatAt)
		all_words = find_first_last_word(arg,[])
		#if all_words != []:
					#features.append('first_word='+all_words[0])
					#features.append('last_word='+all_words[-1])
		#if gov == None:
			#gov = 'none'
		pt = arg.data
		################
		# to print every argument tree into a file, which will be used by java program to find heads
		if pt != '-NONE-':
			#if len(arg.children) == 1 and (arg.children[0].data == '-NONE-' or arg.children[0].data == 'PP'):
			#all_words = find_first_last_word(arg,[])
			if len(arg.children) == 1 and (arg.children[0].data == '-NONE-'):
				
				h_word = 'no-h-word'
				#features.append('h_word_pos='+arg.data)
				h_word_pos=arg.data
				#h_word = 'no-h-word'
				#h_word_pos = 'no-h-word-pos'
			else:
				tree_line = print_tree_file(arg,[])
				arg_tree =  ''.join(tree_line)
				#print arg_tree
				if tree_head_dict.has_key(arg_tree.rstrip()):
					head_word_and_pos = tree_head_dict[arg_tree.rstrip()]
					h_word = head_word_and_pos.split(' ')[1].rstrip(')')
					h_word_pos = head_word_and_pos.split(' ')[0].lstrip('(')
					#features.append('h_word='+head_word_and_pos.split(' ')[1].rstrip(')'))
					#features.append('h_word_pos='+ head_word_and_pos.split(' ')[0].lstrip('('))
				else:
					#print 'not found'
					h_word = 'no-h-word'
					h_word_pos = 'no-h-word-pos'
		else:
				#print 'none'
				h_word = 'no-h-word'
				h_word_pos = 'no-h-word-pos'
		#########################
		#print 'Phrase Type = ' + arg.data
		if predicate.terNo > trNo:
				features.append('position=-1')
		else:
				features.append('position=1')
		#if pt != '-NONE-':
		#list_of_features = [target,target_POS,h_word,h_word_pos,position,pt,gov]#list_of_features+'('+target+','+target_POS+','+h_word+','+h_word_pos+','+str(position)+','+pt+','+gov+')'
		#features.append('layer_cons_focus='+ str(p.count('u') - p.count('d')))
		pred_parent = predicate.parent.data
		if arg.parent != None:
			arg_parent = arg.parent.data
		else:
			arg_parent = 'none'
		pred_parent_pls_arg_parent = pred_parent + arg_parent
		features.append('pred_parent_pls_arg_parent='+ pred_parent + arg_parent)
		features.append('pt='+pt)
		features.append('path='+p)
		##features.append('path_to_BA='+path_to_BA)
		##features.append('path_to_BEI='+path_to_BEI)
		features.append('voice='+voice)
		
		features.append('t_word_plus_pt='+ target + pt)
		
		return (target,target_POS,h_word,h_word_pos,all_words,pt,features)
	#else:
		#continue
		#return (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
		#print 't_word='+str(t_word)+' t_word_pos='+str(t_word_pos)+' h_word='+str(h_word)+' h_word_pos='+str(h_word_pos)+' position='+str(position)+' pt='+str(pt)+' gov='+str(gov.rstrip())+' t_word_plus_pt='+str(t_word_plus_pt)+ ' t_word_plus_h_word='+str(t_word+h_word)+' first_word='+first_word+ ' last_word='+last_word+' voice='+str(voice)+' subcat='+str(subcat)+' subcatStar='+str(subcatStar)+' subcatAt='+str(subcatAt)+' path='+str(p)+' path_to_BA='+str(path_to_BA)+' path_to_BEI='+str(path_to_BEI)+' verb_calss='+str(verb_class)+' verb_class_plus_pt='+(verb_class+pt)+ ' verb_class_plus_h_word='+str(verb_class+h_word)+' l_sib_pt='+str(l_sib_pt)+ ' r_sib_pt='+str(r_sib_pt)+ ' allFrameSets='+str(AllFrameSets)+ ' verb_class_plus_allFrameSets='+str(verb_class+AllFrameSets)+' SemType_h_word='+str(semType_h_word)+' semType_t_word='+str(semType_t_word)+' semType_first_word='+str(semType_first_word)+' semType_last_word='+str(semType_last_word)+' semType_t_pls_l_word='+str(semType_t_word+semType_last_word)+' layer_cons_focus='+layer_cons_focus+' all_labels=' + labels + ' pred_parent_pls_arg_parent='+pred_parent_pls_arg_parent+' label_context='+predicted_label_context+' ?'

def find_gov_arg(t,arg):
 #for ch in t.children:
			#if arg != None:
				while arg.data != 'S' or arg.data != 'VP':
					#print arg.data
					arg = arg.parent
					if arg != None:
						if arg.data == 'S' or arg.data == 'VP':
							#print arg.data
							return arg.data
						else:
							continue
					else:
						return 'none'

def path_arg(t,arg,pred):
			if arg != None:
				full_path = find_full_path_arg(arg,pred)
				(path_to_BA,BA_terNo) = find_path_to_BA_arg(arg,pred,'BA','BA')
				(path_to_BEI,BEI_terNo) = find_path_to_BA_arg(arg,pred,'SB','LB')
				if path_to_BA != [] and 'dBA' in path_to_BA:
					#print path_to_BA
					path_BA = path_to_BA[0:path_to_BA.index('dBA')]
					voice = 'passive'
				else:
					path_BA = 'no-BA'
					voice = 'active'
				if path_to_BEI != []:
					if 'dSB' in path_to_BEI:
						path_BEI = path_to_BEI[0:path_to_BEI.index('dSB')]
						voice = 'passive'
					elif 'dLB' in path_to_BEI:
						path_BEI = path_to_BEI[0:path_to_BEI.index('dLB')]
						voice = 'passive'
					else:
						path_BEI = 'no-BEI'
						voice = 'active'
				else:
					path_BEI = 'no-BEI' 
					voice = 'active'
				return (full_path,''.join(path_BA),''.join(path_BEI),voice,BA_terNo,BEI_terNo)
				
def find_full_path_arg(arg,pred):
				full_path = [arg.data]
				found = False
				partial_path = []
				while found == False and arg!= None and arg.parent != None:
					partial_path = []
					invalid_ch = arg
					arg = arg.parent
					path_node = 'u'+arg.data.rstrip() # 'u' to denote upward direction
					#full_path.append(arg.data.rstrip())
					full_path.append(path_node)
					(partial_path,found) = find_predicate_arg(arg,invalid_ch,pred,[],found)
				full_path = full_path + partial_path
				
				#path_to_BA = 
				return ''.join(full_path)	
def find_predicate_arg(arg,invalid_ch,pred,p_path,f):
	for ch in arg.children:
		if ch != invalid_ch:
			if ch == pred and ch.terNo == pred.terNo and f == False:
				#print ch.data
				#print ch.terNo
				#print n
				f = True
				path_node = 'd'+ch.data.rstrip() # 'd' to denote downward direction
				p_path.append(path_node)
				#p_path.append(ch.data.rstrip())
				break
			elif f == False:
				#f = False
				path_node = 'd'+ch.data.rstrip() # 'd' to denote downward direction
				p_path.append(path_node)
				#p_path.append(ch.data.rstrip())
				#print p_path
				(p_path,f) = find_predicate_arg(ch,'',pred,p_path,f)
		else:
			continue
		if f == False:
			p_path = p_path[0:-1]
	return (p_path,f)
	
def find_path_to_BA_arg(arg,pred,b1,b2):
				full_path = [arg.data]
				found = False
				while found == False and arg!= None and arg.parent != None:
					partial_path = []
					invalid_ch = arg
					arg = arg.parent
					path_node = 'u'+arg.data.rstrip() # 'u' to denote upward direction
					full_path.append(path_node)
					#full_path.append(arg.data)
					(partial_path,found,BA_terNo) = find_BA_arg(arg,invalid_ch,pred,[],found,b1,b2,0)
				if found != False:
					full_path = full_path + partial_path
					#print partial_path
				else:
					full_path = []
					BA_terNo = 0
				
				#path_to_BA = 
				return (full_path,BA_terNo)	
def find_BA_arg(arg,invalid_ch,pred,p_path,f,b1,b2,BA_terNo):
	for ch in arg.children:
		if ch != invalid_ch:
			if ch.data == b1 or ch.data == b2 and f == False:
				#print ch.data
				#print ch.terNo
				#print n
				f = True
				BA_terNo = ch.terNo
				path_node = 'd'+ch.data.rstrip() # 'd' to denote upward direction
				p_path.append(path_node)
				#p_path.append(ch.data)
				break
			elif f == False:
				#f = False
				#print ch.data
				path_node = 'd'+ch.data.rstrip() # 'd' to denote upward direction
				p_path.append(path_node)
				#p_path.append(ch.data)
				#print p_path
				(p_path,f,BA_terNo) = find_BA_arg(ch,'',pred,p_path,f,b1,b2,BA_terNo)
		else:
			continue
		if f == False:
			p_path = p_path[0:-1]
	return (p_path,f,BA_terNo)
		
#######################################################################	
def build_temp_model(roles_dict,total_dict):
	model_temp_dict = {}
	max_count = 0
	for k in roles_dict.keys():
		k_list = k.split(',')
		t = ','.join(k_list[:-1])
		new_prob = float(roles_dict[k])/total_dict[t]
		total_no = float(roles_dict[k])
		if model_temp_dict.has_key(t):
			old_roles = model_temp_dict[t]
			old_roles.append((new_prob,k_list[-1],total_no))
			model_temp_dict[t] = old_roles
			#print model_temp_dict[(semType_h,pos_h,semType_t,pos_t,pt,position,all_pos,passive,left_right_child_pos,all_semType)] 
		else:
			model_temp_dict[t] = [(new_prob,k_list[-1],total_no)]
			
	return model_temp_dict
	

def find_features_without_traces(nh_pairs,parsed,predicate,target,target_POS,tree_head_dict,prop,features):
	terNo_height = nh_pairs
	#if nh_pairs.find('*') == -1 and nh_pairs.find(';') == -1 and nh_pairs.find(',') == -1:
	#list_of_features = []
	terNo = int(terNo_height.split(':')[0])
	height = int(terNo_height.split(':')[1])
	(arg,trNo) = traverse_tree_depth(parsed,terNo,height)
	#print predicate.terNo
	if arg != 0 and arg != None:
		if len(arg.children) == 1 and (arg.children[0].data == '-NONE-'):
			return (0,0,0,0,0,0,0)
		##if len(arg.children) == 1 and (arg.children[0].data == '-NONE-'):
			##print 'None'
		##else:
			##print 'YES'
		gov = find_gov(parsed,terNo,height)
		if gov != None:
			features.append('gov='+gov)
		(p,path_to_BA,path_to_BEI,voice,BA_terNo,BEI_terNo) = path(parsed,terNo,height,predicate)
		if BA_terNo < arg.terNo or BEI_terNo < arg.terNo:
			#voice_position = 'before'
			features.append('voice_position=before')
		else:
			#voice_position = 'after'
			features.append('voice_position=after')
		if arg.parent != None:
			subcatStar = find_subcat(arg.parent)
			(l_sib_pt,r_sib_pt) = find_left_right_child_pt(arg.parent,arg)
			features.append('l_sib_pt='+l_sib_pt)
			features.append('r_sib_pt='+r_sib_pt)
			features.append('subcatStar='+subcatStar)
		#else:
			#subcatStar = 'None'
			#l_sib_pt = 'None'
			#r_sib_pt = 'None'
		subcatAt = find_subcat(arg)
		#print p
		#if path_to_BA != 'no-BA' or path_to_BEI != 'no-BEI': 
			#print path_to_BA
			#print path_to_BEI
		features.append('subcatAt='+subcatAt)
		all_words = find_first_last_word(arg,[])
		#if all_words != []:
					#features.append('first_word='+all_words[0])
					#features.append('last_word='+all_words[-1])
		#if gov == None:
			#gov = 'none'
		pt = arg.data
		################
		# to print every argument tree into a file, which will be used by java program to find heads
		if pt != '-NONE-':
			#if len(arg.children) == 1 and (arg.children[0].data == '-NONE-' or arg.children[0].data == 'PP'):
			#all_words = find_first_last_word(arg,[])
			if len(arg.children) == 1 and (arg.children[0].data == '-NONE-'):
				
				h_word = 'no-h-word'
				#features.append('h_word_pos='+arg.data)
				h_word_pos=arg.data
				#h_word = 'no-h-word'
				#h_word_pos = 'no-h-word-pos'
			else:
				tree_line = print_tree_file(arg,[])
				arg_tree =  ''.join(tree_line)
				#print arg_tree
				if tree_head_dict.has_key(arg_tree.rstrip()):
					head_word_and_pos = tree_head_dict[arg_tree.rstrip()]
					h_word = head_word_and_pos.split(' ')[1].rstrip(')')
					h_word_pos = head_word_and_pos.split(' ')[0].lstrip('(')
					#features.append('h_word='+head_word_and_pos.split(' ')[1].rstrip(')'))
					#features.append('h_word_pos='+ head_word_and_pos.split(' ')[0].lstrip('('))
				else:
					#print 'not found'
					h_word = 'no-h-word'
					h_word_pos = 'no-h-word-pos'
		else:
				#print 'none'
				h_word = 'no-h-word'
				h_word_pos = 'no-h-word-pos'
		#########################
		#print 'Phrase Type = ' + arg.data
		if predicate.terNo > trNo:
				features.append('position=-1')
		else:
				features.append('position=1')
		#if pt != '-NONE-':
		#list_of_features = [target,target_POS,h_word,h_word_pos,position,pt,gov]#list_of_features+'('+target+','+target_POS+','+h_word+','+h_word_pos+','+str(position)+','+pt+','+gov+')'
		features.append('layer_cons_focus='+ str(p.count('u') - p.count('d')))
		pred_parent = predicate.parent.data
		if arg.parent != None:
			arg_parent = arg.parent.data
		else:
			arg_parent = 'none'
		pred_parent_pls_arg_parent = pred_parent + arg_parent
		features.append('pred_parent_pls_arg_parent='+ pred_parent + arg_parent)
		features.append('pt='+pt)
		features.append('path='+p)
		features.append('path_to_BA='+path_to_BA)
		features.append('path_to_BEI='+path_to_BEI)
		features.append('voice='+voice)
		
		features.append('t_word_plus_pt='+ target + pt)
		
		return (target,target_POS,h_word,h_word_pos,all_words,pt,features)
	#else:
		#continue
		#return (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
		#print 't_word='+str(t_word)+' t_word_pos='+str(t_word_pos)+' h_word='+str(h_word)+' h_word_pos='+str(h_word_pos)+' position='+str(position)+' pt='+str(pt)+' gov='+str(gov.rstrip())+' t_word_plus_pt='+str(t_word_plus_pt)+ ' t_word_plus_h_word='+str(t_word+h_word)+' first_word='+first_word+ ' last_word='+last_word+' voice='+str(voice)+' subcat='+str(subcat)+' subcatStar='+str(subcatStar)+' subcatAt='+str(subcatAt)+' path='+str(p)+' path_to_BA='+str(path_to_BA)+' path_to_BEI='+str(path_to_BEI)+' verb_calss='+str(verb_class)+' verb_class_plus_pt='+(verb_class+pt)+ ' verb_class_plus_h_word='+str(verb_class+h_word)+' l_sib_pt='+str(l_sib_pt)+ ' r_sib_pt='+str(r_sib_pt)+ ' allFrameSets='+str(AllFrameSets)+ ' verb_class_plus_allFrameSets='+str(verb_class+AllFrameSets)+' SemType_h_word='+str(semType_h_word)+' semType_t_word='+str(semType_t_word)+' semType_first_word='+str(semType_first_word)+' semType_last_word='+str(semType_last_word)+' semType_t_pls_l_word='+str(semType_t_word+semType_last_word)+' layer_cons_focus='+layer_cons_focus+' all_labels=' + labels + ' pred_parent_pls_arg_parent='+pred_parent_pls_arg_parent+' label_context='+predicted_label_context+' ?'

def find_first_last_word(arg,all_words):
	if arg.word != [] and arg.word != None and arg.data != '-NONE-':
		all_words.append(arg.word)
	for ch in arg.children:
		all_words = find_first_last_word(ch,all_words)
	return all_words

def build_tree_head_dict():
	dict = {}
	#trees = open('argument-trees3.txt').readlines()
	#heads = open('new-heads-gbk.txt')
	#trees = open('../data/argument-trees3-cpb2.txt').readlines()
	trees = open('../data/argument-trees-cpb2-without-functional-tags.txt').readlines()
	heads = open('../data/new-heads-gbk-cpb2.txt')
	for t in trees:
		dict[t.rstrip()] = heads.readline().rstrip()
		#print t.rstrip() + ',' + dict[t.rstrip()]
		#print t.rstrip()
		#print dict[t.rstrip()]
	
	return dict

def build_tree_head_dict_cp1():
	dict = {}
	trees = open('argument-trees3.txt').readlines()
	heads = open('new-heads-gbk.txt')
	#trees = open('argument-trees3-cpb2.txt').readlines()
	#heads = open('new-heads-gbk-cpb2.txt')
	for t in trees:
		dict[t.rstrip()] = heads.readline().rstrip()
		#print t.rstrip() + ',' + dict[t.rstrip()]
		#print t.rstrip()
		#print dict[t.rstrip()]
	
	return dict

def build_simplified_traditional_dict():
	dict = {}
	simplified = open('../data/chinese-words-simplified.txt').readlines()
	traditional = open('../data/chinese-words-traditional.txt')
	for w in simplified:
		dict[w.rstrip()] = traditional.readline().rstrip()
		#print dict[w.rstrip()]
	return dict
def frameset_dict():
	dict = {}
	file = open('../data/self-produced-verbs.txt')
	for l in file.readlines()[1:]:
		tokens = l.rstrip().split('\t')
		dict[tokens[1]] = [tokens[2],tokens[0]]
	return dict
def find_verb_class(frameset,frameset_file_dict):
	frame = frameset
	if frame in frameset_file_dict:
		f_name = '-'.join(frameset_file_dict[frame])
		#full_file_name = './cpb-1.0/data/frames/' +f_name + '.xml' 
		full_file_name = '../data/frames/' +f_name + '.xml' 
		file = open(full_file_name).read()
		framesets = re.compile('<frameset (.*?)</frameset>', re.DOTALL).findall(file)
		verb_class_list = []
		AllFrameSets = re.compile('<frameset id="(.*?)\"', re.DOTALL).findall(file)
		#print AllFrameSets
		for f in framesets:
			arguments = re.compile('<role (.*?)/>', re.DOTALL).findall(f)
			#frameset_id = re.compile('<frameset id=\"(.*?)\">', re.DOTALL).findall(f)
			#print frameset_id
			#AllFrameSets.append(frameset_id[0])
			verb_class_list.append('C'+str(len(arguments)))
		#print verb_class_list
		return (''.join(verb_class_list),''.join([f.split('"')[0] for f in AllFrameSets]))
	else:
		return ('no_verb_class','no-frameset')
def find_subcat(node):
	subcat = []
	subcat.append(node.data.rstrip())
	for ch in node.children:
		subcat.append(ch.data.rstrip())
	return ''.join(subcat)
def find_left_right_child_pt(tree,ch):
	indx = tree.children.index(ch)
	if len(tree.children) == 1:
		right = 'empty'
		left = 'empty'
		#left_role = 'empty'
	elif indx == 0:
		left = 'empty'
		right = tree.children[indx+1].data
		#left_role = 'empty'
	elif indx == len(tree.children)-1:
		right = 'empty'
		left = tree.children[indx-1].data
		#left_role = tree.children[indx-1].semRole
	else:
		left = tree.children[indx-1].data
		right = tree.children[indx+1].data
		#left_role = tree.children[indx-1].semRole
	return (left,right)

def remove_functional_tags(node):
	if node.data.find('-') != -1:
		node.data = node.data.split('-')[0]
	for ch in node.children:
		remove_functional_tags(ch)


def build_context_labels(): # fro training
	context_labels_list = []
	prop_bank = open('propbank.train').readlines()
	idx_1 = 0
	for prop in prop_bank[0:]:
	  label_context = []
	  ids = prop.split(' ')
	  file_id = ids[0].split('/')[2]
	  tree_no = int(ids[1])
	  predicate_no = int(ids[2])
	  frameset = ids[4]
	  args = ids[6:]
	  file_path = os.path.join("./bracketed/", file_id)
	  trees = convert_trees(file_path)
	  
	  expr = ''.join(list(trees[tree_no].rstrip())[1:-1]).rstrip(' ').lstrip(' ')
	  (parsed,r) = parseExpr(expr,0,0)
	  (predicate,pred_terNo) = traverse_tree_depth(parsed,predicate_no,0)
	  if predicate != 0 and predicate.word == ids[4].split('.')[0]:
		for arg in args:
			label = '-'.join(arg.split('-')[1:]).rstrip()
			##if label.split('-')[0] in ['ARG0','ARG1','ARG2','ARG3','ARG4']:
				##label = label.split('-')[0]
			##else:
				##label = label.rstrip()
			if label.rstrip() != 'rel':
			
			 nh_pairs = arg.split('-')[0]
			 if nh_pairs.find('*') == -1 and nh_pairs.find(';') == -1 and nh_pairs.find(',') == -1:
				
				#isNoneTer = isNone(parsed,nh_pairs)
				#if isNoneTer == True:
					#continue
				label_context.append(label)
		#print label_context
		context_labels_list.append(label_context)
	return context_labels_list

def isNone(parsed,nh_pairs):
	terNo_height = nh_pairs
	terNo = int(terNo_height.split(':')[0])
	height = int(terNo_height.split(':')[1])
	(arg,trNo) = traverse_tree_depth(parsed,terNo,height)
	if arg != 0 and arg != None:
		if (len(arg.children) == 1 and (arg.children[0].data == '-NONE-')) or arg.data == '-NONE-':
				return True
		pt = arg.data
		if pt != '-NONE-':
			if len(arg.children) == 1 and (arg.children[0].data == '-NONE-'):
				return True
		else:
				#print 'none'
				return True
		#########################
		return False
	else:
		return True

	
def make_context_list(): # for testing
	list = []
	indexs = open('counter-stats.txt').readlines()
	labels = open('ch-propbank-results.txt').readlines()
	labels_list = [lb.split(' ')[0] for lb in labels]
	start = 0
	upto = 0
	for l in indexs:
		upto = start + int(l.rstrip())
		list.append(labels_list[start:upto])
		start = upto
	return list
def make_context_list_cp1(): # for testing
	list = []
	indexs = open('counter-stats-cp1.txt').readlines()
	labels = open('ch-propbank-results-cp1.txt').readlines()
	labels_list = [lb.split(' ')[0] for lb in labels]
	start = 0
	upto = 0
	for l in indexs:
		upto = start + int(l.rstrip())
		list.append(labels_list[start:upto])
		start = upto
	return list	
def find_pred_trees(node,pred_trees):
	if node.data in ['VV','VC','VA','VE']:
		pred_trees.append((node,node.terNo))
	for ch in node.children:
		find_pred_trees(ch,pred_trees)
	return pred_trees
def pruning(node,predNum,candidates):
	if node.terNo == predNum:
		candidates = find_candidates(node.parent,node,candidates)
		return candidates
	for ch in node.children:
			candidates = pruning(ch,predNum,candidates)
	return candidates

def find_candidates(parrent,node,candidates):
	temp_parent = None
	temp_node = None
	if parrent == None:
		return candidates
	for ch in parrent.children:
		if ch != node:
			if ch.data == 'PP':
				candidates.append(ch)
				for c in ch.children:
					candidates.append(c)
			else:
				candidates.append(ch)
	temp_parrent = parrent.parent
	temp_node = parrent
	candidates = find_candidates(temp_parrent,temp_node,candidates)
	return candidates	