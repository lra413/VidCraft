import os
import story_witer
import caption_adder
import customtkinter as ctk
from tkinter import filedialog
import threading as th
from PIL import Image as pil
import time


#GUI Main window config
app= ctk.CTk()
app.geometry("500x500")
app.title("Vid Craft")
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

#Essential variables
text_file=""
final_destination=""#folder to pu results in
def Browse():
    global text_file
    text_file = filedialog.askopenfilename()
    processLabel.configure(text="Text file selected as "+str(text_file))
    processLabel.update()
    return text_file
def Browse_exit():
    global final_destination
    final_destination=filedialog.askdirectory()
    processLabel.configure(text="Output Folder selected as "+str(final_destination))
    processLabel.update()
    return final_destination
makable = 0
extact=0
story=[]

dotsLabel = ctk.CTkLabel(master=app, text="",font=("Arial" , 20), text_color="#FFCC70")
dotsLabel.place(relx=0.5, rely=0.9,anchor="center")
dots="." #a string that will be used for the Dots() method
count = 0
def Dots (): # This method gives feedback to the player that the program is still running
    global count, dots , processing
    if (processing is True):
        if (count > 15):
            count = -1
            dots = "."
            dotsLabel.configure(text=dots)
            dotsLabel.after(100,Dots)
        else:
            dots = dots + dots[count]
            dotsLabel.configure(text=dots)
            count += 1
            dotsLabel.after(100,Dots)
    else:
        dots = ""
        dotsLabel.configure(text=dots)        

def make_video(content,folder):
    start = time.time()
    processLabel.configure(text="vid CrafT is active")
    processLabel.update()
    print(folder)
    PATH_s=folder
    print(PATH_s)
    try:
        try:
            tmp_story_bucket=open(content,"r")
            for i in tmp_story_bucket:
                story.append(i)
        except:
            story="".join(content)
        maker= open((PATH_s+"/story.txt"),"w")
        Text="".join(story)
        maker.write(Text)
        maker.close()
        processLabel.configure(text="Genrating voices")
        processLabel.update()
        #creates a base video in english and then translate to hindi as well
        story_witer.full_video((PATH_s+"/story.txt"))
        processLabel.configure(text="Genrating video")
        processLabel.update()
        #add captions to english version
        caption_adder.add_caption((PATH_s+"/final.mp4"),"")
        caption_adder.add_caption((PATH_s+"/final_hindi.mp4"),"hindi")
        # strips the long version into a shorter version
        processLabel.configure(text="adding effects")
        processLabel.update()
        story_witer.part_maker((PATH_s+"/output_.mp4"),"")
        # strips the long version into a shorter version for hindi
        story_witer.part_maker((PATH_s+"/output_hindi.mp4"),"hindi")
        processLabel.configure(text="Striping pecies")
        processLabel.update()
        #removes unnecessary files
        os.remove((PATH_s+"/final.mp4"))
        end = time.time()
        processLabel.configure(text="Video generated")
        processLabel.update()
        print(end - start)
    except Exception as reason:
        print("unable to make")
        print("reason is  "+str(reason))
        err_msg="unable to make \n reason is "+str(reason)
        err_msg_file=open(PATH_s+"/error.txt")
        err_msg_file.write(err_msg)
        err_msg_file.close()
        end = time.time()
        print(end - start)
def requirements_cheakers():
    if text_file!="":
        if final_destination!="":
            validity=0
            try:
                selected_txt_file=open(text_file)
                for i in selected_txt_file:
                    content="".join(i)
                validity=1
            except:
                validity=0
                
            if validity==1:
                try:
                    global processing
                    dotsThread = th.Thread(target=Dots)
                    processing = True
                    dotsThread.start()
                    processThread = th.Thread(target=make_video(content=content,folder=final_destination))
                    processThread.start()

                except:
                    processLabel.configure(text="Some error occured")
                    processLabel.update()
            else:
                validity=0
                processLabel.configure(text="Unable to read the given file")
                processLabel.update()
        else:
            processLabel.configure(text="Destination folder not selcted")
            processLabel.update()
    else:
        print(btn_in,btn_out)
        processLabel.configure(text="text file not selcted")
        processLabel.update()

if screen_height>screen_width:    
    logo_width=int(0.2*screen_width)
    logo_height=int(0.2*screen_width)
else:
    logo_width=int(0.2*screen_height)
    logo_height=int(0.2*screen_height)
logo = pil.open("logo.png")
logo.resize([1000,1000])
logo_image=ctk.CTkImage(light_image=logo,size=[logo_width,logo_height])
logo_image_label=ctk.CTkLabel(app,image=logo_image,text="")
logo_image_label.place(relx=0.5,rely=0.2,anchor="center")
label = ctk.CTkLabel(master=app, text="Select story file",font=("Arial" , 20), text_color="#FFCC70")
label.place(relx=0.5, rely=0.3,anchor="center")
btn_in = ctk.CTkButton(master=app, text="Browse",command=Browse)
btn_in.place(relx=0.5,rely=0.345,anchor="center")
label = ctk.CTkLabel(master=app, text="Select story file",font=("Arial" , 20), text_color="#FFCC70")
label.place(relx=0.5, rely=0.45,anchor="center")
btn_out = ctk.CTkButton(master=app, text="Browse",command=Browse_exit)
btn_out.place(relx=0.5,rely=0.495,anchor="center")
processBtn = ctk.CTkButton(master=app, text="Process",command=requirements_cheakers)
processBtn.place(relx=0.5, rely=0.7,anchor="center")
processLabel = ctk.CTkLabel(master=app, text="",font=("Arial" , 20), text_color="#FFCC70")
processLabel.place(relx=0.5, rely=0.8,anchor="center")
app.mainloop()