import time
start_time=time.time()

import os
import story_witer
import caption_adder

makable = 0
counter=0
extact=0
story=[]
while makable==0:
    try:
         base = open(("story "+str(counter)+"/story "+str(counter)+".txt"),"r")
         base.close()
         counter+=1
         extact+=1
    except:
        if extact>0:
            makable=1
            break
        else:
            counter+=1
PATH_s=("story "+str(counter))
print(str(makable)+" the story no is "+str(counter)+" "+PATH_s)
print(os.path.dirname(PATH_s))
while makable==1:
    exiter=0
    print("please note if you start the sentence with generate it will be given to an ai to process and generate a script")
    while exiter!=1:
        content=input("enter the content")
        if content == "exit":
            exiter=1
        else :
            story.append(content)
    if content == "1" or content =="close" or content=="exit":
        confirm_exit=input("do you really want to exit")
        if confirm_exit == "1" or confirm_exit =="close" or confirm_exit=="exit":
            makable+=1
        elif confirm_exit == "run":
            runner_prog="base"
            while runner_prog!="s1" and runner_prog!="p1" and runner_prog!="c1" and runner_prog!="exit": 
                runner_prog=input("please give the function you wnat to run therse are your option\n story writer : s1\n part maker :p1 \n caption adder :c1 \n exit :exit")
                print("you have give input as "+str(runner_prog))
            give_me_path=input("give me the path of the video ")
            if runner_prog =="s1":
                story_witer.full_video(give_me_path)
            elif runner_prog=="p1":
                story_witer.part_maker(give_me_path)
            elif runner_prog=="c1":
                caption_adder.add_caption(give_me_path)
            else:
                makable+=1
                break
        else:
            
            while os.path.exists(PATH_s):
                counter+=1
                PATH_s=("story "+str(counter))
            if not os.path.exists(PATH_s):
                os.makedirs(PATH_s)
            else:
                counter+=1
                PATH_s=("story "+str(counter))
            try:
                maker= open((PATH_s+"/story "+str(counter)+".txt"),"w")
                Text="".join(story)
                maker.write(Text)
                maker.close()
                story_witer.full_video((PATH_s+"/story "+str(counter)+".txt"))
                caption_adder.add_caption((PATH_s+"/final.mp4"),"")
                caption_adder.add_caption((PATH_s+"/final_hindi.mp4"),"hindi")
                story_witer.part_maker((PATH_s+"/output_.mp4"),"")
                story_witer.part_maker((PATH_s+"/output_hindi.mp4"),"hindi")
                os.remove((PATH_s+"/final.mp4"))
                os.remove((PATH_s+"/final_hindi.mp4"))
            except Exception as reason:
                print("unable to make")
                print("reason is  "+str(reason))
                break
            end_time=time.time()
            print("time total taken:"+str((end_time-start_time)))
