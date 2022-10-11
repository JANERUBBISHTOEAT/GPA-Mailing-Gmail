import smtplib
from os.path import dirname, join
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
# from email.utils import formataddr
from email.header import Header
from email.mime.application import MIMEApplication

# Constants
VERSION = str(hex(20221011))
ATTACH_ERR = "Attachment Failed"
LOGIN__ERR = "Login Failed" # Take place in main
IMAGE__ERR = "Image Failed"
ALL_GOOD   = "All Good"
UNKNOWN_ERR= "Unknown Error"
SEND_ERR   = "Sending Failed"
QUIT_ERR   = "Quitting Failed" # Take place in main

my_sender = input('Sender Email: ')
my_pass  = input('Password: ')

# Global
_signature = ""
_position  = ""

def mail(email_info, attach_dir_list, server):
    global my_sender

    my_user =email_info[0] # Address of Recipient
    _Subject=email_info[1]
    _From=   email_info[2] # Nickname of Sender
    _To  =   email_info[3] # Nickname of Recipient
    # _Attr=   attach_list
    _Image = "logo.png"
    try:
#         mail_msg ="\
# 亲爱的" + _To + "同学, <br><br>你好，<br>收到此封邮件意味着你已成功报名 " + _Subject + "。以下为\
# 的时间及具体信息。<br>请在活动当天准时参加，并<b>准备好邀请函上的二维码</b>作为身份标识入场哦!\
# <div><br><br>祝好，<br><br>\
# <font color='#38761d'><b>" + _signature + "</b></font><br>" + _position + "<br>\
# <img src='cid:image1' width='200' height='52' style='border:0px'><br> \
# <font color='#38761d'>\
# <span style='font-size:8pt;font-family:Arial;\
# background-color:transparent;font-weight:700;\
# vertical-align:baseline;white-space:pre-wrap'>\
# Website: <a href='https://uoftgpa.ca' target='_blank'\
# style='font-weight:300;'>uoftgpa.ca</a> | Bilibili: <a \
# href='https://space.bilibili.com/403536025' target='_blank'>\
# UofTGPA</a></span></font>\
# </div>\
# "
        mail_msg ="\
亲爱的" + _To + "同学, <br><br>你好，<br>收到此封邮件意味着你已成功报名" + _Subject + "\
以下为活动时间及具体信息：<br>"

        mail_msg += "请在活动当天准时参加，并准备好邀请函上的二维码作为身份标识入场哦!\
<div><br><br>祝好，<br><br>\
<font color='#38761d'><b>" + _signature + "</b></font><br>" + _position + "<br>\
<img src='cid:image1' width='200' height='52' style='border:0px'><br> \
<font color='#38761d'>\
<span style='font-size:8pt;font-family:Arial;\
background-color:transparent;font-weight:700;\
vertical-align:baseline;white-space:pre-wrap'>\
Website: <a href='https://uoftgpa.ca' target='_blank'\
style='font-weight:300;'>uoftgpa.ca</a> | Bilibili: <a \
href='https://space.bilibili.com/403536025' target='_blank'>\
UofT_GPA</a></span></font>\
</div>\
"

