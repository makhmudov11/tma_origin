import pdfplumber, re, os
from django.core.exceptions import ValidationError
# from pdf2image import convert_from_path
import pytesseract
from PIL import Image

from apps.massoviy.models import Question, PDFFile, Answer


def parse_pdf(file_path, uploaded_file):
    POPPLER_PATH = r"C:\Users\saman\Downloads\Release-25.07.0-0\poppler-25.07.0\Library\bin"
    # pages = convert_from_path(file_path, dpi=300, poppler_path=POPPLER_PATH)
    # try:
    file_id = uploaded_file
    # except PDFFile.DoesNotExist:
    #     return ValidationError("File topilmadi")

    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()

            if not text:
                text = pytesseract.image_to_string(pages[i], lang="eng+uzb")

            if not text.strip():
                continue

            blocks = re.split(r"\n(?=\d+\.)", text)

            for block in blocks:
                block = block.strip()
                if not block or not re.match(r"^\d+\.", block):
                    continue

                lines = block.split("\n")
                q_text = lines[0]
                q_text = re.sub(r"^\d+\.\s*", "", q_text)

                # Savolni yaratamiz
                question = Question.objects.create(
                    text=q_text.strip(),
                    file=file_id
                )

                # Variantlarni ajratamiz
                for line in lines:
                    match = re.match(r"^\s*([A-D])[.)]\s*(.*)", line)
                    if match:
                        label = match.group(1)
                        text_part = match.group(2) if match.group(2) else None

                        Answer.objects.create(
                            text=text_part,
                            label=label,
                            question=question
                        )

                # To‘g‘ri javobni ajratamiz
                answer_match = re.search(r"(Answer|Javob)\s*[:：]\s*([A-D])", block)
                if answer_match:
                    correct_label = answer_match.group(2)  # masalan "C"
                    answer = Answer.objects.get(label=correct_label)
                    answer.is_correct = True
                    answer.save()
    return

    # Agar sahifada rasm bo‘lsa – savolga yoki variantga qo‘shamiz
    # for j, img in enumerate(page.images):
    #     x0, y0, x1, y1 = img["x0"], img["top"], img["x1"], img["bottom"]
    #     pil_page = pages[i]
    #     cropped = pil_page.crop((x0, y0, x1, y1))
    #
    #     image_path = f"media/questions/page_{i}_img_{j}.png"
    #     os.makedirs("media/questions", exist_ok=True)
    #     cropped.save(image_path, "PNG")
    #
    #     # ⚠️ Bu joy muhim: sizga heuristika kerak bo‘ladi
    #     # Masalan: agar rasm variantga yaqin joylashgan bo‘lsa, Option.image sifatida
    #     # aks holda QuestionImage sifatida saqlash mumkin
    #     QuestionImage.objects.create(
    #         question=question,
    #         image=image_path
    #     )

#
# def parse_pdf(file_path, uploaded_file):
#     # PDF sahifalarini rasmga aylantiramiz
#     pages = convert_from_path(file_path)
#
#     with pdfplumber.open(file_path) as pdf:
#         for i, page in enumerate(pdf.pages):
#             text = page.extract_text()
#
#             # Agar text bo‘lmasa OCR ishlatamiz
#             if not text:
#                 text = pytesseract.image_to_string(pages[i], lang="eng+uzb")
#
#             if not text.strip():
#                 continue
#
#             # Sahifa textini savollarga bo‘lib tashlaymiz (1., 2., 3. ...)
#             blocks = re.split(r"\n(?=\d+\.)", text)
#
#             for block in blocks:
#                 block = block.strip()
#                 if not block or not re.match(r"^\d+\.", block):
#                     continue
#
#                 # Savol matni (birinchi satr)
#                 lines = block.split("\n")
#                 q_text = lines[0]
#
#                 # Variantlarni topish (A) B) C) D))
#                 options = [line for line in lines if re.match(r"^[A-D]\)", line)]
#
#                 # Javobni topish (Answer: C yoki Javob: B)
#                 answer_match = re.search(r"(Answer|Javob)\s*[:：]\s*([A-D])", block)
#                 correct_answer = answer_match.group(2) if answer_match else None
#
#                 # Sahifani rasm sifatida saqlash
#                 image_path = f"media/questions/page_{i}.png"
#                 if not os.path.exists("media/questions"):
#                     os.makedirs("media/questions")
#                 pages[i].save(image_path, "PNG")
#
#                 # Modelga saqlash
#                 Question.objects.create(
#                     text=q_text.strip(),
#                     options=options if options else None,
#                     correct_answer=correct_answer,
#                     image=image_path,
#                     source_file=uploaded_file
#                 )
