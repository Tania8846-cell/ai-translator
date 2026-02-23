from flask import Flask, render_template, request
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    translation = None
    roman_text = None
    text_input = ""
    source_lang = "auto"
    target_lang = "en"

    if request.method == "POST":
        text_input = request.form["text"]
        target_lang = request.form["language"]
        source_lang = request.form.get("source_language", "auto")

        try:
            # Translate text
            translation = GoogleTranslator(source=source_lang, target=target_lang).translate(text_input)

            # If target language is an Indian language, create Romanized version
            if target_lang in ["hi", "te", "ml", "ta", "kn", "bn", "gu"]:
                # Map ISO code to Sanscript script
                script_map = {
                    "hi": sanscript.DEVANAGARI,
                    "te": sanscript.TELUGU,
                    "ml": sanscript.MALAYALAM,
                    "ta": sanscript.TAMIL,
                    "kn": sanscript.KANNADA,
                    "bn": sanscript.BENGALI,
                    "gu": sanscript.GUJARATI
                }
                roman_text = transliterate(translation, script_map[target_lang], sanscript.ITRANS)

        except Exception as e:
            translation = f"Error: {e}"

    return render_template("index.html",
                           translation=translation,
                           roman_text=roman_text,
                           text_input=text_input,
                           source_lang=source_lang,
                           target_lang=target_lang)

if __name__ == "__main__":
    app.run(debug=True)
