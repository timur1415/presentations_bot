import json

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


def create_presentation(
    topic: str,
    slides_text: str,
    style_text: str = ""
):

    prs = Presentation()

    data = json.loads(slides_text)

    background_color = hex_to_rgb(
        data["background_color"]
    )

    title_color = hex_to_rgb(
        data["title_color"]
    )

    text_color = hex_to_rgb(
        data["text_color"]
    )

    accent_color = hex_to_rgb(
        data["accent_color"]
    )

    slides_data = data["slides"]

    for i, slide_data in enumerate(slides_data):

        slide = prs.slides.add_slide(
            prs.slide_layouts[6]
        )

        fill = slide.background.fill

        fill.solid()

        fill.fore_color.rgb = background_color

        layout = slide_data.get(
            "layout",
            "minimal"
        )

        if layout == "title":

            line = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(0.8),
                Inches(1.7),
                Inches(3),
                Inches(0.05)
            )

            line.fill.solid()

            line.fill.fore_color.rgb = accent_color

            line.line.fill.background()

        elif layout == "split":

            line = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(7.5),
                Inches(0.8),
                Inches(0.06),
                Inches(5.8)
            )

            line.fill.solid()

            line.fill.fore_color.rgb = accent_color

            line.line.fill.background()

        elif layout == "cards":

            for n in range(2):

                card = slide.shapes.add_shape(
                    MSO_SHAPE.ROUNDED_RECTANGLE,
                    Inches(0.9 + (n * 5.3)),
                    Inches(2.2),
                    Inches(4.6),
                    Inches(2.6)
                )

                card.fill.solid()

                card.fill.fore_color.rgb = RGBColor(
                    255,
                    255,
                    255
                )

                card.line.fill.background()

        title_box = slide.shapes.add_textbox(
            Inches(0.8),
            Inches(0.8),
            Inches(11),
            Inches(0.8)
        )

        title_frame = title_box.text_frame

        title_p = title_frame.paragraphs[0]

        title_p.text = slide_data["title"]

        title_p.font.size = Pt(28)

        title_p.font.bold = True

        title_p.font.color.rgb = title_color

        content_box = slide.shapes.add_textbox(
            Inches(1),
            Inches(2),
            Inches(10.5),
            Inches(4.5)
        )

        content_frame = content_box.text_frame

        for bullet in slide_data["bullets"]:

            p = content_frame.add_paragraph()

            p.text = f"• {bullet}"

            p.font.size = Pt(20)

            p.font.color.rgb = text_color

            p.space_after = Pt(10)

    file_name = f"{topic}.pptx"

    prs.save(file_name)

    return file_name