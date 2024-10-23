import ollama as lama

def script_given_checker(Text):
    prand =""
    script_gen=0
    pass_filter=0
    for i in Text:
        for j in i :
            if j==" ":
                if pass_filter==0:
                    if prand=="generate":
                
                        script_gen=1
                        pass_filter+=1
                    else:
                        script_gen=0        
                    pass_filter+=1
                else:
                    break
            else:
                prand+=str(j)
    return script_gen
def generate_script(context):
    try:
        response=lama.chat("llama3.2", 
                           messages=context,
                           keep_alive=-1)
        return response
    except Exception as error_ollama:
        return error_ollama
