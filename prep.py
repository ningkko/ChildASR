import pandas as pd

df = pd.read_excel("TalkBankDB_transcripts.xls")

def web(x):
    xs = x.split("/")
    newx = xs[1:3]
    return "https://childes.talkbank.org/data/"+"/".join(newx)+".zip"

df["website"] = df["path"].apply(lambda x: web(x))
websites = df["website"].unique()

with open("websites.txt","w") as file:
	file.write("\n".join(websites))
