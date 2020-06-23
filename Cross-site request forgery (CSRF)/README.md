# Cross-site request forgery (CSRF)
> Utkarsh Yadav | 22nd june 2020
---

* Crafting a page in such a way that when a user visits the page a request is
sent to some authenticated server which in turn performs some action
* In case the server useg get requests it is possible to craft a link that will
do the same
* Although in my opnion it doesnt matter because its possible to make a page
in such a way that it's placed between some rediricts and user wont even notice
anything



#### Same Site
An attribute can be added to cookies that can prevent the browser from sending
cookies to a website if the request originates from some other third party website
* There are two types
    - SameSite: cookies will never be include no matter what
    - Lax: Cookies will be executed when the request is a GET request and Is initiated by user clicking
    and not by some script
> If the server accepts  GET requests to perform action user can be phissed to click something
that send our maclicious GET request

#### Pitfalls
* Token is checked only if the request is a POST request
* Token is checked only if its present
* Token is there but not tied to user session (cookie)??
    > In that case one can get a tokken from some other account or (directly from
    website using a get request if its there)??

#### Notes
* Watch any new cookie creation if the value inside the Set-Cookie: can be controlled
its possible to set various cookies in victims browser
* Request a url and execute some javascript using img tag and onerror
* If you want the browser to not include Refferer for the links clicked on your page
    ```html
    <meta name="referrer" content="never"> 
    ```
* Javascript can be used to modify the url in the address bar without any action
deceiving the server in where the requesst is comming from
    ```js
    history.pushState("", "", "/stuff");
    ```
### Refferences
* [WebSec Academy](https://portswigger.net/web-security/csrf)
