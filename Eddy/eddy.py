#!/bin/env python3

############################################################################################################
#
#                                       ASSIGNMENT 1 - COMP2041
#                                               eddy.py
#
#                                       by  Ayusha Priyadarshani
#                                               z5452643
#
#                                              20-04-2024
#                    
############################################################################################################

import sys,re
import difflib as diff

#fetch eddy command from arguments
exp=sys.argv

#initialised available command list for multicommand management
commands=["q","s","p",'d']

#error handling
if len(sys.argv)==1:
    print("usage: eddy [-i] [-n] [-f <script-file> | <sed-command>] [<files>...]")
    exit(1)

#if quit command is called
def q(exp,x=[]):
    #initialise list to contain answer
    Answer=[]
    #initialise file variable to None
    file=None

    #fetch all file names provided in arguments
    for i in range(2,len(sys.argv)):
        if ".txt" in sys.argv[2]:
            file=open(sys.argv[2])

    #if regex NOT in eddy command
    if '/' not in exp:
        
        #remove command keywords to get basic command data
        exp=re.sub('q.*','',exp)
        exp=re.sub('-f','',exp)
        
        #if number is provided
        if len(exp)>0:
            #if we need to quit after printing final line
            if "$" in exp:
                exp=re.sub("\$",'10000000',exp)
               
            num=int(exp)
        else:
            num=1
        
        count=1
        
        #if file is not provided
        if file!=None:
            #add every line to answer list
            for i in file:
                if count<=num:
                    Answer.append(i)
                else:
                    return Answer
                
                count+=1
            
            #return answer
            return Answer
        
        #if input list is None
        elif len(x)==0:
            #get input from stdin
            for x in sys.stdin:
                if count<=num:
                    Answer.append(x)
                else:
                    return Answer
                
                count+=1
            return Answer
       
        #get input from input list
        else:
            for i in x:
                if count<=num:
                    Answer.append(i)
                else:
                    return Answer
                
                count+=1
            return Answer

    else:
        #if regex is present 
        y=re.sub("q","",exp)
        y=re.sub("/","",y)

        #get input from stdin
        for x in sys.stdin:
            if (re.search(y,x))==None:
                Answer.append(x)
            else:
                Answer.append(x)
                #if regex matched, return
                return Answer
                
        return Answer

#if print command is called
def p(exp,x=[]):
    #fetch expression data
    exp=re.sub('p.*','',exp)
    Answer=[]
    if '/' not in exp:
        if "," in exp:
            y=exp.split(',')
            start=int(y[0])
            end=int(y[1])
            
            count=1
            now=0
            if len(x)==0:
                for x in sys.stdin:
                    if start<=count and count<=end:
                        Answer.append(x)
                        Answer.append(x)
                    
                    else:
                        Answer.append(x)
                    
                    count+=1
                return Answer
            else:
                for i in x:
                    if re.search(start,i)!=None:
                        now=1
                    elif re.search(end,i)!=None:
                        now=0
                    elif now==0:
                        Answer.append(i)
                    count+=1
                return Answer
        else:
            #if last line needs to be reprinted
            if "$" in exp:
                exp=exp.strip("$")
                num=-1
            #if numbers are provided
            elif len(exp)!=0:
                num=int(exp)
            #if no number is given
            else:
                num=0

            #no input list provided
            count=1
            if len(x)==0:
                for x in sys.stdin:
                    #if number to be repeated not reached
                    if count!=num and num!=0:
                        Answer.append(x)
                    #if count reached
                    else:
                        Answer.append(x)
                        Answer.append(x)
                    count+=1
                #if last line is reprinted
                if num==-1:
                    Answer.append(x)
                return Answer
            else:
                #fetch input from input list
                for i in x:
                    #check count and append to answer
                    if count!=num and num!=0:
                        Answer.append(i)
                    else:
                        Answer.append(i)
                        Answer.append(i)
                    count+=1
                return Answer
    else:
        #fetch command data from expression
        y=re.sub("p","",exp)
        y=re.sub("/","",y)
        if "," in y:
            #range provided
            y=y.split(',')
            start=y[0]
            end=y[1]
            count=1
            now=0
            #no input data
            if len(x)==0:
                for x in sys.stdin:
                    #if start point reached
                    if re.search(start,x)!=None:
                        Answer.append(x)
                        Answer.append(x)
                        now=1
                    #if end point reached 
                    elif re.search(end,x)!=None:
                        Answer.append(x)
                        Answer.append(x)
                        now=0
                    #if out of range
                    elif now==0:
                        Answer.append(x)
                    #print twice till end point reached
                    elif now==1:
                        Answer.append(x)
                        Answer.append(x)
                    count+=1
                return Answer
        #no range
        else:
            #no input data
            if len(x)==0:
                for x in sys.stdin:
                    if (re.search(y,x))==None:
                        Answer.append(x)
                    else:
                        #append to answer if regex matched
                        Answer.append(x)
                        Answer.append(x)
                return Answer
            else:
                #input list provided
                for i in x:
                    if (re.search(y,i))==None:
                        Answer.append(i)
                    else:
                        #append to answer if regex matched
                        Answer.append(i)
                        Answer.append(i)
                return Answer

