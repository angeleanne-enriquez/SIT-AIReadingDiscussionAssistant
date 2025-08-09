#importing libraries
import os
from os import path
from anthropic import Anthropic
from anthropic.types import MessageParam
import pymupdf
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import customtkinter as ctk
import pyperclip
import fitz

#establish api key as client 
client=Anthropic(api_key="INSERT HERE")

'''submits the prompt to ai for ananlysis'''
def submitPrompt(prompt,systemPrompt):
    generatedText=""
    with client.messages.stream(
        model="claude-3-haiku-20240307", #latest claude api: fast, cheap, good for analyzing pdfs/text
        system=systemPrompt,
        max_tokens=4096,#max amount claude allows 
        messages=[{"role": "user","content": prompt}]
            #contains any prompt sent and any response given
            #facilitates a back and forth
    )as stream:
        try: 
            for text in stream.text_stream: generatedText+=text
        except Exception as e: 
            print(e)
            raise e
    return generatedText

'''extracts text from pdf'''
def readPDF(pdf):
    if not Path(pdf).is_file(): raise FileNotFoundError(f"File not found: {pdf}")
    extractPDF=""
    openPDF=pymupdf.open(pdf)
    for page in openPDF: extractPDF+=page.get_text()
    return extractPDF

def summarize(text):
    print(text.endswith(".pdf"))
    if text.endswith(".pdf"): text=readPDF(Path(text))
    prompt=f"Clearly and concisely summarize the following text. Include all key details, topic sentences, and technical terms. Definitions are helpful. \n\n {text}"
    return submitPrompt(prompt,"") #adds the summary in the outputbox

def browseFiles(textbox):
    textbox.delete("1.0","end-1c")
    filename=filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("PDF files","*.pdf*"),("all files","*.*")))
    textbox.insert(tk.END,filename)

def clear(textbox): textbox.delete("1.0",tk.END)

def paste(textbox): 
    textbox.delete("1.0",tk.END)
    textbox.insert(tk.END,pyperclip.paste())

def copy(textbox): pyperclip.copy(textbox.get("1.0","end-1c"))

def shortcut(event,action): action

#set appearance mode + colors
ctk.set_appearance_mode("system")

#colors
orange="#F39655"
yellow="#FCE385"
green="#7DCC77"
blue="#7FBEEB" 
purple="#A47EC6"
darkPink="#FC6EB3"
lightPink="#F2A1B2"
beige="#E8C6A9"

#hover colors
orangeHover="#F9CBAA"
yellowHover="#FEF1C2"
greenHover="#BEE6BB"
blueHover="#BFDFF5"
purpleHover="#D2BFE3"
darkPinkHover="#FEB7D9"
lightPinkHover="#F9D0D9"
beigeHover="#F4E3D4"

#create window
window=ctk.CTk()
window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
window.title("Class Discussion Using AI")

#fix window grid layout
window.columnconfigure(0,weight=0)
window.columnconfigure(1,weight=1)
window.rowconfigure(0,weight=window.winfo_screenheight())

#create page destroyer
def deletePage():
    for frame in mainFrame.winfo_children(): frame.destroy()

