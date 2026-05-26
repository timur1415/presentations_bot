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


def add_blob(slide, color):

    x = random.uniform(-1, 10)

    y = random.uniform(-1, 6)

    w = random.uniform(2.0, 4.5)

    h = random.uniform(2.0, 4.5)

    shape = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(x),
        Inches(y),
        Inches(w),
        Inches(h)
    )

    shape.fill.solid()

    shape.fill.fore_color.rgb = color

    shape.fill.transparency = 0.65

    shape.line.fill.background()


def add_card(slide):

    x = random.uniform(0.7, 1.4)

    y = random.uniform(1.4, 2.2)

    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(x),
        Inches(y),
        Inches(10.5),
        Inches(4.6)
    )

    card.fill.solid()

    card.fill.fore_color.rgb = RGBColor(
        255,
        255,
        255
    )

    card.fill.transparency = 0.02

    card.line.fill.background()


def add_frame(slide, color):

    frame = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.6),
        Inches(0.6),
        Inches(11.8),
        Inches(6.2)
    )

    frame.fill.background()

    frame.line.color.rgb = color

    frame.line.width = Pt(1.4)


def add_corner(slide, color):

    corner = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(random.choice([0, 10.6])),
        Inches(random.choice([0, 5.7])),
        Inches(2),
        Inches(1.4)
    )

    corner.fill.solid()

    corner.fill.fore_color.rgb = color

    corner.fill.transparency = 0.2

    corner.line.fill.background()


def add_title(slide, title, style):

    positions = [
        (0.8, 0.7),
        (1.0, 0.9),
        (0.9, 1.1)
    ]

    x, y = random.choice(positions)

    box = slide.shapes.add_textbox(
        Inches(x),
        Inches(y),
        Inches(10),
        Inches(0.7)
    )

    p = box.text_frame.paragraphs[0]

    p.text = title

    p.font.size = Pt(28)

    p.font.bold = True

    p.font.color.rgb = style["title"]


def add_content(slide, bullets, style):
    import random
    from pptx.util import Inches, Pt

    variants = [
        "bullets",
        "paragraph",
        "definition",
        "split"
    ]

    variant = random.choice(variants)

    x = 1.0
    y = 1.9
    w = 10
    h = 4.5

    box = slide.shapes.add_textbox(
        Inches(x),
        Inches(y),
        Inches(w),
        Inches(h)
    )

    tf = box.text_frame
    tf.word_wrap = True

    if variant == "bullets":

        for i, bullet in enumerate(bullets):
            p = tf.add_paragraph() if i else tf.paragraphs[0]
            p.text = f"• {bullet}"
            p.font.size = Pt(random.choice([20, 22]))
            p.font.color.rgb = style["text"]
            p.space_after = Pt(14)

    elif variant == "paragraph":

        p = tf.paragraphs[0]

        text = " ".join(bullets)

        p.text = text
        p.font.size = Pt(20)
        p.font.color.rgb = style["text"]
        p.space_after = Pt(12)

    elif variant == "definition":

        if bullets:

            title = slide.shapes.add_textbox(
                Inches(1),
                Inches(1.9),
                Inches(4),
                Inches(0.6)
            )

            p = title.text_frame.paragraphs[0]
            p.text = bullets[0]
            p.font.size = Pt(24)
            p.font.bold = True
            p.font.color.rgb = style["title"]

            desc = slide.shapes.add_textbox(
                Inches(1),
                Inches(2.6),
                Inches(9.5),
                Inches(2.8)
            )

            p2 = desc.text_frame.paragraphs[0]
            p2.text = " ".join(bullets[1:])
            p2.font.size = Pt(20)
            p2.font.color.rgb = style["text"]

    elif variant == "split":

        left = bullets[:len(bullets)//2]
        right = bullets[len(bullets)//2:]

        box1 = slide.shapes.add_textbox(
            Inches(1),
            Inches(2),
            Inches(4.4),
            Inches(4)
        )

        box2 = slide.shapes.add_textbox(
            Inches(6),
            Inches(2),
            Inches(4.4),
            Inches(4)
        )

        tf1 = box1.text_frame
        tf2 = box2.text_frame

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
            data["background_color"]
        ),
        "title": hex_to_rgb(
            data["title_color"]
        ),
        "text": hex_to_rgb(
            data["text_color"]
        ),
        "accent": hex_to_rgb(
            data["accent_color"]
        )
    }

    templates = [
        "blob",
        "blob2",
        "frame",
        "card",
        "corner",
        "minimal",
        "clean",
        "accent"
    ]

    previous = None

    for slide_data in data["slides"]:

        template = random.choice(
            [t for t in templates if t != previous]
        )

        previous = template

        slide = prs.slides.add_slide(
            prs.slide_layouts[6]
        )

        fill = slide.background.fill

        fill.solid()

        fill.fore_color.rgb = style["background"]

        if template == "blob":
            add_blob(
                slide,
                style["accent"]
            )

        elif template == "blob2":

            add_blob(
                slide,
                style["accent"]
            )

            add_blob(
                slide,
                style["accent"]
            )

        elif template == "frame":

            add_frame(
                slide,
                style["accent"]
            )

        elif template == "card":

            add_card(
                slide
            )

        elif template == "corner":

            add_corner(
                slide,
                style["accent"]
            )

        elif template == "accent":

            add_blob(
                slide,
                style["accent"]
            )

            add_corner(
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