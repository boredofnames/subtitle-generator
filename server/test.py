import hashlib
url = "https://rumble.com/v5bf4nf-its-do-or-die-international-affairs-expert-on-putins-reaction-to-ukraines-k.html"
filename = hashlib.shake_256(url.encode()).hexdigest(5)+".vtt"
print(filename)