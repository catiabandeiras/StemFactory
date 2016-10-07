# -*- coding: utf-8 -*-

# import configuration of assets
#from levelconfig.common import cells.cellA, cells.cellB

# base input fields
config = {
    'panels': [
        {
            'id': 'factory',
            'label': 'Factory',
            'params': [
                {
                    'id': 'AREA_FACILITY',
                    'label': 'Total GMP Facility Area',
                    'hidden': True,
                    'value': 400
                },
                {
                    'id': 'AREA_UNIT',
                    'label': 'Area unit',
                    'combobox': True,
                    'options': [
                        { 'value': '1', 'desc': 'sq. mt.'},
                        { 'value': '2', 'desc': 'sq. ft.'},
                    ]
                },
                {
                    'id': 'TOTAL_WORKERS',
                    'label': 'Number of workers',
                    'hidden': True,
                    'value': 1
                },
                {
                    'id': 'TOTAL_BSC',
                    'label': 'Number of BSCs',
                    'hidden': True,
                    'value': 1
                },
                {
                    'id': 'TOTAL_INCUBATORS',
                    'label': 'Number of incubators',
                    'hidden': True,
                    'value': 1

                },
                {
                    'id': 'TOTAL_BIOREACTORS',
                    'label': 'Number of bioreactor systems',
                    'hidden': True,
                    'value': 1
                }
            ]
        },
        {
            'id': 'culture',
            'label': 'Culture Conditions',
            'params': [
            {
                    'id': 'TYPE_OF_ET',
                    'label': 'Type of Expansion technology to use',
                    'hidden': True,
                    'value': 'planar'
                },
                {
                    'id': 'TYPE_OF_MC',
                    'label': 'Type of microcarrier in suspension technology',
                    'hidden': True,
                    'value':'solohill',
                },
                {
                    'id': 'SOURCE_OF_MSC',
                    'label': 'Tissue origin of cells',
                    'hidden': True,
                    'value': 'bm'
                },
                {
                    'id': 'TYPE_OF_MEDIA',
                    'label': 'Culture medium for cell growth',
                    'value': 'fbs',
                    'readonly': True
                },
            ]
        },
        {
            'id': 'growth',
            'label': 'Growth Characteristics',
            'params': [
                {
                    'id': 'INITIAL_CELLS_PER_DONOR_AVG',
                    'label': 'Average initial cells per donor',
                    'hidden': True,
                    'value': 1.05e6
                },
                {
                    'id': 'INITIAL_CELLS_PER_DONOR_SD',
                    'label': 'Standard dev initial cells per donor',
                    'hidden': True,
                    'value': 0
                },
                {
                    'id': 'MAXIMUM_NUMBER_CPD',
                    'label': 'Maximum cumulative population doublings',
                    'hidden': True,
                    'value': 20
                },
                {
                    'id': 'MAX_NO_PASSAGES',
                    'label': 'Maximum cell passages',
                    'hidden': True,
                    'value': 3
                },
                {
                    'id': 'P1',
                    'label': 'Growth rate P1',
                    'hidden': True,
                    'value': 0.21
                },
                {
                    'id': 'P2',
                    'label': 'Growth rate P2',
                    'hidden': True,
                    'value': 0.20
                },
                {
                    'id': 'P3',
                    'label': 'Growth rate P3',
                    'hidden': True,
                    'value': 0.18
                },
            ]
        },
        {
            'id': 'manualOps',
            'label': 'Manual Operations',

        },
        {
            'id': 'manufacturing',
            'label': 'Manufacturing Demand',
            'params': [
                {
                    'id': 'CELL_NUMBER_PER_DOSE',
                    'label': 'Cell number per dose',
                    'hidden': True,
                    'value': 75e6
                },
                {
                    'id': 'ANNUAL_DEMAND',
                    'label': 'Number of doses per year',
                    'hidden': True,
                    'value': 1
                },
                {
                    'id': 'LOT_SIZE',
                    'label': 'Number of doses per lot',
                    'hidden': True,
                    'value': 1
                }
            ]
        },
    ]
}



config['level'] = {
    'number': 2,
    'title': 'This is a title',
    'description': "Let's cure your first pacient",
    'instructions': 'choose between cells A and B and try to obatin a profit',
}


#interactions permitted in level
config['interactions'] = [
    {
        'order': 1,
        'itemTypes': 'assets',
        'title': 'Market',
        'description': 'Buy more equipment, contract workers',
        'items': [market[0], market[1], market[2]],
    },
    {
        'order': 2,
        'itemTypes': 'consumables',
        'title': 'Cocktails',
        'description': 'Choose the cocktail you think will work best for the stated problem',
        'items': [cocktails[0], cocktails[2]]
    }
]
