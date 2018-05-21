import json
from service import FindNearByPoints
import sys


class FindNearbyCustomers(object):

    @staticmethod
    def parse_file(file_path):
        return [json.loads(line) for line in open(file_path)]

    @staticmethod
    def find_near_by_customers(office_latitude, office_longitude, customers, distance, sort_key,
                               near_by_points_service = FindNearByPoints()):

        near_by_customers = near_by_points_service.find_nearby_points_within_distance(
            office_latitude,
            office_longitude,
            customers,
            distance)

        return sorted(near_by_customers, key=lambda ele: ele[sort_key])

if __name__ == "__main__":

    try:
        customers = FindNearbyCustomers.parse_file('customer.txt')
    except FileNotFoundError:
        print("[Error] Unable to open file containing list of customers: %s" % 'customer.txt')
        sys.exit()

    sorted_near_by_customers = FindNearbyCustomers.find_near_by_customers(53.339428, -6.257664, customers, 100, 'user_id')
    for customer in sorted_near_by_customers:
        print('user_id: %s, name: %s' % (customer['user_id'], customer['name']))