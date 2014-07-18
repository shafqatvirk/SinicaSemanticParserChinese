#!/usr/bin/python
#-*- encoding: UTF-8 -*-

import sys
import string, re


def searchShortestPath(p1, p2):
    co_parent=[]
    co_idx=0
    while 1:
        if co_idx>=len(p1) or co_idx>=len(p2) or p1[co_idx]!=p2[co_idx]:
            co_idx-=1
            break

        co_idx+=1

    diffL=p1[co_idx+1:]
    diffL.reverse()
    diffL+=p2[co_idx+1:]

    return diffL

class Generic(object):
    pass

class Info(object):
    def __init__(self, dict=None):
        if dict:
            self.__dict__=dict

    def __str__(self):
        L=[]
        for (name,value) in self.__dict__.items():
            L.append("%s"%(value))
            
        return string.join(L,",")

    def dump(self):
        L=[]
        for (name,value) in self.__dict__.items():
            L.append("    %s: %s"%(name, value))
            
        return "\n"+string.join(L,",\n")+"\n"

    def __repr__(self):
        L=[]
        for (name,value) in self.__dict__.items():
            if isinstance(value, list):
                L.append("'%s':%s"%(name, value))
            else:
                L.append("'%s':'%s'"%(name, value))
            
        return "{"+string.join(L,", ")+"}"

    def setData(self, schemaL, dataL):
        for idx in range(len(schemaL)):
            if schemaL[idx].type=="list":
                self.__dict__[schemaL[idx].name]= dataL[idx].split(schemaL[idx].sep)
            else: # schemaL[idx].type=="string":
                self.__dict__[schemaL[idx].name]= dataL[idx]

    def objStr(self):
        L=[]
        for (name, value) in self.__dict__.items():
            if isinstance(value, list):
                L.append("'%s':%s"%(name, value))
            else:
                if "'" in value:
                    value=value.replace("\\","")
                    value=value.replace('"','\\"')
                    L.append("'%s':\"%s\""%(name, value))
                else:
                    L.append("'%s':'%s'"%(name, value))

        return "{"+string.join(L,", ")+"}"

class Node(object):
    """\
        Class Node:
            Base class of ontology node.

        Data Members:
            node.name: name of this node.
            node.type: type of this node.

        Function Members:
            node.getParent()   : get parent of this node.
            node.getChildList(): get child nodes, including semantic type nodes 
                                 and word nodes.
            node.dump()        : dump data of this node.
            node.usage()       : print this document.
    """
    pathSign={
        "semanticType": ",",
        "category": ".",
        "word": " ",
        "attachWord": "+"
    }

    def __init__(self, _name , _type=None, _level=0):
        self.name=_name
        self.type=_type
        self.level=_level
        self.parent=None
        self.semanticTypeL=[]
        self.categoryL=[]
        self.wordL=[]

    def __repr__(self):
        return self.type+"('"+self.name+"')"

    def __str__(self):
        return self.type+"('"+self.name+"')"

    def usage(self):
        print(self.__doc__)

    def getParent(self):
        return self.parent

    def getChildList(self):
        return self.semanticTypeL+self.categoryL+self.wordL


    def csvStr(self, schema=None):
        treePath=Node.pathSign[self.type]*self.level
        myStr="%s| %s"%(treePath, self.name)
        return myStr

    def objStr(self):
        treePath=Node.pathSign[self.type]*self.level
        myStr="%s| %s"%(treePath, self.name)
        return myStr
        
    def dump(self):
        print("name: %s"%(self.name))
        print("type: %s"%(self.type))

    def traverse(self):
        yield self 

        for idx in range(len(self.semanticTypeL)):
            for node in self.semanticTypeL[idx].traverse():
                yield node

        for idx in range(len(self.categoryL)):
            for node in self.categoryL[idx].traverse():
                yield node

        for idx in range(len(self.wordL)):
            for node in self.wordL[idx].traverse():
                yield node

    def addSemanticTypeNode(self, obj):
        self.semanticTypeL.append(obj)

    def addCategoryNode(self, obj):
        self.categoryL.append(obj)

    def addWordNode(self, obj):
        self.wordL.append(obj)

    def addChild(self, obj):
        obj.parent=self
        if isinstance(obj, WordNode):
            self.addWordNode(obj)

        elif isinstance(obj, CategoryNode):
            self.addCategoryNode(obj)

        else:
            self.addSemanticTypeNode(obj)

    def removeCategoryNodes(self):
        for child in self.semanticTypeL:
            child.removeCategoryNodes()

        L=[]
        for child in self.categoryL:
            child.removeCategoryNodes()
            for word in child.wordL:
                    # 刪除 投胎_2, 轉世_2 等重複的詞
                if re.search('_[0-9]+$', word.name):
                    continue

                word.level-=1
                L.append(word)

        for word in self.wordL:
            # 刪除 投胎_2, 轉世_2 等重複的詞
            if re.search('_[0-9]+$', word.name):
                continue
            L.append(word)

        self.wordL=L
        self.categoryL=[]

