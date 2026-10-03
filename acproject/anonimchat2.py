#anonimchat2
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.config["SECRET_KEY"] = "anonymous-chat-secret"

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)


@app.route("/")
def index():
    return render_template("index.html")


# Kullanıcı bağlandığında
@socketio.on("connect")
def handle_connect(auth=None):

    print()
    print("[YENİ BAĞLANTI]")

    # Socket.IO bağlantısının geldiği IP
    ip = request_ip()

    print(f"IP: {ip}")
    print()


# Kullanıcı sohbete katıldığında
@socketio.on("join")
def handle_join(data):

    print()
    print("JOIN OLAYI GELDİ!")

    name = str(data.get("name", "Anonim")).strip()

    if not name:
        name = "Anonim"

    name = name[:24]

    ip = request_ip()

    print("[KULLANICI]")
    print(f"İsim : {name}")
    print(f"IP   : {ip}")
    print()

    emit(
        "system_message",
        {
            "text": f"{name} sohbete katıldı."
        },
        broadcast=True
    )


# IP adresini bul
def request_ip():

    try:

        # Flask-SocketIO bağlantısının environ bilgisi
        from flask import request

        # Cloudflare Tunnel kullanılıyorsa
        # kullanıcının IP'si bu başlıkta bulunabilir.
        cloudflare_ip = request.headers.get("CF-Connecting-IP")

        if cloudflare_ip:
            return cloudflare_ip

        # Cloudflare yoksa doğrudan bağlantı IP'si
        return request.remote_addr

    except Exception as error:

        print(f"IP alınamadı: {error}")

        return "Bilinmiyor"


# Mesaj gönderildiğinde
@socketio.on("message")
def handle_message(data):

    name = str(data.get("name", "Anonim")).strip()

    message = str(data.get("text", "")).strip()

    if not name:
        name = "Anonim"

    if not message:
        return

    name = name[:24]

    message = message[:1000]

    emit(
        "message",
        {
            "name": name,
            "text": message
        },
        broadcast=True
    )


if __name__ == "__main__":

    print()
    print("==============================")
    print("      ANONYMOUS CHAT")
    print("==============================")
    print()
    print("Sunucu çalışıyor.")
    print()
    print("Kendi bilgisayarından:")
    print("http://127.0.0.1:5000")
    print()
    print("IP kayıt sistemi: AKTİF")
    print()
    print("Durdurmak için CTRL + C")
    print()

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=False
    )

