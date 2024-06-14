import plotly.express as px
from shiny.express import input, render, ui
from shinywidgets import render_widget
from shiny.types import ImgData

# @render.image
# def image():
#     from pathlib import Path
#
#     dir = Path(__file__).resolve().parent
#     img: ImgData = {"src": str(dir / "img/sbs_logo.jpeg"), "width": "100px"}
#     return img


with ui.layout_columns(col_widths=[12, 12, 12]):
    with ui.card(height=400):
        ui.card_header("Выберете фото сварного шва:")
        ui.input_file("file1", "", accept=[".png, .jpeg, .jpg"], multiple=False)
    with ui.layout_column_wrap(fill=False):
        with ui.value_box():
            "Размер изображений(Мб)"
            "$1,000,000"
        with ui.value_box():
            "Разрешение"
            "$1,000,000"
    with ui.card(height=400):
        ui.card_header("Итоговый результат:")
    with ui.card(height=400):
        ui.card_header("Распределение вероятностей по дефекту:")

ui.page_opts(title="Определение дефектов сварных швов с помощь ИИ", window_title="sbs_solution")

with ui.sidebar():
    ui.input_select("var", "Выберите один из вариантов:", choices=["total_bill", "tip"])
