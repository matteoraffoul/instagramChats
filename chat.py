import instaloader
import json
import os
import shutil
import sys
from datetime import datetime
from io import StringIO

# myUsername = str(input("Enter your username:"))

html_template = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Instagram Data Report">
<meta name="author" content="Micha Birklbauer">

<title>Instagram Data Report</title>

<style>
body {
  font-family: "Times New Roman", Times, serif;
}


.main {
  margin-left: 160px;
  font-size: 25px;
  padding: 0px 10px;
}

.main img {
  max-width: 500px;
  width: 100%;
}

.main audio {
  max-width: 500px;
  width: 100%;
}

.main video {
  max-width: 500px;
  width: 100%;
}

@media screen and (max-height: 450px) {
  .sidenav {padding-top: 15px;}
  .sidenav a {font-size: 18px;}
}

.container {
  border: 2px solid #000;
  background-color: #ffffff;
  border-radius: 5px;
  padding: 10px;
  margin: 10px 0;
}

.darker {
  border-color: #000;
  background-color: #66b3ff;
}

.container::after {
  content: "";
  clear: both;
  display: table;
}

.container img {
  max-width: 500px;
  width: 100%;
}

.container img.left {
  float: left;
  max-width: 60px;
  width: 100%;
  margin-right: 20px;
  border-radius: 50%;
}

.container img.right {
  float: right;
  max-width: 60px;
  width: 100%;
  margin-left: 20px;
  border-radius: 50%;
}

.container audio {
  max-width: 500px;
  width: 100%;
}

.container video {
  max-width: 500px;
  width: 100%;
}

.time-right {
  float: right;
  color: #000;
}

.time-left {
  float: left;
  color: #000;
}
</style>
</head>
<body>

<h2 id="messages">Messages</h2>

