import json
import random

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE


def hex_to_rgb(hex_color: str):
    hex_color = hex_color.replace("#", "")

    return RGBColor(
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )


def is_light_color(color: RGBColor):
    brightness = (
        color[0] * 299 +
        color[1] * 587 +
        color[2] * 114
    ) / 1000

    return brightness > 170


def get_contrast_text_color(bg_color: RGBColor):
    if is_light_color(bg_color):
        return RGBColor(25, 25, 25)

    return RGBColor(245, 245, 245)


def add_content(slide, bullets, style, layout):

    if layout == "cards":

        positions = [
            (0.8, 2.0),
            (6.0, 2.0),
            (0.8, 4.2),
            (6.0, 4.2)
        ]

        for i, bullet in enumerate(bullets[:4]):

            x, y = positions[i]

            card_color = RGBColor(
                255,
                255,
                255
            )

            card = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(x),
                Inches(y),
                Inches(4.4),
                Inches(1.5)
            )

            card.fill.solid()

            card.fill.fore_color.rgb = card_color

            card.fill.transparency = 0.05

            card.line.fill.background()

            box = slide.shapes.add_textbox(
                Inches(x + 0.25),
                Inches(y + 0.35),
                Inches(3.8),
                Inches(0.8)
            )

            p = box.text_frame.paragraphs[0]

            p.text = bullet

            p.font.size = Pt(18)

            p.font.color.rgb = get_contrast_text_color(
                card_color
            )

        return

    positions = [
        (0.8, 2.0),
        (1.2, 2.4),
        (1.6, 2.8),
        (2.0, 2.2)
    ]

    x, y = random.choice(positions)

    box = slide.shapes.add_textbox(
        Inches(x),
        Inches(y),
        Inches(6.3),
        Inches(4.2)
    )

    tf = box.text_frame

    tf.clear()

    use_bullets = random.choice(
        [True, False]
    )

    for i, bullet in enumerate(bullets):

        p = tf.add_paragraph() if i else tf.paragraphs[0]

        if use_bullets:
            p.text = f"• {bullet}"
        else:
            p.text = bullet

        p.font.size = Pt(20)

        p.font.color.rgb = style["text"]

        p.space_after = Pt(14)


def create_presentation(
    topic: str,
    slides_text: str,
    style_text: str = ""
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

    slides = data["slides"]

    for index, data in enumerate(slides):

        slide = prs.slides.add_slide(
            prs.slide_layouts[6]
        )

        fill = slide.background.fill

        fill.solid()

        fill.fore_color.rgb = style["background"]

        layout = data.get(
            "layout",
            "minimal"
        )

        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(11.2),
            Inches(0.4),
            Inches(0.8),
            Inches(0.8)
        )

        circle.fill.solid()

        circle.fill.fore_color.rgb = style["accent"]

        circle.fill.transparency = 0.82

        circle.line.fill.background()

        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0.8),
            Inches(1.45),
            Inches(2.7),
            Inches(0.04)
        )

        line.fill.solid()

        line.fill.fore_color.rgb = style["accent"]

        line.line.fill.background()

        if layout == "split":

            side_line = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(7.2),
                Inches(1.8),
                Inches(0.04),
                Inches(4.8)
            )

            side_line.fill.solid()

            side_line.fill.fore_color.rgb = style["accent"]

            side_line.line.fill.background()

        elif layout == "stacked":

            for i in range(3):

                block = slide.shapes.add_shape(
                    MSO_SHAPE.ROUNDED_RECTANGLE,
                    Inches(8),
                    Inches(2 + i * 1.25),
                    Inches(3),
                    Inches(0.8)
                )

                block.fill.solid()

                block.fill.fore_color.rgb = style["accent"]

                block.fill.transparency = 0.2

                block.line.fill.background()

        elif layout == "accent":

            accent = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(7.5),
                Inches(2),
                Inches(4),
                Inches(3)
            )

            accent.fill.solid()

            accent.fill.fore_color.rgb = style["accent"]

            accent.fill.transparency = 0.15

            accent.line.fill.background()

        elif layout == "title":

            title_block = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(0.8),
                Inches(2),
                Inches(10.5),
                Inches(3.5)
            )

            title_block.fill.solid()

            title_block.fill.fore_color.rgb = style["accent"]

            title_block.fill.transparency = 0.85

            title_block.line.fill.background()

        title_box = slide.shapes.add_textbox(
            Inches(0.8),
            Inches(0.7),
            Inches(11),
            Inches(0.8)
        )

        p = title_box.text_frame.paragraphs[0]

        p.text = data["title"]

        p.font.size = Pt(28)

        p.font.bold = True

        p.font.color.rgb = style["title"]

        add_content(
            slide,
            data["bullets"],
            style,
            layout
        )

        num_box = slide.shapes.add_textbox(
            Inches(12.1),
            Inches(7.0),
            Inches(0.5),
            Inches(0.3)
        )

        num = num_box.text_frame.paragraphs[0]

        num.text = str(index + 1)

        num.font.size = Pt(11)

        num.font.color.rgb = style["accent"]

    file_name = f"{topic}.pptx"

    prs.save(file_name)

    return file_name