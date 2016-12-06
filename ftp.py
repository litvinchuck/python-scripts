'''
A minimalistic FTP util. A shell client for Python ftplib

getwelcome - Return the welcome message sent by the server in reply to the initial connection. (This message sometimes contains disclaimers or help information that may be relevant to the user.)
connect [host=''] [port=0] [timeout=None] - Connect to the given host and port. The default port number is 21, as specified by the FTP protocol specification. It is rarely needed to specify a different port number. This function should be called only once for each instance; it should not be called at all if a host was given when the instance was created. All other methods can only be used after a connection has been made. The optional timeout parameter specifies a timeout in seconds for the connection attempt. If no timeout is passed, the global default timeout setting will be used.
login [user='anonymous'] [passwd=''] [acct=''] - Log in as the given user. The passwd and acct parameters are optional and default to the empty string. If no user is specified, it defaults to 'anonymous'. If user is 'anonymous', the default passwd is 'anonymous@'. This function should be called only once for each instance, after a connection has been established; it should not be called at all if a host and user were given when the instance was created. Most FTP commands are only allowed after the client has logged in. The acct parameter supplies “accounting information”; few systems implement this.
set_debuglevel [level] - Set the instance’s debugging level. This controls the amount of debugging output printed. The default, 0, produces no debugging output. A value of 1 produces a moderate amount of debugging output, generally a single line per request. A value of 2 or higher produces the maximum amount of debugging output, logging each line sent and received on the control connection.
nlst [directory] - Return a list of file names as returned by the NLST command. The optional argument is a directory to list (default is the current server directory). Multiple arguments can be used to pass non-standard options to the NLST command.
dir [directory] - Produce a directory listing as returned by the LIST command, printing it to standard output. The optional argument is a directory to list (default is the current server directory).
cwd [pathname] - Set the current directory on the server.
mkd [pathname] - Create a new directory on the server.
pwd - Return the pathname of the current directory on the server.
rmd [dirname] - Remove the directory named dirname on the server.
size [filename] - Request the size of the file named filename on the server. On success, the size of the file is returned as an integer, otherwise None is returned. Note that the SIZE command is not standardized, but is supported by many common server implementations.
rename [fromname] [toname] - Rename file fromname on the server to toname.
delete [filename] - Remove the file named filename from the server. If successful, returns the text of the response.
quit - Send a QUIT command to the server and close the connection.
exit - Send a QUIT command to the server and close the connection. Same as quit.
close - Send a QUIT command to the server and close the connection. Same as quit.
help - display help

'''

from ftplib import FTP, error_perm, all_errors
from getpass import getpass
import sys, readline

print("FTP util\n")

host = input("Enter FTP hostname: ").replace('http://', '').replace('ftp://', '')
user = input("Enter username: ")
password = getpass("Enter password: ")

try:
    ftp = FTP(host)
except all_errors as error:
    print(error)
    input()
    sys.exit()
else:
    print(ftp.getwelcome())

try:
    print(ftp.login(user, password))
except error_perm as error:
    print(error)
    input()
    sys.exit()

readline.set_startup_hook()  # Enables input history

while True:
    command = input(">> ").split(" ")
    if command[0] in ('exit', 'quit', 'close'):
        print(ftp.quit())
        sys.exit()
    elif command[0] == 'help':
        print(__doc__)
    elif len(command[0]) == 0:
        continue
    else:
        try:
            func = getattr(ftp, command[0])
            command[1:] = list(map(lambda argument: int(argument) if argument.isdigit() else argument, command[1:]))
            result = func(*command[1:])
            if result:
                print(result)
        except all_errors as error:
            print(error)
        except TypeError as error:
            print('Invalid ammount of arguments')
        except AttributeError:
            print('Unknown command')
