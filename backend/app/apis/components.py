from flask import request, jsonify
from flask_restx import Resource, Namespace, fields

from backend.database.creation import (
    Processor,
    Motherboard,
    VideoCard,
    Ssd,
    PowerUnit,
    Ram,
)
from backend.database.flask_managers import update_profile, get_component, COMPONENTS
from backend.app.services.middlewares import TokenService
from backend.app.services.decorators import convert_error, clear_duplicates
from backend.app.others.responses import CommentResponse, CustomResponse
from backend.app.models.response_models import (
    ProfileResponseSchema,
    CommentResponseSchema,
    ProcessorResponseSchema,
    ProcessorFullResponseSchema,
)
from backend.app.documentation.output_models import (
    UnauthorizedResponseSchema,
    SuccessResponseSchema,
)
from backend.database.creation import db

api = Namespace("components", description="Components")


@clear_duplicates
def get_names_response(component_name: str):
    return [el.name for el in get_component(component_name)]


@api.route(f"/names/{Processor.__tablename__}")
class ProcessorNameResource(Resource):
    @convert_error
    def get(self):
        """
        ---
          summary: Получение всех названий процессоров
          responses:
            '200':
              description: Успешное получение информации
              schema:
                type: array
                items:
                  type: string
                example:
                  - "AMD Ryzen 5 8400F OEM"
                  - "AMD Ryzen 7 3700X OEM"
                  - "Intel Core i5-10600KF OEM"
                  - "AMD Ryzen 9 5900XT BOX"
                  - "Intel Core Ultra 7 265KF OEM"
                  - "Intel Core i5-13600KF OEM"
                  - "Intel Core i7-13790F OEM"
                  - "Intel Core i9-12900KF OEM"
                  - "Intel Core i5-13600KF BOX"
                  - "Intel Core i7-14700KF OEM"
                  - "AMD Ryzen 7 5700X3D BOX"
                  - "AMD Ryzen 5 3500X OEM"

          tags:
            - Components-names
        """
        # TokenService(request=request)
        return jsonify(get_names_response(component_name=Processor.__tablename__))


@api.route(f"/names/{VideoCard.__tablename__}")
class VideoCardNameResource(Resource):
    @convert_error
    def get(self):
        """
        ---
          summary: Получение всех названий процессоров
          responses:
            '200':
              description: Успешное получение информации
              schema:
                type: array
                items:
                  type: string
                example:
                  - "Palit GeForce RTX 4060 Ti White"
                  - "ASUS GeForce RTX 5070 Ti TUF Gaming OC Edition"
                  - "GIGABYTE AMD Radeon RX 7600 GAMING OC"
                  - "Gainward GeForce RTX 5080 Phoenix"
                  - "Gainward GeForce RTX 3050 Ghost"
                  - "MSI GeForce RTX 5080 VANGUARD SOC LAUNCH EDITION"
                  - "PNY Quadro T1000"
                  - "PNY Quadro RTX 5000 Ada Generation"
                  - "MSI GeForce RTX 4060 VENTUS 2X WHITE"
                  - "ASUS GeForce RTX 5080 ROG Astral OC Edition"
                  - "GIGABYTE GeForce RTX 5070 AORUS MASTER"
                  - "INNO3D GeForce RTX 4060 TWIN X2"
                  - "GIGABYTE GeForce RTX 5080 AERO OC SFF"

          tags:
            - Components-names
        """
        # TokenService(request=request)
        return jsonify(get_names_response(component_name=VideoCard.__tablename__))


@api.route(f"/names/{Ssd.__tablename__}")
class SsdNameResource(Resource):
    @convert_error
    def get(self):
        """
        ---
          summary: Получение всех названий процессоров
          responses:
            '200':
              description: Успешное получение информации
              schema:
                type: array
                items:
                  type: string
                example:
                  - "Patriot Viper VP4300 Lite"
                  - "ADATA XPG GAMMIX S60"
                  - "ADATA LEGEND 800"
                  - "Patriot Viper VP4300"
                  - "ARDOR GAMING Ally AL1284"
                  - "MSI SPATIUM M450"
                  - "WD Blue SN570"
                  - "Samsung 970 EVO Plus"
                  - "Apacer PP3480"
                  - "Acer FA200"
                  - "Apacer AS2280Q4U"
                  - "ARDOR GAMING Ally ALG412816"
                  - "Crucial T700"
                  - "Apacer AS2280P4"

          tags:
            - Components-names
        """
        # TokenService(request=request)
        return jsonify(get_names_response(component_name=Ssd.__tablename__))


