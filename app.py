import uuid
import os
from flask import Flask, request, jsonify

from embeddings import create_embeddings

app = Flask(__name__)

#vamos a crear los endpoints
    #recibir un pdf
    #extraer texto
    #crear embeddings
    #guardar embeddings en chroma
    #devolver el chatbot_id

chatbot_status = {} # Crea una estructura general que va a contener los chatbots y su status, tambien tener un registro

@app.route('/build_chatbot', methods=['POST'])
def build_chatbot():
    #recibir un pdf
    if 'file' not in request.files:
        return jsonify({'error': 'No file found'}),400 # Si no se encontro un archivo en la peticion, devolver un error 400
    
    file = request.files['file'] # Extraer el archivo de la peticion
    file.save(os.path.join('pdf_files',file.filename)) # Guardar el archivo en el sistema de archivos
    
    chatbot_id = str(uuid.uuid4()) # Crear un chatbot_id unico
    chatbot_status[chatbot_id] = {'status': 'Creating embeddings'} # Agregar el chatbot_id a la estructura de chatbot_status
    create_embeddings(file.filename)

    chatbot_status[chatbot_id] = {'status': 'Embeddings ready'} # Actualizar el status del chatbot_id
    #devolver el chatbot_id
    return jsonify({'chatbot_id': chatbot_id}), 201



#recibir un chatbot_id y una pregunta
#va a acceder a la base de datos de vectores
#Hacer query con la pregunta ->documentos relevantes
#Va a preguntar a OpenAI la pregunta + los documentos relevantes
#Devolver la respuesta

@app.route('/ask_chatbot/string:chatbot_id', methods=['POST']) #agregaremos un id para identificar al chatbot al que le estamos preguntando
def ask_chatbot(chatbot_id):
    print(chatbot_id)

if __name__ == '__main__':
    app.run(debug=True)