import sys

from business import find_businesses
from geocoder import get_coordinates
from mapapi_pg import show_map


def main():
    toponym_to_find = " ".join(sys.argv[1:])
    if toponym_to_find:
        lat, lon = get_coordinates(toponym_to_find)
        adress_ll = f"{lat},{lon}"
        span = "0.05, 0.05"
        organization = find_businesses(adress_ll, span, "аптека")
        point_params = []
        for i in organization[:10]:
            point = i['geometry']['coordinates']
            org_lat = float(point[0])
            org_lon = float(point[1])
            orgs_params = f'{org_lat},{org_lon},'
            clock = i['properties']['CompanyMetaData']['Hours']['text']
            if 'круглосуточно' in clock:
                orgs_params += 'pm2gnm'
            elif clock == '':
                orgs_params += 'pm2grm'
            else:
                orgs_params += 'pm2blm'
            point_params.append(orgs_params)
            print(clock)
        show_map(map_type='map', add_params=f'pt={"~".join(point_params)}')


if __name__ == '__main__':
    main()
