import os,sys
import math
import random
import time 
def map_add(mp, key1,key2, value):
    if (key1 not in mp):
        mp[key1] = {}
    if (key2 not in mp[key1]):
        mp[key1][key2] = 0.0
    mp[key1][key2] += value
    
def map_add1(mp,key1,key2):
    if(key1 not in mp):
        mp[key1]={}
    mp[key1][key2]=1

def map_add2(mp,key):
    if (key not in mp):
        mp[key] = 0
    mp[key]+=1

f = open("data/relation2id.txt","r")
relation2id = {}
id2relation = {}
relation_num = 0
for line in f:
    seg = line.strip().split()
    relation2id[seg[0]] = int(seg[1])
    id2relation[int(seg[1])]=seg[0]
    id2relation[int(seg[1])+1345]="~"+seg[0]
    relation_num+=1
f.close()

f = open("data/train.txt","r")
ok = {}
a ={}

for line in f:
    seg = line.strip().split()
    e1 = seg[0]
    e2 = seg[1]
    rel = seg[2]
    if (e1+" "+e2 not in ok):
        ok[e1+" "+e2]={}
    ok[e1+" "+e2][relation2id[rel]]=1
    if (e2+" "+e1 not in ok):
        ok[e2+" "+e1]={}
    ok[e2+" "+e1][relation2id[rel]+relation_num]=1
    if (e1 not in a):
        a[e1]={}
    if (relation2id[rel] not in a[e1]):
        a[e1][relation2id[rel]]={}
    a[e1][relation2id[rel]][e2]=1
    if (e2 not in a):
        a[e2]={}
    if ((relation2id[rel]+relation_num) not in a[e2]):
        a[e2][relation2id[rel]+relation_num]={}
    a[e2][relation2id[rel]+relation_num][e1]=1
f.close()


f = open("data/test.txt","r")
for line in f:
    seg = line.strip().split()
    if (seg[0]+" "+seg[1] not in ok):
        ok[seg[0]+' '+seg[1]]={}
    if (seg[1]+" "+seg[0] not in ok):
        ok[seg[1]+' '+seg[0]]={}
f.close()

h_e_p = {}

f = open("data/e1_e2.txt","r")
for line in f:
    seg = line.strip().split()
    ok[seg[0]+" "+seg[1]] = {}
    ok[seg[1]+" "+seg[0]] = {}
f.close()

path_dict = {}
path_r_dict = {}
m_e = {}

f = open("data/path_1.txt","r")
for line in f:
    seg = line.strip().split()
    if (len(seg)==2):
        path_dict[seg[0]]=int(seg[1])
    else:
        path_dict[seg[0]+" "+seg[1]]=int(seg[2])
f.close()


f = open("data/path_2.txt","r")
for line in f:
    seg = line.strip().split()
    if (len(seg)==2):
        path_r_dict[seg[0]]=int(seg[1])
    else:
        path_r_dict[seg[0]+" "+seg[1]]=int(seg[2])
f.close()


g = open("data/path2.txt","w")

train_path = {}


step = 0
time1= time.time()
path_num = 0

h_e_p={}
h_e_p1={}
h_e_p2={}
e2e={}
for e1 in a:
    for rel1 in a[e1]:
        e2_set = a[e1][rel1]
        for e2 in e2_set:
            map_add(h_e_p,e1+' '+e2,str(rel1),1.0/len(e2_set))
            map_add(h_e_p1,e1+' '+e2,str(rel1),1.0/len(e2_set))
            map_add1(e2e,e1,e2)
print time.time()-time1,len(h_e_p),len(e2e)

for key in h_e_p1:
    seg=key.split()
    e1=seg[0]
    e2=seg[1]
    if(e2 in e2e):
        e3_set=e2e[e2]
        for e3 in e3_set:
            if(e2+' '+e3 in h_e_p1 and e1+' '+e3 in ok):
                for rel1 in h_e_p1[key]:
                    for rel2 in h_e_p1[e2+' '+e3]:
                        map_add(h_e_p,e1+' '+e3,rel1+' '+rel2,h_e_p1[key][rel1]*h_e_p1[e2+' '+e3][rel2])
                        map_add(h_e_p2,e1+' '+e3,rel1+' '+rel2,h_e_p1[key][rel1]*h_e_p1[e2+' '+e3][rel2])