#if -n command is called
def n(exp):
    
    Answer=[]
    
    #if p command is used in conjunction
    if 'p' in exp:
        #clean expression
        exp=re.sub("p","",exp)
        #if no regex
        if '/' not in exp:
            #if end of line used
            if "$" in exp:
                check=1
                exp=exp.strip("$")
                num=-1
            else:
                num=int(exp)
            count=1
            for x in sys.stdin:
                if count!=num:
                    pass
                else:
                    Answer.append(x)
                    return Answer
                count+=1
            #print last line if true
            Answer.append(x)
            return Answer
        
        else:
            #clean expression
            exp=re.sub("p","",exp)
            y=re.sub("/","",exp)
            for x in sys.stdin:
                if (re.search(y,x))==None:
                    continue
                else:
                    Answer.append(x)
            
            return Answer
    else:
        return Answer

#if d command is called 
def d(exp,x=[]):
    
    Answer=[]
    if '/' not in exp:
        #clean expression
        exp=re.sub('d.*','',exp)
        if "," in exp:
            #range given
            y=exp.split(',')
            start=int(y[0])
            end=int(y[1])
            
            count=1
            now=0
            #input list not provided
            if len(x)==0:
                for x in sys.stdin:
                    #if item in range, dont print
                    if start<=count and count<=end:
                        pass
                    else:
                        Answer.append(x)
                    count+=1
                return Answer
            #input list provided
            else:
                for i in x:
                    #if item in range, dont print
                    if start<=count and count<=end:
                        pass
                    else:
                        Answer.append(i)
                    count+=1
                return Answer
        else:
            check=0
            #delete last line
            if "$" in exp:
                check=1
                exp=exp.strip("$")
                num=-1
            elif len(exp)!=0:
                num=int(exp)
            else:
                num=0
            count=1
            if len(x)==0:
                for x in sys.stdin:
                    #if remove count reached, skip
                    if count==num or num==0:
                        pass
                    else:
                        Answer.append(x)
                    count+=1
                #remove last line 
                if check==1:
                    Answer.pop()
                return Answer
            else:
                #for item in input list
                for i in x:
                    if count==num or num==0:
                        pass
                    else:
                        Answer.append(i)
                    count+=1
                if check==1:
                    Answer.pop()
                return Answer
    else:
        #clean expression
        y=re.sub("d.*","",exp)
        y=re.sub("/","",y)
        if "," in y:
            #range given
            y=y.split(',')
            start=y[0].replace(' ','')
            end=y[1].replace(' ','')
            
            count=1
            now=0
            if len(x)==0:
                for x in sys.stdin:
                    #range start matched
                    if re.search(start,x)!=None:
                        now=1
                    #range end matched
                    elif re.search(end,x)!=None:
                        now=0
                    #if not in range
                    elif now==0:
                        Answer.append(x)
                    count+=1
                return Answer
            else:
                for i in x:
                    #range start matched
                    if re.search(start,i)!=None:
                        now=1
                    #range end matched
                    elif re.search(end,i)!=None:
                        now=0
                    #not in range
                    elif now==0:
                        Answer.append(i)
                    count+=1
                return Answer
        else:
            #range not given
            if len(x)==0:
                for x in sys.stdin:
                    #if regex matched, continue
                    if (re.search(y,x))!=None:
                        continue
                    else:
                        Answer.append(x)
                return Answer
            else:
                for i in x:
                    #if regex matched, continue
                    if (re.search(y,i))!=None:
                        continue
                    else:
                        Answer.append(i)
                        
                return Answer
            