#create home page 
def homePage():
    deletePage()
    homePage=ctk.CTkFrame(master=mainFrame,fg_color=orange)
    homePage.pack(fill="both",expand=True)
    homeTitle=ctk.CTkLabel(
        master=homePage,
        text="Home",
        corner_radius=0,
        text_color="black",
        font=("Roboto",30))
    homeTitle.pack(fill="x",padx=10,pady=10,anchor="n")
    homeDescriptionFrame=ctk.CTkFrame(
        master=homePage,
        border_width=1,
        border_color="black")
    homeDescriptionFrame.pack(fill="x",padx=10,pady=10)
    homeDescription=ctk.CTkTextbox(
        master=homeDescriptionFrame,
        height=(len('''Welcome! This tool is used to primarily generate class discussions but can also summarize PDFs/text. \nPlease use the buttons on the left to go to the proper page.''')//2),
        wrap=tk.WORD,
        font=("Roboto",16))
    homeDescription.insert("1.0",
    '''Welcome! This tool is used to primarily generate class discussions but can also summarize PDFs/text. 
    \nPlease use the buttons on the left to go to the proper page.''')
    homeDescription.pack(fill="x",padx=10,pady=10,anchor="n")
    homeDescription.configure(state="disabled")

#create summary page
def summaryPage():
    deletePage()
    summaryPage=ctk.CTkFrame(master=mainFrame,fg_color=yellow)
    summaryPage.pack(fill="both",expand=True)

    summaryTitle=ctk.CTkLabel(
        master=summaryPage,
        text="PDF/Text Summarizer",
        corner_radius=0,
        text_color="black",
        font=("Roboto",30))
    summaryTitle.pack(fill="x",pady=10,anchor="n")

    summaryDescriptionFrame=ctk.CTkFrame(
        master=summaryPage,
        border_width=1,
        border_color="black")
    summaryDescriptionFrame.pack(fill="x",padx=10,pady=10)
    summaryDescription=ctk.CTkTextbox(
        master=summaryDescriptionFrame,
        height=(len('''Welcome! This is where you can summarize PDFs/text. 
        \n Please paste your text or path to your PDF file in the left textbox. The summary will then be generated in the right textbox by either pressing the "Summarize" button or pressing CTRL+Enter.
        \n There are five buttons below. The "Summarize" button summarizes the text/PDF file. The "Clear Text/Path" button deletes everything inside the left textbox. The "Paste Text/Path" automatically pastes the text/path to your PDF file into the left textbox. The "Browse Files" button allows you to manually select a PDF file you wish to summarize. Lastly, the "Copy Summary" button copies the summary outputted in the right textbox.
        \n To navigate to a different page, please use the buttons on the left to go to the proper page.
        \n Please make sure that your path is not in quotes before summarizing!''')//4)+20,
        wrap=tk.WORD,
        font=("Roboto",16))
    summaryDescription.insert(
        "1.0",
        '''Welcome! This is where you can summarize PDFs/text. 
        \n Please paste your text or path to your PDF file in the left textbox. The summary will then be generated in the right textbox by either pressing the "Summarize" button or pressing CTRL+Enter.
        \n There are five buttons below. The "Summarize" button summarizes the text/PDF file. The "Clear Text/Path" button deletes everything inside the left textbox. The "Paste Text/Path" automatically pastes the text/path to your PDF file into the left textbox. The "Browse Files" button allows you to manually select a PDF file you wish to summarize. Lastly, the "Copy Summary" button copies the summary outputted in the right textbox.
        \n To navigate to a different page, please use the buttons on the left to go to the proper page.
        \n Please make sure that your path is not in quotes before summarizing!''')
    summaryDescription.pack(fill="x",anchor="n")
    summaryDescription.configure(state="disabled")

    summaryTextboxFrame=ctk.CTkFrame(
        master=summaryPage,
        border_width=1,
        border_color="black")
    summaryTextboxFrame.pack(fill="x",padx=10,pady=10)
    
    summaryInputTextbox=ctk.CTkTextbox(
        master=summaryTextboxFrame,
        wrap=tk.WORD,
        font=("Roboto",16))
    summaryInputTextbox.pack(fill="both",expand=True,padx=10,pady=10,side="left",anchor="n")
    
    summaryOutputTextbox=ctk.CTkTextbox(
        master=summaryTextboxFrame,
        wrap=tk.WORD,
        font=("Roboto",16))
    summaryOutputTextbox.pack(fill="both",expand=True,padx=10,pady=10,side="left",anchor="n")
    
    '''summarizes pdf/text for the summary page'''
    def summarizePDForText():
        summaryOutputTextbox.delete("1.0",tk.END) #clears output to make space for the new summary
        text=summaryInputTextbox.get("1.0","end-1c") #end-1c gets the last character of the path 
        summary=summarize(text)
        summaryOutputTextbox.insert(tk.END, summary) #adds the summary in the outputbox

    summaryInputTextbox.bind("<Control-Return>",lambda event: shortcut(event,summarizePDForText()))

    summaryButtonFrame=ctk.CTkFrame(
        master=summaryPage,
        border_width=1,
        border_color="black")
    summaryButtonFrame.pack(fill="x",padx=10,pady=10)
    browseFilesButton=ctk.CTkButton(
        master=summaryButtonFrame,
        text="Browse Files",
        text_color="black",
        font=("Roboto",16),
        fg_color=orange,
        hover_color=orangeHover,
        command=lambda textbox=summaryInputTextbox: browseFiles(textbox))
    browseFilesButton.pack(padx=10,pady=10,side="left",anchor="n")
    summarizeButton=ctk.CTkButton(
        master=summaryButtonFrame,
        text="Summarize",
        text_color="black",
        font=("Roboto",16),
        fg_color=green,
        hover_color=greenHover,
        command=summarizePDForText)  
    summarizeButton.pack(padx=10,pady=10,side="left",anchor="n")
    clearButton=ctk.CTkButton(
        master=summaryButtonFrame,
        text="Clear Text/Path",
        text_color="black",
        font=("Roboto",16),
        fg_color=blue,
        hover_color=blueHover,
        command=lambda textbox=summaryInputTextbox: clear(textbox))
    clearButton.pack(padx=10,pady=10,side="left",anchor="n")
    pasteButton=ctk.CTkButton(
        master=summaryButtonFrame,
        text="Paste Text/Path",
        text_color="black",
        font=("Roboto",16),
        fg_color=purple,
        hover_color=purpleHover,
        command=lambda textbox=summaryInputTextbox: paste(textbox))
    pasteButton.pack(padx=10,pady=10,side="left",anchor="n")
    copyButton=ctk.CTkButton(
        master=summaryButtonFrame,
        text="Copy Summary",
        text_color="black",
        font=("Roboto",16),
        fg_color=darkPink,
        hover_color=darkPinkHover,
        command=lambda textbox=summaryOutputTextbox: copy(textbox))
    copyButton.pack(padx=10,pady=10,side="left",anchor="n")

#create discussion page
def discussionPage():
    deletePage()
    discussionPage=ctk.CTkScrollableFrame(master=mainFrame,fg_color=blue)
    discussionPage.pack(fill="both",expand=True)
    discussionTitle=ctk.CTkLabel(
        master=discussionPage,
        text="Class Discussion",
        corner_radius=0,
        text_color="black",
        font=("Roboto",30))
    discussionTitle.pack(fill="x",pady=10,anchor="n")

    discussionDescriptionFrame=ctk.CTkFrame(
        master=discussionPage,
        border_width=1,
        border_color="black")
    discussionDescriptionFrame.pack(fill="x",padx=10,pady=10)
    discussionDescription=ctk.CTkTextbox(
        master=discussionDescriptionFrame,
        wrap=tk.WORD,
        font=("Roboto",16))
    discussionDescription.insert(
        "1.0",
        '''Welcome! This is where you can generate a class discussion about a PDF's contents. This can include creating questions to making personas to answer those questions. 
        \nFirst, please describe how you want AI to generate a class discussion in the left textbox.
        \nHere is a good example of describing how you want AI to generate a class discussion:
            I’d like you to help me practice teaching a class on K-Pop fanship. I am going to ask you a question. Please create three student personas: Student 1, Student 2, and Student 3. Please pick one of them at random to answer the question. Provide an answer from them. Then, ask two follow-up questions. Make the first an "exploration" question, inviting them to expand on their answer in some way. Provide their answer. Make the second a "challenge" question, pushing back on their responses, perhaps by citing contrary evidence. Provide their answer. Then, pick one of the other students to respond to what they heard from the first student. After that, ask the final student to respond to what they heard from the first student. The question is, how does k-pop fanship affect one's mental state, if at all?
        \nWhen you have finish typing your prompt, click the "Generate Class Discussion Button." You will first be asked to choose the PDF you wished to create a class discussion about. After selecting your PDF, the AI will simulate a class discussion according to how you described and output it in the right textbox.
        \nYou can also generate a list of questions for a discussion. First, write how many questions you would like AI to generate. Then, click on the "Generate Questions" button. You will be asked to choose the PDF you wish to center your questions around. After selecting your PDF, the AI will list out a series of questions you can use in your class discussion, from challenging to follow-up, and output it in the right textbox.
        \nTo navigate to a different page, please use the buttons on the left to go to the proper page.''')
    discussionDescription.pack(fill="x",anchor="n")
    discussionDescription.configure(state="disabled")
    
    textTextboxFrame=ctk.CTkFrame(
        master=discussionPage,
        border_width=1,
        border_color="black")
    textTextboxFrame.pack(fill="x",padx=10,pady=10)
    textTextbox=ctk.CTkTextbox(
        master=textTextboxFrame,
        wrap=tk.WORD,
        font=("Roboto",16))
    textTextbox.pack(fill="x",padx=10,pady=10)
    discussionTextboxFrame=ctk.CTkFrame(
        master=discussionPage,
        border_width=1,
        border_color="black")
    discussionTextboxFrame.pack(fill="x",padx=10,pady=10)
    discussionInputTextbox=ctk.CTkTextbox(
        master=discussionTextboxFrame,
        wrap=tk.WORD,
        font=("Roboto",16))
    discussionInputTextbox.pack(fill="both",expand=True,padx=10,pady=10,side="left",anchor="n")
    discussionOutputTextbox=ctk.CTkTextbox(
        master=discussionTextboxFrame,
        wrap=tk.WORD,
        font=("Roboto",16))
    discussionOutputTextbox.pack(fill="both",expand=True,padx=10,pady=10,side="left",anchor="n")
    
    def generateDiscussion():
        discussionOutputTextbox.delete("1.0",tk.END) #clears output to make space for the new summary
        summary=summarize(textTextbox.get("1.0","end-1c"))
        guidelines=discussionInputTextbox.get("1.0","end-1c")
        prompt=f'''
        Generate a class discussion in a college setting. 
        Create personas and ask a wide variety of questions. Include other features as described in the guidelines. 
        All personas should contribute to the discussion. The personas' answers must be supported by details from the text and their interpretation of the question. 
        Ensure that the discussion does not conclude open-ended. You should close the discussion.

        This is the text: {summary}

        These are the guidelines: {guidelines}
        ''' 
        systemPrompt="You are a college professor hosting a class discussion similar to a Socratic seminar."
        discussionOutputTextbox.insert(tk.END,submitPrompt(prompt,systemPrompt)) #adds the summary in the outputbox
    
    def generateQuestions():
        discussionOutputTextbox.delete("1.0",tk.END) #clears output to make space for the new summary
        summary=summarize(textTextbox.get("1.0","end-1c"))
        guidelines=discussionInputTextbox.get("1.0","end-1c")
        prompt=f'''
        Generate ten questions appropriate for a college class discussion focusing on the text. 
        Include types of questions described in the guidelines. 
        
        This is the text: {summary}

        These are the guidelines: {guidelines}
        ''' 
        systemPrompt="You are a college professor preparing questions for a class discussion."
        discussionOutputTextbox.insert(tk.END,submitPrompt(prompt,systemPrompt)) #adds the summary in the outputbox

    discussionButtonFrame=ctk.CTkFrame(
        master=discussionPage,
        border_width=1,
        border_color="black")
    discussionButtonFrame.pack(fill="x",padx=10,pady=10)
    browseFilesButton=ctk.CTkButton(
        master=discussionButtonFrame,
        text="Browse Files",
        width=len("Browse Files"), 
        text_color="black",
        font=("Roboto",16),
        fg_color=orange,
        hover_color=orangeHover,
        command=lambda textbox=textTextbox: browseFiles(textbox))
    browseFilesButton.pack(padx=10,pady=10,side="left",anchor="n")
    discussionButton=ctk.CTkButton(
        master=discussionButtonFrame,
        text="Generate Discussion",
        text_color="black",
        font=("Roboto",16),
        fg_color=yellow,
        hover_color=yellowHover,
        command=generateDiscussion)  
    discussionButton.pack(padx=10,pady=10,side="left",anchor="n")
    generateQuestionsButton=ctk.CTkButton(
        master=discussionButtonFrame,
        text="Generate Questions",
        text_color="black",
        font=("Roboto",16),
        fg_color=blue,
        hover_color=blueHover,
        command=generateQuestions)  
    generateQuestionsButton.pack(padx=10,pady=10,side="left",anchor="n")
    clearGuidelinesButton=ctk.CTkButton(
        master=discussionButtonFrame,
        text="Clear Guidelines",
        text_color="black",
        font=("Roboto",16),
        fg_color=purple,
        hover_color=purpleHover,
        command=lambda textbox=discussionInputTextbox: clear(textbox))
    clearGuidelinesButton.pack(padx=10,pady=10,side="left",anchor="n")
    clearTextPathButton=ctk.CTkButton(
        master=discussionButtonFrame,
        text="Clear Text/Path",
        text_color="black",
        font=("Roboto",16),
        fg_color=darkPink,
        hover_color=darkPinkHover,
        command=lambda textbox=textTextbox: clear(textbox))
    clearTextPathButton.pack(padx=10,pady=10,side="left",anchor="n")
    copyButton=ctk.CTkButton(
        master=discussionButtonFrame,
        text="Copy Discussion/Questions",
        text_color="black",
        font=("Roboto",16),
        fg_color=lightPink,
        hover_color=lightPinkHover,
        command=lambda textbox=discussionOutputTextbox: copy(textbox))
    copyButton.pack(padx=10,pady=10,side="left",anchor="n")

def chatbotPage():
    deletePage()
    chatbotPage=ctk.CTkScrollableFrame(master=mainFrame,fg_color=blue)
    chatbotPage.pack(fill="both",expand=True)

    chatbotTitle=ctk.CTkLabel(
        master=chatbotPage,
        text="Chatbot Discussion",
        corner_radius=0,
        text_color="black",
        font=("Roboto",30))
    chatbotTitle.pack(fill="x",pady=10,anchor="n")

    chatbotDescriptionFrame=ctk.CTkFrame(
        master=chatbotPage,
        border_width=1,
        border_color="black")
    chatbotDescriptionFrame.pack(fill="x",padx=10,pady=10)

    chatbotDescription=ctk.CTkTextbox(
        master=chatbotDescriptionFrame,
        height=(len('''Welcome! This is where you can create your own AI personas to generate a discussion among them. You are allowed to customize three different personas by checking off their degree level, job level, and area of the business industry. You can also type in other characters you would like for your persona in the "Your Own Prompt" textbox.
        \n After finishing your customizations, click the button on the bottom of the screen to generate a discussion amongst your AI personas. After you click on it, you will be asked to choose a PDF of which your discussion will be based upon. Then, after generating the discussion itself, the program will have a pop-up window with your discussion printed out on the screen for you.'''))//4,
        wrap=tk.WORD,
        font=("Roboto",16))
    chatbotDescription.insert(
        "1.0",
        '''Welcome! This is where you can create your own AI personas to generate a discussion among them. You are allowed to customize three different personas by checking off their degree level, job level, and area of the business industry. You can also type in other characters you would like for your persona in the "Your Own Prompt" textbox.
        \n After finishing your customizations, click the button on the bottom of the screen to generate a discussion amongst your AI personas. After you click on it, you will be asked to choose a PDF of which your discussion will be based upon. Then, after generating the discussion itself, the program will have a pop-up window with your discussion printed out on the screen for you.''')
    chatbotDescription.pack(fill="x",anchor="n")
    chatbotDescription.configure(state="disabled")

    gradeList=["Associates","Undergraduate","Masters","PHD"]
    jobList=["Chief Officer","President/Vice President","Director","Manager"]
    areaList=["Operations","Finance","Marketing","Sales","Analysis","Project Management","Risk Management","E-Commerce"]

    chatbotCustom1Title=ctk.CTkLabel(
        master=chatbotPage,
        text="Customize Chatbot #1",
        corner_radius=0,
        text_color="black",
        font=("Roboto",20))
    chatbotCustom1Title.pack(fill="x",pady=10,anchor="n")
    chatbotCustom1Frame=ctk.CTkFrame(
        master=chatbotPage,
        corner_radius=0,
        border_width=1,
        border_color="black")
    chatbotCustom1Frame.pack(padx=10,pady=10)
    
    grade1=tk.StringVar()
    chatbotCustom1GradeFrame=ctk.CTkFrame(
        master=chatbotCustom1Frame,
        width=200,
        corner_radius=0,
        border_width=1,
        border_color="black",
        fg_color=orange)
    chatbotCustom1GradeFrame.pack(padx=10,pady=10,anchor="n",side="left")
    chatbotGrade1Title=ctk.CTkLabel(
        master=chatbotCustom1GradeFrame,
        text="Grade Level",
        corner_radius=0,
        font=("Roboto",18),
        fg_color=("#BDBDBD","#212121"))
    chatbotGrade1Title.pack(padx=5,pady=5,fill="x")
    for grade in gradeList:
        gradeRadioButton=ctk.CTkRadioButton(
            master=chatbotCustom1GradeFrame,
            text=grade,
            border_color="black",
            fg_color="#7A4B2B",
            hover_color=orangeHover,
            text_color="black",
            font=("Roboto",16),
            variable=grade1,
            value=grade)
        gradeRadioButton.pack(padx=5,pady=5,anchor="w")

    job1=tk.StringVar()
    chatbotCustom1LevelFrame=ctk.CTkFrame(
        master=chatbotCustom1Frame,
        width=200,
        corner_radius=0,
        border_width=1,
        border_color="black",
        fg_color=yellow)
    chatbotCustom1LevelFrame.pack(padx=10,pady=10,anchor="n",side="left")
    chatbotLevel1Title=ctk.CTkLabel(
        master=chatbotCustom1LevelFrame,
        text="Job Level",
        corner_radius=0,
        font=("Roboto",18),
        fg_color=("#BDBDBD","#212121"))
    chatbotLevel1Title.pack(padx=5,pady=5,fill="x")
    for job in jobList:
        jobRadioButton=ctk.CTkRadioButton(
            master=chatbotCustom1LevelFrame,
            text=job,
            border_color="black",
            fg_color="#7E7243",
            hover_color=yellowHover,
            text_color="black",
            font=("Roboto",16),
            variable=job1,
            value=job)
        jobRadioButton.pack(padx=5,pady=5,anchor="w")

    area1=tk.StringVar()
    chatbotCustomArea1Frame=ctk.CTkFrame(
        master=chatbotCustom1Frame,
        width=200,
        corner_radius=0,
        border_width=1,
        border_color="black",
        fg_color=green)
    chatbotCustomArea1Frame.pack(padx=10,pady=10,anchor="n",side="left")
    chatbotArea1Title=ctk.CTkLabel(
        master=chatbotCustomArea1Frame,
        text="Area of Business",
        corner_radius=0,
        font=("Roboto",18),
        fg_color=("#BDBDBD","#212121"))
    chatbotArea1Title.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
    cols=2
    for index,area in enumerate(areaList):
        row=(index//cols)+1
        col=index%cols
        areaRadioButton=ctk.CTkRadioButton(
            master=chatbotCustomArea1Frame,
            text=area,
            border_color="black",
            fg_color="#3F663C",
            hover_color=greenHover,
            text_color="black",
            font=("Roboto",16),
            variable=area1,
            value=area)
        areaRadioButton.grid(row=row,column=col,padx=5, pady=5, sticky="ew")
        
    chatbotCustomUserInput1Frame=ctk.CTkFrame(
        master=chatbotCustom1Frame,
        width=200,
        corner_radius=0,
        border_width=1,
        border_color="black",
        fg_color=purple)
    chatbotCustomUserInput1Frame.pack(padx=10,pady=10,anchor="n",side="left")
    chatbotUserInput1Title=ctk.CTkLabel(
        master=chatbotCustomUserInput1Frame,
        text="Your Own Prompt",
        corner_radius=0,
        font=("Roboto",18),
        fg_color=("#BDBDBD","#212121"))
    chatbotUserInput1Title.pack(padx=5,pady=5,fill="x")
    chatbotUserInput1Textbox=ctk.CTkTextbox(
        master=chatbotCustomUserInput1Frame,
        wrap=tk.WORD,
        font=("Roboto",16))
    chatbotUserInput1Textbox.pack(fill="both",expand=True,padx=10,pady=10,side="left",anchor="n")

    chatbotCustom2Title=ctk.CTkLabel(
        master=chatbotPage,
        text="Customize Chatbot #2",
        corner_radius=0,
        text_color="black",
        font=("Roboto",20))
    chatbotCustom2Title.pack(fill="x",pady=10,anchor="n")
    chatbotCustom2Frame=ctk.CTkFrame(
        master=chatbotPage,
        corner_radius=0,
        border_width=1,
        border_color="black")
    chatbotCustom2Frame.pack(padx=10,pady=10)
    
    grade2=tk.StringVar()
    chatbotCustom2GradeFrame=ctk.CTkFrame(
        master=chatbotCustom2Frame,
        width=200,
        corner_radius=0,
        border_width=1,
        border_color="black",
        fg_color=orange)
    chatbotCustom2GradeFrame.pack(padx=10,pady=10,anchor="n",side="left")
    chatbotGrade2Title=ctk.CTkLabel(
        master=chatbotCustom2GradeFrame,
        text="Grade Level",
        corner_radius=0,
        font=("Roboto",18),
        fg_color=("#BDBDBD","#212121"))
    chatbotGrade2Title.pack(padx=5,pady=5,fill="x")
    for grade in gradeList:
        gradeRadioButton=ctk.CTkRadioButton(
            master=chatbotCustom2GradeFrame,
            text=grade,
            border_color="black",
            fg_color="#7A4B2B",
            hover_color=orangeHover,
            text_color="black",
            font=("Roboto",16),
            variable=grade2,
            value=grade)
        gradeRadioButton.pack(padx=5,pady=5,anchor="w")

    job2=tk.StringVar()
    chatbotCustom2LevelFrame=ctk.CTkFrame(
        master=chatbotCustom2Frame,
        width=200,
        corner_radius=0,
        border_width=1,
        border_color="black",
        fg_color=yellow)
    chatbotCustom2LevelFrame.pack(padx=10,pady=10,anchor="n",side="left")
    chatbotLevel2Title=ctk.CTkLabel(
        master=chatbotCustom2LevelFrame,
        text="Job Level",
        corner_radius=0,
        font=("Roboto",18),
        fg_color=("#BDBDBD","#212121"))
    chatbotLevel2Title.pack(padx=5,pady=5,fill="x")
    for job in jobList:
        jobRadioButton=ctk.CTkRadioButton(
            master=chatbotCustom2LevelFrame,
            text=job,
            border_color="black",
            fg_color="#7E7243",
            hover_color=yellowHover,
            text_color="black",
            font=("Roboto",16),
            variable=job2,
            value=job)
        jobRadioButton.pack(padx=5,pady=5,anchor="w")

    area2=tk.StringVar()
    chatbotCustomArea2Frame=ctk.CTkFrame(
        master=chatbotCustom2Frame,
        width=200,
        corner_radius=0,
        border_width=1,
        border_color="black",
        fg_color=green)
    chatbotCustomArea2Frame.pack(padx=10,pady=10,anchor="n",side="left")
    chatbotArea2Title=ctk.CTkLabel(
        master=chatbotCustomArea2Frame,
        text="Area of Business",
        corner_radius=0,
        font=("Roboto",18),
        fg_color=("#BDBDBD","#212121"))
    chatbotArea2Title.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
    cols=2
    for index,area in enumerate(areaList):
        row=(index//cols)+1
        col=index%cols
        areaRadioButton=ctk.CTkRadioButton(
            master=chatbotCustomArea2Frame,
            text=area,
            border_color="black",            
            fg_color="#3F663C",
            hover_color=greenHover,
            text_color="black",
            font=("Roboto",16),
            variable=area2,
            value=area)
        areaRadioButton.grid(row=row,column=col,padx=5, pady=5, sticky="ew")
    
    chatbotCustomUserInput2Frame=ctk.CTkFrame(
        master=chatbotCustom2Frame,
        width=200,
        corner_radius=0,
        border_width=1,
        border_color="black",
        fg_color=purple)
    chatbotCustomUserInput2Frame.pack(padx=10,pady=10,anchor="n",side="left")
    chatbotUserInput2Title=ctk.CTkLabel(
        master=chatbotCustomUserInput2Frame,
        text="Your Own Prompt",
        corner_radius=0,
        font=("Roboto",18),
        fg_color=("#BDBDBD","#212121"))
    chatbotUserInput2Title.pack(padx=5,pady=5,fill="x")
    chatbotUserInput2Textbox=ctk.CTkTextbox(
        master=chatbotCustomUserInput2Frame,
        wrap=tk.WORD,
        font=("Roboto",16))
    chatbotUserInput2Textbox.pack(fill="both",expand=True,padx=10,pady=10,side="left",anchor="n")

    chatbotCustom3Title=ctk.CTkLabel(
        master=chatbotPage,
        text="Customize Chatbot #3",
        corner_radius=0,
        text_color="black",
        font=("Roboto",20))
    chatbotCustom3Title.pack(fill="x",pady=10,anchor="n")
    chatbotCustom3Frame=ctk.CTkFrame(
        master=chatbotPage,
        corner_radius=0,
        border_width=1,
        border_color="black")
    chatbotCustom3Frame.pack(padx=10,pady=10)
    
    grade3=tk.StringVar()
    chatbotCustom3GradeFrame=ctk.CTkFrame(
        master=chatbotCustom3Frame,
        width=200,
        corner_radius=0,
        border_width=1,
        border_color="black",
        fg_color=orange)
    chatbotCustom3GradeFrame.pack(padx=10,pady=10,anchor="n",side="left")
    chatbotGrade3Title=ctk.CTkLabel(
        master=chatbotCustom3GradeFrame,
        text="Grade Level",
        corner_radius=0,
        font=("Roboto",18),
        fg_color=("#BDBDBD","#212121"))
    chatbotGrade3Title.pack(padx=5,pady=5,fill="x")
    for grade in gradeList:
        gradeRadioButton=ctk.CTkRadioButton(
            master=chatbotCustom3GradeFrame,
            text=grade,
            border_color="black",
            fg_color="#7A4B2B",
            hover_color=orangeHover,
            text_color="black",
            font=("Roboto",16),
            variable=grade3,
            value=grade)
        gradeRadioButton.pack(padx=5,pady=5,anchor="w")

    job3=tk.StringVar()
    chatbotCustom3LevelFrame=ctk.CTkFrame(
        master=chatbotCustom3Frame,
        width=200,
        corner_radius=0,
        border_width=1,
        border_color="black",
        fg_color=yellow)
    chatbotCustom3LevelFrame.pack(padx=10,pady=10,anchor="n",side="left")
    chatbotLevel3Title=ctk.CTkLabel(
        master=chatbotCustom3LevelFrame,
        text="Job Level",
        corner_radius=0,
        font=("Roboto",18),
        fg_color=("#BDBDBD","#212121"))
    chatbotLevel3Title.pack(padx=5,pady=5,fill="x")
    for job in jobList:
        jobRadioButton=ctk.CTkRadioButton(
            master=chatbotCustom3LevelFrame,
            text=job,
            border_color="black",
            fg_color="#7E7243",
            hover_color=yellowHover,
            text_color="black",
            font=("Roboto",16),
            variable=job3,
            value=job)
        jobRadioButton.pack(padx=5,pady=5,anchor="w")

    area3=tk.StringVar()
    chatbotCustomArea3Frame=ctk.CTkFrame(
        master=chatbotCustom3Frame,
        width=200,
        corner_radius=0,
        border_width=1,
        border_color="black",
        fg_color=green)
    chatbotCustomArea3Frame.pack(padx=10,pady=10,anchor="n",side="left")
    chatbotArea3Title=ctk.CTkLabel(
        master=chatbotCustomArea3Frame,
        text="Area of Business",
        corner_radius=0,
        font=("Roboto",18),
        fg_color=("#BDBDBD","#212121"))
    chatbotArea3Title.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
    cols=2
    for index,area in enumerate(areaList):
        row=(index//cols)+1
        col=index%cols
        areaRadioButton=ctk.CTkRadioButton(
            master=chatbotCustomArea3Frame,
            text=area,
            border_color="black",
            fg_color="#3F663C",
            hover_color=greenHover,
            text_color="black",
            font=("Roboto",16),
            variable=area3,
            value=area)
        areaRadioButton.grid(row=row,column=col,padx=5, pady=5, sticky="ew")
    
    chatbotCustomUserInput3Frame=ctk.CTkFrame(
        master=chatbotCustom3Frame,
        width=200,
        corner_radius=0,
        border_width=1,
        border_color="black",
        fg_color=purple)
    chatbotCustomUserInput3Frame.pack(padx=10,pady=10,anchor="n",side="left")
    chatbotUserInput3Title=ctk.CTkLabel(
        master=chatbotCustomUserInput3Frame,
        text="Your Own Prompt",
        corner_radius=0,
        font=("Roboto",18),
        fg_color=("#BDBDBD","#212121"))
    chatbotUserInput3Title.pack(padx=5,pady=5,fill="x")
    chatbotUserInput3Textbox=ctk.CTkTextbox(
        master=chatbotCustomUserInput3Frame,
        wrap=tk.WORD,
        font=("Roboto",16))
    chatbotUserInput3Textbox.pack(fill="both",expand=True,padx=10,pady=10,side="left",anchor="n")    

    textTextboxFrame=ctk.CTkFrame(
        master=chatbotPage,
        border_width=1,
        border_color="black")
    textTextboxFrame.pack(fill="x",padx=10,pady=10)
    textTextbox=ctk.CTkTextbox(
        master=textTextboxFrame,
        wrap=tk.WORD,
        font=("Roboto",16))
    textTextbox.pack(fill="x",padx=10,pady=10)

    def chatbotDiscussionPopup():
        discussionPopup=ctk.CTkToplevel()
        discussionPopup.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
        discussionPopup.title("Generate 6-Question Discussion with Your AI Chatbots")
        discussionPopup.configure(fg_color=blue)
        discussionPopupTitle=ctk.CTkLabel(
            master=discussionPopup,
            text="3-Chatbot Discussion",
            corner_radius=0,
            text_color="black",
            font=("Roboto",30))
        discussionPopupTitle.pack(fill="x",padx=10,pady=10,anchor="n")

        chatbotDiscussionButtonFrame=ctk.CTkFrame(
            master=discussionPopup,
            border_width=1,
            border_color="black")
        chatbotDiscussionButtonFrame.pack(fill="x",padx=10,pady=10)

        discussionPopupOutputFrame=ctk.CTkFrame(
            master=discussionPopup,
            border_width=1,
            border_color="black")
        discussionPopupOutputFrame.pack(fill="both",expand="True",padx=10,pady=10)

        summary=summarize(textTextbox.get("1.0","end-1c"))

        def chatbotDiscussion(question):
            chatbot1="Their highest level of education is "+grade1.get()+". Their job level is "+job1.get()+". They work in "+area1.get()+". Here are some additional details about them: "+chatbotUserInput1Textbox.get("1.0","end-1c")
            chatbot2="Their highest level of education is "+grade2.get()+". Their job level is "+job2.get()+". They work in "+area2.get()+". Here are some additional details about them: "+chatbotUserInput2Textbox.get("1.0","end-1c")
            chatbot3="Their highest level of education is "+grade3.get()+". Their job level is "+job3.get()+". They work in "+area3.get()+". Here are some additional details about them: "+chatbotUserInput3Textbox.get("1.0","end-1c")
            if question=="": 
                prompt=f'''
                Clearly ask 6 separate questions about the reading.
                After each persona answers the current question, ask the next question.
                Repeat this process until you have asked 6 questions.

                The personas will answer questions together and discuss it among themselves. The personas should behave as if they are all in the same discussion and address each other by name. Personas should speak in first person. 
                Support the personas' answers with details from the reading and their experience according to their background.
                Limit personas' answers to be less than five sentences for every question throughout the entire discussion.
                Ensure that the discussion does not conclude open-ended. 

                These are the descriptions of the three personas:\nPersona 1: {chatbot1}.\nPersona 2: {chatbot2}.\nPersona 3: {chatbot3}.
                
                This is the reading: {summary}

                The format will be as follows:
                Question (Number):

                Persona 1 Answer:

                Persona 2 Answer:
                
                Persona 3 Answer:
                '''
                systemPrompt=f"You are to host an engaging discussion between three personas by asking questions and allowing the personas to discuss it among themselves."
            else: 
                prompt=f'''
                Generate a discussion between three personas in response to the question. 
                The personas will answer questions together and discuss it among themselves. The personas should behave as if they are all in the same discussion and address each other by name. Personas should speak in first person.
                Support the personas' answers with details from the reading and their experience according to their background. Encourage the personas to ask each other follow-up questions and answer them.
                Maintain personas' answers to be at least four sentences. Ensure that the discussion does not conclude open-ended. 
            
                These are the descriptions of the three personas:\nPersona 1: {chatbot1}.\nPersona 2: {chatbot2}.\nPersona 3: {chatbot3}.
                
                This is the reading: {summary}

                This is the question: {question}

                The format will be as follows:
                {question}:

                Persona 1 Answer:

                Persona 2 Answer:
                
                Persona 3 Answer:                
                '''
                systemPrompt = f"You are to host an engaging discussion between three personas by allowing the personas to discuss the question among themselves."
            return submitPrompt(prompt,systemPrompt) #adds the summary in the outputbox

        def sixQuestionDiscussion(): 
            for child in discussionPopupOutputFrame.winfo_children(): child.destroy()
            discussionPopupOutputTextbox=ctk.CTkTextbox(
                master=discussionPopupOutputFrame,
                wrap=tk.WORD,
                font=("Roboto",16))
            discussionPopupOutputTextbox.pack(fill="both",expand=True,padx=10,pady=10)
            discussionPopupOutputTextbox.delete("1.0",tk.END)
            discussionPopupOutputTextbox.insert(tk.END,chatbotDiscussion(""))
            discussionPopupOutputTextbox.configure(state="disabled")

            copyChatbotDiscussionButton=ctk.CTkButton(
                master=chatbotDiscussionButtonFrame,
                text="Copy Discussion",
                command=lambda textbox=discussionPopupOutputTextbox: copy(textbox),
                border_width=1,
                border_color="black",
                fg_color=green,
                hover_color=greenHover,
                text_color="black",
                font=("Roboto",16),
                hover=True)
            copyChatbotDiscussionButton.pack(padx=10,pady=10,side="left",anchor="n")

        def generateTenQuestionDiscussion(question):
            tenQuestionDiscussionPopup=ctk.CTkToplevel()
            tenQuestionDiscussionPopup.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
            tenQuestionDiscussionPopup.title("Generate Chat with Your AI Chatbots")
            tenQuestionDiscussionPopup.configure(fg_color=blue)
            tenQuestionDiscussionPopupTitle=ctk.CTkLabel(
                master=tenQuestionDiscussionPopup,
                text="3-Chatbot Discussion",
                corner_radius=0,
                text_color="black",
                font=("Roboto",30))
            tenQuestionDiscussionPopupTitle.pack(fill="x",padx=10,pady=10,anchor="n")

            tenQuestionDiscussionButtonFrame=ctk.CTkFrame(
                master=tenQuestionDiscussionPopup,
                border_width=1,
                border_color="black")
            tenQuestionDiscussionButtonFrame.pack(fill="x",padx=10,pady=10)
            
            tenQuestionPopupOutputFrame=ctk.CTkFrame(
                master=tenQuestionDiscussionPopup,
                border_width=1,
                border_color="black")
            tenQuestionPopupOutputFrame.pack(fill="both",expand="True",padx=10,pady=10)
            tenQuestionPopupOutputTextbox=ctk.CTkTextbox(
                master=tenQuestionPopupOutputFrame,
                wrap=tk.WORD,
                font=("Roboto",16))
            tenQuestionPopupOutputTextbox.pack(fill="both",expand=True,padx=10,pady=10)
            tenQuestionPopupOutputTextbox.insert(tk.END,chatbotDiscussion(question))
            tenQuestionPopupOutputTextbox.configure(state="disabled")

            copyChatbotDiscussionButton=ctk.CTkButton(
                master=tenQuestionDiscussionButtonFrame,
                text="Copy Discussion",
                command=lambda textbox=tenQuestionPopupOutputTextbox: copy(textbox),
                border_width=1,
                border_color="black",
                fg_color=yellow,
                hover_color=yellowHover,
                text_color="black",
                font=("Roboto",16),
                hover=True)
            copyChatbotDiscussionButton.pack(padx=10,pady=10,side="left",anchor="n")
            
        def generateTenQuestions():
            button=0
            for child in chatbotDiscussionButtonFrame.winfo_children():
                if isinstance(child, ctk.CTkButton): 
                    button+=1
                    if button>2: child.destroy()
            for child in discussionPopupOutputFrame.winfo_children(): child.destroy()
            prompt=f'''
            Generate 10 questions based on the reading. 
            Include thought-provoking, challenging, and followup questions.  
            Separate each question by newlines. Indicate what number question it is. 

            This is the reading: {summary}

            This is the format: 
            Question (Number): Question
            '''
            systemPrompt=f"You create questions appropriate for professional discussions."
            questions=submitPrompt(prompt,systemPrompt) #adds the summary in the outputbox 
            questionsList=questions.splitlines()
            for question in questionsList: 
                if question=="": questionsList.remove("")
            for question in questionsList:
                questionButton=ctk.CTkButton(
                    master=discussionPopupOutputFrame,
                    text=question,
                    border_color="black",
                    fg_color=orange,
                    hover_color=orangeHover,
                    text_color="black",
                    font=("Roboto",14),
                    command=lambda question=question: generateTenQuestionDiscussion(question))
                questionButton._text_label.configure(wraplength=discussionPopupOutputFrame.winfo_width()-30)
                questionButton.pack(padx=5,pady=5,anchor="w")

        generateChatbotDiscussionButton=ctk.CTkButton(
            master=chatbotDiscussionButtonFrame,
            text="Generate 6-Question Discussion with Your AI Chatbots",
            command=sixQuestionDiscussion,
            border_width=1,
            border_color="black",
            fg_color=orange,
            hover_color=orangeHover,
            text_color="black",
            font=("Roboto",16),
            hover=True)
        generateChatbotDiscussionButton.pack(padx=10,pady=10,side="left",anchor="n")
        generateChatbotQuestionsButton=ctk.CTkButton(
            master=chatbotDiscussionButtonFrame,
            text="Generate and Select 10 Questions Your AI Chatbots",
            command=generateTenQuestions,
            border_width=1,
            border_color="black",
            fg_color=yellow,
            hover_color=yellowHover,
            text_color="black",
            font=("Roboto",16),
            hover=True)
        generateChatbotQuestionsButton.pack(padx=10,pady=10,side="left",anchor="n")

        textTextbox.bind("<Control-Return>",lambda event: shortcut(event,chatbotDiscussionPopup()))

    chatbotButtonFrame=ctk.CTkFrame(
        master=chatbotPage,
        border_width=1,
        border_color="black")
    chatbotButtonFrame.pack(fill="x",padx=10,pady=10)
    browseFilesButton=ctk.CTkButton(
        master=chatbotButtonFrame,
        text="Browse Files",
        command=lambda textbox=textTextbox: browseFiles(textbox),
        border_width=1,
        border_color="black",
        fg_color=orange,
        hover_color=orangeHover,
        text_color="black",
        font=("Roboto",16),
        hover=True)
    browseFilesButton.pack(padx=10,pady=10,side="left",anchor="n")
    generateChatbotDiscussionButton=ctk.CTkButton(
        master=chatbotButtonFrame,
        text="Generate Discussions and Select Questions with Your AI Chatbots",
        command=chatbotDiscussionPopup,
        border_width=1,
        border_color="black",
        fg_color=yellow,
        hover_color=yellowHover,
        text_color="black",
        font=("Roboto",16),
        hover=True)
    generateChatbotDiscussionButton.pack(padx=10,pady=10,side="left",anchor="n")

#create options menu 
sideMenuFrame=ctk.CTkFrame(
    master=window,
    width=200,
    corner_radius=0,
    border_width=1,
    border_color="black")
sideMenuFrame.grid(row=0,column=0,sticky="ns")
sideMenuFrame.pack_propagate(False)
#create buttons for options menu 
homeButton=ctk.CTkButton(
    master=sideMenuFrame,
    text="Home",
    command=homePage,
    width=200, 
    corner_radius=0,
    border_width=1,
    fg_color=orange,
    border_color="black",
    hover_color="#F9CBAA",
    text_color="black",
    font=("Roboto",16),
    hover=True)
homeButton.pack()
summaryButton=ctk.CTkButton(
    master=sideMenuFrame,
    text="PDF/Text Summarizer",
    command=summaryPage,
    width=200,
    corner_radius=0,
    border_width=1,
    fg_color=yellow,
    border_color="black",
    hover_color="#FEF1C2",
    text_color="black",
    font=("Roboto",16),
    hover=True)
summaryButton.pack()
discussionButton=ctk.CTkButton(
    master=sideMenuFrame,
    text="Class Discussion",
    command=discussionPage,
    width=200,
    corner_radius=0,
    border_width=1,
    fg_color=green,
    border_color="black",
    hover_color=greenHover,
    text_color="black",
    font=("Roboto",16),
    hover=True)
discussionButton.pack()
chatbotButton=ctk.CTkButton(
    master=sideMenuFrame,
    text="Chatbot Discussion",
    command=chatbotPage,
    width=200, 
    corner_radius=0,
    border_width=1,
    fg_color=blue,
    border_color="black",
    hover_color=blueHover,
    text_color="black",
    font=("Roboto",16),
    hover=True)
chatbotButton.pack()

#create main frame 
mainFrame=ctk.CTkFrame(
    master=window,
    corner_radius=0,
    border_width=1,
    border_color="black")
mainFrame.grid(row=0,column=1,sticky="nsew")

#make home page the first one
homePage()

#runs the window
window.mainloop()