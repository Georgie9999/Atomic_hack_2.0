from shiny import reactive
from shiny.express import input, render, ui
from shiny.types import ImgData, FileInfo
import pandas as pd
from shinywidgets import render_widget
from ultralytics import YOLO
from PIL import Image
import plotly.express as px
import sys

ui.page_opts(title="Определение дефектов сварных швов с помощь ИИ", window_title="sbs_solution")

names = {0: "Прилегающие дефекты", 1: "Дефекты целостности",
         2: "Дефекты геометрии", 3: "Дефекты постобработки",
         4: "Дефекты невыполнения"}
dict_class = {}

with ui.layout_columns(col_widths=[12, 12, 12, 12, 12]):
    with ui.card(height=300):
        ui.card_header("Выберете фото сварного шва:")
        ui.input_file("file1", "", accept=[".png, .jpeg, .jpg", ".csv"], multiple=False)


        @reactive.calc
        def parsed_file():
            file: list[FileInfo] | None = input.file1()
            if file is None:
                return pd.DataFrame()
            img = Image.open(file[0]["datapath"])
            return pd.DataFrame({"img": [img]})  # pyright: ignore[reportUnknownMemberType]

    with ui.layout_column_wrap(fill=False):
        with ui.value_box():
            ui.card_header("Размер изображения (Мб):")


            @render.table
            def img_mb():
                image = parsed_file()

                if image.empty:
                    return pd.DataFrame()
                size = round(sys.getsizeof(image.img[0].tobytes())/ 1_048_5760, 2)
                print(size)
                img_mb_info = pd.DataFrame(
                    {
                        "Size": [size]
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

    with ui.card(height=200):
        ui.card_header("Памятка по дефектам:")


        @render.table
        def info():
            return pd.DataFrame({0: "Прилегающие дефекты", 1: "Дефекты целостности",
                                 2: "Дефекты геометрии", 3: "Дефекты постобработки",
                                 4: "Дефекты невыполнения"}, index=[0])
    with ui.card(height=800):
        ui.card_header("Итоговый результат:")


        @render.image
        def img_show_image():
            image = parsed_file()

            if image.empty:
                return pd.DataFrame()

            net = YOLO('./best.pt')
            result = net(image.img[0])[0]
            for box in result.boxes:
                item = int(box.cls.item())
                if item not in dict_class:
                    dict_class[item] = [box.conf.item()]
                else:
                    dict_class[item].append(box.conf.item())
            result.save(filename="photo.png")
            img: ImgData = {"src": './photo.png', "width": "1200px"}

            return img

    with ui.card(height=400):
        ui.card_header("Статистика обработки изображения:")


        @render_widget
        def plot():
            image = parsed_file()
            if image.empty:
                return pd.DataFrame()

            data = {"class": [names[x] for x in dict_class.keys()], "count": [len(dict_class[x]) for x in dict_class]}

            scatterplot = px.histogram(
                data_frame=data,
                x="class",
                y="count", nbins=20
            ).update_layout(
                title={"text": "Количество дефектов каждого из класса"},
                yaxis_title="Количество",
                xaxis_title="Название дефекта",
            )
            return scatterplot
