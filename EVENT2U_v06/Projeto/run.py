from app import create_app
import webview

app = create_app()


if __name__ == "__main__":
    #app.run(debug=True)   
    webview.create_window("EVENT2U", app, width=1500, height=1000, resizable=False, fullscreen=False, confirm_close=True)
    webview.start()