@api.route(f"/names/{PowerUnit.__tablename__}")
class PowerUnitNameResource(Resource):
    @convert_error
    def get(self):
        """
        ---
          summary: Получение всех названий процессоров
          responses:
            '200':
              description: Успешное получение информации
              schema:
                type: array
                items:
                  type: string
                example:
                  - "Formula V Line VL-1200G5 MOD"
                  - "Lian Li SP750"
                  - "ExeGate 80 PLUS Bronze 1000PPH OEM"
                  - "Chieftec SMART 500W"
                  - "Thermaltake Toughpower SFX 750W Platinum"
                  - "Cougar STC500 500W"
                  - "DEEPCOOL PN850M"
                  - "Chieftec VALUE 500W"
                  - "SilverStone ST1000-PTS"
                  - "Formula AP-600ММ"
                  - "DEEPCOOL GamerStorm PN650M"
                  - "Chieftec CORE 600W BULK"
                  - "PowerCase PW600"
                  - "Thermaltake Toughpower GF 650W"

          tags:
            - Components-names
        """
        # TokenService(request=request)
        return jsonify(get_names_response(component_name=PowerUnit.__tablename__))


@api.route(f"/names/{Ram.__tablename__}")
class RamNameResource(Resource):
    @convert_error
    def get(self):
        """
        ---
          summary: Получение всех названий процессоров
          responses:
            '200':
              description: Успешное получение информации
              schema:
                type: array
                items:
                  type: string
                example:
                  - "Corsair Vengeance RGB RT"
                  - "G.Skill RIPJAWS M5"
                  - "G.Skill Trident Z Neo"
                  - "Acer Predator Pallas II"
                  - "G.Skill Ripjaws M5 RGB"
                  - "Kingston Fury Renegade White RGB"
                  - "Apacer"
                  - "Apacer NOX"
                  - "Kingston Fury Beast Black AMD"
                  - "Kingston Fury Renegade White"
                  - "G.Skill Trident Z Neo RGB"
                  - "ADATA XPG SPECTRIX D35G RGB"
                  - "Team Group T-Force Xtreem CKD"

          tags:
            - Components-names
        """
        # TokenService(request=request)
        return jsonify(get_names_response(component_name=Ram.__tablename__))


@api.route(f"/names/{Motherboard.__tablename__}")
class MotherboardNameResource(Resource):
    @convert_error
    def get(self):
        """
        ---
          summary: Получение всех названий материнских плат
          responses:
            '200':
              description: Успешное получение информации
              schema:
                type: array
                items:
                  type: string
                example:
                  - "ASUS TUF GAMING Z790-PRO WIFI"
                  - "ASUS PRIME B650M-A II"
                  - "ASUS PRIME B760M-A"
                  - "ASRock Phantom Gaming B760I Lightning WiFi"
                  - "ASUS PRIME Z790-P"
                  - "GIGABYTE Z790 GAMING X"
                  - "ASUS ProArt B760-CREATOR"
                  - "GIGABYTE B650 AORUS ELITE AX"
                  - "MSI MEG Z890 GODLIKE"
                  - "GIGABYTE X870 GAMING WIFI6"
                  - "ASUS PRIME X670-P-CSM"

          tags:
            - Components-names
        """
        # TokenService(request=request)
        return jsonify(get_names_response(component_name=Motherboard.__tablename__))


@api.route("/processors")
class ProcessorResource(Resource):

    @convert_error
    def get(self):
        """
        ---
          summary: Получение информации для карточек процессоров
          responses:
            '200':
              description: Успешное получение информации
              schema:
                type: array
                items:
                  type: object
                  properties:
                    TDP:
                      type: string
                    name:
                      type: string
                    price:
                      type: string
                    socket:
                      type: string
                  example:
                    - TDP: "253 Вт"
                      name: "Intel Core i7-14700KF OEM"
                      price: "32 299 ₽"
                      socket: "LGA 1700"
                    - TDP: "125 Вт"
                      name: "Intel Core i5-10600KF OEM"
                      price: "9 399 ₽"
                      socket: "LGA 1200"
                    - TDP: "105 Вт"
                      name: "AMD Ryzen 9 5900X BOX"
                      price: "29 299 ₽"
                      socket: "AM4"

          tags:
            - Processors
        """
        # TokenService(request=request)
        components = [
            ProcessorResponseSchema().dump(el) for el in get_component("processors")
        ]
        return jsonify(components)

    @convert_error
    def post(self):
        """
        ---
          summary: Получение подробной информации о процессоре по названию
          schema:
          responses:
            '200':
              description: Успешное получение информации
              schema: SuccessResponseSchema

            '401':
              description: Пользователь не авторизован, нужно перенаправить на авторизацию
              schema: UnauthorizedResponseSchema

          tags:
            - Processors
        """
        # TokenService(request=request)
        components = [
            ProcessorResponseSchema().load(el) for el in get_component("processors")
        ]
        # print(component)
        print(components.__class__)
        return jsonify(components)
