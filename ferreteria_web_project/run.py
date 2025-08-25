from waitress import serve
from ferreteria_web_project.wsgi import application  # ❌ cambiar de ferreteria_web/ferreteria_web.wsgi

if __name__ == "__main__":
    print("🚀 Servidor corriendo en http://0.0.0.0:8000")
    serve(application, host="0.0.0.0", port=8000)
