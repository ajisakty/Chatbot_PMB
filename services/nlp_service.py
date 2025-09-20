from sentence_transformers import SentenceTransformer, util
from services.faq_service import load_faq
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Load SBERT Model
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Buat stopword remover
stop_factory = StopWordRemoverFactory()
stop_remover = stop_factory.create_stop_word_remover()

def preprocess(text):
    """Lowercase + hapus stopword bahasa Indonesia"""
    text = text.lower()
    text = stop_remover.remove(text)
    return text

def get_best_answer(user_question, threshold=0.6):
    faq = load_faq()
    if not faq:
        return "Database FAQ Kosong, Silahkan hubungi admin."
    
    # Preprocess pertanyaan & FAQ
    question = [preprocess(item["question"]) for item in faq]
    answer = [item["answer"] for item in faq]
    user_question_proc = preprocess(user_question)

    # Encode
    emb_user = model.encode(user_question_proc, convert_to_tensor=True)
    emb_faq = model.encode(question, convert_to_tensor=True)

    # Similarity
    cos_sim = util.pytorch_cos_sim(emb_user, emb_faq)[0]
    best_idx = cos_sim.argmax().item()
    best_score = cos_sim[best_idx].item()

    if best_score >= threshold:
        return answer[best_idx]
    else:
        return "Jika ada pertanyaan yang lebih detail bisa hubungi admin kami."