# Remove image rely on the uncontrolled server
# <img src='https://uoftgpa.ca/home/img/GPA_mail.png' width='200' height='52' style='border:0px'>

        #创建一个带附件的实例
        msg = MIMEMultipart()
        # msg = MIMEText(mail_msg, 'html', 'utf-8')
        msg['From'] = Header(_From, 'utf-8')  # 括号里的对应发件人邮箱昵称
        msg['To'] = Header(_To, 'utf-8')              # 括号里的对应收件人邮箱昵称
        msg['Subject'] = Header(_Subject, 'utf-8')            # 邮件的主题，也可以说是标题
        msg.attach(MIMEText(mail_msg, 'html', 'utf-8'))

        # cover.jpg
        # filename = "cover.jpg"
        # att0 = MIMEApplication(open(join(dirname(__file__), _Att_Dir + "\\" + filename), 'rb').read())
        # att0.add_header("Content-Disposition", 'attachment', filename = ('utf-8', '', filename))
        # msg.attach(att0)
        # In case of multiple Attachments
        for _Att_Dir, _File_Type in attach_dir_list:
            # 构造附件n，传送当前目录下的 "" 文件
            try:
                # att1 = MIMEText(open(join(dirname(__file__), _Att_Dir + "\\" + _To + _File_Type), 'rb').read(), 'base64', 'utf-8')
                # att1["Content-Type"] = 'application/octet-stream'
                # # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
                # att1["Content-Disposition"] = 'attachment; filename=' + _To + _File_Type
                # msg.attach(att1)
                filename = _To + _File_Type
                att1 = MIMEApplication(open(join(dirname(__file__), _Att_Dir + "\\" + filename), 'rb').read())
                att1.add_header("Content-Disposition", 'attachment', filename = ('utf-8', '', filename))
                msg.attach(att1)
            except Exception as e:
                print("\n" + ATTACH_ERR + ": " + _Att_Dir + "\\" + filename + ": \n" + str(e))
                return ATTACH_ERR


        # 指定图片为当前目录
        try:
            fp = open(join(dirname(__file__), _Image), 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
            # 定义图片 ID，在 HTML 文本中引用
            msgImage.add_header('Content-ID', '<image1>')
            msg.attach(msgImage)
        except Exception as e:
            print("\n" + IMAGE__ERR + ": " + _Image + ": \n" + str(e))
            return IMAGE__ERR

#         # for test
#         message = """From: {} <{}>
# To: {} <{}>
# Subject: {}
# {}""".format("name_from", my_sender, "name_to", my_user, "subject", "body")

        # Send
        try:
            # server=smtplib.SMTP_SSL("smtp.gmail.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            # server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            # server.sendmail(my_sender, my_user, message)  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            # server.quit()  # 关闭连接
        except Exception as e:
            print("\n" + SEND_ERR + ": " + _To + ": \n" + str(e))
            return SEND_ERR

    except Exception as e:
        print("\n" + SEND_ERR + ": " + _To + ": \n" + str(e))
        return UNKNOWN_ERR
    return ALL_GOOD

def test_mail():
    global _signature
    global _position

    print ("These information will \
be used for sending formal emails if \
you claim that the test mail is correct.\n\
PLEASE CHECK TWICE\n")

    try:
        server=smtplib.SMTP_SSL("smtp.gmail.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25

        # server=smtplib.SMTP("smtp.office365.com", 587)  # 发件人邮箱中的SMTP服务器，端口是25
        # server.ehlo()
        # server.starttls()
        # server.ehlo()

        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
    except Exception as e:
        print("\n" + LOGIN__ERR + ": \n" + str(e))
        input(LOGIN__ERR)
        return LOGIN__ERR

    _From =  input("From (Sender Nickname): ").strip()
    _To   =  input("To (Recipitent Nickname): ").strip()
    _Subject=input("Subject: ").strip()
    my_user =input("Your Email Please (For testing):\n").strip()
    # _From = "UofT GPA"
    # _To = "admin"
    # _Subject = "hej world"
    # my_user = "zheyuan.wei2003@gmail.com"

    email_info = []
    email_info.append(my_user)
    email_info.append(_Subject)
    email_info.append(_From)
    email_info.append(_To)

    _signature = input("Your signature: ").strip()
    _position  = input("Your position : ").strip()
    # _signature = "Zheyuan Wei"
    # _position = "null"
    
    attach_dir_list = [] # Can be empty
    att = input("Do you have any attachments to send? If so type the dir below: (Type no to end this loop)\n").strip()
    if (att.lower() != "no"):
        filetype = input("What's the filetype?(eg: .png)\n").strip()
    while (att.lower() != 'no'):
        attach_dir_list.append((att, filetype)) # (direction, filetypr)
        att = input("\nDo you have any other attachment to send?(Type no to end this loop)\n").strip()
        if (att.lower() != "no"):
            filetype = input("What's the filetype?\n").strip()
    print("\n----------------------------")
    print("Sending mail to: {} [{}]".format(_To, my_user))
    print(mail(email_info, attach_dir_list, server))
    return email_info, attach_dir_list, server


if __name__ == "__main__":
    print("Running on ver." + VERSION[2:])
    email_info, attach_dir_list, server = test_mail()
    server.quit()  # 关闭连接