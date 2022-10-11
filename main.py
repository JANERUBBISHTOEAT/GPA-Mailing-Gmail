from re import M
from mail import mail, test_mail
from mail import VERSION as mail_VERSION
from mail import my_sender,my_pass
from os.path import join, dirname
import smtplib
from progress.bar import Bar

# Constants
VERSION = str(hex(20221011))
SEPERATOR = "#"
_ENCODING = "utf-8"
SENT_MARK = "SENT"

# my_sender= input('Sender Email: ')
# my_pass  = input('Password: ')

# Constants
LOGIN__ERR = "Login Failed"
ALL_GOOD   = "All Good"
QUIT_ERR   = "Quitting Failed"
MAIl_LIST  = "res.txt"

# Global
cnt = 0
name_List = []
mail_List = []
sent_List = []
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

def read_record():
    global cnt
    global name_List
    global mail_List
    global sent_List

    print("----------------------------")
    print("Reading records from " + MAIl_LIST + ":")
    
    try: 
        fp = open(join(dirname(__file__), MAIl_LIST), mode = 'r', encoding = _ENCODING)
    except:
        print("[ERROR] Cannot find file: "+ join(dirname(__file__), MAIl_LIST))
        input()
        return False
    # "Check#Code#Name"
    text = fp.read()
    # print(text)
    for line in text.split('\n'):
        if SEPERATOR in line:
            sent_List.append(line.split(SEPERATOR)[0])
            mail_List.append(line.split(SEPERATOR)[1])
            name_List.append(line.split(SEPERATOR)[2].rstrip('\n'))
            if (sent_List[cnt]):
                print("|-√- " + mail_List[cnt] + '|' + name_List[cnt])
            else:
                print("|--- " + mail_List[cnt] + '|' + name_List[cnt])
            cnt += 1
        else:
            print("Unexpected Format Detected")
    fp.close()
    print(str(len(name_List)) + " records read sucesfully.")
    print("-----------------------\n")
    return True

def mass_mail(email_info, attach_dir_list):
    """
    # Data Info:
    
    # my_user =email_info[0] # Address of Recipient
    # _Subject=email_info[1]
    # _From=   email_info[2] # Nickname of Sender
    # _To  =   email_info[3] # Nickname of Recipient
    """



    succ_cnt = 0
    fail_cnt = 0
    igno_cnt = 0

    try:
        server=smtplib.SMTP_SSL("smtp.gmail.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
    except Exception:
        input(LOGIN__ERR)
        return (0, 0, 0)
    
    with Bar('Sending', max=cnt, fill = '▪') as bar:
        for i in range(cnt):
            if sent_List[i] == SENT_MARK:
                print(name_List[i] + " is marked as sent. Ignored.")
                igno_cnt += 1
                continue
            email_info[0] = mail_List[i]
            email_info[3] = name_List[i]
            status = mail(email_info, attach_dir_list, server)
            print(status)

            if (status == ALL_GOOD):
                fp = open(join(dirname(__file__), MAIl_LIST), mode = 'w', encoding = _ENCODING) # rerwite res.
                sent_List[i] = SENT_MARK
                i = 0
                for i in range(cnt-1):
                    fp.write(sent_List[i] + SEPERATOR + mail_List[i] + SEPERATOR + name_List[i] + '\n')
                    # print("Writing information: {}, {}".format(cnt, scanned[i] + '#' + name_List[i]))
                i += 1
                fp.write(sent_List[i] + SEPERATOR + mail_List[i] + SEPERATOR + name_List[i]) # Avoid ending \n
                fp.close()
                succ_cnt += 1
                bar.next()
            else:
                print("\n" + status + " in: " + mail_List[i] + '|' + name_List[i])
                fail_cnt += 1

    try:
        server.quit()  # 关闭连接
    except Exception:
        input(QUIT_ERR)
        return (igno_cnt, succ_cnt, fail_cnt)

    return (igno_cnt, succ_cnt, fail_cnt)



if __name__ == "__main__":
    print("Running on ver." + VERSION[2:])

    if mail_VERSION != VERSION:
        print("Version does not match!\nModule \"mail\" is running on ver.{}".format(mail_VERSION[2:]))
        exit ("Version Failure")
        
    if(read_record()):
        email_info, attach_dir_list, tmp_server = test_mail()
        tmp_server.quit()

        manual_check = input("Did the test mail go well? Type your [email] to confirm, and continue to send mass emails.\n").strip()
        if (manual_check != email_info[0] and manual_check != "key"): # Mater key
            print("Check all the info and try again.")
            input()
            exit()

        result = mass_mail(email_info, attach_dir_list)

        # # Activity Monitoring
        # email_info[0]  = 'zheyuan.wei@mail.utoronto.ca'
        # email_info[1]  = email_info[1] + \
        #                 "|Total: " + str(cnt) + \
        #                 "|Ignored: " + str(result[0]) + \
        #                 "|Succeeded: " + str(result[1]) + \
        #                 "|Failed: " + str(result[2]) + "|"
        # email_info[3]  = '管理员'
        # mail(email_info, attach_dir_list, server) # No prompt

        # # Activity Monitoring Forward
        # email_info[0]  = 'hello@utscgpa.org'
        # mail(email_info, attach_dir_list, server) # No prompt

        print("-----------------------------------")
        print("    Total: {}\n    Ignored:{}\n    Succeeded: {}\n    Failed: {}"\
            .format(cnt, result[0], result[1], result[2]))
        input("-----------------------------------")