class SemanticTypeNode(Node):
    """
        Class SemanticTypeNode:
            Semantic type Node of the ontology tree.

        Data members:

        Member functions:
            node.getHypernym()   : Get hypernym of this node. It will return a 
                                   semantic type node.
            node.getHyponymList(): Get hyponym list of this node. It will return
                                   a list of semantic type nodes.
            node.getWordList()   : Get word nodes of this semantic type. It will
                                   return a list of word nodes.
            node.getParent()     : Do the same thing as node.getHypernym() does.
            node.getChildList()  : Get child nodes, including semantic type 
                                       nodes and word nodes. It will return semantic
                                   type nodes as will as word nodes
            node.dump()          : Dump data of this node.
            node.usage()         : Print this document.
    """
    def __init__(self, _name, _type="semanticType", _level=0):
        super(SemanticTypeNode, self).__init__(_name, _type, _level)

    def __dir__(self):
        L=['name','type']+['getHypernym()','getHyponymList()','getWordList()','dump()','usage()']
        return L
            
    def getHypernym(self):
        return self.getParent()

    def getHypernymPath(self):
        L=[self]
        node=self.getParent()
        while node:
            L.append(node)
            node=node.getParent()
        L.reverse()
        return L

    def getHyponymList(self):
        return self.semanticTypeL

    def getWordList(self):
        return self.wordL

class CategoryNode(Node):
    """
        Class CategoryNode:
            CategoryNode of the ontology tree.
    """
    def __init__(self, _name, _type="category", _level=0):
        super(CategoryNode, self).__init__(_name, _type, _level)

class WordNode(Node):
    """
        Class WordNode:
            WordNode of the ontology tree.

        Data members:
            node.name     : name of this node (alias of node.word).
            node.type     : type of this node (must be 'word' for WordNode).
            node.sid      : each word node has an unique serial number.
            node.word     : word form.
            node.pos      : part-of-speech.
            node.pos_long : fine-grained part-of-speech.
            node.meaning  : meaning in English.
            node.ehownet  : EHowNet definition.

        Member functions:
            node.getSemanticType() : Get semantic type of this word node.
            node.getSynonymList()  : Get synonym set of this word node.
            node.getParent()	   : Do the same thing as node.getSemanticType()
                                     does.
            node.dump()            : Dump data of this node.
            node.usage()           : Print this document.
    """
    def __init__(self, _name, _type="word", _level=0):
        super(WordNode, self).__init__(_name, _type, _level)

    def __dir__(self):
        L=['name','type']+self.info.__dict__.keys()+['getSemanticType()','getParent()','dump()','usage()']
        return L

    def __getattr__(self, attr):
        if not (attr in self.info.__dict__):
            raise AttributeError
        return self.info.__dict__[attr]

    def usage(self):
        print(self.__doc__)

    def __repr__(self):
        return self.type+"('"+self.name+"|"+self.eng+"')"

    def __str__(self):
        return self.__repr__()

    def getSemanticType(self):
        return self.getParent()

    def getSynonymList(self):
        tax=self.getSemanticType()
        wordList=tax.getWordList()
        return wordList

    def csvStr(self, schema=None):
        treePath=Node.pathSign[self.type]*self.level
        if not schema:
            myStr="%s| %s\t%s\t%s"%(treePath, self.name, self.info.sid, self.info.ehownet)
        else:
            dataL=[]
            for k in schema:
                v=self.info.__dict__[k]
                if isinstance(v,list):
                    v=string.join(v,",")
                dataL.append("%s"%(v))
            myStr="%s| %s"%(treePath, string.join(dataL,"\t"))
        return myStr

    def objStr(self):
        treePath=Node.pathSign[self.type]*self.level
        myStr="%s| %s\t%s"%(treePath, self.name, self.info.objStr())
        return myStr

    def dump(self):
        print("name: %s"%(self.name))
        print("type: %s"%(self.type))
        for (k,v) in self.info.__dict__.items():
            print("%s: %s" %(k,v))