#if s command is called
def s(exp,x=[]):
    Answer=[]
    #if command does not start with s
    if re.search("^s",exp)!=None:
        delimiter=list(exp)[1]
        
        if "g" not in exp:
            if "[" in exp:
                rpl_word=re.findall(f"\[(\d+)\]",exp)
                
                rpl_with=re.sub(rpl_word[0],"",exp)
                
                rpl_with=rpl_with.replace(f"{delimiter}","")
                
                rpl_with=re.sub(f"s\[","",rpl_with)
                
                rpl_with=re.sub(f"\]","",rpl_with)
                
                rpl_with=rpl_with.strip(f"{delimiter}")
                
                new_rpl_word=[]
                for i in rpl_word:
                    for j in i:
                        new_rpl_word.append(j)
                
                #print(new_rpl_word)
                #rpl_word=re.findall(r"/[a-zA-Z]+/",exp)
                    
                for x in sys.stdin:
                    count=0
                    for item in new_rpl_word:
                        if (re.search(item,x))==None:
                            if count==0:
                                count+=1
                                continue
                            else:
                                Answer.append(x)
                        else:
                            x=re.sub(item,rpl_with,x,1)
                            Answer.append(x)
                            break
                
                return Answer
            else:
                rpl_word=re.findall(f"s{delimiter}[a-zA-Z]+{delimiter}",exp)
                if len(rpl_word)==0:
                    rpl_word=re.findall(f"s{delimiter}(\d+){delimiter}",exp)
                rpl_with=re.sub(rpl_word[0],"",exp)
                rpl_with=re.sub(f"s{delimiter}","",rpl_with)
                rpl_with=rpl_with.strip(f"{delimiter}")
                
                rpl_word=rpl_word[0]
                rpl_word=re.sub(f"s{delimiter}","",rpl_word)
                rpl_word=re.sub(f"{delimiter}","",rpl_word)

                

                if len(x)==0:
                    for x in sys.stdin:
                        x=re.sub(rpl_word,rpl_with,x,1)
                        Answer.append(x)

                    return Answer
                
                else:
                    for i in x:
                        i=re.sub(rpl_word,rpl_with,i,1)
                        Answer.append(x)

                    return Answer
        
        else:
            exp=re.sub("g","",exp)
            if "[" in exp:
                rpl_word=re.findall(f"s{delimiter}\[(\d+)\]{delimiter}",exp)
                rpl_with=re.sub(rpl_word[0],"",exp)
                rpl_with=re.sub(f"s{delimiter}\[","",rpl_with)
                rpl_with=re.sub(f"\]{delimiter}","",rpl_with)
                rpl_with=rpl_with.strip(f"{delimiter}")
                
                new_rpl_word=[]
                for i in rpl_word:
                    for j in i:
                        new_rpl_word.append(j)
                
                #print(new_rpl_word)
                #rpl_word=re.findall(r"/[a-zA-Z]+/",exp)
                    
                for x in sys.stdin:
                    count=0
                    for item in new_rpl_word:
                        if (re.search(item,x))==None:
                            if count==0:
                                count+=1
                                continue
                            else:
                                Answer.append(x)
                        else:
                            x=re.sub(item,rpl_with,x)
                            Answer.append(x)
                            return Answer
                    
                return Answer
            else:
                rpl_word=re.findall(f"s{delimiter}[a-zA-Z]+{delimiter}",exp)
                if len(rpl_word)==0:
                    rpl_word=re.findall(f"s{delimiter}(\d+){delimiter}",exp)
                rpl_with=re.sub(rpl_word[0],"",exp)
                rpl_with=re.sub(f"s{delimiter}","",rpl_with)
                rpl_with=rpl_with.strip(f"{delimiter}")
                
                rpl_word=rpl_word[0]
                rpl_word=re.sub(f"s{delimiter}","",rpl_word)
                rpl_word=re.sub(f"{delimiter}","",rpl_word)

                for x in sys.stdin:
                    x=re.sub(rpl_word,rpl_with,x)
                    Answer.append(x)
                
                return Answer
    else:
        delimiter="/"
        #if expression doesnt start with a delimiter
        if re.search(f"^{delimiter}",exp)==None:
            
            #fetch count
            count =re.findall(r"[\d+]s",exp)
            
            count=count[0].strip("s")
            
            exp=re.sub(count,"",exp,1)
            
            #if repeated substitution command not present
            if "g" not in exp:
                #fetch replace word and replace with word
                rpl_word=re.findall(f"s{delimiter}(\d+){delimiter}",exp)
                rpl_with=re.sub(rpl_word[0],"",exp)
                rpl_with=re.sub(f"s{delimiter}","",rpl_with)
                rpl_with=rpl_with.strip(f"{delimiter}")
                
                rpl_word=rpl_word[0]
                rpl_word=re.sub(f"s{delimiter}","",rpl_word)
                rpl_word=re.sub(f"{delimiter}","",rpl_word)

                num=1
                for x in sys.stdin:
                    #count to be substituted reached
                    if num==int(count):
                        #make changes and append
                        x=re.sub(rpl_word,rpl_with,x,1)
                    Answer.append(x)
                    num+=1
                return Answer
            else:
                #repeated substitution present
                exp=re.sub("g","",exp)

                #find replace words
                rpl_word=re.findall(f"s{delimiter}(\d+){delimiter}",exp)
                rpl_with=re.sub(rpl_word[0],"",exp)
                rpl_with=re.sub(f"s{delimiter}","",rpl_with)
                rpl_with=rpl_with.strip(f"{delimiter}")
                
                rpl_word=rpl_word[0]
                rpl_word=re.sub(f"s{delimiter}","",rpl_word)
                rpl_word=re.sub(f"{delimiter}","",rpl_word)

                
                num=1
                for x in sys.stdin:
                    #replace if regex match
                    if num==int(count):
                        x=re.sub(rpl_word,rpl_with,x)
                    Answer.append(x)
                    num+=1
                return Answer
        
        else:
            #regex present
            regex =re.findall(f".*{delimiter}s",exp)
            
            #clean regex
            regex=regex[0].strip(f"{delimiter}s")
            
            #clean expression
            exp=re.sub(regex,"",exp).lstrip(f"{delimiter}").strip("g")
            regex=regex.replace("/","")
            
            #if multiple replace with regex given
            if "[" in exp:
                rpl_word=re.findall(f"\[(\d+)\]",exp)
                
                rpl_with=re.sub(rpl_word[0],"",exp)
                
                rpl_with=rpl_with.replace(f"{delimiter}","")
                
                rpl_with=re.sub(f"s\[","",rpl_with)
                
                rpl_with=re.sub(f"\]","",rpl_with)
                
                rpl_with=rpl_with.strip(f"{delimiter}")
                
                #get replace with list
                new_rpl_word=[]
                for i in rpl_word:
                    for j in i:
                        new_rpl_word.append(j)
            
                #if range given
                if "," in regex:
                    y=regex.split(',')
                    start=y[0]
                    end=y[1]
                    
                now=0
                for x in sys.stdin:
                    #if start regex matched
                    if re.search(start,x)!=None:
                        now=1
                    #in range
                    if now==1:
                        #replace words
                        for item in new_rpl_word:
                            x=re.sub(item,rpl_with,x)
                        Answer.append(x)
                    #not in range
                    elif now==0:
                        Answer.append(x)
                    #if end regex matches
                    if re.search(end,x)!=None:
                        now=0
                
                return Answer
            #if single replace with given
            else:
                rpl_word=re.findall(f"s{delimiter}(\d+){delimiter}",exp)
                rpl_with=re.sub(rpl_word[0],"",exp)
                rpl_with=re.sub(f"s{delimiter}","",rpl_with)
                rpl_with=rpl_with.strip(f"{delimiter}")
                
                rpl_word=rpl_word[0]
                rpl_word=re.sub(f"s{delimiter}","",rpl_word)
                rpl_word=re.sub(f"{delimiter}","",rpl_word)
                #range given
                if "," in regex:
                    y=regex.split(',')
                    start=y[0]
                    end=y[1]
                    now=0
                    if len(x)==0:
                        for x in sys.stdin:
                            #start regex matched
                            if re.search(start,x)!=None:
                                now=1
                            #in range
                            if now==1:
                                x=re.sub(rpl_word,rpl_with,x)
                                Answer.append(x)
                            #not in range
                            elif now==0:
                                Answer.append(x)
                            #end regex matched
                            if re.search(end,x)!=None:
                                now=0
                        return Answer
                #range not given
                else:
                    #no input list given
                    if len(x)==0:
                        for x in sys.stdin:
                            if re.search(regex,x):
                                x=re.sub(rpl_word,rpl_with,x)
                            Answer.append(x)
                    return Answer

