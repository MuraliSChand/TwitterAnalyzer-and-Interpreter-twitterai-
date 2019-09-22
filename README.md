# TwitterAnalyzer-and-Interpreter-twitterai-
This one will allow you to analyze your own timeline tweets and trends if you want with location showing system in real time.

Hi there,
This repository contains three files(modules) of python.

1.twitter

This one contains Twitter class which will enable you to start your streaming.
NOTE :- You need to pass your tokens to it

To start streaming call Twitter().start(track=list of words or hash tags)

You can stop it by calling Twitter().stop()
All data will be stored and processed each time so you need to specify the filename.

2.practice

You don't see this one in your usage very often. This module is just runs in background while we analyzing the data
It contains the Practice class which takes three params
(file #the file in which your data contained ,add_retweets = False , add_handles = True #includes or excludes hashtags and twitter handles from the data)

NOTE :- To visualize the locations of tweets you need to use this class directly.Practice(args).show_location()

3.analyzer

This one will let you analyze the data by calling prcatice.Prcatice() and accessing it's methods everytime. Then this module will visualize things in a proper manner.

analyzer.Analyze(file), send filename of your tweets created in twitter module. 

contains:-

main function with name show_viz(words=[]), words will be analyzed for sentiment and others.
NOTE :- send words to this function those you want to analyze.

show_viz uses these three functions in background.

wrapper :- analyze() :- will analyze tweet rate (per one minute) on each word and visualize them
wrapper :- sent_analyze(words) :- will analyze sentiments of all words and will plot them.
wrapper :- top_words() :- this will show you the top 10 words of all tweets