"""


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)


def getProfilePic(username):
    global dataTemp
    for elemento in dataTemp:
        print("Ricerca foto profile")
        username2 = elemento.split(":")[0]
        path = elemento.split(":")[1]
        if username2 == username:
            return path
    print("Foto non trovata. La sto scaricando")
    with Capturing() as output:
        downloadProfilePic(username)
    for x in output:
        if ".//chat//icons" in x:
            file_path = x.replace(" already exists", "").replace(chr(92), "//").replace("chat//", "")
            temp7 = username + ":" + file_path
            dataTemp.append(temp7)
            return file_path
        if "https://raw.githubusercontent.com/matteoraffoul/instagramChats/master/44884218_345707102882519_2446069589734326272_n.jpg" in x:
            file_path = "https://raw.githubusercontent.com/matteoraffoul/instagramChats/master/44884218_345707102882519_2446069589734326272_n.jpg"
            temp7 = username + ":" + file_path
            dataTemp.append(temp7)
            return file_path


def downloadProfilePic(username):
    parser = instaloader.Instaloader(dirname_pattern=".//chat//icons", filename_pattern="{owner_username}",
                                     save_metadata=False, download_pictures=False, download_videos=False,
                                     download_video_thumbnails=False, download_geotags=False, download_comments=True,
                                     compress_json=False, post_metadata_txt_pattern=None,
                                     storyitem_metadata_txt_pattern=None, max_connection_attempts=3,
                                     request_timeout=None, rate_controller=None, resume_prefix='iterator',
                                     check_resume_bbd=True)
    try:
        parser.download_profile(username, profile_pic_only=True)
    except instaloader.exceptions.ProfileNotExistsException:
        print("https://raw.githubusercontent.com/matteoraffoul/instagramChats/master/44884218_345707102882519_2446069589734326272_n.jpg")
        return
    try:
        os.remove(".//chat//icons//" + username + "_id")
    except:
        pass
    return


def writeMessaggioChat(messaggio, ora):
    username = messaggi["sender"]
    if username != myUsername:
        b = '<div class="container">\n'
        c = '<img src="' + str(getProfilePic(username)) + '" alt="' + str(messaggi["sender"]) + '" class="left" style="width:100%;">\n'
        d = '<p>\n'
        f = '<b>Text:</b>' + messaggio + "\n"
        g = '</p>' "\n"
        h = '<span class="time-right">' + ora + '</span>\n'
        i = '</div>\n'
        full = b + c + d + f + g + h + i
        chat.write(full)
    else:
        b = '<div class="container darker">\n'
        c = '<img src="' + str(getProfilePic(username)) + '" alt="' + str(myUsername) + '" class="right" style="width:100%;">\n'
        d = '<p>\n'
        f = '<b>Text:</b>' + messaggio + "\n"
        g = '</p>\n'
        h = '<span class="time-left">' + ora + '</span>\n'
        i = '</div>\n'
        full = b + c + d + f + g + h + i
        chat.write(full)
    return


def writeMediaChat(ora):
    username = messaggi["sender"]
    if username != myUsername:
        b = '<div class="container">\n'
        c = '<img src="' + str(getProfilePic(username)) + '" alt="' + str(messaggi["sender"]) + '" class="left" style="width:100%;">\n'
        d = '<p>\n'
        f = '<b>MEDIA INVIATO</b>' + "\n"
        g = '</p>' "\n"
        h = '<span class="time-right">' + ora + '</span>\n'
        i = '</div>\n'
        full = b + c + d + f + g + h + i
        chat.write(full)
    else:
        b = '<div class="container darker">\n'
        c = '<img src="' + str(getProfilePic(username)) + '" alt="' + str(myUsername) + '" class="right" style="width:100%;">\n'
        d = '<p>\n'
        f = '<b>MEDIA INVIATO</b>' + "\n"
        g = '</p>\n'
        h = '<span class="time-left">' + ora + '</span>\n'
        i = '</div>\n'
        full = b + c + d + f + g + h + i
        chat.write(full)
    return


def writeLiveChat(ora):
    username = messaggi["sender"]
    if username != myUsername:
        b = '<div class="container">\n'
        c = '<img src="' + str(getProfilePic(username)) + '" alt="' + str(messaggi["sender"]) + '" class="left" style="width:100%;">\n'
        d = '<p>\n'
        f = '<b>INVITO AD UNA DIRETTA</b>' + "\n"
        g = '</p>' "\n"
        h = '<span class="time-right">' + ora + '</span>\n'
        i = '</div>\n'
        full = b + c + d + f + g + h + i
        chat.write(full)
    else:
        b = '<div class="container darker">\n'
        c = '<img src="' + str(getProfilePic(username)) + '" alt="' + str(myUsername) + '" class="right" style="width:100%;">\n'
        d = '<p>\n'
        f = '<b>INVITO AD UNA DIRETTA</b>' + "\n"
        g = '</p>\n'
        h = '<span class="time-left">' + ora + '</span>\n'
        i = '</div>\n'
        full = b + c + d + f + g + h + i
        chat.write(full)
    return


def writeActionChat(action, ora):
    username = messaggi["sender"]
    if username != myUsername:
        b = '<div class="container">\n'
        c = '<img src="' + str(getProfilePic(username)) + '" alt="' + str(messaggi["sender"]) + '" class="left" style="width:100%;">\n'
        d = '<p>\n'
        f = '<b>AZIONE:</b>' + action + "\n"
        g = '</p>' "\n"
        h = '<span class="time-right">' + ora + '</span>\n'
        i = '</div>\n'
        full = b + c + d + f + g + h + i
        chat.write(full)
    else:
        b = '<div class="container darker">\n'
        c = '<img src="' + str(getProfilePic(username)) + '" alt="' + str(myUsername) + '" class="right" style="width:100%;">\n'
        d = '<p>\n'
        f = '<b>AZIONE:</b>' + action + "\n"
        g = '</p>\n'
        h = '<span class="time-left">' + ora + '</span>\n'
        i = '</div>\n'
        full = b + c + d + f + g + h + i
        chat.write(full)
    return


def writeVideoCallChat(videocall, ora):
    username = messaggi["sender"]
    if username != myUsername:
        b = '<div class="container">\n'
        c = '<img src="' + str(getProfilePic(username)) + '" alt="' + str(messaggi["sender"]) + '" class="left" style="width:100%;">\n'
        d = '<p>\n'
        f = '<b>CHIAMATA:</b>' + videocall + "\n"
        g = '</p>' "\n"
        h = '<span class="time-right">' + ora + '</span>\n'
        i = '</div>\n'
        full = b + c + d + f + g + h + i
        chat.write(full)
    else:
        b = '<div class="container darker">\n'
        c = '<img src="' + str(getProfilePic(username)) + '" alt="' + str(myUsername) + '" class="right" style="width:100%;">\n'
        d = '<p>\n'
        f = '<b>CHIAMATA:</b>' + videocall + "\n"
        g = '</p>\n'
        h = '<span class="time-left">' + ora + '</span>\n'
        i = '</div>\n'
        full = b + c + d + f + g + h + i
        chat.write(full)
    return


def writeVocalMessageChat(ora, time):
    username = messaggi["sender"]
    if username != myUsername:
        b = '<div class="container">\n'
        c = '<img src="' + str(getProfilePic(username)) + '" alt="' + str(messaggi["sender"]) + '" class="left" style="width:100%;">\n'
        d = '<p>\n'
        f = '<b>VOCALE: </b>' + vocalMessage(time) + "\n"
        g = '</p>' "\n"
        h = '<span class="time-right">' + ora + '</span>\n'
        i = '</div>\n'
        full = b + c + d + f + g + h + i
        chat.write(full)
    else:
        b = '<div class="container darker">\n'
        c = '<img src="' + str(getProfilePic(username)) + '" alt="' + str(myUsername) + '" class="right" style="width:100%;">\n'
        d = '<p>\n'
        f = '<b>VOCALE: </b>' + vocalMessage(time) + "\n"
        g = '</p>\n'
        h = '<span class="time-left">' + ora + '</span>\n'
        i = '</div>\n'
        full = b + c + d + f + g + h + i
        chat.write(full)
    return


def vocalMessage(oraInvio):
    with open("media.json", "rb") as file_json:
        media = json.load(file_json)
        media["direct"].reverse()
        for direct in media["direct"]:
            if oraInvio == direct["taken_at"]:
                file_path = direct["path"].replace("/", r"\\")
                file_path = ".\\" + file_path
                html_string = '''<audio style="width: 20%; height:;" controls="controls" preload="none" src="''' + file_path + '''" type="audio/mp4">'''
                return html_string
        return "VOCALE NON TROVATO"


def printChat(messaggio):
    print(time, " - ", messaggi["sender"], ": ", messaggio, "\n")
    return


def main():
    with open("messages.json", 'rb') as json_file:

        data = json.load(json_file)

        for item in data:

            global chat, time, messaggi, partecipanti
            partecipanti = item["participants"]
            conversazione = item["conversation"]
            partecipanti.remove(myUsername)
            if len(partecipanti) > 1:

                for checkGroup in conversazione:

                    if "action" in checkGroup:

                        item = checkGroup["action"].split("named the group ")
                        item.remove(item[0])

                        if len(item) == 0:
                            pass

                        else:
                            chat = open(".\\chat\\" + item[0] + ".html", "w", encoding="utf-8")
                            a = '<h3>' + item[0] + '</h3>\n'
                            pieno = html_template + a
                            chat.write(pieno)
            else:
                try:
                    chat = open(".\\chat\\" + partecipanti[0] + ".html", "w", encoding="utf-8")
                    a = '<h3>' + partecipanti[0] + '</h3>\n'
                    pieno = html_template + a
                    chat.write(pieno)
                except IndexError:
                    pass

            conversazione.reverse()

            for messaggi in conversazione:
                orario = datetime.strptime(messaggi["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                time = orario.strftime("%Y-%m-%d %H:%M:%S")

                if "text" in messaggi:
                    writeMessaggioChat(messaggi["text"], time)

                if "heart" in messaggi:
                    writeMessaggioChat(messaggi["heart"], time)

                if "media_share_url" in messaggi:
                    writeMediaChat(time)

                if "animated_media_images" in messaggi:
                    writeMediaChat(time)

                if "media" in messaggi:
                    writeMediaChat(time)

                if "media_url" in messaggi:
                    writeMediaChat(time)

                if "live_video_invite" in messaggi:
                    writeLiveChat(time)

                if "action" in messaggi:
                    writeActionChat(messaggi["action"], time)

                if "video_call_action" in messaggi:
                    messaggio = messaggi["video_call_action"]
                    writeVideoCallChat(messaggi["video_call_action"], time)

                if "voice_media" in messaggi:
                    writeVocalMessageChat(time, messaggi["created_at"])

        chat.close()


if __name__ == "__main__":
    global dataTemp
    dataTemp = ["ciao:ciao"]
    copytree("direct", ".\\chat\\direct")
    try:
        myUsername = "alixelmex"
        os.mkdir("chat")
        os.mkdir(".\\chat\\data")
        main()
        os.mkdir(".\\chat\\icons")
    except Exception as e:
        main()
