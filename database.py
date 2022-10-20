import sqlserver
import pwdverification as pwd
import regex as re
try:
    db = sqlserver.adgsqlserver(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=OpenCommerce;Trusted_Connection=yes;')
except Exception as e:
    print('error failed to do task ... more info on error:', e)

def tableexists(tblname)
    return db.ExecuteQuery("SELECT * FROM " + tblname)

def CreateUsersTable():
    if not tableexists('tblUsers'):
        query = '''
        CREATE TABLE [dbo].[tblUsers](
        [UserID] [int] IDENTITY(1,1) NOT NULL,
        [UserName] [varchar](300) NOT NULL,
        [UserPassword] [varchar](300) NOT NULL,
        [UserEmail] [varchar](300) NOT NULL,
        [UserRole] [varchar](300) NOT NULL,
        [UserStatus] [varchar](300) NOT NULL,
        [UserCreatedDate] [varchar](300) NOT NULL,
        [UserLastLoginDate] [varchar](300) NOT NULL,
        [UserLastLoginIP] [varchar](300) NOT NULL,
        [UserLastLoginBrowser] [varchar](300) NOT NULL,
        [UserLastLoginOS] [varchar](300) NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
            [UserID] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]        
        '''
        db.ExecuteQuery(query)
        print('tblUsers created')
    else:
        print('tblUsers already exists')


CreateUsersTable()


def CheckIfUserExists(username):
    query = "SELECT * FROM tblUsers WHERE UserName = '" + username + "'"
    usernames = db.GetRecordsOfColumn(query, 'UserName')
    if len(usernames) > 0:
        return True
    else:
        return False


def AddUser(username, password, email, role, status, createddate, lastlogindate, lastloginip, lastloginbrowser, lastloginos):
    password = pwd.hash_password(password)
    # convert bytes to string
    password = password.decode('utf-8')
    # verify if email is valid with regex
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return {'status': 'error', 'message': 'Email is not valid'}

    query = "INSERT INTO tblUsers (UserName, UserPassword, UserEmail, UserRole, UserStatus, UserCreatedDate, UserLastLoginDate, UserLastLoginIP, UserLastLoginBrowser, UserLastLoginOS) VALUES ('" + username + \
        "', '" + password + "', '" + email + "', '" + role + "', '" + status + "', '" + createddate + "', '" + \
            lastlogindate + "', '" + lastloginip + "', '" + \
        lastloginbrowser + "', '" + lastloginos + "')"

    if CheckIfUserExists(username):
        return {'status': 'error', 'message': 'Username already exists'}
    else:
        if db.ExecuteQuery(query):
            return {'status': 'success', 'message': 'User added successfully'}
        else:
            return {'status': 'error', 'message': 'Failed to add user'}


def AuthUser(username, password):
    query = "SELECT * FROM tblUsers WHERE UserName = '" + username + "'"
    data = db.GetRecordsAsDict(query)
    records = data['results']
    for record in records:
        if username == record['UserName']:
            if pwd.check_password(password, record['UserPassword'].encode('utf-8')):
                return {'status': 'success', 'message': 'User authenticated successfully'}
            else:
                return {'status': 'error', 'message': 'Password is incorrect'}
    return {'status': 'error', 'message': 'Password is incorrect'}
