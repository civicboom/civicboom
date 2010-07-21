#--------------------------------------------------
# Timed Task Executor
#--------------------------------------------------
#
# The web server has a controller called task
# These action are locked down to only accept requests from localhost
# These actions are used to perform maintinence and timed actions
#
# This script takes a port "-p 5000" if the server is not on 80
# if no arguments are described then it will execute all tasks in the tasks list
# other wise it will execute the task
#
# This program is designed to be run by a cron tasks
#
# Examples of use
#
#  python script.py -p 5000 mooose_badger_maintain monkeys
#    - will execute
#       http://localhost:5000/tasks/mooose_badger_maintain
#       http://localhost:5000/tasks/monkeys
#
# python script.py
#    - will execute (based on default task array)
#       http://localhost:5000/tasks/(task1)
#       http://localhost:5000/tasks/(task2)
#       http://localhost:5000/tasks/(task3)
#       http://localhost:5000/tasks/(..etc)
#
#--------------------------------------------------
# Example of setting up a cron job
# crontab -e
#
# or just use Anacron folders /etc/cron.daily/
#
# Add to the contab file the following to trigger the script at 3am every day
# one line is an example of a local test script, the other is a production enviroment
#
# # m  h   dom mon dow   command
#   0  03  *   *   *     python ~/indiconews/svn/indiconews/indicofb/tasks.py -p 5000
#   0  03  *   *   *     python /data/website/tasks.py
#
#--------------------------------------------------
#
# Example of Importing for single use for one off tasks
#  load up the python shell in the indicofb folder
#
#  import tasks
#  tasks.server_address = 'http://localhost:5000/task/' #if you are running a local dev port, on live server this is not needed because the default is ok
#  tasks.option_verbose = True
#  tasks.do_task("all_follow_civicboom")
#

from optparse import OptionParser
import urllib2
import datetime
import sys


response_completed_ok = "task:ok"


parser = OptionParser()
parser.add_option("-p", "--port",    action="store",      type="int"  ,  dest="server_port", help="the port the server is currently running on")
parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose"    , help="prinout task response even if successful")


line_break = "-----------------------------------------"
server_address = 'http://localhost/task/'
option_verbose = False

def main():
    # Defaults
    tasks = ["expire_syndication_articles","remove_ghost_reporters","assignment_near_expire","message_clean"]

    # Parse Command Line Options
    (options, args) = parser.parse_args()

    # Setup Server URL
    global server_address
    server_port = ""
    if options.server_port: server_port = ':%s' % options.server_port
    server_address = 'http://localhost%s/task/' % server_port

    global option_verbose
    option_verbose = options.verbose

    # Create task list from arguments if exisit
    if len(args) >= 1:
        tasks = args

    # Run tasks
    print "Running indicofb timed tasks @ %s" % datetime.datetime.now()
    for task in tasks:
        do_task(task)

# Execute Individual Task - Printing details and timing
def do_task(task):
    time_start = datetime.datetime.now()
    url        = server_address + task
    print "%s:" % url,
    sys.stdout.flush()
    print "%s" % execute_task(url),
    time_duration = datetime.datetime.now() - time_start
    print "(%s sec)" % time_duration.seconds

# Execute Individual Task - safely - returning true if contains successful response - else print response and false
def execute_task(url):
    response_ok = False
    try:
        response_text = str(urllib2.urlopen(url).read())
        if response_text.find(response_completed_ok) >= 0: response_ok = True
        if option_verbose or (not option_verbose and response_text):
            print ""
            print line_break
            print response_text
            print line_break
    except: pass
    return response_ok

# Main
if __name__ == "__main__": main()
