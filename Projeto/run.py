from app import create_app
#import webview

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)        
    '''
    webview.create_window(
    "EVENT2U", app, width=800, height=600, resizable=True, 
    confirm_close=True, fullscreen=False)
    webview.start()
    '''
