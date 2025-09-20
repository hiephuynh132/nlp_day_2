from flask import Flask, render_template, request
import spacy_stanza
from spacy import displacy

app = Flask(__name__)

# Tải mô hình tiếng Việt
#nlp = spacy.load("vi_core_news_sm")
nlp = spacy_stanza.load_pipeline("vi")

# Bảng dịch POS
pos_vi = {
    "NOUN": "Danh từ",
    "PROPN": "Danh từ riêng",
    "VERB": "Động từ",
    "ADJ": "Tính từ",
    "ADV": "Trạng từ",
    "PRON": "Đại từ",
    "DET": "Từ hạn định",
    "ADP": "Giới từ",
    "CCONJ": "Liên từ đẳng lập",
    "SCONJ": "Liên từ phụ thuộc",
    "NUM": "Số",
    "PUNCT": "Dấu câu",
    "AUX": "Trợ động từ",
    "PART": "Tiểu từ",
    "INTJ": "Thán từ",
    "SYM": "Ký hiệu",
    "X": "Không xác định"
}


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    ents_html = None
    if request.method == "POST":
        text = request.form["text"]
        doc = nlp(text)
        tokens = [(token.text, pos_vi[token.pos_]) for token in doc]
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        ents_html = displacy.render(doc, style="ent")
        result = {"tokens": tokens, "entities": entities}
    return render_template("index.html", result=result, ents_html=ents_html)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8888)
