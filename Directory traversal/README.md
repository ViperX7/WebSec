# Directory traversal

> Utkarsh Yadav | 11th August 2020
---

## Intro
Directory or path traversal occours when the webapp uses some kind of api to 
load or view files using their filenames and do not check the file name
properly. As a result an attacker can supply path to any file on te server
and read it's content and in some cases even execute code.


## ---
* Check how all the resources are loaded images/scripts/embeded content etc
* look for filenames in url parameters


## Bypassing Protections
* sometimes `../` can be blocked but directly referencing the file could be
  allowed like using `/etc/passwd` rather than using `../../../../../../etc/passwd`
* The application might be replacing/removing all instance of `../` to bypass 
  this we can simpaly use `....//` in this case when `../` is removed we will
  still get the `../`
* Try double urlencoding or single urlencoding to bypass the WAF or just some
  application logic
* If the starting part of the path is checked try going some dirs in direction
  of the path then back link  
  `/var/www/html/images/users../../../../../../etc/passwd`
* If the application is appending or requires a file extentions at the end of the filename 
  provided then you can try using null bytes at the end of the filename  
  - If the application require you to have a extention  
    > `../../../../../../etc/passwd%00.jpg`  

  - If the application is appending the extention itself  
    > `../../../../../../etc/passwd%00`
