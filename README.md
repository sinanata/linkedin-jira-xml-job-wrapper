# Linkedin & Jira XML Job Wrapper by <a href="https://exceptionly.com">Exceptionly</a>
The way we wrap jobs at <a href="https://exceptionly.com">Exceptionly</a>. Exceptiony uses <a href="https://www.atlassian.com/software/jira">Jira</a> for operational purposes, so all of our active jobs live on Jira. We automatically wrap our <a href="https://linkedin.com">linkedin</a> job slots using this project. This project is built in alignment with <a href="https://docs.microsoft.com/en-us/linkedin/talent/job-postings/xml-feeds-development-guide">XML Feeds Development Guide</a> by MSFT

This approach saved a lot of time for our talent acquisition team. Hope it does the same if you go ahead and make a crazy decision of running operations HR operations over Jira.

## Python file checks:
As you may know, Job Slots over Linkedin are city sensitive, so your XML output should include all job/city variations separately.
<a href="https://github.com/sinanata/linkedin-jira-xml-job-wrapper/blob/main/us-states.csv"><strong>us-states.csv</strong></a> file is necessary for inserting proper city/state information if you are publishing jobs for the US.

## Python file generates:
Once you automatically upload this to your host, Linkedin crawlers come and consume this file for generating your jobs lots.
<a href="https://github.com/sinanata/linkedin-jira-xml-job-wrapper/blob/main/exceptionlyjds.xml"><strong>exceptionlyjds.xml</strong></a>

## Python file external dependencies:
pip install jira  --> <a href="https://jira.readthedocs.io/">Python Jira</a><br/>
pip install lxml  --> <a href="https://lxml.de/installation.html">Python lxml</a><br/>

### Python file built-in module dependencies:
<a href="https://docs.python.org/3/library/csv.html">csv</a><br/>
<a href="https://docs.python.org/3/library/collections.html">collections</a><br/>
<a href="https://docs.python.org/3/library/ftplib.html">ftplib</a><br/>
<a href="https://docs.python.org/3/library/os.html">os</a><br/>

## Python file end-result live on Linkedin:
<img width="798" alt="sample-job-post-by-exceptionly" src="https://user-images.githubusercontent.com/2798897/167887136-53b4095f-c038-4361-929f-62e72bdc5175.png">