#multiple commands called
def semi_colon(exp):
    test=[]
    
    if exp==sys.argv:
        #substitute comment #s 
        exp=re.sub("#.*;","",exp[1]) 

        for x in exp:
            #find commands and add to list
            if x in commands:
                test.append(x)
    else:
        exp=re.sub("#.*;","",exp)
        for x in exp:
            if x in commands:
                test.append(x)

    
    
    count=0
    #if d is called first
    if test[0]=="d":
        
        if exp==sys.argv:
            word=sys.argv[1]
        else:
            word=exp
        #find first and second commands
        exp1=re.sub(";.*$","",word)
        exp2=re.sub(".*;","",word)
        
        #compare both commands
        string1 = exp1
        string2 = test[1]

        A = set(string1) # Store all string1 list items in set A
        B = set(string2) # Store all string2 list items in set B
        
        str_diff1 = A.symmetric_difference(B)

        string3 = exp2
        string4 = test[0]

        C = set(string3) # Store all string1 list items in set A
        D = set(string4) # Store all string2 list items in set B

        str_diff2 = C.symmetric_difference(D)

        #if commands are deleting and changing at the same counter
        #continue
        if str_diff1==str_diff2:
            pass
        else:
            #swap command 1 and command 2
            temp=test[1]
            test[1]=test[0]
            test[0]=temp
            count=1
    
    #commands not swapped
    if count==0:
        if exp==sys.argv:
            word=sys.argv[1]
        else:
            word=exp
        #get first and seconds
        exp2=re.sub(";.*","",word)
        exp1=re.sub(".*;","",word)

    #find commands in list 
    #execute respective function
    if test[0]=="q":
        Answer=q(exp2)
    elif test[0]=="p":
        Answer=p(exp2)
    elif test[0]=="s":
        Answer=s(exp2)
    elif test[0]=='d':
        Answer=d(exp2)
    

    #if both command are terminated at the same time
    string1 = exp1
    string2 = test[1]

    A = set(string1) # Store all string1 list items in set A
    B = set(string2) # Store all string2 list items in set B
    
    str_diff1 = A.symmetric_difference(B)

    string3 = exp2
    string4 = test[0]

    C = set(string3) # Store all string1 list items in set A
    D = set(string4) # Store all string2 list items in set B

    str_diff2 = C.symmetric_difference(D)

    

    Final=[]
    
    #second command is terminated if equal
    if str_diff1==str_diff2:
        Final=Answer
    else:
        #execute second command
        if test[1]=="q":
            Final=q(exp1,Answer)
        elif test[1]=="p":
            Final=p(exp1,Answer)
        elif test[1]=="s":
            Final=s(exp1,Answer)
        elif test[1]=="d":
            Final=d(exp1,Answer)

    #print final answer
    for i in range(0,len(Final)):
        print(Final[i],end="") 

