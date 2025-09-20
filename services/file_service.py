import pandas as pd
from services.faq_service import save_faq

def excel_to_json(file_path: str, output_path: str = "data/faq.json"):
    """
    Convert file Excel menjadi JSON untuk FAQ.
    Excel harus punya kolom: 'question' dan 'answer'.
    """
    df = pd.read_excel(file_path)

    # Validasi kolom
    required_cols = {"question", "answer"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"File Excel harus mengandung kolom: {required_cols}")

    # Bersihkan data & handle NaN
    df = df.fillna("")

    faq_data = []
    for _, row in df.iterrows():
        faq_data.append({
            "question": str(row["question"]).strip(),
            "answer": str(row["answer"]).strip()
        })

    # Simpan ke JSON lewat service
    save_faq(faq_data, output_path)

    return faq_data