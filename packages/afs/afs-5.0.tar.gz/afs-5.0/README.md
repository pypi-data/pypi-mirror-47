# AFS

[![N|Solid](https://alpes.cloud/up/04f421c9980ab436d97dd6a910bcaf49.svg)](https://www.systemcorp.ai)



[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)]()

AFS is a Python based library, that helps Deep / Machine Learning specialists to track their models during
training without accessing server, and getting notifications full of their desired information via beloved
Social Media platforms.

[![N|Solid](https://alpes.cloud/up/32bddf91ffdf1fc2a66614f8a2fbbdaa.png)](https://www.systemcorp.ai)




# PROS
  - Built as lightweight as possible
  - Takes 14 arguments, therefore users can check almost everything while their model is training
  - Back-End is built on Flask framework, and open-sourced. You can contribute to implement more
  Social Media platforms' APIs.

# TODO

  - Finish working on Back-End for Facebook Messenger.

### Used Frameworks & Libraries

AFS is built totally on Python & Node.JS.

* [Python 3] - for library building
* [Node.JS] - for Back-End


### Installation

Python 3.6+ required to use.

Get the package from [PyPi]

```sh
$ pip install AFS
```



### Usage

Import the AFS and reach 'teller' function.
Define the AFS.teller function inside the training loop, and pass the arguments.

```sh
$ import AFS as afs
$ afs.teller(arg1, arg2)
```

Then, reach uID function, and pass the 'yes' string, that will basically create unique id for you, by which you'll then verify your session with the chatbot.

```sh
$ afs.uID("yes")
```
After the execution of the training loop, this line will print unique ID for you that is generated super randomly to minimize the similarities.

It'll look like this: 

```sh
$ Your unique ID is ---  231409296064663:68137457840134:27374860406350
```
Copy the unique ID, and text the AFS bot the plain text to verify your session.
And, it's all done.


# Arguments

```sh

'teller' function takes maximum of 14 arguments. Default values are 0s.

$iteration argument is for counting iterations. type = number.

$distribution argument is basically a divider, for every how many iterations do you need to send the GET request. type = number.

$maxiter is a maximum of iterations, after which the model finishes training. type = number.

$epochdistribution is the same as 'distribution' argument, but for epochs. type = number.

$epoch counts epochs. type = number.

$testloss takes test loss as an information. type = number.

$valloss takes validation loss as an information. type = number.


```


# JSON Instance

The API sends the JSON array, that is basically stringified version of combination of dictionaries.


# Implementations

  The Flask server is deployed on Heroku, and implemented only in Facebook Messenger for now.
  Next Social Media Platforms:

  - [Slack]
  - [Discord]




License
----

BSD 3-Clause Licence




[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>
   [OpenCV]: <https://opencv.org>
   [Single Shot Detection (SSD)]: <https://arxiv.org/pdf/1512.02325.pdf>
   [ResNet50]: <https://arxiv.org/pdf/1512.03385.pdf>
   [Python 3]: <https://python.org>
   [Flask]: <http://flask.pocoo.org>
   [PyPi]: <https://pypi.org>
   [Slack]: <https://slack.com>
   [Discord]: <https://discordapp.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