#call semi colon func
if ';' in exp[1]:
    semi_colon(exp)

#call -f func
elif 'f' in exp[1]:
    file = sys.argv[2]
    stream=open(file)
    
    test=[]
    exp=""
    count=0
    for line in stream:
        line=line.replace("\n",";")
        exp+=(line)
        count+=1
        for i in line:
            if i in commands:
                test.append(i)
    
    exp=re.sub(";$","",exp)
    
    if len(test)>1:
        semi_colon(exp)
    
    else:
        if test[0]=="q":
            Answer=q(exp)
        elif test[0]=="p":
            Answer=p(exp)
        elif test[0]=="s":
            Answer=s(exp)
        elif test[0]=='d':
            Answer=d(exp)
        
        for i in Answer:
            print(i,end="")

#call q func
elif 'q' in exp[1]:
    exp=exp[1]
    Answer=(q(exp))
    for i in range(0,len(Answer)):
        print(Answer[i],end="")

#call p func
elif 'p' in exp[1]:
    exp=exp[1]
    Answer=(p(exp))
    for i in range(0,len(Answer)):
        print(Answer[i],end="")

#call -n func
elif '-n' in exp[1]:
    exp=exp[2]
    Answer=(n(exp))
    for i in range(0,len(Answer)):
        print(Answer[i],end="")

