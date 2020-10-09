from webexteamssdk import WebexTeamsAPI
import webbrowser


url="https://google.de"

webbrowser.open(url,new=2)



api = WebexTeamsAPI(client_id='Cbbb54d9e35aa736ef45c2e21b3cef7d5d44f0dbf86535732768540c456e13b63',client_secret='052ac0a80718fc4471128a5db6185a03c3786c2ec631ee1efd73909f528a20d1', redirect_uri='http://localhost:8080/oauth/code')




if __name__ =="__main__":
    print("hola")