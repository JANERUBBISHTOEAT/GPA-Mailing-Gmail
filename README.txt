# GPA-Mail

Workspace
│  logo.png
│  mail.py
│  main.py
│  res.txt
│
├─res0
│      test_name.png
│      NAME1.png
│      NAME2.png
│
└─res1
        test_name.png
        NAME1.png
        NAME2.png

Batch:
  Make sure res.txt follow format:
    #MAIL1#NAME1
    #MAIL2#NAME2
    #MAIL3#NAME3
    #MAIL4#NAME4
    
  Then run main.py
    From: ( Fill with sender's nickname )
    To:   ( Fill with recipient's nickname )
    Subject: ( Fill with name of the evnet, just the name )
    Your Email Please:
    ( Type your email in order to send a test email
    in advance of sending formal emails. )
    
    Your signature: ( Will be used to sign the email )
    Your position : ( Also, to sign the email )
    
    Do you have any attachments to send?
    ( Type the directory that contains attachments you want to sen. 
    If no attchments needed, type 'no'. just no.)
    What's the filetype?
    ( Type the filetype of your attachments )
    Loop. Untill you type a 'no'.
    
    Sending...
    
    Then this program will print the status for each eamil.
    'All Good' means all good.
    ...
    
    At the end, a statics will be given.
    Total: n
    Succeeded: a
    Failed: b
    
    if a + b != n, that means dureing the procedure a unhandled fault has happended. 
  
Single:
  No need to fill res.txt
  Follow instructions above.
  The same procedure.

w