#call d func
elif 'd' in exp[1]:
    exp=exp[1]
    Answer=(d(exp))
    for i in range(0,len(Answer)):
        print(Answer[i],end="")

#call s func
elif 's' in exp[1]:
    exp=exp[1]
    Answer=(s(exp))
    for i in range(0,len(Answer)):
        print(Answer[i],end="")

#if append command called 
elif 'a' in exp[1]:
    exp=exp[1].split('a')
    #get count
    if exp[0]=="$":
        num=-1
    #print after every item
    elif len(exp[0])==0:
        num=0
    else:
        num=int(exp[0])
    #get word
    exp=exp[1].replace(" ","")
    
    count=1
    for x in sys.stdin:
        #count not equal to number
        if count!=num:
            print(x,end="")
        else:
            #count equal
            #print after sequence
            print(x,end="")
            print(exp)
        count+=1
        #if need to print after every item
        if num==0:
            print(exp)
    #if need to print after last item 
    if num==-1:
        print(exp)

#if insert command called
elif 'i' in exp[1]:
    #retrieved count 
    exp=exp[1].split('i')
    if exp[0]=="$":
        num=-1
    elif len(exp[0])==0:
        num=0
    else:
        num=int(exp[0])
    #retrieved word
    exp=exp[1].replace(" ","")
    
    #add all input to list
    input=[]
    for x in sys.stdin:
        input.append(x)
    
    for i in range(0,len(input)):
        #print before last item
        if num==-1:
            #if last item reached
            if i==len(input)-1:
                print(exp)
        #if count reached or 
        #print before each item
        if i==num-1 or num==0:
            print(exp)
        #print sequence
        print(input[i],end="")
        
#if change command called
elif 'c' in exp[1]:
    #retrieved count 
    exp=exp[1].split('c')
    if exp[0]=="$":
        num=-1
    elif len(exp[0])==0:
        num=0
    else:
        num=int(exp[0])
    #retrieved word
    exp=exp[1].replace(" ","")
    
    #add all input to list
    input=[]
    for x in sys.stdin:
        input.append(x)
    
    for i in range(0,len(input)):
        #if count reached or 
        #change each item
        if i==num-1 or num==0:
            print(exp)
        #print sequence
        elif num!=-1:
            print(input[i],end="")
        #change last item
        if i==len(input)-1:
            #if last item reached
            if num==-1:
                print(exp)
        
