import json
import random

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE


def hex_to_rgb(hex_color):
    hex_color = hex_color.replace("#", "")

    return RGBColor(
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16)
    )


def add_background_shapes(slide, color):

    positions = [
        (-1.3, -1.0),
        (10.8, -1.0),

        (-1.3, 5.3),
        (10.8, 5.3),

        (-1.2, 2.2),
        (11.0, 2.2),

        (4.8, -1.1),
        (4.8, 5.6)
    ]

    shape_types = [
        MSO_SHAPE.OVAL,
        MSO_SHAPE.RECTANGLE,
        MSO_SHAPE.DIAMOND
    ]

    for _ in range(random.randint(2, 4)):

        x, y = random.choice(positions)

        size = random.uniform(1.0, 2.4)

        shape = slide.shapes.add_shape(
            random.choice(shape_types),
            Inches(x),
            Inches(y),
            Inches(size),
            Inches(size)
        )

        shape.fill.solid()

        shape.fill.fore_color.rgb = color

        shape.fill.transparency = 0.82

        shape.line.fill.background()


def add_frame(slide, color):

    frame = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.45),
        Inches(0.55),
        Inches(12.0),
        Inches(6.0)
    )

    frame.fill.background()

    frame.line.color.rgb = color

    frame.line.width = Pt(1.1)


def add_title(slide, title, style):

    box = slide.shapes.add_textbox(
        Inches(0.9),
        Inches(0.55),
        Inches(10.8),
        Inches(0.7)
    )

    p = box.text_frame.paragraphs[0]

    p.text = title

    p.font.size = Pt(26)

    p.font.bold = True

    p.font.color.rgb = style["title"]

    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.9),
        Inches(1.15),
        Inches(2.2),
        Inches(0.03)
    )

    line.fill.solid()

    line.fill.fore_color.rgb = style["accent"]

    line.line.fill.background()


def split_long_text(items):

    result = []

    for item in items:

        parts = item.split(". ")

        for part in parts:

            part = part.strip()

            if part:
                result.append(part)

    return result[:8]


def add_content(slide, bullets, style):

    bullets = split_long_text(bullets)

    if len(bullets) <= 4:

        box = slide.shapes.add_textbox(
            Inches(1.1),
            Inches(1.8),
            Inches(10),
            Inches(3.8)
        )

        tf = box.text_frame

        tf.word_wrap = True

        for i, bullet in enumerate(bullets):

            p = tf.add_paragraph() if i else tf.paragraphs[0]

            p.text = bullet

            p.font.size = Pt(22)

            p.font.color.rgb = style["text"]

            p.space_after = Pt(16)

    else:

        mid = len(bullets) // 2

        left = bullets[:mid]

        right = bullets[mid:]

        box1 = slide.shapes.add_textbox(
            Inches(1.1),
            Inches(1.8),
            Inches(4.7),
            Inches(4.3)
        )

        box2 = slide.shapes.add_textbox(
            Inches(6.2),
            Inches(1.8),
            Inches(4.7),
            Inches(4.3)
        )

        tf1 = box1.text_frame
        tf2 = box2.text_frame

        tf1.word_wrap = True
        tf2.word_wrap = True

        for i, bullet in enumerate(left):

            p = tf1.add_paragraph() if i else tf1.paragraphs[0]

            p.text = bullet

            p.font.size = Pt(20)

            p.font.color.rgb = style["text"]

            p.space_after = Pt(12)

        for i, bullet in enumerate(right):

            p = tf2.add_paragraph() if i else tf2.paragraphs[0]

            p.text = bullet

            p.font.size = Pt(20)

            p.font.color.rgb = style["text"]

            p.space_after = Pt(12)


def create_presentation(
    topic,
    slides_text,
    style_text=""
):

    prs = Presentation()

    data = json.loads(slides_text)

    style = {
        "background": hex_to_rgb(
            data.get("background_color",
                "#08192E"
            )
        ),

        "title": hex_to_rgb(
            data.get(
                "title_color",
                "#FFFFFF"
            )
        ),

        "text": hex_to_rgb(
            data.get(
                "text_color",
                "#D8DEE9"
            )
        ),

        "accent": hex_to_rgb(
            data.get(
                "accent_color",
                "#25C6F7"
            )
        )
    }

    for slide_data in data["slides"]:

        slide = prs.slides.add_slide(
            prs.slide_layouts[6]
        )

        fill = slide.background.fill

        fill.solid()

        fill.fore_color.rgb = style["background"]

        add_background_shapes(
            slide,
            style["accent"]
        )

        add_frame(
            slide,
            style["accent"]
        )

        add_title(
            slide,
            slide_data["title"],
            style
        )

        add_content(
            slide,
            slide_data["bullets"],
            style
        )

    file_name = f"{topic}.pptx"

    prs.save(file_name)

    return file_name