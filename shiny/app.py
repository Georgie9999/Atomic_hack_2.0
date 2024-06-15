from shiny import reactive
from shiny.express import input, render, ui
import os
from shiny.types import ImgData, FileInfo
import pandas as pd
from pathlib import Path
from PIL import Image

# @render.image
# def image():
#     from pathlib import Path
#
#     dir = Path(__file__).resolve().parent
#     img: ImgData = {"src": str(dir / "img/sbs_logo.jpeg"), "width": "100px"}
#     return img


ui.page_opts(title="Определение дефектов сварных швов с помощь ИИ", window_title="sbs_solution")

with ui.layout_columns(col_widths=[12, 12, 12]):
    with ui.card(height=400):
        ui.card_header("Выберете фото сварного шва:")
        ui.input_file("file1", "", accept=[".png, .jpeg, .jpg", ".csv"], multiple=False)


        @reactive.calc
        def parsed_file():
            file: list[FileInfo] | None = input.file1()
            if file is None:
                return pd.DataFrame()
            img = Image.open(file[0]["datapath"])
            img.save('../shiny/img/photo.png')
            return pd.DataFrame({"img": [img]})  # pyright: ignore[reportUnknownMemberType]

    with ui.layout_column_wrap(fill=False):
        with ui.value_box():
            ui.card_header("Размер изображения (Мб):")


            @render.table
            def img_mb():
                image = parsed_file()

                if image.empty:
                    return pd.DataFrame()
                print(image.img[0].fp)
                img_mb_info = pd.DataFrame(
                    {
                        "Size": [os.path.getsize('img/photo.png') / 1_048_576]
                    }
                )
                return img_mb_info

        with ui.value_box():
            ui.card_header("Разрешение:")


            @render.table
            def img_size():
                image = parsed_file()

                if image.empty:
                    return pd.DataFrame()
                width, height = image.img[0].size
                img_size_info = pd.DataFrame(
                    {
                        "Height": [height],
                        "Width": [width]
                    }
                )
                return img_size_info
    with ui.card(height=400):
        ui.card_header("Итоговый результат:")


        @render.image
        def img_show_image():
            image = parsed_file()

            if image.empty:
                return pd.DataFrame()

            img: ImgData = {"src": "../shiny/img/sbs_logo.jpeg", "width": "100px"}
            os.remove("img/photo.png")

            return img
    with ui.card(height=400):
        ui.card_header("Распределение вероятностей по дефекту:")
