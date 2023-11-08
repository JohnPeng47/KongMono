import requests
import bs4
import json
import re

def print_keys(k, levels=0):
    for key in k.keys():
        print("--->" * levels, key)
        if isinstance(k[key], dict):
            print_keys(k[key], levels=levels+1)

def clean_transcript(transcript):
    stripped_transcript = re.sub(r'\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}\.\d{3}', '', transcript)
    stripped_transcript = re.sub(r'\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', '', stripped_transcript)
    return stripped_transcript.replace("01: ", "")

def scrape_transcript_summaries(post_id):
    res = requests.get('https://www.hubermantranscripts.com/post/' + post_id)
    html = bs4.BeautifulSoup(res.text, 'html.parser')
    raw = html.find('script', id='__NEXT_DATA__', type='application/json')
    transcript = json.loads(raw.text)

    ## Summaries
    summaries_res = []
    summaries = transcript["props"]["pageProps"]["summary"]
    for i in range(len(summaries.keys())):
        summaries_res.append(summaries[str(i)]["summary"])

    ## Transcripts
    transcripts_res = ""
    transcripts = transcript["props"]["pageProps"]["transcript"]
    for i in range(len(transcripts.keys())):
        transcripts_res += clean_transcript(transcripts[str(i)])
        
    return summaries_res, transcripts_res

post_id = "0093_uxZFl4BDOGk"
scrape_transcript_summaries(post_id)