# linkedin-jira-xml-job-wrapper
The way we wrap jobs at <a href="https://exceptionly.com">Exceptionly</a>. Exceptiony uses Jira for operational purposes, so all of our active jobs live on Jira. We automatically wrap our linkedin job slots using this project.

This approach saved a lot of time for our talent acquisition team. Hope it does the same if you go ahead and make a crazy decision of running operations HR operations over Jira.

## Dependencies:
pip install jira  --> <a href="https://jira.readthedocs.io/">Python Jira</a>
pip install lxml  --> <a href="https://lxml.de/installation.html">lxml</a>
### Built-in moduless:
csv               --> <a href="https://docs.python.org/3/library/csv.html">csv</a>
collections       --> <a href="https://docs.python.org/3/library/collections.html">collections</a>
ftplib            --> <a href="https://docs.python.org/3/library/ftplib.html">ftplib</a>
os                --> <a href="https://docs.python.org/3/library/os.html">os</a>
