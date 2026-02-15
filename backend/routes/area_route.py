from flask import Blueprint, jsonify, request
from database import Area, Herb, ChineseHerb
import json
import re
import osmnx as ox

area_bp = Blueprint('area', __name__, url_prefix='/api/areas')

@area_bp.route('/', methods=['GET'])
def get_areas():
    areas = Area.query.all()
    result = {
        "areas": []
    }
    for area in areas:
        coordinates = json.loads(area.coordinates)  # Deserialize into a list
        result["areas"].append({
            "type": area.type,
            "coordinates": coordinates
        })
    return jsonify(result)

@area_bp.route('/herb/<int:id>', methods=['GET'])
def get_herb_area(id):
    lang = request.args.get('lang', 'zh')
    if lang == 'en':
        herb = Herb.query.filter_by(id=id).first()
        provinces = [
            'Anhui', 'Beijing', 'Chongqing', 'Fujian', 'Gansu', 'Guangdong', 'Guangxi', 'Guizhou', 'Hainan', 'Hebei',
            'Heilongjiang', 'Henan', 'Hong Kong', 'Hubei', 'Hunan', 'Inner Mongolia', 'Jiangsu', 'Jiangxi', 'Jilin',
            'Liaoning', 'Macau', 'Ningxia', 'Qinghai', 'Shaanxi', 'Shandong', 'Shanghai', 'Shanxi', 'Sichuan',
            'Tianjin', 'Tibet', 'Xinjiang', 'Yunnan', 'Zhejiang'
        ]
    else:
        herb = ChineseHerb.query.filter_by(id=id).first()
        provinces = [
            '安徽', '北京', '重庆', '福建', '甘肃', '广东', '广西', '贵州', '海南', '河北', '黑龙江', '河南', '香港', '湖北', '湖南',
            '内蒙古', '江苏', '江西', '吉林', '辽宁', '澳门', '宁夏', '青海', '陕西', '山东', '上海', '山西', '四川', '天津', '台湾',
            '新疆', '云南', '浙江'
        ]
    area_str = herb.production_regions

    if lang == 'en':
        # Build a regular expression pattern to match the full province name
        pattern = r'\b(?:' + '|'.join(re.escape(province) for province in provinces) + r')\b'
        matches = re.findall(pattern, area_str, flags=re.IGNORECASE)

        # Deduplication and preserve the original capitalization
        unique_matches = []
        seen = set()
        result = {
            "areas": []
        }
        for match in matches:
            for province in provinces:
                if province.lower() == match.lower() and province not in seen:
                    unique_matches.append(province)
                    seen.add(province)
    else:

        # Build a regular expression pattern to match the full Chinese province names
        pattern = r'(' + '|'.join(re.escape(province) for province in provinces) + r')'
        matches = re.findall(pattern, area_str)

        # Deduplication and preserve the original capitalization
        unique_matches = []
        seen = set()
        result = {
            "areas": []
        }
        for match in matches:
            if match not in seen:
                unique_matches.append(match)
                seen.add(match)
    if unique_matches:
        for province in unique_matches:
            boundary = ox.geocode_to_gdf(province)

            # Extract geometric objects
            geometry = boundary.geometry.iloc[0]

            # Check the geometry type and extract the coordinates
            if geometry.geom_type == "Polygon":

                # Extract the coordinates of the outer ring
                coords = list(geometry.exterior.coords)
                sampled_coords = coords[::25]
                standard_coords = []
                for sc in sampled_coords:
                    standard_coords.append([sc[1], sc[0]])
                result['areas'].append({
                    "type": "Polygon",
                    "coordinates": standard_coords
                })
            elif geometry.geom_type == "MultiPolygon":

                # In the case of MultiPolygon, extract the coordinates of all child Polygons
                polygons_coords = []
                for polygon in geometry.geoms:
                    coords = list(polygon.exterior.coords)
                    sampled_coords = coords[::25]
                    polygons_coords.append(sampled_coords)
                standard_coords = []
                for pc in polygons_coords:
                    temp = []
                    for c in pc:
                        temp.append([c[1], c[0]])
                    standard_coords.append(temp)
                result['areas'].append({
                    "type": "MultiPolygon",
                    "coordinates": standard_coords
                })
            else:
                raise ValueError("几何类型不支持")
    return jsonify(result)
