##Ticket viewer by Yitao HE for coding challenge, email:yitaohe2@illinois.edu
##created at Nov 26, 2021

Thanks for using Ticket Viewer!
Ticket Viewer is used for retrieving&displaying up to 100 tickets when connected to zendesk API

To start:
1. Please have python3 and pip installed
   https://www.python.org/downloads/
   https://pip.pypa.io/en/stable/installation/
2. Install python library by running file "pipInstall" in the folder,
   or using command(Some pip version requires using pip3 instead of pip):
   pip install prettytable
3. Generate a zendesk OAuth API token, you may refer to following website for details:
   https://developer.zendesk.com/documentation/ticketing/working-with-oauth/creating-and-using-oauth-tokens-with-the-api/#create-an-oauth-client
4. Edit file "configure" in the folder to establish connection,
   replace first line with your zendesk subdomain
   replace second line with OAuth token
5. You are all set! Now you can run ticketViewer with command:
   ./ticketViewer
   or(Some python version requires using python3 instead of python):
   python ticketViewer.py
