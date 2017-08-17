from arabic_reshaper import arabic_reshaper, ArabicReshaper
from fpdf import FPDF
from bidi.algorithm import get_display
import os


"""
Method: sub_words.
Parameters: integer (counter)  , array of words/strings, integer (number of words per line) .
It takes the array of words and returns a sublist form (counter) to (counter + number of words per line).
"""


def sub_words(i, words_array, number_of_words):
    if (i + number_of_words) < len(words_array):
        return words_array[i:i + number_of_words]
    else:
        return words_array[i:len(words_array)]


"""
Method: merge_words.
Parameters: array of words/strings.
It takes the array of words and returns a string represents the array words after concatenation.
"""


def merge_words(words_sub_array):
    line = ""
    for i in range(0, len(words_sub_array)):
        line = line + words_sub_array[i] + " "
    return line


"""
Method: split_text.
Parameters: string (text).
It takes the text and return array of lines (strings) of the text where each line of length = number_of_words.
"""


def split_text(text):
    number_of_words = 15  # Number of words per line.
    output = []
    text_array = text.split("\n")  # Split the text into paragraphs.
    text_array = text_array[::-1]  # Reverse paragraphs order because the printing in the pdf from bottom to top.
    for paragraph in text_array:
        if len(paragraph.split(" ")) > number_of_words:
            all_words = paragraph.split(" ")
            i = 0
            while i < len(all_words):
                sub_array = sub_words(i, all_words, number_of_words)
                output = [merge_words(sub_array)] + output
                i += number_of_words
        else:
            output = output + [paragraph]
    return output


def generate_arabic_pdf(text):

    pdf = FPDF(format='letter', unit='in')
    pdf.add_page()
    pdf.add_font('DejaVu', '', os.path.abspath("font/stc.ttf"), uni=True)
    pdf.set_font('DejaVu', '', 15)
    pdf.ln(0.15)
    effective_page_width = pdf.w - 2 * pdf.l_margin

    # Page title
    title = 'العنوان'
    reshaped_text_title = arabic_reshaper.reshape(title)
    bidi_text_title = get_display(reshaped_text_title)
    pdf.cell(effective_page_width, 0.50, bidi_text_title, align='C', border='B')
    pdf.ln(0.90)

    pdf.set_font('DejaVu', '', 10)  # Reset the font size.
    # Link describes the following lines -> https://github.com/mpcabd/python-arabic-reshaper
    configuration = {
        'language': 'Arabic',
        'delete_harakat': True,
        'support_ligatures': True,
    }
    reshaper = ArabicReshaper(configuration=configuration)
    reshaped_text = reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)

    text_lines = split_text(bidi_text)  # Split the text into lines.
    for i in range(0, len(text_lines)):
        pdf.multi_cell(effective_page_width, 0.30, text_lines[i], align='R')  # Print the lines to the pdf.

    pdf.output('output.pdf')  # Save the pdf with name output.


# Test

text_test = """
أعلنت المديرية العامة للدفاع المدني جاهزيتها لمواجهة الطوارئ والحفاظ على سلامة ضيوف الرحمن خلال موسم الحج لهذا العام 1438هـ بالعاصمة المقدسة والمدينة المنورة والمشاعر من خلال خطط تفصيلية بمشاركة أكثر من 32 جهة حكومية واستشارية تشارك في تنفيذ خطة الدفاع المدني للطوارئ في الحج.

وأوضحت المديرية العامة للدفاع المدني خلال المؤتمر الصحفي لقيادات قوات الدفاع المدني بالحج والذي عقد اليوم الأربعاء بالعاصمة المقدسة بحضور اللواء حمد بن عبدالعزيز المبدل قائد قوات الدفاع المدني بالحج، تجنيد أكثر من 17 ألف من رجال الدفاع المدني يدعمهم أكثر من 3 آلاف آلية ومعدة متطورة لتوفير أعلى درجات السلامة من المخاطر لضيوف الرحمن والتصدي لكل ما يهددهم من مخاطر في جميع أعمال ومناطق الحج، حيث خضع جميع الضباط والأفراد المشاركين في الحج لتدريب نوعي حسب المتغيرات والمستجدات التي تم رصدها .

"""

generate_arabic_pdf(text_test)