print time.time()-time1,len(h_e_p),len(h_e_p2)
'''
for key in h_e_p2:
    seg=key.split()
    e1=seg[0]
    e3=seg[1]
    if (e3 in e2e):
        e4_set=e2e[e3]
        for e4 in e4_set:
            if(e3+' '+e4 in h_e_p1 and e1+' '+e4 in ok):
                for rel in h_e_p2[key]:
                    for rel4 in h_e_p1[e3+' '+e4]:
                        map_add(h_e_p,e1+' '+e4,rel+' '+rel4,h_e_p2[key][rel]*h_e_p1[e3+' '+e4][rel4])
print time.time()-time1,len(h_e_p)

'''
for e1 in a:
    for e2 in a:
        e_1 = e1
        e_2 = e2
        if (e_1+" "+e_2 in h_e_p):
            path_num+=len(h_e_p[e_1+" "+e_2])
            bb = {}
            aa = {}
            g.write(str(e_1)+" "+str(e_2)+"\n")
            sum = 0.0
            for rel_path in h_e_p[e_1+' '+e_2]:
                bb[rel_path] = h_e_p[e_1+' '+e_2][rel_path]
                sum += bb[rel_path]
            for rel_path in bb:
                bb[rel_path]/=sum
                if bb[rel_path]>0.01:
                    aa[rel_path] = bb[rel_path]
            g.write(str(len(aa)))
            for rel_path in aa:
                train_path[rel_path] = 1
                g.write(" "+str(len(rel_path.split()))+" "+rel_path+" "+str(aa[rel_path]))
            g.write("\n")
    #print path_num, time.time()-time1
    sys.stdout.flush()
g.close()
print time.time()-time1
g = open("data/confidence.txt","w")
for rel_path in train_path:
    
    out = []
    for i in range(0,relation_num):
        if (rel_path in path_dict and rel_path+"->"+str(i) in path_r_dict):
            out.append(" "+str(i)+" "+str(path_r_dict[rel_path+"->"+str(i)]*1.0/path_dict[rel_path]))
    if (len(out)>0):
        g.write(str(len(rel_path.split()))+" "+rel_path+"\n")
        g.write(str(len(out)))
        for i in range(0,len(out)):
            g.write(out[i])
        g.write("\n")
g.close()
def work(dir):
    f = open("data/"+dir+".txt","r")
    g = open("data/"+dir+"_pra.txt","w")
    for line in f:
        seg = line.strip().split()
        e1 = seg[0]
        e2 = seg[1]
        rel = relation2id[seg[2]]
        g.write(str(e1)+" "+str(e2)+' '+str(rel)+"\n")
        b = {}
        a = {}
        if (e1+' '+e2 in h_e_p):
            sum = 0.0
            for rel_path in h_e_p[e1+' '+e2]:
                b[rel_path] = h_e_p[e1+' '+e2][rel_path]
                sum += b[rel_path]
            for rel_path in b:
                b[rel_path]/=sum
                if b[rel_path]>0.01:
                    a[rel_path] = b[rel_path]
        g.write(str(len(a)))
        for rel_path in a:
            g.write(" "+str(len(rel_path.split()))+" "+rel_path+" "+str(a[rel_path]))
        g.write("\n")
        g.write(str(e2)+" "+str(e1)+' '+str(rel+relation_num)+"\n")
        e1 = seg[1]
        e2 = seg[0]
        b = {}
        a = {}
        if (e1+' '+e2 in h_e_p):
            sum = 0.0
            for rel_path in h_e_p[e1+' '+e2]:
                b[rel_path] = h_e_p[e1+' '+e2][rel_path]
                sum += b[rel_path]
            for rel_path in b:
                b[rel_path]/=sum
                if b[rel_path]>0.01:
                    a[rel_path] = b[rel_path]
        g.write(str(len(a)))
        for rel_path in a:
            g.write(" "+str(len(rel_path.split()))+" "+rel_path+" "+str(a[rel_path]))
        g.write("\n")
    f.close()
    g.close()
work("train")
work("test")