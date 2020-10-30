

def load_database(dataset: str = None, mode: str = 'csv'):
    if mode == 'csv':
        method_name = 'load_from_csv'
    elif mode == 'json':
        method_name = 'load_from_json'
    else:
        raise AssertionError('no such mode \'' + mode + "'")

    if dataset is None:
        print(f'loading BillOfLading')
        BillOfLading.load_from_csv(ROOT_DIR / 'scripts/bol-10000.csv')
    print(f'loading Address')
    Address.load_from_csv(ROOT_DIR / 'spreadsheet_data/da-base-OLTP - Address.csv')
    print(f'loading BusinessEntity')
    BusinessEntity.load_from_csv(ROOT_DIR / 'spreadsheet_data/da-base-OLTP - BusinessEntity.csv')
    print(f'loading Commodity')
    Commodity.load_from_csv(ROOT_DIR / 'spreadsheet_data/da-base-OLTP - Commodity.csv')
    print(f'loading Container')
    Container.load_from_csv(ROOT_DIR / 'spreadsheet_data/da-base-OLTP - Container.csv')
    print(f'loading ContainerModel')
    ContainerModel.load_from_csv(ROOT_DIR / 'spreadsheet_data/da-base-OLTP - ContainerModel.csv')
    print(f'loading Port')
    Port.load_from_csv(ROOT_DIR / 'spreadsheet_data/da-base-OLTP - Port.csv')
    print(f'loading Vehicle')
    Vehicle.load_from_csv(ROOT_DIR / 'spreadsheet_data/da-base-OLTP - Vehicle.csv')

    if dataset is not None:
        for cls in [
            BillOfLading,
            Leg,
            LegBridge,
            Voyage,
            LegSchedule,
            LegScheduleBridge,
            VoyageSchedule,
            Shipment,
        ]:
            print(f'loading {cls.__name__}')
            method = getattr(cls, method_name)
            method(ROOT_DIR / f'database/{dataset}/{cls.__name__}.{mode}')


def dump_database(dataset: str, mode: str = 'csv'):
    if mode == 'csv':
        method_name = 'dump_to_csv'
    elif mode == 'json':
        method_name = 'dump_to_json'
    elif mode == 'sql':
        method_name = 'dump_to_sql'
    else:
        raise AssertionError('no such mode \'' + mode + "'")

    for cls in [
        BillOfLading,
        Shipment,
        Voyage,
        Leg,
        LegBridge,
        LegSchedule,
        LegScheduleBridge,
        VoyageSchedule,
    ]:
        print(f'dumping {cls.__name__}'.ljust(30) + f'{time.ctime(time.time())}')
        method = getattr(cls, method_name)
        method(ROOT_DIR / f'database/{dataset}/{cls.__name__}.{mode}')
