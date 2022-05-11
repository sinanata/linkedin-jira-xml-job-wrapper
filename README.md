# linkedin-jira-xml-job-wrapper
The way we wrap jobs at <a href="https://exceptionly.com">Exceptionly</a>. Exceptiony uses <a href="https://www.atlassian.com/software/jira">Jira</a> for operational purposes, so all of our active jobs live on Jira. We automatically wrap our <a href="https://linkedin.com">linkedin</a> job slots using this project.

This approach saved a lot of time for our talent acquisition team. Hope it does the same if you go ahead and make a crazy decision of running operations HR operations over Jira.

## Checks:
As you may know, Job Slots over Linkedin are city sensitive, so your XML output should include all job/city variations separately.


## Generates:

## Dependencies:
pip install jira  --> <a href="https://jira.readthedocs.io/">Python Jira</a>
pip install lxml  --> <a href="https://lxml.de/installation.html">lxml</a>

### Built-in moduless:
csv               --> <a href="https://docs.python.org/3/library/csv.html">csv</a><br/>
collections       --> <a href="https://docs.python.org/3/library/collections.html">collections</a><br/>
ftplib            --> <a href="https://docs.python.org/3/library/ftplib.html">ftplib</a><br/>
os                --> <a href="https://docs.python.org/3/library/os.html">os</a><br/>
