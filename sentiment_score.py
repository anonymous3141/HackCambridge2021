import openai
import random
from googlesearch import search

def evaluate_sentiment(entry):
    openai.api_key = "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"
    base = """
    Sentiment classification:\n
    Climate change: Proposal to spend 25% of EU budget on climate change: positive\n
    Climate change: July 'marginally' warmest month on record: negative\n
    Climate change: More than 3bn could live in extreme heat: negative\n
    Climate change: UK to speed up target to cut carbon emissions: positive\n
    """
    dat = "Climate change: "+ " ".join(entry)+": "
    response = openai.Completion.create(
      engine="text-davinci-001",
      prompt=base+dat,
      temperature=0,
      max_tokens=20,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    output = response['choices'][0]["text"]

    if "positive" in output:
        # positive sentiment
        return 1
    elif "negative" in output:
        # negative sentiment
        return -1
    else:
        # neutral
        return 0

def clean_reuters_url(url):
    # take url and output heading
    # e.g https://www.reuters.com/world/americas/something-has-changed-young-female-led-cabinet-reflects-chiles-modern-twist-2022-01-21/
    title_and_date = url.split('/')[-2]
    words = title_and_date.split('-')[:-3] # remove yy, mm, dd

    return " ".join(words)

def sample():
    NUM_LINKS = 30
    titles = []
    SEARCH_PROMPT = "reuters climate news"
    for url in search(SEARCH_PROMPT, tld="co.uk", num=NUM_LINKS, stop=NUM_LINKS, pause=2, extra_params={'tbm':'nws'}):
        # search google news
        titles.append(clean_reuters_url(url))
    return titles

def unit_test_evaluator():
    # outputs 1, -1
    print(evaluate_sentiment("IMF Outlines $50 Billion Climate and Resilience Lending Plan"))
    print(evaluate_sentiment("EU Faces Major Pushback Over Plan to Call Gas, Nuclear"))

def unit_test_scrape():
    print(sample())
    #print(clean_reuters_url("https://www.reuters.com/world/americas/something-has-changed-young-female-led-cabinet-reflects-chiles-modern-twist-2022-01-21/"))

def get_sentiment_score(debug=False):
    sum_score = 0
    news_list = sample()
    for news in news_list:
        res = evaluate_sentiment(news)
        sum_score += res
        if debug: print(news, res)
    if debug: print(sum_score)
    return sum_score