class EHowNetTree(object):
    """\
        Class EHowNetTree: 
            EHowNet ontology tree.

        Data Members:
            tree.rootNode: root of the ontology tree.

        Function Members:
            tree.searchWord(word): search nodes of EHowNet ontology for the word.
            tree.traverseDistance(x,y): search shortest distance from x to y, x,y can be word, WordNode, SemanticTypeNode

            tree.traversePath(x,y): search shortest distance Path from x to y, x,y can be word, WordNode, SemanticTypeNode

            tree.usage(): print this document.
    """
    def usage(self):
        print(self.__doc__)

    def __dir__(self):
        return ['rootNode','searchWord(word)','usage()']

    def __init__(self, infile=None):
        self.rootNode=None
        self.m_word2node={}
        if infile!=None:
            self.loadObjTree(infile)

    def searchWord(self, word):
        if isinstance(word, unicode):
            word=word.encode("UTF-8")
        return self.m_word2node.get(word,[])[:] # make a copy of list

    def traverseDistance(self, obj1, obj2):
        sp=self.traversePath(obj1, obj2)
        if sp==None:
            return None
        else:
            return len(sp)

    def traversePath(self, obj1, obj2):
        if isinstance(obj1, str):
            nL=self.searchWord(obj1)
            tL=[n.getSemanticType() for n in nL]
            pL1=[t.getHypernymPath() for t in tL]
        elif isinstance(obj1, WordNode):
            tL=[obj1.getSemanticType()]
            pL1=[t.getHypernymPath() for t in tL]
        elif isinstance(obj1, SemanticTypeNode):
            pL1=[obj1.getHypernymPath()]

        if isinstance(obj2, str):
            nL=self.searchWord(obj2)
            tL=[n.getSemanticType() for n in nL]
            pL2=[t.getHypernymPath() for t in tL]
        elif isinstance(obj2, WordNode):
            tL=[obj2.getSemanticType()]
            pL2=[t.getHypernymPath() for t in tL]
        elif isinstance(obj2, SemanticTypeNode):
            pL2=[obj2.getHypernymPath()]

        if len(pL1)==0 or len(pL2)==0:
            return None

        sp=None
        sp_len=999
        for idx in range(len(pL1)):
            p1=pL1[idx]
            for jdx in range(len(pL2)):
                p2=pL2[jdx]
                p=searchShortestPath(p1,p2)
                if len(p)<sp_len:
                    sp=p
                    sp_len=len(p)

        return sp



    def removeCategoryNodes(self):
        # 1. move word node to parent
        # 2. remove the category node
        self.rootNode.removeCategoryNodes()

    def removeWordNodes(self):
        # traverse each node, and remove word nodes
        # because word nodes have no children, so
        # we can just clear the wordL 
        for node in self.rootNode.traverse():
            if not isinstance(node, WordNode): 
                node.wordL=[]

    def appendInfo(self, infoFile):
        Info.nodeName="word"
        f=open(infoFile)
        line=f.readline().strip("\r\n")
        L=line.split("\t")
        schemaL=[]
        for idx in range(len(L)):
            obj=Generic()
            if L[idx][-1]=="]":
                m=re.search('^(.+)\[(.*)\]$',L[idx])
                obj.name=m.group(1)
                obj.type="list"
                if len(m.group(2))>0:
                    obj.sep=m.group(2)
                else:
                    obj.sep=","

            else:
                obj.name=L[idx]
                obj.type="string"
            schemaL.append(obj)
        T={}
        for line in f:
            line=line.strip("\r\n")
            itemL=[]
            for item in line.split("\t"):
                itemL.append(item.strip())
            sid=itemL[0]
            T[sid]=Info()
            T[sid].setData(schemaL, itemL)

        for node in self.rootNode.traverse():
            if isinstance(node, WordNode):
                if node.info.sid in T:
                    node.info=T[node.info.sid]

    def writeCSVFile(self, schema=None, treeFile=sys.stdout):
        if isinstance(treeFile, file):
            outf=treeFile
        else:
            outf=open(treeFile, "w")

        for node in self.rootNode.traverse():
            outf.write("%s\n"%(node.csvStr(schema)))
        outf.close()

    def writeObjTree(self, treeFile=sys.stdout):
        if isinstance(treeFile, file):
            outf=treeFile
        else:
            outf=open(treeFile, "w")

        for node in self.rootNode.traverse():
            outf.write("%s\n"%(node.objStr()))
        outf.close()

    def loadObjTree(self, treeFile):
        line_no=0
        f=open(treeFile)
        stackL=[]
        for line in f:
            line=line.rstrip("\r\n")
            if len(line)==0:
                continue

            nodePath=line[:line.find("|")]
            info=line[line.find("|")+2:]
            L=info.split("\t")

            #print line
            if len(nodePath)==0:
                obj=SemanticTypeNode(info, "semanticType", len(nodePath))

            elif nodePath[0]==",":
                obj=SemanticTypeNode(info, "semanticType", len(nodePath))

            elif nodePath[0]==".":
                obj=CategoryNode(info, "category", len(nodePath))

            elif nodePath[0]==" ":
                obj=WordNode(L[0], "word", len(nodePath))
                obj.info=Info(eval(L[1]))

            elif nodePath[0]=="+":
                obj=WordNode(L[0], "attachWord", len(nodePath))
                obj.info=Info(eval(L[1]))

            if len(stackL)==0:
                stackL.append(obj)

            elif obj.level > stackL[-1].level:
                stackL[-1].addChild(obj)
                stackL.append(obj)

            elif obj.level <= stackL[-1].level:
                while obj.level <= stackL[-1].level:
                    stackL.pop()

                stackL[-1].addChild(obj)
                stackL.append(obj)

            if not obj.name in self.m_word2node:
                self.m_word2node[obj.name]=[]
            self.m_word2node[obj.name].append(obj)
            line_no+=1
        self.rootNode=stackL[0]


    def readCSVFile(self, treeFile):
        line_no=0
        f=open(treeFile)
        stackL=[]
        for line in f:
            line=line.rstrip("\r\n")
            if len(line)==0:
                continue

            nodePath=line[:line.find("|")]
            info=line[line.find("|")+2:]
            L=info.split("\t")

            #print line
            if len(nodePath)==0:
                obj=SemanticTypeNode(info, "semanticType", len(nodePath))

            elif nodePath[0]==",":
                obj=SemanticTypeNode(info, "semanticType", len(nodePath))

            elif nodePath[0]==".":
                obj=CategoryNode(info, "category", len(nodePath))

            elif nodePath[0]==" ":
                obj=WordNode(L[0], "word", len(nodePath))
                obj.info=Info()
                obj.info.word = obj.name
                obj.info.sid = L[1]
                obj.info.ehownet = L[2]

            elif nodePath[0]=="+":
                obj=WordNode(L[0], "attachWord", len(nodePath))
                obj.info=Info()
                obj.info.word = obj.name
                obj.info.sid = L[1]
                obj.info.ehownet = L[2]

            if len(stackL)==0:
                stackL.append(obj)

            elif obj.level > stackL[-1].level:
                stackL[-1].addChild(obj)
                stackL.append(obj)

            elif obj.level <= stackL[-1].level:
                while obj.level <= stackL[-1].level:
                    stackL.pop()

                stackL[-1].addChild(obj)
                stackL.append(obj)

            if not obj.name in self.m_word2node:
                self.m_word2node[obj.name]=[]
            self.m_word2node[obj.name].append(obj)
            line_no+=1
        self.rootNode=stackL[0]

if __name__=="__main__":
    tree=EHowNetTree()
    #tree.readCSVFile("../data/resultSimple.csv")
    #tree.removeCategoryNodes()
    #tree.appendInfo("../data/ckip_dictionary.txt")
    #tree.writeCSVFile()
    tree.writeObjTree()
