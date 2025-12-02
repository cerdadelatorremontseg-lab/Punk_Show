from flask import Flask, render_template, request, session, redirect, url_for
import random


app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  

BASE_MUSICAL = {
    "rabia": [
        {"artista": "The Clash", "cancion": "London Calling", "porque": "Para canalizar la rabia en energía revolucionaria"},
        {"artista": "Dead Kennedys", "cancion": "Holiday in Cambodia", "porque": "Crítica social que convierte la ira en conciencia"},
        {"artista": "Black Flag", "cancion": "Rise Above", "porque": "Punk crudo para superar la frustración"},
        {"artista": "Rage Against The Machine", "cancion": "Killing in the Name", "porque": "Rabia contra el sistema convertida en himno (Parte de el top 3 de bandas de la Creadora de la Data Base)"},
        {"artista": "Bad Brains", "cancion": "Pay to Cum", "porque": "Hardcore veloz para liberar tensiones"}
    ],
    "tristeza": [
        {"artista": "The Smiths", "cancion": "How Soon Is Now?", "porque": "Melancolía existencial que abraza la tristeza"},
        {"artista": "Joy Division", "cancion": "Love Will Tear Us Apart", "porque": "Post-punk que transforma el dolor en belleza"},
        {"artista": "Patti Smith", "cancion": "Because the Night", "porque": "Poesía rock que redime el sufrimiento"},
        {"artista": "Sonic Youth", "cancion": "Teen Age Riot", "porque": "Noise rock que acompaña la introspección"},
        {"artista": "The Cure", "cancion": "A Forest", "porque": "Atmósfera gótica para introspección"}
    ],
    "ansiedad": [
        {"artista": "Talking Heads", "cancion": "Psycho Killer", "porque": "Nerviosismo convertido en funk punk neurotico"},
        {"artista": "The Stooges", "cancion": "Search and Destroy", "porque": "Garage rock primitivo que te acompaña"},
        {"artista": "Fugazi", "cancion": "Waiting Room", "porque": "Post-hardcore que transforma la ansiedad"},
        {"artista": "IDLES", "cancion": "Never Fight a Man With a Perm", "porque": "Punk moderno que confronta las inseguridades"}
    ],
    "rebeldia": [
        {"artista": "Sex Pistols", "cancion": "Anarchy in the UK", "porque": "Manifiesto punk que desafía toda autoridad (La canción favorita de la creadora de la Data Base)"},
        {"artista": "The Ramones", "cancion": "Blitzkrieg Bop", "porque": "Rebelión en forma de solo tocar musica sin mucha ciencia"},
        {"artista": "MC5", "cancion": "Kick Out the Jams", "porque": "Rock de protesta que incita a la acción directa"},
        {"artista": "Crass", "cancion": "Do They Owe Us a Living?", "porque": "Anarko-punk que cuestiona el sistema económico"},
        {"artista": "Bikini Kill", "cancion": "Rebel Girl", "porque": "Canción que empodera la rebeldía feminista"}
    ],
    "apatia": [  
        {"artista": "Pixies", "cancion": "Where Is My Mind?", "porque": "Rock alternativo para desapegarse de la realidad"},
        {"artista": "The Velvet Underground", "cancion": "Heroin", "porque": "Experimento sonoro que navega el desinterés"},
        {"artista": "PJ Harvey", "cancion": "Rid of Me", "porque": "Rock visceral que despierta los sentidos adormecidos"},
        {"artista": "Parquet Courts", "cancion": "Wide Awake", "porque": "Punk-funk que ironiza sobre la desconexión moderna"}
    ]  
}


def analizar_estado_emocional(respuestas):
    """Analiza las respuestas para determinar el estado emocional predominante"""
    emociones = {
        "rabia": 0,
        "tristeza": 0,
        "ansiedad": 0,
        "rebeldia": 0,
        "apatia": 0
    }
   
    # Pregunta 1
    emociones[respuestas[0]] += 2
   
    # Pregunta 2
    intensidad = respuestas[1]
    if intensidad == "alta":
        emociones[respuestas[0]] += 2
    elif intensidad == "media":
        emociones[respuestas[0]] += 1
   
    # Pregunta 3
    accion = respuestas[2]
    if accion == "destruir":
        emociones["rabia"] += 1
        emociones["rebeldia"] += 1
    elif accion == "escapar":
        emociones["apatia"] += 1
    elif accion == "transformar":
        emociones["rebeldia"] += 1
    elif accion == "reflexionar":
        emociones["tristeza"] += 1
   
    emocion_predominante = max(emociones.items(), key=lambda x: x[1])[0]
   
    return emocion_predominante


def obtener_recomendaciones(emocion, num_recomendaciones=3):
    """Obtiene recomendaciones musicales basadas en la emoción"""
    if emocion in BASE_MUSICAL:
        canciones = BASE_MUSICAL[emocion].copy()
        random.shuffle(canciones)
        return canciones[:num_recomendaciones]
    return []


@app.route('/')
def inicio():
    session.clear()
    return render_template('index.html')


@app.route('/preguntas', methods=['GET', 'POST'])
def preguntas():
    if request.method == 'POST':
        session['respuestas'] = [
            request.form.get('pregunta1'),
            request.form.get('pregunta2'),
            request.form.get('pregunta3')
        ]
        return redirect(url_for('resultados'))
   
    return render_template('preguntas.html')


@app.route('/resultados')
def resultados():
    if 'respuestas' not in session:
        return redirect(url_for('index'))
   
    respuestas = session['respuestas']
    emocion = analizar_estado_emocional(respuestas)
    recomendaciones = obtener_recomendaciones(emocion)
   
    return render_template('resultados.html',
                         emocion=emocion,
                         recomendaciones=recomendaciones,
                         respuestas=respuestas)
    
if __name__ == '__main__':
    app.run(debug=True)